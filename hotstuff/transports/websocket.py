"""WebSocket transport implementation."""
import json
import time
import threading
from typing import Optional, Dict, Any, Callable, List
import websocket

from hotstuff.types import (
    WebSocketTransportOptions,
    JSONRPCMessage,
    JSONRPCResponse,
    JSONRPCNotification,
    Subscription,
    SubscriptionData,
    WSMethod,
    SubscribeResult,
    UnsubscribeResult,
    PongResult,
)
from hotstuff.utils import ENDPOINTS_URLS


class WebSocketTransport:
    """WebSocket transport for real-time subscriptions."""
    
    def __init__(self, options: Optional[WebSocketTransportOptions] = None):
        """
        Initialize WebSocket transport.
        
        Args:
            options: Transport configuration options
        """
        options = options or WebSocketTransportOptions()
        
        self.is_testnet = options.is_testnet
        self.timeout = options.timeout
        
        # Setup server endpoints
        self.server = {
            "mainnet": ENDPOINTS_URLS["mainnet"]["ws"],
            "testnet": ENDPOINTS_URLS["testnet"]["ws"],
        }
        
        if options.server:
            if "mainnet" in options.server:
                self.server["mainnet"] = options.server["mainnet"]
            if "testnet" in options.server:
                self.server["testnet"] = options.server["testnet"]
        
        self.keep_alive = options.keep_alive or {
            "interval": 30.0,
            "timeout": 10.0,
        }
        
        self.ws: Optional[websocket.WebSocket] = None
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 5
        self.reconnect_delay = 1.0
        
        self.message_queue: Dict[str, dict] = {}
        self.message_id_counter = 0
        self._lock = threading.Lock()
        
        self.subscriptions: Dict[str, Subscription] = {}
        self.subscription_callbacks: Dict[str, Callable] = {}
        
        self.keep_alive_thread: Optional[threading.Thread] = None
        self.receive_thread: Optional[threading.Thread] = None
        self._running = False
        
        self.auto_connect = options.auto_connect
        if self.auto_connect:
            self.connect()
    
    def _cleanup(self):
        """Cleanup resources."""
        self._running = False
        
        if self.keep_alive_thread and self.keep_alive_thread.is_alive():
            self.keep_alive_thread = None
        
        if self.receive_thread and self.receive_thread.is_alive():
            self.receive_thread = None
        
        # Clear pending messages
        with self._lock:
            self.message_queue.clear()
    
    def _start_keep_alive(self):
        """Start keep-alive ping loop."""
        interval = self.keep_alive.get("interval")
        if not interval:
            return
        
        while self._running:
            try:
                time.sleep(interval)
                if self._running:
                    self.ping()
            except Exception as e:
                print(f"Keep-alive error: {e}")
                break
    
    def _handle_incoming_message(self, message: dict):
        """Handle incoming WebSocket message."""
        # Check if it's a JSON-RPC response
        if "id" in message and ("result" in message or "error" in message):
            self._handle_jsonrpc_response(message)
            return
        
        # Check if it's a notification
        if "method" in message and "params" in message and "id" not in message:
            self._handle_jsonrpc_notification(message)
            return
    
    def _handle_jsonrpc_response(self, response: dict):
        """Handle JSON-RPC response."""
        msg_id = str(response.get("id"))
        with self._lock:
            if msg_id in self.message_queue:
                self.message_queue[msg_id] = response
    
    def _handle_jsonrpc_notification(self, notification: dict):
        """Handle JSON-RPC notification."""
        method = notification.get("method")
        params = notification.get("params")
        
        if method in ("subscription", "event") and params:
            channel = params.get("channel")
            data = params.get("data")
            
            # Find matching subscriptions
            for sub_id, subscription in self.subscriptions.items():
                if subscription.channel == channel:
                    callback = self.subscription_callbacks.get(sub_id)
                    if callback:
                        subscription_data = SubscriptionData(
                            channel=channel,
                            data=data,
                            timestamp=time.time()
                        )
                        try:
                            callback(subscription_data)
                        except Exception as e:
                            print(f"Callback error: {e}")
    
    def _receive_messages(self):
        """Receive messages from WebSocket."""
        while self._running and self.ws:
            try:
                message = self.ws.recv()
                if message:
                    data = json.loads(message)
                    self._handle_incoming_message(data)
            except websocket.WebSocketConnectionClosedException:
                if self._running and self.reconnect_attempts < self.max_reconnect_attempts:
                    self._reconnect()
                break
            except json.JSONDecodeError as e:
                print(f"Failed to parse message: {e}")
            except Exception as e:
                print(f"Receive error: {e}")
                if self._running and self.reconnect_attempts < self.max_reconnect_attempts:
                    self._reconnect()
                break
    
    def _reconnect(self):
        """Reconnect to WebSocket."""
        self._cleanup()
        time.sleep(self.reconnect_delay * self.reconnect_attempts)
        self.reconnect_attempts += 1
        self.connect()
    
    def _send_jsonrpc_message(self, message: dict) -> Any:
        """Send a JSON-RPC message and wait for response."""
        if not self.is_connected():
            self.connect()
        
        # Assign message ID if not present
        if "id" not in message or message["id"] is None:
            self.message_id_counter += 1
            message["id"] = str(self.message_id_counter)
        
        msg_id = str(message["id"])
        
        # Initialize response slot
        with self._lock:
            self.message_queue[msg_id] = None
        
        # Send message
        self.ws.send(json.dumps(message))
        
        # Wait for response with timeout
        start_time = time.time()
        timeout = self.timeout or 10.0
        
        while True:
            with self._lock:
                response = self.message_queue.get(msg_id)
                if response is not None:
                    del self.message_queue[msg_id]
                    if "error" in response:
                        error = response["error"]
                        raise Exception(f"JSON-RPC Error {error.get('code')}: {error.get('message')}")
                    return response.get("result")
            
            if time.time() - start_time > timeout:
                with self._lock:
                    self.message_queue.pop(msg_id, None)
                raise Exception("Request timeout")
            
            time.sleep(0.01)
    
    def _format_subscription_params(
        self,
        channel: str,
        payload: dict
    ) -> dict:
        """Format subscription parameters."""
        subscription = {
            "channel": channel,
            **payload,
        }
        return subscription
    
    def _subscribe_to_channels(self, params: dict) -> SubscribeResult:
        """Subscribe to channels."""
        self.message_id_counter += 1
        message = {
            "jsonrpc": "2.0",
            "method": WSMethod.SUBSCRIBE,
            "params": params,
            "id": str(self.message_id_counter),
        }
        
        result = self._send_jsonrpc_message(message)
        return SubscribeResult(**result) if isinstance(result, dict) else result
    
    def _unsubscribe_from_channels(self, channels: List[str]) -> UnsubscribeResult:
        """Unsubscribe from channels."""
        self.message_id_counter += 1
        message = {
            "jsonrpc": "2.0",
            "method": WSMethod.UNSUBSCRIBE,
            "params": channels,
            "id": str(self.message_id_counter),
        }
        
        result = self._send_jsonrpc_message(message)
        return UnsubscribeResult(**result) if isinstance(result, dict) else result
    
    def is_connected(self) -> bool:
        """Check if WebSocket is connected."""
        return self.ws is not None and self.ws.connected
    
    def connect(self):
        """Connect to WebSocket server."""
        url = self.server["testnet" if self.is_testnet else "mainnet"]
        
        try:
            self.ws = websocket.create_connection(url, timeout=self.timeout)
            self.reconnect_attempts = 0
            self._running = True
            
            # Start keep-alive thread
            if self.keep_alive.get("interval"):
                self.keep_alive_thread = threading.Thread(target=self._start_keep_alive, daemon=True)
                self.keep_alive_thread.start()
            
            # Start receiving messages thread
            self.receive_thread = threading.Thread(target=self._receive_messages, daemon=True)
            self.receive_thread.start()
        
        except Exception as e:
            raise Exception(f"Failed to connect: {e}")
    
    def disconnect(self):
        """Disconnect from WebSocket server."""
        self._cleanup()
        
        if self.ws:
            self.ws.close()
            self.ws = None
    
    def ping(self) -> PongResult:
        """Send ping to server."""
        self.message_id_counter += 1
        message = {
            "jsonrpc": "2.0",
            "method": WSMethod.PING,
            "id": str(self.message_id_counter),
        }
        
        self._send_jsonrpc_message(message)
        return PongResult(pong=True)
    
    def subscribe(
        self,
        channel: str,
        payload: dict,
        listener: Callable
    ) -> Dict[str, Any]:
        """
        Subscribe to a channel.
        
        Args:
            channel: The channel to subscribe to
            payload: Subscription parameters
            listener: Callback function for updates
            
        Returns:
            Subscription result with unsubscribe method
        """
        if not self.is_connected():
            self.connect()
        
        subscription_id = f"{channel}_{time.time()}"
        
        subscription = Subscription(
            id=subscription_id,
            channel=channel,
            symbol=payload.get("instrumentId") or payload.get("symbol"),
            params=payload,
            timestamp=time.time()
        )
        
        self.subscription_callbacks[subscription_id] = listener
        
        try:
            subscription_params = self._format_subscription_params(channel, payload)
            result = self._subscribe_to_channels(subscription_params)
            
            if result.status == "subscribed" and result.channels:
                server_channel = result.channels[0]
                subscription.channel = server_channel
                self.subscriptions[subscription_id] = subscription
                
                return {
                    "subscriptionId": subscription_id,
                    "status": result.status,
                    "channels": result.channels,
                    "unsubscribe": lambda: self.unsubscribe(subscription_id),
                }
            else:
                self.subscription_callbacks.pop(subscription_id, None)
                error_msg = result.error or f"Subscription {result.status}"
                raise Exception(f"Server rejected subscription: {error_msg}")
        
        except Exception as e:
            self.subscriptions.pop(subscription_id, None)
            self.subscription_callbacks.pop(subscription_id, None)
            raise e
    
    def unsubscribe(self, subscription_id: str):
        """Unsubscribe from a channel."""
        subscription = self.subscriptions.get(subscription_id)
        if not subscription:
            raise Exception(f"Subscription {subscription_id} not found")
        
        try:
            if self.is_connected():
                self._unsubscribe_from_channels([subscription.channel])
            
            self.subscriptions.pop(subscription_id, None)
            self.subscription_callbacks.pop(subscription_id, None)
        
        except Exception as e:
            print(f"Failed to unsubscribe: {e}")
            self.subscriptions.pop(subscription_id, None)
            self.subscription_callbacks.pop(subscription_id, None)
            raise e
    
    def get_subscriptions(self) -> List[Subscription]:
        """Get all active subscriptions."""
        return list(self.subscriptions.values())
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()

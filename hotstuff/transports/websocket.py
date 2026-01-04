"""WebSocket transport implementation."""
import asyncio
import json
from typing import Optional, Dict, Any, Callable, List
import websockets
from websockets.client import WebSocketClientProtocol

from hotstuff_sdk.types import (
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
from hotstuff_sdk.utils import ENDPOINTS_URLS


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
        
        self.ws: Optional[WebSocketClientProtocol] = None
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 5
        self.reconnect_delay = 1.0
        
        self.message_queue: Dict[str, asyncio.Future] = {}
        self.message_id_counter = 0
        
        self.subscriptions: Dict[str, Subscription] = {}
        self.subscription_callbacks: Dict[str, Callable] = {}
        
        self.connection_promise: Optional[asyncio.Task] = None
        self.keep_alive_task: Optional[asyncio.Task] = None
        self.receive_task: Optional[asyncio.Task] = None
        
        self.auto_connect = options.auto_connect
        if self.auto_connect:
            # Don't await here, just schedule it
            asyncio.create_task(self._auto_connect())
    
    async def _auto_connect(self):
        """Auto-connect on initialization."""
        try:
            await self.connect()
        except Exception as e:
            print(f"Auto-connect failed: {e}")
    
    async def _ensure_connected(self):
        """Ensure the WebSocket is connected."""
        if self.ws and not self.ws.closed:
            return
        
        if self.connection_promise:
            await self.connection_promise
            return
        
        await self.connect()
    
    def _cleanup(self):
        """Cleanup resources."""
        if self.keep_alive_task:
            self.keep_alive_task.cancel()
            self.keep_alive_task = None
        
        if self.receive_task:
            self.receive_task.cancel()
            self.receive_task = None
        
        # Reject all pending messages
        for future in self.message_queue.values():
            if not future.done():
                future.set_exception(Exception("WebSocket disconnected"))
        
        self.message_queue.clear()
    
    async def _start_keep_alive(self):
        """Start keep-alive ping loop."""
        interval = self.keep_alive.get("interval")
        if not interval:
            return
        
        while True:
            try:
                await asyncio.sleep(interval)
                await self.ping()
            except asyncio.CancelledError:
                break
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
        future = self.message_queue.pop(msg_id, None)
        
        if future and not future.done():
            if "error" in response:
                error = response["error"]
                future.set_exception(
                    Exception(f"JSON-RPC Error {error.get('code')}: {error.get('message')}")
                )
            else:
                future.set_result(response.get("result"))
    
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
                            timestamp=asyncio.get_event_loop().time()
                        )
                        try:
                            callback(subscription_data)
                        except Exception as e:
                            print(f"Callback error: {e}")
    
    async def _receive_messages(self):
        """Receive messages from WebSocket."""
        try:
            async for message in self.ws:
                try:
                    data = json.loads(message)
                    self._handle_incoming_message(data)
                except json.JSONDecodeError as e:
                    print(f"Failed to parse message: {e}")
                except Exception as e:
                    print(f"Error handling message: {e}")
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"Receive error: {e}")
            # Trigger reconnection
            if self.reconnect_attempts < self.max_reconnect_attempts:
                asyncio.create_task(self._reconnect())
    
    async def _reconnect(self):
        """Reconnect to WebSocket."""
        self._cleanup()
        await asyncio.sleep(self.reconnect_delay * self.reconnect_attempts)
        self.reconnect_attempts += 1
        await self.connect()
    
    async def _send_jsonrpc_message(self, message: dict) -> Any:
        """Send a JSON-RPC message and wait for response."""
        await self._ensure_connected()
        
        # Assign message ID if not present
        if "id" not in message or message["id"] is None:
            self.message_id_counter += 1
            message["id"] = str(self.message_id_counter)
        
        msg_id = str(message["id"])
        
        # Create future for response
        future = asyncio.Future()
        self.message_queue[msg_id] = future
        
        # Set timeout
        if self.timeout:
            async def timeout_handler():
                await asyncio.sleep(self.timeout)
                if msg_id in self.message_queue:
                    self.message_queue.pop(msg_id)
                    if not future.done():
                        future.set_exception(Exception("Request timeout"))
            
            asyncio.create_task(timeout_handler())
        
        # Send message
        await self.ws.send(json.dumps(message))
        
        # Wait for response
        return await future
    
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
    
    async def _subscribe_to_channels(self, params: dict) -> SubscribeResult:
        """Subscribe to channels."""
        message = {
            "jsonrpc": "2.0",
            "method": WSMethod.SUBSCRIBE,
            "params": params,
            "id": None,  # Will be assigned
        }
        
        result = await self._send_jsonrpc_message(message)
        return SubscribeResult(**result) if isinstance(result, dict) else result
    
    async def _unsubscribe_from_channels(self, channels: List[str]) -> UnsubscribeResult:
        """Unsubscribe from channels."""
        message = {
            "jsonrpc": "2.0",
            "method": WSMethod.UNSUBSCRIBE,
            "params": channels,
            "id": None,
        }
        
        result = await self._send_jsonrpc_message(message)
        return UnsubscribeResult(**result) if isinstance(result, dict) else result
    
    def is_connected(self) -> bool:
        """Check if WebSocket is connected."""
        return self.ws is not None and not self.ws.closed
    
    async def connect(self):
        """Connect to WebSocket server."""
        url = self.server["testnet" if self.is_testnet else "mainnet"]
        
        try:
            self.ws = await websockets.connect(url)
            self.reconnect_attempts = 0
            
            # Start keep-alive
            if self.keep_alive.get("interval"):
                self.keep_alive_task = asyncio.create_task(self._start_keep_alive())
            
            # Start receiving messages
            self.receive_task = asyncio.create_task(self._receive_messages())
        
        except Exception as e:
            raise Exception(f"Failed to connect: {e}")
    
    async def disconnect(self):
        """Disconnect from WebSocket server."""
        self._cleanup()
        
        if self.ws:
            await self.ws.close()
            self.ws = None
    
    async def ping(self) -> PongResult:
        """Send ping to server."""
        message = {
            "jsonrpc": "2.0",
            "method": WSMethod.PING,
            "id": None,
        }
        
        result = await self._send_jsonrpc_message(message)
        return PongResult(pong=True)
    
    async def subscribe(
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
        await self._ensure_connected()
        
        subscription_id = f"{channel}_{asyncio.get_event_loop().time()}"
        
        subscription = Subscription(
            id=subscription_id,
            channel=channel,
            symbol=payload.get("instrumentId") or payload.get("symbol"),
            params=payload,
            timestamp=asyncio.get_event_loop().time()
        )
        
        self.subscription_callbacks[subscription_id] = listener
        
        try:
            subscription_params = self._format_subscription_params(channel, payload)
            result = await self._subscribe_to_channels(subscription_params)
            
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
    
    async def unsubscribe(self, subscription_id: str):
        """Unsubscribe from a channel."""
        subscription = self.subscriptions.get(subscription_id)
        if not subscription:
            raise Exception(f"Subscription {subscription_id} not found")
        
        try:
            if self.is_connected():
                await self._unsubscribe_from_channels([subscription.channel])
            
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
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.disconnect()


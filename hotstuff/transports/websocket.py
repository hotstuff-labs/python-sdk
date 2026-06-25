"""WebSocket transport implementation."""
import json
import time
import logging
import threading
import socket
import ssl
from typing import Optional, Dict, Any, Callable, List
from urllib.parse import urlparse
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

logger = logging.getLogger(__name__)


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
                logger.warning("Keep-alive error: %s", e)
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
                            logger.error("Callback error: %s", e)
    
    def _receive_messages(self):
        """Receive messages from WebSocket."""
        while self._running and self.ws:
            try:
                message = self.ws.recv()
                if message:
                    data = json.loads(message)
                    self._handle_incoming_message(data)
            except websocket.WebSocketTimeoutException:
                # An idle recv timeout is normal for sparse channels (e.g. a
                # maker's fills): the socket is healthy, just no frame arrived.
                # Keep the connection and keep listening.
                continue
            except websocket.WebSocketConnectionClosedException:
                if self._running and self.reconnect_attempts < self.max_reconnect_attempts:
                    self._reconnect()
                break
            except json.JSONDecodeError as e:
                logger.warning("Failed to parse message: %s", e)
            except Exception as e:
                logger.error("Receive error: %s", e)
                if self._running and self.reconnect_attempts < self.max_reconnect_attempts:
                    self._reconnect()
                break
    
    def _reconnect(self):
        """Reconnect to WebSocket and replay subscriptions."""
        self._cleanup()
        time.sleep(self.reconnect_delay * self.reconnect_attempts)
        self.reconnect_attempts += 1
        self.connect()
        self._resubscribe_all()

    def _resubscribe_all(self):
        """Replay all known subscriptions onto a freshly reconnected socket.

        `_cleanup` intentionally keeps `self.subscriptions` / callbacks, so the
        local registry survives a reconnect. The server, however, has no record
        of the old subscriptions after the socket is replaced, so we must
        re-send each subscribe request and refresh the server-echoed channel
        used for notification matching.
        """
        if not self.subscriptions:
            return

        for sub_id, subscription in list(self.subscriptions.items()):
            base = subscription.base_channel or subscription.channel
            try:
                params = self._format_subscription_params(base, subscription.params or {})
                result = self._subscribe_to_channels(params)
                if result.status == "subscribed" and result.channels:
                    subscription.channel = result.channels[0]
                else:
                    logger.warning(
                        "Resubscribe rejected for %s (%s): %s",
                        sub_id,
                        base,
                        result.error or result.status,
                    )
            except Exception as e:
                logger.error("Failed to resubscribe %s (%s): %s", sub_id, base, e)
    
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

    def _create_ipv4_socket(self, url: str) -> Optional[socket.socket]:
        """Create a connected IPv4 socket for websocket-client."""
        parsed = urlparse(url)
        hostname = parsed.hostname
        if hostname is None:
            return None

        if parsed.port is not None:
            port = parsed.port
        elif parsed.scheme == "wss":
            port = 443
        else:
            port = 80

        addrinfo = socket.getaddrinfo(hostname, port, socket.AF_INET, socket.SOCK_STREAM)
        last_error = None

        for family, socktype, proto, _, sockaddr in addrinfo:
            raw_socket = socket.socket(family, socktype, proto)
            raw_socket.settimeout(self.timeout)

            try:
                raw_socket.connect(sockaddr)

                if parsed.scheme == "wss":
                    context = ssl.create_default_context()
                    tls_socket = context.wrap_socket(raw_socket, server_hostname=hostname)
                    tls_socket.settimeout(self.timeout)
                    return tls_socket

                return raw_socket
            except Exception as exc:
                last_error = exc
                raw_socket.close()

        if last_error is not None:
            raise last_error
        return None
    
    def connect(self):
        """Connect to WebSocket server."""
        url = self.server["testnet" if self.is_testnet else "mainnet"]
        
        try:
            ipv4_socket = self._create_ipv4_socket(url)
            if ipv4_socket is not None:
                self.ws = websocket.create_connection(url, timeout=self.timeout, socket=ipv4_socket)
            else:
                self.ws = websocket.create_connection(url, timeout=self.timeout)

            # Enable TCP keepalive so a dead peer is detected even on idle
            # channels, independent of the application-level ping loop.
            try:
                if self.ws.sock is not None:
                    self.ws.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            except (OSError, AttributeError) as e:
                logger.debug("Unable to enable TCP keepalive: %s", e)

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

    def _create_abort_error(self) -> Exception:
        """Create a consistent abort error."""
        return Exception("The operation was aborted")

    def _is_signal_aborted(self, signal: Optional[Any]) -> bool:
        """Check whether an optional signal-like object is aborted."""
        if signal is None:
            return False

        # JS-like signal support
        if getattr(signal, "aborted", False):
            return True

        # threading.Event support
        is_set = getattr(signal, "is_set", None)
        if callable(is_set):
            try:
                return bool(is_set())
            except Exception:
                return False

        return False

    def _normalize_request_result(self, result: Any) -> Any:
        """Normalize websocket request payload shape to match HTTP transport."""
        if isinstance(result, dict) and "data" in result and result.get("data") is not None:
            return result["data"]
        return result

    def request(
        self,
        endpoint: str,
        payload: Any,
        signal: Optional[Any] = None
    ) -> Any:
        """
        Send a request over websocket.

        Args:
            endpoint: Request type ('info', 'exchange', or 'explorer')
            payload: Request payload
            signal: Optional signal-like object with `aborted` or `is_set()`

        Returns:
            Request result payload
        """
        if self._is_signal_aborted(signal):
            raise self._create_abort_error()

        self.message_id_counter += 1
        message = {
            "jsonrpc": "2.0",
            "method": WSMethod.POST,
            "params": {
                "type": "action" if endpoint == "exchange" else endpoint,
                "payload": payload,
            },
            "id": str(self.message_id_counter),
        }

        result = self._send_jsonrpc_message(message)

        if self._is_signal_aborted(signal):
            raise self._create_abort_error()

        return self._normalize_request_result(result)
    
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
            timestamp=time.time(),
            base_channel=channel,
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
            logger.error("Failed to unsubscribe: %s", e)
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

"""Type definitions for transports."""
from typing import Optional, Dict, Any, Callable, Awaitable, Union
from dataclasses import dataclass


@dataclass
class HttpTransportOptions:
    """Options for HTTP transport configuration."""
    is_testnet: bool = False
    timeout: Optional[float] = 3.0
    server: Optional[Dict[str, Dict[str, str]]] = None
    headers: Optional[Dict[str, str]] = None
    on_request: Optional[Callable] = None
    on_response: Optional[Callable] = None


@dataclass
class WebSocketTransportOptions:
    """Options for WebSocket transport configuration."""
    is_testnet: bool = False
    timeout: Optional[float] = 10.0
    server: Optional[Dict[str, str]] = None
    keep_alive: Optional[Dict[str, Optional[float]]] = None
    auto_connect: bool = True


@dataclass
class JSONRPCMessage:
    """JSON-RPC 2.0 message."""
    jsonrpc: str = "2.0"
    method: Optional[str] = None
    params: Optional[Union[Dict[str, Any], list]] = None
    id: Optional[Union[str, int]] = None
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None


@dataclass
class JSONRPCResponse:
    """JSON-RPC 2.0 response."""
    jsonrpc: str
    id: Union[str, int]
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None


@dataclass
class JSONRPCNotification:
    """JSON-RPC 2.0 notification."""
    jsonrpc: str
    method: str
    params: Optional[Dict[str, Any]] = None


@dataclass
class SubscriptionData:
    """Subscription data."""
    channel: str
    data: Any
    timestamp: float


@dataclass
class Subscription:
    """Subscription information."""
    id: str
    channel: str
    symbol: Optional[str]
    params: Dict[str, Any]
    timestamp: float


class WSMethod:
    """WebSocket method names."""
    SUBSCRIBE = "subscribe"
    UNSUBSCRIBE = "unsubscribe"
    PING = "ping"


@dataclass
class SubscribeResult:
    """Result of subscription."""
    status: str
    channels: Optional[list] = None
    error: Optional[str] = None
    
    def __init__(self, status: str, channels: Optional[list] = None, error: Optional[str] = None, **kwargs):
        """Initialize SubscribeResult, ignoring extra fields like 'id'."""
        self.status = status
        self.channels = channels
        self.error = error


@dataclass
class UnsubscribeResult:
    """Result of unsubscription."""
    status: str
    channels: Optional[list] = None
    
    def __init__(self, status: str, channels: Optional[list] = None, **kwargs):
        """Initialize UnsubscribeResult, ignoring extra fields like 'id'."""
        self.status = status
        self.channels = channels


@dataclass
class PongResult:
    """Pong response."""
    pong: bool = True


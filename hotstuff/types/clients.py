"""Type definitions for client parameters."""
from typing import TypeVar, Generic, Optional, Callable, Awaitable, Any
from dataclasses import dataclass

# Type variable for transport
T = TypeVar('T')


@dataclass
class InfoClientParameters(Generic[T]):
    """Parameters for InfoClient."""
    transport: T


@dataclass
class ExchangeClientParameters(Generic[T]):
    """Parameters for ExchangeClient."""
    transport: T
    wallet: Any
    nonce: Optional[Callable[[], Awaitable[int]]] = None


@dataclass
class SubscriptionClientParameters(Generic[T]):
    """Parameters for SubscriptionClient."""
    transport: T


@dataclass
class ActionRequest:
    """Action request."""
    action: str
    params: dict


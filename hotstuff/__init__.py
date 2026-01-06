"""Hotstuff Python SDK.

A Python SDK for interacting with Hotstuff Labs decentralized exchange.
"""

__version__ = "0.0.1-beta.1"

from hotstuff.transports import HttpTransport, WebSocketTransport
from hotstuff.apis import InfoClient, ExchangeClient, SubscriptionClient
from hotstuff.types import (
    HttpTransportOptions,
    WebSocketTransportOptions,
)
from hotstuff.utils import NonceManager, sign_action, EXCHANGE_OP_CODES

# Export method types for convenience
from hotstuff.methods.exchange.trading import (
    UnitOrder,
    BrokerConfig,
    PlaceOrderParams,
    CancelByOidParams,
    CancelByCloidParams,
    CancelAllParams,
)
from hotstuff.methods.exchange.account import AddAgentParams

__all__ = [
    # Version
    "__version__",
    # Transports
    "HttpTransport",
    "WebSocketTransport",
    # Clients
    "InfoClient",
    "ExchangeClient",
    "SubscriptionClient",
    # Transport Types
    "HttpTransportOptions",
    "WebSocketTransportOptions",
    # Exchange Method Types (for backward compatibility)
    "UnitOrder",
    "BrokerConfig",
    "PlaceOrderParams",
    "CancelByOidParams",
    "CancelByCloidParams",
    "CancelAllParams",
    "AddAgentParams",
    # Utils
    "NonceManager",
    "sign_action",
    "EXCHANGE_OP_CODES",
]


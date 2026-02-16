"""Hotstuff Python SDK.

A Python SDK for interacting with Hotstuff L1.
"""

__version__ = "0.0.1-beta.8"

# Transports
from hotstuff.transports import HttpTransport, WebSocketTransport

# Clients
from hotstuff.apis import InfoClient, ExchangeClient, SubscriptionClient

# Transport Types
from hotstuff.types import (
    HttpTransportOptions,
    WebSocketTransportOptions,
)

# Utils
from hotstuff.utils import NonceManager, sign_action, EXCHANGE_OP_CODES

# Exceptions
from hotstuff.exceptions import (
    HotstuffError,
    HotstuffAPIError,
    HotstuffConnectionError,
    HotstuffTimeoutError,
    HotstuffAuthenticationError,
    HotstuffValidationError,
    HotstuffInsufficientFundsError,
    HotstuffOrderError,
    HotstuffRateLimitError,
    HotstuffWebSocketError,
    HotstuffSubscriptionError,
)

# Exchange Method Types (for convenience)
from hotstuff.methods.exchange.trading import (
    UnitOrder,
    BrokerConfig,
    PlaceOrderParams,
    CancelByOidParams,
    CancelByCloidParams,
    CancelAllParams,
)
from hotstuff.methods.exchange.account import AddAgentParams

# Market data types (clean imports without 'global' keyword)
from hotstuff.methods.info.market import (
    TickerParams,
    Ticker,
    OrderbookParams,
    OrderbookResponse,
    InstrumentsParams,
    InstrumentsResponse,
    TradesParams,
    Trade,
    OracleParams,
    OracleResponse,
)

# Subscription types (clean imports)
from hotstuff.methods.subscription.channels import (
    TickerSubscriptionParams,
    TradeSubscriptionParams,
    OrderbookSubscriptionParams,
)

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
    # Exceptions
    "HotstuffError",
    "HotstuffAPIError",
    "HotstuffConnectionError",
    "HotstuffTimeoutError",
    "HotstuffAuthenticationError",
    "HotstuffValidationError",
    "HotstuffInsufficientFundsError",
    "HotstuffOrderError",
    "HotstuffRateLimitError",
    "HotstuffWebSocketError",
    "HotstuffSubscriptionError",
    # Exchange Method Types
    "UnitOrder",
    "BrokerConfig",
    "PlaceOrderParams",
    "CancelByOidParams",
    "CancelByCloidParams",
    "CancelAllParams",
    "AddAgentParams",
    # Market Data Types
    "TickerParams",
    "Ticker",
    "OrderbookParams",
    "OrderbookResponse",
    "InstrumentsParams",
    "InstrumentsResponse",
    "TradesParams",
    "Trade",
    "OracleParams",
    "OracleResponse",
    # Subscription Types
    "TickerSubscriptionParams",
    "TradeSubscriptionParams",
    "OrderbookSubscriptionParams",
    # Utils
    "NonceManager",
    "sign_action",
    "EXCHANGE_OP_CODES",
]


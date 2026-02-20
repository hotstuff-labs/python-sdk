"""Hotstuff Python SDK.

A Python SDK for interacting with Hotstuff L1.
"""

__version__ = "0.0.1-beta.10"

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
from hotstuff.utils import NonceManager, sign_action

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
    UnitCancelByOrderId,
    UnitCancelByClOrderId,
    CancelByOidParams,
    CancelByCloidParams,
    CancelAllParams,
)

from hotstuff.methods.exchange.collateral import (
    AccountSpotWithdrawRequestParams,
    AccountDerivativeWithdrawRequestParams,
    AccountSpotBalanceTransferRequestParams,
    AccountDerivativeBalanceTransferRequestParams,
    AccountInternalBalanceTransferRequestParams,
)

from hotstuff.methods.exchange.account import (
    AddAgentParams, 
    RevokeAgentParams,
    UpdatePerpInstrumentLeverageParams, 
    ApproveBrokerFeeParams, 
    CreateReferralCodeParams, 
    SetReferrerParams, 
    ClaimReferralRewardsParams,
)

from hotstuff.methods.exchange.vault import (
    DepositToVaultParams,
    RedeemFromVaultParams,
)


# Market data types (clean imports without 'global' keyword)
from hotstuff.methods.info.market import (
    OracleParams,
    OracleResponse,
    SupportedCollateralParams,
    SupportedCollateral,
    InstrumentsParams,
    InstrumentsResponse,
    TickerParams,
    Ticker,
    OrderbookParams,
    OrderbookResponse,
    TradesParams,
    Trade,
    MidsParams,
    Mid,
    BBOParams,
    BBO,
    ChartParams,
    ChartPoint,
)

# Account data types (clean imports without 'global' keyword)
from hotstuff.methods.info.account import (
    OpenOrdersParams,
    OpenOrdersResponse,
    PositionsParams,
    Position,
    AccountSummaryParams,
    AccountSummaryResponse,
    ReferralSummaryParams,
    ReferralSummaryResponse,
    UserFeeInfoParams,
    UserFeeInfoResponse,
    AccountHistoryParams,
    AccountHistoryResponse,
    OrderHistoryParams,
    OrderHistoryResponse,
    FillsParams,
    FillsResponse,
    FundingHistoryParams,
    FundingHistoryResponse,
    TransferHistoryParams,
    TransferHistoryResponse,
    InstrumentLeverageParams,
    InstrumentLeverageResponse,
    AgentsParams,
    AgentsResponse,
    Agent,
    AccountInfoParams,
    AccountInfoResponse,
)

from hotstuff.methods.info.vault import (
    VaultsParams,
    VaultsResponse,
    SubVaultsParams,
    SubVaultsResponse,
    VaultBalancesParams,
    VaultBalancesResponse,
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
    "AddAgentParams",
    "RevokeAgentParams",
    "UpdatePerpInstrumentLeverageParams",
    "ApproveBrokerFeeParams",
    "CreateReferralCodeParams",
    "SetReferrerParams",
    "ClaimReferralRewardsParams",
    "UnitOrder",
    "BrokerConfig",
    "PlaceOrderParams",
    "CancelByOidParams",
    "CancelByCloidParams",
    "CancelAllParams",
    "UnitCancelByOrderId",
    "UnitCancelByClOrderId",
    "AccountSpotWithdrawRequestParams",
    "AccountDerivativeWithdrawRequestParams",
    "AccountSpotBalanceTransferRequestParams",
    "AccountDerivativeBalanceTransferRequestParams",
    "AccountInternalBalanceTransferRequestParams",
    "DepositToVaultParams",
    "RedeemFromVaultParams",
    # Market Data Types
    "OracleParams",
    "OracleResponse",
    "SupportedCollateralParams",
    "SupportedCollateral",
    "InstrumentsParams",
    "InstrumentsResponse",
    "TickerParams",
    "Ticker",
    "OrderbookParams",
    "OrderbookResponse",
    "TradesParams",
    "Trade",
    "MidsParams",
    "Mid",
    "BBOParams",
    "BBO",
    "ChartParams",
    "ChartPoint",
    # Account Data Types
    "OpenOrdersParams",
    "OpenOrdersResponse",
    "PositionsParams",
    "Position",
    "AccountSummaryParams",
    "AccountSummaryResponse",
    "ReferralSummaryParams",
    "ReferralSummaryResponse",
    "UserFeeInfoParams",
    "UserFeeInfoResponse",
    "AccountHistoryParams",
    "AccountHistoryResponse",
    "OrderHistoryParams",
    "OrderHistoryResponse",
    "FillsParams",
    "FillsResponse",
    "FundingHistoryParams",
    "FundingHistoryResponse",
    "TransferHistoryParams",
    "TransferHistoryResponse",
    "InstrumentLeverageParams",
    "InstrumentLeverageResponse",
    "AgentsParams",
    "AgentsResponse",
    "Agent",
    "AccountInfoParams",
    "AccountInfoResponse",
    # Vault Data Types
    "VaultsParams",
    "VaultsResponse",
    "SubVaultsParams",
    "SubVaultsResponse",
    "VaultBalancesParams",
    "VaultBalancesResponse",
    # Subscription Types
    "TickerSubscriptionParams",
    "TradeSubscriptionParams",
    "OrderbookSubscriptionParams",
    # Utils
    "NonceManager",
    "sign_action",
    "EXCHANGE_OP_CODES",
]


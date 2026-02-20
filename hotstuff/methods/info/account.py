"""Account info method types."""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Optional

from hotstuff.utils.address import validate_ethereum_address


# Open Orders Method
@dataclass
class OpenOrdersParams:
    """Parameters for open orders query."""
    user: str
    page: Optional[int] = None
    limit: Optional[int] = None
    
    def __post_init__(self):
        """Validate and checksum the user address."""
        self.user = validate_ethereum_address(self.user)


@dataclass
class OpenOrder:
    """Open order information."""
    order_id: int
    user: str
    instrument_id: int
    instrument: str
    side: Literal["s", "b"]
    limit_price: str
    size: str
    unfilled: str
    state: Literal["open", "filled", "cancelled", "triggered"]
    cloid: str
    tif: Literal["GTC", "IOC", "FOK"]
    post_only: bool
    reduce_only: bool
    timestamp: str
    tpsl: Optional[str] = None  # Can be "tp", "sl", or ""
    trigger_px: Optional[str] = None
    trigger_price: Optional[str] = None  # Alternative field name
    is_market: Optional[bool] = None  # Optional market order flag
    grouping: Optional[str] = None  # Optional grouping


@dataclass
class OpenOrdersResponse:
    """Open orders response."""
    orders: List[OpenOrder] = field(default_factory=list)
    # Pagination fields (optional)
    page: Optional[int] = None
    limit: Optional[int] = None
    total_count: Optional[int] = None
    total_pages: Optional[int] = None
    has_next: Optional[bool] = None
    has_prev: Optional[bool] = None


# Positions Method
@dataclass
class PositionsParams:
    """Parameters for positions query."""
    user: str
    instrument: Optional[str] = None
    
    def __post_init__(self):
        """Validate and checksum the user address."""
        self.user = validate_ethereum_address(self.user)


@dataclass
class Position:
    """Individual position information."""
    user: str
    instrument_id: int
    instrument: str
    side: Literal["LONG", "SHORT"]
    size: str
    entry_price: str
    margin: str
    unrealized_pnl: str
    mark_price: Optional[str] = None
    realized_pnl: Optional[str] = None
    liquidation_price: Optional[str] = None
    leverage: Optional[str] = None
    margin_type: Optional[str] = None
    updated_at: Optional[int] = None


# Note: positions endpoint returns List[Position] directly, not wrapped in PositionsResponse
PositionsResponse = List[Position]


# Account Summary Method
@dataclass
class AccountSummaryParams:
    """Parameters for account summary query."""
    user: str
    
    def __post_init__(self):
        """Validate and checksum the user address."""
        self.user = validate_ethereum_address(self.user)


@dataclass
class AccountSummaryResponse:
    """Account summary response."""
    address: str
    margin_mode: Optional[str] = None  # e.g. "cross", "isolated"
    multi_asset_mode: Optional[bool] = None
    hedge_mode: Optional[bool] = None
    spot_collateral: Optional[Dict[str, Any]] = field(default_factory=dict)
    collateral: Optional[Dict[str, Any]] = field(default_factory=dict)  # e.g. {"USDC": {"balance", "withdrawable_balance"}}
    vault_balances: Optional[Dict[str, Any]] = field(default_factory=dict)
    staked_collateral: Optional[float] = None
    perp_positions: Optional[Dict[str, Any]] = field(default_factory=dict)  # instrument -> position details
    initial_margin_utilization: Optional[float] = None
    maintenance_margin_utilization: Optional[float] = None
    upnl: Optional[float] = None
    total_account_equity: Optional[float] = None
    margin_balance: Optional[float] = None
    initial_margin: Optional[float] = None
    maintenance_margin: Optional[float] = None
    total_volume: Optional[float] = None
    total_pnl: Optional[float] = None
    available_balance: Optional[float] = None
    withdrawable_balance_notional: Optional[float] = None
    transfer_margin_req: Optional[float] = None
    max_drawdown: Optional[float] = None
    vault_summary: Optional[Dict[str, Any]] = field(default_factory=dict)
    spot_account_equity: Optional[float] = None
    derivative_account_equity: Optional[float] = None
    spot_volume: Optional[float] = None
    perp_volume: Optional[float] = None


# Referral Summary Method
@dataclass
class ReferralSummaryParams:
    """Parameters for referral summary query."""
    user: str
    
    def __post_init__(self):
        """Validate and checksum the user address."""
        self.user = validate_ethereum_address(self.user)


@dataclass
class ReferralVolumeBreakdown:
    """Volume breakdown by maker/taker."""
    maker_volume: float
    taker_volume: float


@dataclass
class ReferredUser:
    """Referred user details."""
    code: str
    joined_at: int
    referred_volume: float
    perp_volume: ReferralVolumeBreakdown
    spot_volume: ReferralVolumeBreakdown
    stable_spot_volume: ReferralVolumeBreakdown
    referred_perp_rewards: float
    referred_spot_rewards: float


@dataclass
class ReferralTier:
    """Referral tier information."""
    total_referred_volume: float
    fee_discount_rate: float
    referrer_commission: float


@dataclass
class ReferralSummaryResponse:
    """Referral summary response."""
    address: str
    referrer: str
    referrer_code: str
    refer_timestamp: int
    is_affiliate: bool
    codes: List[str]
    referred_users: Dict[str, ReferredUser]
    to_claim_perp_rewards: float
    to_claim_spot_rewards: float
    claimed_perp_rewards: float
    claimed_spot_rewards: float
    total_referred_volume: float
    rolling_referred_volume: float
    referral_tier: ReferralTier
    updated_at: int


# User Fee Info Method
@dataclass
class UserFeeInfoParams:
    """Parameters for user fee info query."""
    user: str
    
    def __post_init__(self):
        """Validate and checksum the user address."""
        self.user = validate_ethereum_address(self.user)


@dataclass
class UserFeeInfoResponse:
    """User fee info response."""
    account: str
    spot_volume_14d: Optional[str] = None
    spot_volume_30d: Optional[str] = None
    stable_spot_volume_14d: Optional[str] = None
    stable_spot_volume_30d: Optional[str] = None
    perp_volume_14d: Optional[str] = None
    perp_volume_30d: Optional[str] = None
    option_volume_14d: Optional[str] = None
    option_volume_30d: Optional[str] = None
    total_volume_threshold: Optional[int] = None
    perp_maker_fee_rate: Optional[float] = None
    perp_taker_fee_rate: Optional[float] = None
    spot_maker_fee_rate: Optional[float] = None
    spot_taker_fee_rate: Optional[float] = None
    stable_spot_maker_fee_rate: Optional[float] = None
    stable_spot_taker_fee_rate: Optional[float] = None
    option_maker_fee_rate: Optional[float] = None
    option_taker_fee_rate: Optional[float] = None


# Account History Method
@dataclass
class AccountHistoryParams:
    """Parameters for account history query."""
    user: str
    
    def __post_init__(self):
        """Validate and checksum the user address."""
        self.user = validate_ethereum_address(self.user)


@dataclass
class AccountHistory:
    """Account history entry."""
    address: str
    total_pnl: str
    total_volume: float
    account_value: str
    created_at: str
    # Additional fields returned by API
    perp_volume: Optional[float] = None
    spot_volume: Optional[float] = None
    stable_spot_volume: Optional[float] = None
    perp_pnl: Optional[str] = None
    spot_pnl: Optional[str] = None


# Note: account history endpoint returns List[AccountHistory] directly
AccountHistoryResponse = List[AccountHistory]


# Order History Method
@dataclass
class OrderHistoryParams:
    """Parameters for order history query."""
    user: str
    instrument_id: Optional[str] = None
    limit: Optional[int] = None
    
    def __post_init__(self):
        """Validate and checksum the user address."""
        self.user = validate_ethereum_address(self.user)


@dataclass
class OrderHistoryEntry:
    """Single order history entry."""
    order_id: Optional[int] = None
    oid: Optional[int] = None
    user: Optional[str] = None
    instrument_id: Optional[int] = None
    instrument: Optional[str] = None
    side: Optional[Literal["s", "b"]] = None
    price: Optional[str] = None
    size: Optional[str] = None
    state: Optional[str] = None
    created_at: Optional[str] = None
    timestamp: Optional[str] = None
    cloid: Optional[str] = None
    tif: Optional[str] = None
    filled: Optional[str] = None
    unfilled: Optional[str] = None


@dataclass
class OrderHistoryResponse:
    """Order history response."""
    orders: List[OrderHistoryEntry] = field(default_factory=list)
    page: Optional[int] = None
    limit: Optional[int] = None
    total_count: Optional[int] = None
    total_pages: Optional[int] = None
    has_next: Optional[bool] = None
    has_prev: Optional[bool] = None


# Trade History Method (Fills)
@dataclass
class FillsParams:
    """Parameters for trade history (fills) query."""
    user: str
    instrument_id: Optional[str] = None
    limit: Optional[int] = None
    
    def __post_init__(self):
        """Validate and checksum the user address."""
        self.user = validate_ethereum_address(self.user)


@dataclass
class Fill:
    """Single fill / trade history entry."""
    instrument_id: int
    instrument: str
    account: str
    order_id: int
    trade_id: int
    side: Literal["b", "s"]
    position_side: str
    price: str
    size: str
    cloid: Optional[str] = None
    direction: Optional[str] = None  # e.g. "openLong", "closeLong", "openShort", "closeShort"
    closed_pnl: Optional[str] = None
    start_size: Optional[str] = None
    start_price: Optional[str] = None
    fee: Optional[str] = None
    broker_fee: Optional[str] = None
    fee_token_id: Optional[int] = None
    crossed: Optional[bool] = None
    tx_hash: Optional[str] = None
    fill_type: Optional[int] = None
    notional_value: Optional[str] = None
    block_timestamp: Optional[str] = None
    # liquidation_info optional object when fill is from liquidation

@dataclass
class FillsResponse:
    """Fills response. API returns data in top-level 'data' key."""
    entries: List[Fill] = field(default_factory=list)
    page: Optional[int] = None
    limit: Optional[int] = None
    total_count: Optional[int] = None
    total_pages: Optional[int] = None
    has_next: Optional[bool] = None
    has_prev: Optional[bool] = None


# Funding History Method
@dataclass
class FundingHistoryParams:
    """Parameters for funding history query."""
    user: str
    
    def __post_init__(self):
        """Validate and checksum the user address."""
        self.user = validate_ethereum_address(self.user)


@dataclass
class FundingHistoryEntry:
    """Single funding history entry."""
    user: str
    instrument_id: int
    settlement_currency: int
    funding_payment: str
    funding_rate: str
    mark_price: str
    size: str
    timestamp: str


@dataclass
class FundingHistoryResponse:
    """Funding history response. API returns data in top-level 'data' key."""
    entries: List[FundingHistoryEntry] = field(default_factory=list)
    page: Optional[int] = None
    limit: Optional[int] = None
    total_count: Optional[int] = None
    total_pages: Optional[int] = None
    has_next: Optional[bool] = None
    has_prev: Optional[bool] = None


# Transfer History Method
@dataclass
class TransferHistoryParams:
    """Parameters for transfer history query."""
    user: str
    
    def __post_init__(self):
        """Validate and checksum the user address."""
        self.user = validate_ethereum_address(self.user)

@dataclass
class TransferHistory:
    """Transfer history entry."""
    from_address: str  # 'from' in API response
    to: str
    collateral_id: int
    amount: str
    tx_hash: str
    type: Literal["deposit", "spot_withdraw", "derivative_withdraw", "spot_balance_transfer", "derivative_balance_transfer", "internal_balance_transfer", "vault_deposit", "vault_withdraw"]
    timestamp: str

# Note: transfer history endpoint returns List[TransferHistory] directly
TransferHistoryResponse = List[TransferHistory]


# Instrument Leverage Method
@dataclass
class InstrumentLeverageParams:
    """Parameters for instrument leverage query."""
    user: str
    symbol: str
    
    def __post_init__(self):
        """Validate and checksum the user address."""
        self.user = validate_ethereum_address(self.user)

@dataclass
class InstrumentLeverageResponse:
    """Instrument leverage response."""
    address: str
    instrument_id: int
    instrument: str
    margin_type: str  # e.g. "isolated", "cross"
    leverage: str
    updated_at: int


# Referral Info Method
@dataclass
class ReferralInfoParams:
    """Parameters for referral info query."""
    user: str
    
    def __post_init__(self):
        """Validate and checksum the user address."""
        self.user = validate_ethereum_address(self.user)

@dataclass
class ReferralInfoResponse:
    """Referral info response."""
    pass

# Agents Method
@dataclass
class AgentsParams:
    """Parameters for agents query."""
    user: str
    
    def __post_init__(self):
        """Validate and checksum the user address."""
        self.user = validate_ethereum_address(self.user)

@dataclass
class Agent:
    """Agent information."""
    user: str
    agent_address: Optional[str] = None
    agent_name: Optional[str] = None
    created_at_block_timestamp: Optional[int] = None
    valid_until_timestamp: Optional[int] = None
    
    def __post_init__(self):
        """Validate and checksum Ethereum addresses."""
        self.user = validate_ethereum_address(self.user)
        if self.agent_address:
            self.agent_address = validate_ethereum_address(self.agent_address)

@dataclass
class AgentsResponse:
    """Agents response."""
    pass

# Account Info Method
@dataclass
class AccountInfoParams:
    """Parameters for account info query."""
    user: str
    collateralId: Optional[int] = None
    includeHistory: Optional[bool] = None
    
    def __post_init__(self):
        """Validate and checksum the user address."""
        self.user = validate_ethereum_address(self.user)

@dataclass
class AccountInfoAccount:
    """Account details within account info response."""
    address: str
    role: int
    margin_mode: Literal["cross", "isolated"]
    multi_asset_mode: bool
    hedge_mode: bool
    referrer: str
    referral_codes: List[str]
    referral_timestamp: int
    created_at_block_timestamp: int

@dataclass
class AccountInfoReward:
    """Reward entry within account info response."""
    account: str
    collateral_id: int
    source: str
    is_spot: bool
    amount: str
    claim_amount: str
    created_at: int

@dataclass
class AccountInfoResponse:
    """Account info response."""
    account: AccountInfoAccount
    rewards: List[AccountInfoReward] = field(default_factory=list)
    history: List[AccountInfoReward] = field(default_factory=list)



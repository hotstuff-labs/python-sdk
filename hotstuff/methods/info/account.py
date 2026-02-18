"""Account info method types."""
from typing import Dict, List, Literal, Optional, Annotated
from pydantic import BaseModel, Field, ConfigDict, field_validator, RootModel

from hotstuff.utils.address import validate_ethereum_address


# Type alias for validated Ethereum addresses (similar to viem's Address type)
EthereumAddress = Annotated[
    str,
    Field(
        ...,
        description="Ethereum address (validated and checksummed)",
        examples=["0x1234567890123456789012345678901234567890"],
    ),
]


# Open Orders Method
class OpenOrdersParams(BaseModel):
    """Parameters for open orders query."""
    user: str = Field(..., description="User address")
    page: Optional[int] = Field(None, description="Page number")
    limit: Optional[int] = Field(None, description="Number of orders per page")
    
    @field_validator('user', mode='before')
    @classmethod
    def validate_user_address(cls, v: str) -> str:
        """Validate and checksum the user address."""
        return validate_ethereum_address(v)


class OpenOrder(BaseModel):
    """Open order information."""
    model_config = ConfigDict(extra='allow')
    
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
    tpsl: Optional[str] = None  # Can be "tp", "sl", or ""
    trigger_px: Optional[str] = None
    trigger_price: Optional[str] = None  # Alternative field name
    post_only: bool
    reduce_only: bool
    is_market: Optional[bool] = None  # Optional market order flag
    grouping: Optional[str] = None  # Optional grouping
    timestamp: str


class OpenOrdersResponse(BaseModel):
    """Open orders response."""
    model_config = ConfigDict(extra='allow')
    
    orders: List[OpenOrder] = Field(default_factory=list, description="List of open orders")
    # Pagination fields (optional)
    page: Optional[int] = None
    limit: Optional[int] = None
    total_count: Optional[int] = Field(None, alias="totalCount")
    total_pages: Optional[int] = Field(None, alias="totalPages")
    has_next: Optional[bool] = Field(None, alias="hasNext")
    has_prev: Optional[bool] = Field(None, alias="hasPrev")


# Positions Method
class PositionsParams(BaseModel):
    """Parameters for positions query."""
    user: str = Field(..., description="User address")
    instrument: Optional[str] = Field(None, description="Filter by instrument")
    
    @field_validator('user', mode='before')
    @classmethod
    def validate_user_address(cls, v: str) -> str:
        """Validate and checksum the user address."""
        return validate_ethereum_address(v)


class Position(BaseModel):
    """Individual position information."""
    model_config = ConfigDict(populate_by_name=True, extra='allow')
    
    user: str
    instrument_id: int = Field(alias="instrumentId")
    instrument: str
    side: Literal["LONG", "SHORT"]
    size: str
    entry_price: str = Field(alias="entryPrice")
    mark_price: Optional[str] = Field(None, alias="markPrice")
    margin: str
    unrealized_pnl: str = Field(alias="unrealizedPnl")
    realized_pnl: Optional[str] = Field(None, alias="realizedPnl")
    liquidation_price: Optional[str] = Field(None, alias="liquidationPrice")
    leverage: Optional[str] = None
    margin_type: Optional[str] = Field(None, alias="marginType")
    updated_at: Optional[int] = Field(None, alias="updatedAt")


# Note: positions endpoint returns List[Position] directly, not wrapped in PositionsResponse
PositionsResponse = List[Position]


# Account Summary Method
class AccountSummaryParams(BaseModel):
    """Parameters for account summary query."""
    user: str = Field(..., description="User address")
    
    @field_validator('user', mode='before')
    @classmethod
    def validate_user_address(cls, v: str) -> str:
        """Validate and checksum the user address."""
        return validate_ethereum_address(v)


class AccountSummaryResponse(BaseModel):
    """Account summary response."""
    total_balance: str
    total_equity: str
    total_free: str
    total_margin: str
    total_profit_loss: str


# Referral Summary Method
class ReferralSummaryParams(BaseModel):
    """Parameters for referral summary query."""
    user: str = Field(..., description="User address")
    
    @field_validator('user', mode='before')
    @classmethod
    def validate_user_address(cls, v: str) -> str:
        """Validate and checksum the user address."""
        return validate_ethereum_address(v)


class ReferralSummaryResponse(BaseModel):
    """Referral summary response."""
    model_config = ConfigDict(populate_by_name=True, extra='allow')
    
    referral_code: Optional[str] = Field(None, alias="referralCode")
    total_referrals: Optional[int] = Field(None, alias="totalReferrals")
    total_volume: Optional[str] = Field(None, alias="totalVolume")
    total_rewards: Optional[str] = Field(None, alias="totalRewards")
    tier: Optional[str] = None


# User Fee Info Method
class UserFeeInfoParams(BaseModel):
    """Parameters for user fee info query."""
    user: str = Field(..., description="User address")
    
    @field_validator('user', mode='before')
    @classmethod
    def validate_user_address(cls, v: str) -> str:
        """Validate and checksum the user address."""
        return validate_ethereum_address(v)


class UserFeeInfoResponse(BaseModel):
    """User fee info response."""
    model_config = ConfigDict(populate_by_name=True, extra='allow')
    
    account: str
    spot_volume_14d: Optional[str] = Field(None, alias="spotVolume14d")
    spot_volume_30d: Optional[str] = Field(None, alias="spotVolume30d")
    stable_spot_volume_14d: Optional[str] = Field(None, alias="stableSpotVolume14d")
    stable_spot_volume_30d: Optional[str] = Field(None, alias="stableSpotVolume30d")
    perp_volume_14d: Optional[str] = Field(None, alias="perpVolume14d")
    perp_volume_30d: Optional[str] = Field(None, alias="perpVolume30d")
    option_volume_14d: Optional[str] = Field(None, alias="optionVolume14d")
    option_volume_30d: Optional[str] = Field(None, alias="optionVolume30d")
    total_volume_threshold: Optional[int] = Field(None, alias="totalVolumeThreshold")
    perp_maker_fee_rate: Optional[float] = Field(None, alias="perpMakerFeeRate")
    perp_taker_fee_rate: Optional[float] = Field(None, alias="perpTakerFeeRate")
    spot_maker_fee_rate: Optional[float] = Field(None, alias="spotMakerFeeRate")
    spot_taker_fee_rate: Optional[float] = Field(None, alias="spotTakerFeeRate")
    stable_spot_maker_fee_rate: Optional[float] = Field(None, alias="stableSpotMakerFeeRate")
    stable_spot_taker_fee_rate: Optional[float] = Field(None, alias="stableSpotTakerFeeRate")
    option_maker_fee_rate: Optional[float] = Field(None, alias="optionMakerFeeRate")
    option_taker_fee_rate: Optional[float] = Field(None, alias="optionTakerFeeRate")


# Account History Method
class AccountHistoryParams(BaseModel):
    """Parameters for account history query."""
    user: str = Field(..., description="User address")
    
    @field_validator('user', mode='before')
    @classmethod
    def validate_user_address(cls, v: str) -> str:
        """Validate and checksum the user address."""
        return validate_ethereum_address(v)


class AccountHistoryResponse(BaseModel):
    """Account history response."""
    pass 


# Order History Method
class OrderHistoryParams(BaseModel):
    """Parameters for order history query."""
    model_config = ConfigDict(populate_by_name=True)
    
    user: str = Field(..., description="User address")
    instrument_id: Optional[str] = Field(None, alias="instrumentId", description="Filter by instrument ID")
    limit: Optional[int] = Field(None, description="Number of orders to return")
    
    @field_validator('user', mode='before')
    @classmethod
    def validate_user_address(cls, v: str) -> str:
        """Validate and checksum the user address."""
        return validate_ethereum_address(v)


class OrderHistoryEntry(BaseModel):
    """Single order history entry."""
    model_config = ConfigDict(populate_by_name=True, extra='allow')
    
    order_id: Optional[int] = Field(None, alias="orderId")
    oid: Optional[int] = None
    user: Optional[str] = None
    instrument_id: Optional[int] = Field(None, alias="instrumentId")
    instrument: Optional[str] = None
    side: Optional[Literal["s", "b"]] = None
    price: Optional[str] = None
    size: Optional[str] = None
    state: Optional[str] = None
    created_at: Optional[str] = Field(None, alias="createdAt")
    timestamp: Optional[str] = None
    cloid: Optional[str] = None
    tif: Optional[str] = None
    filled: Optional[str] = None
    unfilled: Optional[str] = None


class OrderHistoryResponse(BaseModel):
    """Order history response."""
    model_config = ConfigDict(populate_by_name=True, extra='allow')
    
    orders: List[OrderHistoryEntry] = Field(default_factory=list, description="List of order history entries")
    page: Optional[int] = None
    limit: Optional[int] = None
    total_count: Optional[int] = Field(None, alias="totalCount")
    total_pages: Optional[int] = Field(None, alias="totalPages")
    has_next: Optional[bool] = Field(None, alias="hasNext")
    has_prev: Optional[bool] = Field(None, alias="hasPrev")


# Trade History Method (Fills)
class TradeHistoryParams(BaseModel):
    """Parameters for trade history (fills) query."""
    model_config = ConfigDict(populate_by_name=True)
    
    user: str = Field(..., description="User address")
    instrument_id: Optional[str] = Field(None, alias="instrumentId", description="Filter by instrument ID")
    limit: Optional[int] = Field(None, description="Number of trades to return")
    
    @field_validator('user', mode='before')
    @classmethod
    def validate_user_address(cls, v: str) -> str:
        """Validate and checksum the user address."""
        return validate_ethereum_address(v)


class TradeHistoryEntry(BaseModel):
    """Single fill / trade history entry."""
    model_config = ConfigDict(populate_by_name=True, extra='allow')
    
    instrument_id: int = Field(..., alias="instrumentId")
    instrument: str
    account: str
    order_id: int = Field(..., alias="orderId")
    cloid: Optional[str] = None
    trade_id: int = Field(..., alias="tradeId")
    side: Literal["b", "s"]
    position_side: str = Field(..., alias="positionSide")
    direction: Optional[str] = None  # e.g. "openLong", "closeLong", "openShort", "closeShort"
    price: str
    size: str
    closed_pnl: Optional[str] = Field(None, alias="closedPnl")
    start_size: Optional[str] = Field(None, alias="startSize")
    start_price: Optional[str] = Field(None, alias="startPrice")
    fee: Optional[str] = None
    broker_fee: Optional[str] = Field(None, alias="brokerFee")
    fee_token_id: Optional[int] = Field(None, alias="feeTokenId")
    crossed: Optional[bool] = None
    tx_hash: Optional[str] = Field(None, alias="txHash")
    fill_type: Optional[int] = Field(None, alias="fillType")
    notional_value: Optional[str] = Field(None, alias="notionalValue")
    block_timestamp: Optional[str] = Field(None, alias="blockTimestamp")
    # liquidation_info optional object when fill is from liquidation


class TradeHistoryResponse(BaseModel):
    """Trade history (fills) response. API returns data in top-level 'data' key."""
    model_config = ConfigDict(populate_by_name=True, extra='allow')
    
    entries: List[TradeHistoryEntry] = Field(default_factory=list, description="List of fill/trade entries")
    page: Optional[int] = None
    limit: Optional[int] = None
    total_count: Optional[int] = Field(None, alias="totalCount")
    total_pages: Optional[int] = Field(None, alias="totalPages")
    has_next: Optional[bool] = Field(None, alias="hasNext")
    has_prev: Optional[bool] = Field(None, alias="hasPrev")


# Funding History Method
class FundingHistoryParams(BaseModel):
    """Parameters for funding history query."""
    user: str = Field(..., description="User address")
    
    @field_validator('user', mode='before')
    @classmethod
    def validate_user_address(cls, v: str) -> str:
        """Validate and checksum the user address."""
        return validate_ethereum_address(v)


class FundingHistoryEntry(BaseModel):
    """Single funding history entry."""
    model_config = ConfigDict(populate_by_name=True, extra='allow')
    
    user: str
    instrument_id: int = Field(..., alias="instrumentId")
    settlement_currency: int = Field(..., alias="settlementCurrency")
    funding_payment: str = Field(..., alias="fundingPayment")
    funding_rate: str = Field(..., alias="fundingRate")
    mark_price: str = Field(..., alias="markPrice")
    size: str
    timestamp: str


class FundingHistoryResponse(BaseModel):
    """Funding history response. API returns data in top-level 'data' key."""
    model_config = ConfigDict(populate_by_name=True, extra='allow')
    
    entries: List[FundingHistoryEntry] = Field(default_factory=list, description="List of funding history entries")
    page: Optional[int] = None
    limit: Optional[int] = None
    total_count: Optional[int] = Field(None, alias="totalCount")
    total_pages: Optional[int] = Field(None, alias="totalPages")
    has_next: Optional[bool] = Field(None, alias="hasNext")
    has_prev: Optional[bool] = Field(None, alias="hasPrev")


# Transfer History Method
class TransferHistoryParams(BaseModel):
    """Parameters for transfer history query."""
    user: str = Field(..., description="User address")
    
    @field_validator('user', mode='before')
    @classmethod
    def validate_user_address(cls, v: str) -> str:
        """Validate and checksum the user address."""
        return validate_ethereum_address(v)


class TransferHistoryResponse(BaseModel):
    """Transfer history response."""
    pass 


# Instrument Leverage Method
class InstrumentLeverageParams(BaseModel):
    """Parameters for instrument leverage query."""
    user: str = Field(..., description="User address")
    symbol: str = Field(..., description="Instrument symbol")
    
    @field_validator('user', mode='before')
    @classmethod
    def validate_user_address(cls, v: str) -> str:
        """Validate and checksum the user address."""
        return validate_ethereum_address(v)


class InstrumentLeverageResponse(BaseModel):
    """Instrument leverage response."""
    model_config = ConfigDict(populate_by_name=True, extra='allow')
    
    address: str
    instrument_id: int = Field(..., alias="instrumentId")
    instrument: str
    margin_type: str = Field(..., alias="marginType")  # e.g. "isolated", "cross"
    leverage: str
    updated_at: int = Field(..., alias="updatedAt")


# Referral Info Method
class ReferralInfoParams(BaseModel):
    """Parameters for referral info query."""
    user: str = Field(..., description="User address")
    
    @field_validator('user', mode='before')
    @classmethod
    def validate_user_address(cls, v: str) -> str:
        """Validate and checksum the user address."""
        return validate_ethereum_address(v)


class ReferralInfoResponse(BaseModel):
    """Referral info response."""
    pass 


# Sub Accounts List Method
class SubAccountsListParams(BaseModel):
    """Parameters for sub accounts list query."""
    user: str = Field(..., description="User address")
    
    @field_validator('user', mode='before')
    @classmethod
    def validate_user_address(cls, v: str) -> str:
        """Validate and checksum the user address."""
        return validate_ethereum_address(v)


class SubAccountsListResponse(BaseModel):
    """Sub accounts list response."""
    pass 


# Agents Method
class AgentsParams(BaseModel):
    """Parameters for agents query."""
    user: str = Field(..., description="User address")
    
    @field_validator('user', mode='before')
    @classmethod
    def validate_user_address(cls, v: str) -> str:
        """Validate and checksum the user address."""
        return validate_ethereum_address(v)


class Agent(BaseModel):
    """Agent information."""
    user: str = Field(..., description="User address")
    agent_address: Optional[str] = Field(None, description="Agent address")
    agent_name: Optional[str] = Field(None, description="Agent name")
    created_at_block_timestamp: Optional[int] = Field(None, description="Creation timestamp")
    valid_until_timestamp: Optional[int] = Field(None, description="Validity expiration timestamp")
    
    model_config = ConfigDict(populate_by_name=True)
    
    @field_validator('user', 'agent_address', mode='before')
    @classmethod
    def validate_addresses(cls, v: Optional[str]) -> Optional[str]:
        """Validate and checksum Ethereum addresses."""
        if v is None or v == "":
            return v
        return validate_ethereum_address(v)


class AgentsResponse(BaseModel):
    """Agents response."""
    pass


# User Balance Info Method
class UserBalanceInfoParams(BaseModel):
    """Parameters for user balance info query."""
    user: str = Field(..., description="User address")
    type: Literal["all", "spot", "derivative"] = Field(..., description="Balance type")
    
    @field_validator('user', mode='before')
    @classmethod
    def validate_user_address(cls, v: str) -> str:
        """Validate and checksum the user address."""
        return validate_ethereum_address(v)


class UserBalanceInfoResponse(BaseModel):
    """User balance info response.
    Keys are collateral currency IDs (e.g. "1"), values are balance strings.
    """
    model_config = ConfigDict(extra='allow')
    
    spot: Dict[str, str] = Field(default_factory=dict, description="Spot balances by collateral currency ID")
    derivative: Dict[str, str] = Field(default_factory=dict, description="Derivative balances by collateral currency ID")


# Account Info Method
class AccountInfoParams(BaseModel):
    """Parameters for account info query."""
    model_config = ConfigDict(populate_by_name=True)
    
    user: str = Field(..., description="User address")
    collateral_id: Optional[int] = Field(None, alias="collateralID", description="Collateral ID")
    include_history: Optional[bool] = Field(None, alias="includeHistory", description="Include history")
    
    @field_validator('user', mode='before')
    @classmethod
    def validate_user_address(cls, v: str) -> str:
        """Validate and checksum the user address."""
        return validate_ethereum_address(v)


class AccountInfoResponse(BaseModel):
    """Account info response."""
    pass 

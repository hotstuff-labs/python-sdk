"""Account info method types."""
from typing import List, Literal, Optional, Annotated
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
    
    maker_fee: Optional[str] = Field(None, alias="makerFee")
    taker_fee: Optional[str] = Field(None, alias="takerFee")
    volume_tier: Optional[str] = Field(None, alias="volumeTier")
    trading_volume_30d: Optional[str] = Field(None, alias="tradingVolume30d")
    discount: Optional[str] = None


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


class OrderHistoryResponse(BaseModel):
    """Order history response."""
    pass 


# Trade History Method
class TradeHistoryParams(BaseModel):
    """Parameters for trade history query."""
    model_config = ConfigDict(populate_by_name=True)
    
    user: str = Field(..., description="User address")
    instrument_id: Optional[str] = Field(None, alias="instrumentId", description="Filter by instrument ID")
    limit: Optional[int] = Field(None, description="Number of trades to return")
    
    @field_validator('user', mode='before')
    @classmethod
    def validate_user_address(cls, v: str) -> str:
        """Validate and checksum the user address."""
        return validate_ethereum_address(v)


class TradeHistoryResponse(BaseModel):
    """Trade history response."""
    pass 


# Funding History Method
class FundingHistoryParams(BaseModel):
    """Parameters for funding history query."""
    user: str = Field(..., description="User address")
    
    @field_validator('user', mode='before')
    @classmethod
    def validate_user_address(cls, v: str) -> str:
        """Validate and checksum the user address."""
        return validate_ethereum_address(v)


class FundingHistoryResponse(BaseModel):
    """Funding history response."""
    pass 


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
    pass 


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
    """User balance info response."""
    pass 


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

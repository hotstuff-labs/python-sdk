"""Global subscription method types."""
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, field_validator
from eth_utils import is_address, to_checksum_address


def validate_ethereum_address(value: str) -> str:
    """
    Validate and normalize an Ethereum address.
    
    Args:
        value: The address string to validate
        
    Returns:
        Checksummed address string
        
    Raises:
        ValueError: If the address is invalid
    """
    if not isinstance(value, str):
        raise ValueError(f"Address must be a string, got {type(value)}")
    
    if not is_address(value):
        raise ValueError(f"Invalid Ethereum address: {value}")
    
    return to_checksum_address(value)


# Chart types
SupportedChartResolutions = Literal["1", "5", "15", "60", "240", "1D", "1W"]
SupportedChartTypes = Literal["mark", "ltp", "index"]


# Subscription parameter types
class TickerSubscriptionParams(BaseModel):
    """Parameters for ticker subscription."""
    symbol: str = Field(..., description="Trading pair symbol")


class MidsSubscriptionParams(BaseModel):
    """Parameters for mids subscription."""
    symbol: str = Field(..., description="Trading pair symbol")


class BBOSubscriptionParams(BaseModel):
    """Parameters for BBO subscription."""
    symbol: str = Field(..., description="Trading pair symbol")


class OrderbookSubscriptionParams(BaseModel):
    """Parameters for orderbook subscription."""
    instrument_id: str = Field(..., description="Instrument ID")


class TradeSubscriptionParams(BaseModel):
    """Parameters for trade subscription."""
    instrument_id: str = Field(..., description="Instrument ID")


class ChartSubscriptionParams(BaseModel):
    """Parameters for chart subscription."""
    symbol: str = Field(..., description="Trading pair symbol")
    chart_type: SupportedChartTypes = Field(..., description="Chart type")
    resolution: SupportedChartResolutions = Field(..., description="Chart resolution")


class AccountOrderUpdatesParams(BaseModel):
    """Parameters for account order updates subscription."""
    address: str = Field(..., description="User address")
    
    @field_validator('address', mode='before')
    @classmethod
    def validate_address(cls, v: str) -> str:
        """Validate and checksum the user address."""
        return validate_ethereum_address(v)


class AccountBalanceUpdatesParams(BaseModel):
    """Parameters for account balance updates subscription."""
    address: str = Field(..., description="User address")
    
    @field_validator('address', mode='before')
    @classmethod
    def validate_address(cls, v: str) -> str:
        """Validate and checksum the user address."""
        return validate_ethereum_address(v)


class PositionsSubscriptionParams(BaseModel):
    """Parameters for positions subscription."""
    address: str = Field(..., description="User address")
    
    @field_validator('address', mode='before')
    @classmethod
    def validate_address(cls, v: str) -> str:
        """Validate and checksum the user address."""
        return validate_ethereum_address(v)


class FillsSubscriptionParams(BaseModel):
    """Parameters for fills subscription."""
    address: str = Field(..., description="User address")
    
    @field_validator('address', mode='before')
    @classmethod
    def validate_address(cls, v: str) -> str:
        """Validate and checksum the user address."""
        return validate_ethereum_address(v)


class AccountSummarySubscriptionParams(BaseModel):
    """Parameters for account summary subscription."""
    user: str = Field(..., description="User address")
    
    @field_validator('user', mode='before')
    @classmethod
    def validate_user_address(cls, v: str) -> str:
        """Validate and checksum the user address."""
        return validate_ethereum_address(v)


class BlocksSubscriptionParams(BaseModel):
    """Parameters for blocks subscription."""
    pass


class TransactionsSubscriptionParams(BaseModel):
    """Parameters for transactions subscription."""
    pass


# Orderbook subscription
class OrderbookItem(BaseModel):
    """Orderbook item."""
    price: float
    size: float
    amount: Optional[float] = None  # Alternative field name


class Orderbook(BaseModel):
    """Orderbook subscription data."""
    instrument_id: str
    instrument_name: Optional[str] = None  # Alternative field name
    asks: List[OrderbookItem]
    bids: List[OrderbookItem]
    timestamp: int


# Trade subscription
class Trade(BaseModel):
    """Trade subscription data."""
    id: str
    instrument: str
    instrument_name: Optional[str] = None
    maker: str
    taker: str
    price: float
    size: float
    timestamp: int
    side: Literal["buy", "sell"]


# Order update subscription
class OrderUpdate(BaseModel):
    """Order update subscription data."""
    id: str
    account: str
    instrument: str
    price: float
    size: float
    side: Literal["buy", "sell"]
    status: str
    timestamp: int


# Account balance update subscription
class BalanceItem(BaseModel):
    """Balance item."""
    asset: str
    total: float
    available: float
    locked: float


class AccountBalanceUpdate(BaseModel):
    """Account balance update subscription data."""
    account: str
    balances: List[BalanceItem]
    timestamp: int


# Chart update subscription
class ChartUpdate(BaseModel):
    """Chart update subscription data."""
    open: float
    high: float
    low: float
    close: float
    volume: float
    time: int  # in milliseconds

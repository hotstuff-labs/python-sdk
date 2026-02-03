"""Subscription channel method types."""
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, field_validator

from hotstuff.utils.address import validate_ethereum_address


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
    user: str = Field(..., description="User address")
    
    @field_validator('user', mode='before')
    @classmethod
    def validate_user(cls, v: str) -> str:
        """Validate and checksum the user address."""
        return validate_ethereum_address(v)
    
    # Alias for backward compatibility
    @property
    def address(self) -> str:
        """Alias for user field (deprecated)."""
        return self.user


class AccountBalanceUpdatesParams(BaseModel):
    """Parameters for account balance updates subscription."""
    user: str = Field(..., description="User address")
    
    @field_validator('user', mode='before')
    @classmethod
    def validate_user(cls, v: str) -> str:
        """Validate and checksum the user address."""
        return validate_ethereum_address(v)
    
    @property
    def address(self) -> str:
        """Alias for user field (deprecated)."""
        return self.user


class PositionsSubscriptionParams(BaseModel):
    """Parameters for positions subscription."""
    user: str = Field(..., description="User address")
    
    @field_validator('user', mode='before')
    @classmethod
    def validate_user(cls, v: str) -> str:
        """Validate and checksum the user address."""
        return validate_ethereum_address(v)
    
    @property
    def address(self) -> str:
        """Alias for user field (deprecated)."""
        return self.user


class FillsSubscriptionParams(BaseModel):
    """Parameters for fills subscription."""
    user: str = Field(..., description="User address")
    
    @field_validator('user', mode='before')
    @classmethod
    def validate_user(cls, v: str) -> str:
        """Validate and checksum the user address."""
        return validate_ethereum_address(v)
    
    @property
    def address(self) -> str:
        """Alias for user field (deprecated)."""
        return self.user


class AccountSummarySubscriptionParams(BaseModel):
    """Parameters for account summary subscription."""
    user: str = Field(..., description="User address")
    
    @field_validator('user', mode='before')
    @classmethod
    def validate_user(cls, v: str) -> str:
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
    amount: Optional[float] = None


class Orderbook(BaseModel):
    """Orderbook subscription data."""
    instrument_id: str
    instrument_name: Optional[str] = None
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
    time: int

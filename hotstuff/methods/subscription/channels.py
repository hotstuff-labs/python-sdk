"""Subscription channel method types."""
from dataclasses import dataclass, field
from typing import List, Literal, Optional

from hotstuff.utils.address import validate_ethereum_address


# Chart types
SupportedChartResolutions = Literal["1", "5", "15", "60", "240", "1D", "1W"]
SupportedChartTypes = Literal["mark", "ltp", "index"]


# Subscription parameter types
@dataclass
class TickerSubscriptionParams:
    """Parameters for ticker subscription."""
    symbol: str


@dataclass
class MidsSubscriptionParams:
    """Parameters for mids subscription."""
    symbol: str


@dataclass
class BBOSubscriptionParams:
    """Parameters for BBO subscription."""
    symbol: str


@dataclass
class OrderbookSubscriptionParams:
    """Parameters for orderbook subscription."""
    instrument_id: str


@dataclass
class TradeSubscriptionParams:
    """Parameters for trade subscription."""
    instrument_id: str


@dataclass
class ChartSubscriptionParams:
    """Parameters for chart subscription."""
    symbol: str
    chart_type: SupportedChartTypes
    resolution: SupportedChartResolutions


@dataclass
class AccountOrderUpdatesParams:
    """Parameters for account order updates subscription."""
    user: str
    
    def __post_init__(self):
        """Validate and checksum the user address."""
        self.user = validate_ethereum_address(self.user)
    
    @property
    def address(self) -> str:
        """Alias for user field (deprecated)."""
        return self.user


@dataclass
class AccountBalanceUpdatesParams:
    """Parameters for account balance updates subscription."""
    user: str
    
    def __post_init__(self):
        """Validate and checksum the user address."""
        self.user = validate_ethereum_address(self.user)
    
    @property
    def address(self) -> str:
        """Alias for user field (deprecated)."""
        return self.user


@dataclass
class PositionsSubscriptionParams:
    """Parameters for positions subscription."""
    user: str
    
    def __post_init__(self):
        """Validate and checksum the user address."""
        self.user = validate_ethereum_address(self.user)
    
    @property
    def address(self) -> str:
        """Alias for user field (deprecated)."""
        return self.user


@dataclass
class FillsSubscriptionParams:
    """Parameters for fills subscription."""
    user: str
    
    def __post_init__(self):
        """Validate and checksum the user address."""
        self.user = validate_ethereum_address(self.user)
    
    @property
    def address(self) -> str:
        """Alias for user field (deprecated)."""
        return self.user


@dataclass
class AccountSummarySubscriptionParams:
    """Parameters for account summary subscription."""
    user: str
    
    def __post_init__(self):
        """Validate and checksum the user address."""
        self.user = validate_ethereum_address(self.user)


@dataclass
class BlocksSubscriptionParams:
    """Parameters for blocks subscription."""
    pass


@dataclass
class TransactionsSubscriptionParams:
    """Parameters for transactions subscription."""
    pass


# Orderbook subscription
@dataclass
class OrderbookItem:
    """Orderbook item."""
    price: float
    size: float
    amount: Optional[float] = None


@dataclass
class Orderbook:
    """Orderbook subscription data."""
    instrument_id: str
    asks: List[OrderbookItem]
    bids: List[OrderbookItem]
    timestamp: int
    instrument_name: Optional[str] = None


# Trade subscription
@dataclass
class Trade:
    """Trade subscription data."""
    id: str
    instrument: str
    maker: str
    taker: str
    price: float
    size: float
    timestamp: int
    side: Literal["buy", "sell"]
    instrument_name: Optional[str] = None


# Order update subscription
@dataclass
class OrderUpdate:
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
@dataclass
class BalanceItem:
    """Balance item."""
    asset: str
    total: float
    available: float
    locked: float


@dataclass
class AccountBalanceUpdate:
    """Account balance update subscription data."""
    account: str
    balances: List[BalanceItem]
    timestamp: int


# Chart update subscription
@dataclass
class ChartUpdate:
    """Chart update subscription data."""
    open: float
    high: float
    low: float
    close: float
    volume: float
    time: int

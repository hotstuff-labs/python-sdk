"""Market info method types (public/global market data)."""
from dataclasses import dataclass, field
from typing import List, Literal, Optional, Union


# Oracle Method
@dataclass
class OracleParams:
    """Parameters for oracle price query."""
    symbol: str


@dataclass
class OracleResponse:
    """Oracle price response."""
    symbol: str
    index_price: str
    ext_mark_price: str
    updated_at: int


# Supported Collateral Method
@dataclass
class SupportedCollateralParams:
    """Parameters for supported collateral query."""
    pass


@dataclass
class BridgeByChain:
    """Bridge chain configuration."""
    bridge_chain_type: int
    bridge_chain_id: int
    token_address: str
    bridge_contract_address: str
    enabled: bool


@dataclass
class WeightTier:
    """Weight tier configuration."""
    amount: float
    weight: float


@dataclass
class CollRisk:
    """Collateral risk configuration."""
    weight_tiers: Optional[List[WeightTier]] = None
    max_margin_cap: Optional[float] = None
    stale_price_guard_weight: Optional[float] = None
    enabled: Optional[bool] = None


@dataclass
class SupportedCollateral:
    """Supported collateral information."""
    id: int
    symbol: str
    name: str
    decimals: int
    default_coll_weight: Optional[float] = None
    price_index: Optional[str] = None
    type: Optional[int] = None
    bridge_by_chain: Optional[List[BridgeByChain]] = None
    coll_risk: Optional[CollRisk] = None
    withdrawal_fee: Optional[int] = None
    added_at_block: Optional[int] = None


# Instruments Method
@dataclass
class InstrumentsParams:
    """Parameters for instruments query."""
    type: Literal["perps", "spot", "all"]


@dataclass
class MarginTier:
    """Margin tier configuration."""
    notional_usd_threshold: str
    max_leverage: int
    mmr: float
    mmd: float


@dataclass
class PerpInstrument:
    """Perpetual instrument information."""
    id: int
    name: str
    price_index: str
    lot_size: float
    tick_size: float
    settlement_currency: int
    only_isolated: bool
    max_leverage: int
    delisted: bool
    min_notional_usd: int
    margin_tiers: List[MarginTier]
    listed_at_block_timestamp: int


@dataclass
class SpotInstrument:
    """Spot instrument information."""
    id: int
    name: str
    price_index: str
    lot_size: int
    tick_size: float
    base_asset: int
    quote_asset: int
    stable_pair: bool
    min_size_in_quote_asset: int
    listed_at_block_timestamp: int


@dataclass
class InstrumentsResponse:
    """Instruments response.
    
    Testnet may return only perps (no spot key); both lists default to empty
    when the key is missing so validation succeeds on testnet and mainnet.
    """
    perps: List[PerpInstrument] = field(default_factory=list)
    spot: List[SpotInstrument] = field(default_factory=list)


# Ticker Method
@dataclass
class TickerParams:
    """Parameters for ticker query."""
    symbol: str


@dataclass
class Ticker:
    """Ticker information."""
    symbol: str
    mark_price: str
    mid_price: str
    index_price: str
    best_bid_price: str
    best_ask_price: str
    best_bid_size: str
    best_ask_size: str
    volume_24h: str
    change_24h: str
    last_updated: int
    type: Optional[str] = None
    funding_rate: Optional[str] = None
    open_interest: Optional[str] = None
    max_trading_price: Optional[str] = None
    min_trading_price: Optional[str] = None
    last_price: Optional[str] = None


# Orderbook Method
@dataclass
class OrderbookParams:
    """Parameters for orderbook query."""
    symbol: str
    depth: Optional[int] = None


@dataclass
class OrderbookLevel:
    """Orderbook level (bid/ask)."""
    price: str
    size: str


@dataclass
class OrderbookResponse:
    """Orderbook response."""
    bids: List[OrderbookLevel]
    asks: List[OrderbookLevel]
    instrument_name: str
    timestamp: int
    sequence_number: int


# Trades Method
@dataclass
class TradesParams:
    """Parameters for trades query."""
    symbol: str
    limit: Optional[int] = None


@dataclass
class Trade:
    """Trade information."""
    instrument_id: int
    instrument: str
    trade_id: int
    tx_hash: str
    side: Literal["b", "s"]
    price: str
    size: str
    maker: str
    taker: str
    timestamp: str


# Mids Method
@dataclass
class MidsParams:
    """Parameters for mids query."""
    pass


@dataclass
class Mid:
    """Mid price information."""
    symbol: str
    mid_price: str


# BBO Method
@dataclass
class BBOParams:
    """Parameters for best bid/offer query."""
    symbol: str


@dataclass
class BBO:
    """Best bid/offer information."""
    symbol: str
    best_bid_price: str
    best_ask_price: str
    best_bid_size: str
    best_ask_size: str


# Chart Method
SupportedChartResolutions = Literal["1", "5", "15", "60", "240", "1D", "1W"]
SupportedChartTypes = Literal["mark", "ltp", "index"]


@dataclass
class ChartParams:
    """Parameters for chart data query."""
    symbol: str
    resolution: SupportedChartResolutions
    from_: int
    to: int
    chart_type: SupportedChartTypes


@dataclass
class ChartPoint:
    """Chart data point."""
    open: float
    high: float
    low: float
    close: float
    volume: float
    time: int

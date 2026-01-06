"""Global info method types."""
from typing import List, Literal, Optional, Union
from pydantic import BaseModel, Field, ConfigDict, field_validator


# Oracle Method
class OracleParams(BaseModel):
    """Parameters for oracle price query."""
    symbol: str = Field(..., description="Symbol to get oracle price for")


class OracleResponse(BaseModel):
    """Oracle price response."""
    symbol: str
    index_price: str
    ext_mark_price: str
    updated_at: int


# Supported Collateral Method
class SupportedCollateralParams(BaseModel):
    """Parameters for supported collateral query."""
    pass


class BridgeByChain(BaseModel):
    """Bridge chain configuration."""
    bridge_chain_type: int
    bridge_chain_id: int
    token_address: str
    bridge_contract_address: str
    enabled: bool


class WeightTier(BaseModel):
    """Weight tier configuration."""
    amount: int
    weight: int


class CollRisk(BaseModel):
    """Collateral risk configuration."""
    weight_tiers: List[WeightTier]
    max_margin_cap: int
    stale_price_guard_weight: int


class SupportedCollateral(BaseModel):
    """Supported collateral information."""
    id: int
    symbol: str
    name: str
    decimals: int
    default_coll_weight: int
    price_index: str
    type: int
    bridge_by_chain: List[BridgeByChain]
    coll_risk: List[CollRisk]
    withdrawal_fee: int
    added_at_block: int


# Instruments Method
class InstrumentsParams(BaseModel):
    """Parameters for instruments query."""
    type: Literal["perps", "spot", "all"] = Field(..., description="Instrument type filter")


class MarginTier(BaseModel):
    """Margin tier configuration."""
    notional_usd_threshold: str
    max_leverage: int
    mmr: float  # Can be fractional
    mmd: int


class PerpInstrument(BaseModel):
    """Perpetual instrument information."""
    id: int
    name: str
    price_index: str
    lot_size: float  # Can be fractional (e.g., 1e-05)
    tick_size: float  # Can be fractional (e.g., 0.1, 1e-06)
    settlement_currency: int
    only_isolated: bool
    max_leverage: int
    delisted: bool
    min_notional_usd: int
    margin_tiers: List[MarginTier]
    listed_at_block_timestamp: int


class SpotInstrument(BaseModel):
    """Spot instrument information."""
    id: int
    name: str
    price_index: str
    lot_size: int
    tick_size: float  # Can be fractional (e.g., 0.0001)
    base_asset: int
    quote_asset: int
    stable_pair: bool
    min_size_in_quote_asset: int
    listed_at_block_timestamp: int


class InstrumentsResponse(BaseModel):
    """Instruments response."""
    perps: List[PerpInstrument]
    spot: List[SpotInstrument]


# Ticker Method
class TickerParams(BaseModel):
    """Parameters for ticker query."""
    symbol: str = Field(..., description="Trading pair symbol")


class Ticker(BaseModel):
    """Ticker information."""
    type: Literal["perp", "spot"]
    symbol: str
    mark_price: str
    mid_price: str
    index_price: str
    best_bid_price: str
    best_ask_price: str
    best_bid_size: str
    best_ask_size: str
    funding_rate: str
    open_interest: str
    volume_24h: str
    change_24h: str
    max_trading_price: str
    min_trading_price: str
    last_updated: int
    last_price: str


# Orderbook Method
class OrderbookParams(BaseModel):
    """Parameters for orderbook query."""
    symbol: str = Field(..., description="Trading pair symbol")
    depth: Optional[int] = Field(None, description="Orderbook depth")


class OrderbookLevel(BaseModel):
    """Orderbook level (bid/ask)."""
    price: str  # API may return int/float, but we store as string for precision
    size: str   # API may return int/float, but we store as string for precision
    
    @field_validator('price', mode='before')
    @classmethod
    def convert_price_to_string(cls, v: Union[str, int, float]) -> str:
        """Convert numeric price to string."""
        if not isinstance(v, str):
            return str(v)
        return v
    
    @field_validator('size', mode='before')
    @classmethod
    def convert_size_to_string(cls, v: Union[str, int, float]) -> str:
        """Convert numeric size to string."""
        if not isinstance(v, str):
            return str(v)
        return v


class OrderbookResponse(BaseModel):
    """Orderbook response."""
    bids: List[OrderbookLevel]
    asks: List[OrderbookLevel]
    instrument_name: str
    timestamp: int
    sequence_number: int


# Trades Method
class TradesParams(BaseModel):
    """Parameters for trades query."""
    symbol: str = Field(..., description="Trading pair symbol")
    limit: Optional[int] = Field(None, description="Number of trades to return")


class Trade(BaseModel):
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
class MidsParams(BaseModel):
    """Parameters for mids query."""
    pass


class Mid(BaseModel):
    """Mid price information."""
    symbol: str
    mid_price: str


# BBO Method
class BBOParams(BaseModel):
    """Parameters for best bid/offer query."""
    symbol: str = Field(..., description="Trading pair symbol")


class BBO(BaseModel):
    """Best bid/offer information."""
    symbol: str
    best_bid_price: str
    best_ask_price: str
    best_bid_size: str
    best_ask_size: str


# Chart Method
SupportedChartResolutions = Literal["1", "5", "15", "60", "240", "1D", "1W"]
SupportedChartTypes = Literal["mark", "ltp", "index"]


class ChartParams(BaseModel):
    """Parameters for chart data query."""
    model_config = ConfigDict(populate_by_name=True)
    
    symbol: str = Field(..., description="Trading pair symbol")
    resolution: SupportedChartResolutions = Field(..., description="Chart resolution")
    from_: int = Field(..., alias="from", description="Start timestamp")
    to: int = Field(..., description="End timestamp")
    chart_type: SupportedChartTypes = Field(..., description="Chart type")


class ChartPoint(BaseModel):
    """Chart data point."""
    open: float
    high: float
    low: float
    close: float
    volume: float
    time: int

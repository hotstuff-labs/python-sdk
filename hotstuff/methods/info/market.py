"""Market info method types (public/global market data)."""
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
    model_config = ConfigDict(populate_by_name=True, extra='allow')
    
    bridge_chain_type: int = Field(alias="bridgeChainType")
    bridge_chain_id: int = Field(alias="bridgeChainId")
    token_address: str = Field(alias="tokenAddress")
    bridge_contract_address: str = Field(alias="bridgeContractAddress")
    enabled: bool


class WeightTier(BaseModel):
    """Weight tier configuration."""
    model_config = ConfigDict(extra='allow')
    
    amount: float  # Can be large numbers as float
    weight: float  # Can be fractional


class CollRisk(BaseModel):
    """Collateral risk configuration."""
    model_config = ConfigDict(populate_by_name=True, extra='allow')
    
    weight_tiers: Optional[List[WeightTier]] = Field(default=None, alias="weightTiers")
    max_margin_cap: Optional[float] = Field(default=None, alias="maxMarginCap")
    stale_price_guard_weight: Optional[float] = Field(default=None, alias="stalePriceGuardWeight")
    enabled: Optional[bool] = None


class SupportedCollateral(BaseModel):
    """Supported collateral information."""
    model_config = ConfigDict(populate_by_name=True, extra='allow')
    
    id: int
    symbol: str
    name: str
    decimals: int
    default_coll_weight: Optional[float] = Field(default=None, alias="defaultCollWeight")
    price_index: Optional[str] = Field(default=None, alias="priceIndex")
    type: Optional[int] = None
    bridge_by_chain: Optional[List[BridgeByChain]] = Field(default=None, alias="bridgeByChain")
    coll_risk: Optional[CollRisk] = Field(default=None, alias="collRisk")
    withdrawal_fee: Optional[int] = Field(default=None, alias="withdrawalFee")
    added_at_block: Optional[int] = Field(default=None, alias="addedAtBlock")


# Instruments Method
class InstrumentsParams(BaseModel):
    """Parameters for instruments query."""
    type: Literal["perps", "spot", "all"] = Field(..., description="Instrument type filter")


class MarginTier(BaseModel):
    """Margin tier configuration."""
    notional_usd_threshold: str
    max_leverage: int
    mmr: float
    mmd: float


class PerpInstrument(BaseModel):
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


class SpotInstrument(BaseModel):
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


class InstrumentsResponse(BaseModel):
    """Instruments response.
    
    Testnet may return only perps (no spot key); both lists default to empty
    when the key is missing so validation succeeds on testnet and mainnet.
    """
    perps: List[PerpInstrument] = Field(default_factory=list, description="Perpetual instruments")
    spot: List[SpotInstrument] = Field(default_factory=list, description="Spot instruments (may be omitted on testnet)")


# Ticker Method
class TickerParams(BaseModel):
    """Parameters for ticker query."""
    symbol: str = Field(..., description="Trading pair symbol")


class Ticker(BaseModel):
    """Ticker information."""
    model_config = ConfigDict(extra='allow')
    
    type: Optional[str] = None
    symbol: str
    mark_price: str
    mid_price: str
    index_price: str
    best_bid_price: str
    best_ask_price: str
    best_bid_size: str
    best_ask_size: str
    funding_rate: Optional[str] = None
    open_interest: Optional[str] = None
    volume_24h: str
    change_24h: str
    max_trading_price: Optional[str] = None
    min_trading_price: Optional[str] = None
    last_updated: int
    last_price: Optional[str] = None


# Orderbook Method
class OrderbookParams(BaseModel):
    """Parameters for orderbook query."""
    symbol: str = Field(..., description="Trading pair symbol")
    depth: Optional[int] = Field(None, description="Orderbook depth")


class OrderbookLevel(BaseModel):
    """Orderbook level (bid/ask)."""
    price: str
    size: str
    
    @field_validator('price', mode='before')
    @classmethod
    def convert_price_to_string(cls, v: Union[str, int, float]) -> str:
        """Convert numeric price to string."""
        return str(v) if not isinstance(v, str) else v
    
    @field_validator('size', mode='before')
    @classmethod
    def convert_size_to_string(cls, v: Union[str, int, float]) -> str:
        """Convert numeric size to string."""
        return str(v) if not isinstance(v, str) else v


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

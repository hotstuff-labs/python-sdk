"""Trading exchange method types."""
from dataclasses import dataclass, field
from typing import List, Literal, Optional

from hotstuff.utils.address import validate_ethereum_address


# Place Order Method
@dataclass
class UnitOrder:
    """Single order unit."""
    instrument_id: int
    side: Literal["b", "s"]
    position_side: Literal["LONG", "SHORT", "BOTH"]
    price: str
    size: str
    tif: Literal["GTC", "IOC", "FOK"]
    ro: bool
    po: bool
    cloid: Optional[str] = None
    trigger_px: Optional[str] = None
    is_market: Optional[bool] = None
    tpsl: Optional[Literal["tp", "sl", ""]] = None
    grouping: Optional[Literal["position", "normal", ""]] = None
    
    def __post_init__(self):
        """Validate instrument_id."""
        if self.instrument_id <= 0:
            raise ValueError("instrument_id must be greater than 0")


@dataclass
class BrokerConfig:
    """Broker configuration."""
    broker: str
    fee: str
    
    def __post_init__(self):
        """Validate and checksum the broker address."""
        if self.broker != "":
            self.broker = validate_ethereum_address(self.broker)


@dataclass
class PlaceOrderParams:
    """Parameters for placing an order."""
    orders: List[UnitOrder]
    expires_after: int
    broker_config: Optional[BrokerConfig] = None
    nonce: Optional[int] = None


# Cancel By Oid Method
@dataclass
class UnitCancelByOrderId:
    """Cancel by order ID unit."""
    oid: int
    instrumentId: int
    
    def __post_init__(self):
        """Validate instrumentId."""
        if self.instrumentId <= 0:
            raise ValueError("instrumentId must be greater than 0")


@dataclass
class CancelByOidParams:
    """Parameters for cancelling by order ID."""
    cancels: List[UnitCancelByOrderId]
    expires_after: int
    nonce: Optional[int] = None


# Cancel By Cloid Method
@dataclass
class UnitCancelByClOrderId:
    """Cancel by client order ID unit."""
    cloid: str
    instrument_id: int
    
    def __post_init__(self):
        """Validate instrument_id."""
        if self.instrument_id <= 0:
            raise ValueError("instrument_id must be greater than 0")


@dataclass
class CancelByCloidParams:
    """Parameters for cancelling by client order ID."""
    cancels: List[UnitCancelByClOrderId]
    expires_after: int
    nonce: Optional[int] = None


# Cancel All Method
@dataclass
class CancelAllParams:
    """Parameters for cancelling all orders."""
    expires_after: int
    nonce: Optional[int] = None

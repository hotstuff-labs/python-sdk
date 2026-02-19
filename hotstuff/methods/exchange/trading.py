"""Trading exchange method types."""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Optional
import time
from hotstuff.utils.address import validate_ethereum_address


# Place Order Method
@dataclass
class UnitOrder:
    """Single order unit."""
    instrumentId: int
    side: Literal["b", "s"]
    positionSide: Literal["LONG", "SHORT", "BOTH"]
    price: str
    size: str
    tif: Literal["GTC", "IOC", "FOK"]
    ro: bool
    po: bool
    cloid: Optional[str] = None
    triggerPx: Optional[str] = None
    isMarket: Optional[bool] = None
    tpsl: Optional[Literal["tp", "sl", ""]] = None
    grouping: Optional[Literal["position", "normal", ""]] = None
    
    def __post_init__(self):
        """Validate instrument_id."""
        if self.instrumentId <= 0:
            raise ValueError("instrumentId must be greater than 0")
        if self.cloid is None:
            self.cloid = generate_cloid()
        if self.triggerPx is None:
            self.triggerPx = ""
        if self.isMarket is None:
            self.isMarket = False
        if self.tpsl is None:
            self.tpsl = ""
        if self.grouping is None:
            self.grouping = ""
    
    def to_api_dict(self) -> Dict[str, Any]:
        """Convert to API dict."""
        return {
            "instrumentId": self.instrumentId,
            "side": self.side,
            "positionSide": self.positionSide,
            "price": self.price,
            "size": self.size,
            "tif": self.tif,
            "ro": self.ro,
            "po": self.po,
            "cloid": self.cloid,
            "triggerPx": self.triggerPx,
            "isMarket": self.isMarket,
            "tpsl": self.tpsl,
            "grouping": self.grouping,
        }


@dataclass
class BrokerConfig:
    """Broker configuration."""
    broker: str
    fee: str
    
    def __post_init__(self):
        """Validate and checksum the broker address."""
        if self.broker != "":
            self.broker = validate_ethereum_address(self.broker)
    
    def to_api_dict(self) -> Dict[str, Any]:
        """Convert to API dict."""
        return {"broker": self.broker, "fee": self.fee}


@dataclass
class PlaceOrderParams:
    """Parameters for placing an order."""
    orders: List[UnitOrder]
    expiresAfter: int
    brokerConfig: Optional[BrokerConfig] = None
    nonce: Optional[int] = None
    
    def to_api_dict(self) -> Dict[str, Any]:
        """Convert to API dict, omitting None values."""
        result = {
            "orders": [order.to_api_dict() for order in self.orders],
            "expiresAfter": self.expiresAfter,
        }
        if self.brokerConfig is not None:
            result["brokerConfig"] = self.brokerConfig.to_api_dict()
        return result


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
    expiresAfter: int
    nonce: Optional[int] = None


# Cancel By Cloid Method
@dataclass
class UnitCancelByClOrderId:
    """Cancel by client order ID unit."""
    cloid: str
    instrumentId: int
    
    def __post_init__(self):
        """Validate instrument_id."""
        if self.instrumentId <= 0:
            raise ValueError("instrument_id must be greater than 0")


@dataclass
class CancelByCloidParams:
    """Parameters for cancelling by client order ID."""
    cancels: List[UnitCancelByClOrderId]
    expiresAfter: int
    nonce: Optional[int] = None


# Cancel All Method
@dataclass
class CancelAllParams:
    """Parameters for cancelling all orders."""
    expiresAfter: int
    nonce: Optional[int] = None


def generate_cloid():
    return f"cloid-{int(time.time())}"
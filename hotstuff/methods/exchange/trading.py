"""Trading exchange method types."""
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator, field_serializer

from hotstuff.utils.address import validate_ethereum_address


# Place Order Method
class UnitOrder(BaseModel):
    """Single order unit."""
    instrument_id: int = Field(..., gt=0, alias="instrumentId", description="Instrument ID")
    side: Literal["b", "s"] = Field(..., description="Order side: 'b' for buy, 's' for sell")
    position_side: Literal["LONG", "SHORT", "BOTH"] = Field(..., alias="positionSide", description="Position side")
    price: str = Field(..., description="Order price")
    size: str = Field(..., description="Order size")
    tif: Literal["GTC", "IOC", "FOK"] = Field(..., description="Time in force")
    ro: bool = Field(..., description="Reduce-only flag")
    po: bool = Field(..., description="Post-only flag")
    cloid: Optional[str] = Field(None, description="Client order ID (optional)")
    trigger_px: Optional[str] = Field(None, alias="triggerPx", description="Trigger price")
    is_market: Optional[bool] = Field(None, alias="isMarket", description="Market order flag")
    tpsl: Optional[Literal["tp", "sl", ""]] = Field(None, description="Take profit/stop loss")
    grouping: Optional[Literal["position", "normal", ""]] = Field(None, description="Order grouping")

    model_config = ConfigDict(populate_by_name=True)
    
    @field_serializer('cloid', 'trigger_px', 'tpsl', 'grouping')
    def serialize_optional_strings(self, value: Optional[str], _info) -> str:
        """Convert None to empty string for optional string fields to match API expectations."""
        return "" if value is None else value


class BrokerConfig(BaseModel):
    """Broker configuration."""
    broker: str = Field(..., description="Broker address")
    fee: str = Field(..., description="Broker fee")
    
    @field_validator('broker', mode='before')
    @classmethod
    def validate_broker_address(cls, v: str) -> str:
        """Validate and checksum the broker address."""
        if v == "":
            return v  # Allow empty string for no broker
        return validate_ethereum_address(v)


class PlaceOrderParams(BaseModel):
    """Parameters for placing an order."""
    orders: List[UnitOrder] = Field(..., description="List of orders to place")
    expires_after: int = Field(..., alias="expiresAfter", description="Expiration timestamp")
    broker_config: Optional[BrokerConfig] = Field(None, alias="brokerConfig", description="Broker configuration")
    nonce: Optional[int] = Field(None, description="Transaction nonce")

    model_config = ConfigDict(populate_by_name=True)


# Cancel By Oid Method
class UnitCancelByOrderId(BaseModel):
    """Cancel by order ID unit."""
    oid: int = Field(..., description="Order ID")
    instrument_id: int = Field(..., gt=0, description="Instrument ID")


class CancelByOidParams(BaseModel):
    """Parameters for cancelling by order ID."""
    cancels: List[UnitCancelByOrderId] = Field(..., description="List of orders to cancel")
    expires_after: int = Field(..., alias="expiresAfter", description="Expiration timestamp")
    nonce: Optional[int] = Field(None, description="Transaction nonce")

    model_config = ConfigDict(populate_by_name=True)


# Cancel By Cloid Method
class UnitCancelByClOrderId(BaseModel):
    """Cancel by client order ID unit."""
    cloid: str = Field(..., description="Client order ID")
    instrument_id: int = Field(..., gt=0, description="Instrument ID")


class CancelByCloidParams(BaseModel):
    """Parameters for cancelling by client order ID."""
    cancels: List[UnitCancelByClOrderId] = Field(..., description="List of orders to cancel")
    expires_after: int = Field(..., alias="expiresAfter", description="Expiration timestamp")
    nonce: Optional[int] = Field(None, description="Transaction nonce")

    model_config = ConfigDict(populate_by_name=True)


# Cancel All Method
class CancelAllParams(BaseModel):
    """Parameters for cancelling all orders."""
    expires_after: int = Field(..., alias="expiresAfter", description="Expiration timestamp")
    nonce: Optional[int] = Field(None, description="Transaction nonce")

    model_config = ConfigDict(populate_by_name=True)

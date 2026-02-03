"""Trading exchange method types."""
import re
from typing import List, Literal, Optional, Any
from pydantic import BaseModel, Field, ConfigDict, field_validator, field_serializer

from hotstuff.utils.address import validate_ethereum_address


# Regex pattern for valid cloid: 0x followed by exactly 32 hex digits (128-bit)
CLOID_PATTERN = re.compile(r'^0x[0-9a-fA-F]{32}$')


def validate_cloid(value: Optional[str]) -> Optional[str]:
    """
    Validate client order ID format.
    
    Args:
        value: The cloid string to validate
        
    Returns:
        The validated cloid string (lowercase hex)
        
    Raises:
        ValueError: If the cloid format is invalid
    """
    if value is None or value == "":
        return None
    
    if not CLOID_PATTERN.match(value):
        raise ValueError(
            f"Invalid cloid format: '{value}'. "
            "ClOrdID must be 0x followed by 32 hex digits (128-bit). "
            "Example: 0x1234567890abcdef1234567890abcdef"
        )
    
    # Return lowercase for consistency
    return value.lower()


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
    cloid: Optional[str] = Field(
        None, 
        description="Client order ID (optional). Format: 0x + 32 hex digits (128-bit). Example: 0x1234567890abcdef1234567890abcdef"
    )
    trigger_px: Optional[str] = Field(None, alias="triggerPx", description="Trigger price")
    is_market: Optional[bool] = Field(None, alias="isMarket", description="Market order flag")
    tpsl: Optional[Literal["tp", "sl", ""]] = Field(None, description="Take profit/stop loss")
    grouping: Optional[Literal["position", "normal", ""]] = Field(None, description="Order grouping")

    model_config = ConfigDict(populate_by_name=True)
    
    @field_validator('cloid', mode='before')
    @classmethod
    def validate_cloid_format(cls, v: Optional[str]) -> Optional[str]:
        """Validate cloid format: 0x + 32 hex digits."""
        return validate_cloid(v)
    
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
    cloid: str = Field(
        ..., 
        description="Client order ID. Format: 0x + 32 hex digits (128-bit). Example: 0x1234567890abcdef1234567890abcdef"
    )
    instrument_id: int = Field(..., gt=0, description="Instrument ID")
    
    @field_validator('cloid', mode='before')
    @classmethod
    def validate_cloid_format(cls, v: str) -> str:
        """Validate cloid format: 0x + 32 hex digits."""
        result = validate_cloid(v)
        if result is None:
            raise ValueError("cloid is required for cancel by cloid")
        return result


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

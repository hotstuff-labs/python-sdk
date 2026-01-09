"""Type definitions for exchange methods."""
from typing import Optional, List
from dataclasses import dataclass


@dataclass
class UnitOrder:
    """Single order unit."""
    instrument_id: int
    side: str  # 'b' or 's'
    position_side: str  # 'LONG', 'SHORT', or 'BOTH'
    price: str
    size: str
    tif: str  # 'GTC', 'IOC', or 'FOK'
    ro: bool  # reduce-only
    po: bool  # post-only
    cloid: str  # client order ID
    trigger_px: Optional[str] = None
    is_market: Optional[bool] = None
    tpsl: Optional[str] = None  # 'tp', 'sl', or ''
    grouping: Optional[str] = None  # 'position', 'normal', or ''


@dataclass
class BrokerConfig:
    """Broker configuration."""
    broker: str
    fee: str


@dataclass
class PlaceOrderParams:
    """Parameters for placing an order."""
    orders: List[UnitOrder]
    expiresAfter: int
    broker_config: Optional[BrokerConfig] = None
    nonce: Optional[int] = None


@dataclass
class UnitCancelByOrderId:
    """Cancel by order ID unit."""
    oid: int
    instrument_id: int


@dataclass
class CancelByOidParams:
    """Parameters for cancelling by order ID."""
    cancels: List[UnitCancelByOrderId]
    expiresAfter: int
    nonce: Optional[int] = None


@dataclass
class UnitCancelByClOrderId:
    """Cancel by client order ID unit."""
    cloid: str
    instrument_id: int


@dataclass
class CancelByCloidParams:
    """Parameters for cancelling by client order ID."""
    cancels: List[UnitCancelByClOrderId]
    expiresAfter: int
    nonce: Optional[int] = None


@dataclass
class CancelAllParams:
    """Parameters for cancelling all orders."""
    expiresAfter: int
    nonce: Optional[int] = None


@dataclass
class AddAgentParams:
    """Parameters for adding an agent."""
    agent_name: str
    agent: str
    for_account: str
    agent_private_key: str
    signer: str
    valid_until: int
    signature: Optional[str] = None
    nonce: Optional[int] = None


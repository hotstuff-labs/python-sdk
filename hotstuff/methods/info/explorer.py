"""Explorer info method types."""
from dataclasses import dataclass
from typing import Optional


# Blocks Method
@dataclass
class BlocksParams:
    """Parameters for blocks query."""
    offset: int
    limit: int


@dataclass
class BlocksResponse:
    """Blocks response."""
    pass


# Block Details Method
@dataclass
class BlockDetailsParams:
    """Parameters for block details query."""
    block_hash: Optional[str] = None
    block_height: Optional[int] = None


@dataclass
class BlockDetailsResponse:
    """Block details response."""
    pass


# Transactions Method
@dataclass
class TransactionFilter:
    """Transaction filter."""
    account: Optional[str] = None
    tx_type: Optional[int] = None


@dataclass
class TransactionsParams:
    """Parameters for transactions query."""
    offset: Optional[int] = None
    limit: Optional[int] = None
    filter: Optional[TransactionFilter] = None


@dataclass
class TransactionsResponse:
    """Transactions response."""
    pass


# Transaction Details Method
@dataclass
class TransactionDetailsParams:
    """Parameters for transaction details query."""
    tx_hash: str


@dataclass
class TransactionDetailsResponse:
    """Transaction details response."""
    pass

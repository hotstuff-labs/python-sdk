"""Explorer info method types."""
from typing import Optional
from pydantic import BaseModel, Field


# Blocks Method
class BlocksParams(BaseModel):
    """Parameters for blocks query."""
    offset: int = Field(..., description="Offset for pagination")
    limit: int = Field(..., description="Number of blocks to return")


class BlocksResponse(BaseModel):
    """Blocks response."""
    pass  # TODO: Define structure when API response is known


# Block Details Method
class BlockDetailsParams(BaseModel):
    """Parameters for block details query."""
    block_hash: Optional[str] = Field(None, description="Block hash")
    block_height: Optional[int] = Field(None, description="Block height")


class BlockDetailsResponse(BaseModel):
    """Block details response."""
    pass  # TODO: Define structure when API response is known


# Transactions Method
class TransactionFilter(BaseModel):
    """Transaction filter."""
    account: Optional[str] = Field(None, description="Filter by account")
    tx_type: Optional[int] = Field(None, description="Filter by transaction type")


class TransactionsParams(BaseModel):
    """Parameters for transactions query."""
    offset: Optional[int] = Field(None, description="Offset for pagination")
    limit: Optional[int] = Field(None, description="Number of transactions to return")
    filter: Optional[TransactionFilter] = Field(None, description="Transaction filter")


class TransactionsResponse(BaseModel):
    """Transactions response."""
    pass  # TODO: Define structure when API response is known


# Transaction Details Method
class TransactionDetailsParams(BaseModel):
    """Parameters for transaction details query."""
    tx_hash: str = Field(..., description="Transaction hash")


class TransactionDetailsResponse(BaseModel):
    """Transaction details response."""
    pass  # TODO: Define structure when API response is known

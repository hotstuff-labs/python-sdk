"""Vault info method types."""
from typing import Optional, Annotated
from pydantic import BaseModel, Field, field_validator
from eth_utils import is_address, to_checksum_address


def validate_ethereum_address(value: str) -> str:
    """
    Validate and normalize an Ethereum address.
    
    Args:
        value: The address string to validate
        
    Returns:
        Checksummed address string
        
    Raises:
        ValueError: If the address is invalid
    """
    if not isinstance(value, str):
        raise ValueError(f"Address must be a string, got {type(value)}")
    
    if not is_address(value):
        raise ValueError(f"Invalid Ethereum address: {value}")
    
    # Return checksummed address (EIP-55)
    return to_checksum_address(value)


# Type alias for validated Ethereum addresses (similar to viem's Address type)
EthereumAddress = Annotated[
    str,
    Field(
        ...,
        description="Ethereum address (validated and checksummed)",
        examples=["0x1234567890123456789012345678901234567890"],
    ),
]


# Vaults Method
class VaultsParams(BaseModel):
    """Parameters for vaults query."""
    pass


class VaultsResponse(BaseModel):
    """Vaults response."""
    pass 


# Sub Vaults Method
class SubVaultsParams(BaseModel):
    """Parameters for sub vaults query."""
    vault_address: EthereumAddress = Field(..., description="Vault address")
    
    @field_validator('vault_address', mode='before')
    @classmethod
    def validate_vault_address(cls, v: str) -> str:
        """Validate and checksum the vault address."""
        return validate_ethereum_address(v)


class SubVaultsResponse(BaseModel):
    """Sub vaults response."""
    pass 


# Vault Balances Method
class VaultBalancesParams(BaseModel):
    """Parameters for vault balances query."""
    vault_address: EthereumAddress = Field(..., description="Vault address")
    user: Optional[EthereumAddress] = Field(None, description="User address")
    
    @field_validator('vault_address', 'user', mode='before')
    @classmethod
    def validate_addresses(cls, v: Optional[str]) -> Optional[str]:
        """Validate and checksum Ethereum addresses."""
        if v is None:
            return None
        return validate_ethereum_address(v)


class VaultBalancesResponse(BaseModel):
    """Vault balances response."""
    pass 

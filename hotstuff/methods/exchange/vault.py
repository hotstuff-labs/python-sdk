"""Vault exchange method types."""
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator
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


# Deposit To Vault Method
class DepositToVaultParams(BaseModel):
    """Parameters for depositing to a vault."""
    vault_address: str = Field(..., alias="vaultAddress", description="Vault address")
    amount: str = Field(..., description="Deposit amount")
    nonce: Optional[int] = Field(None, description="Transaction nonce")

    model_config = ConfigDict(populate_by_name=True)

    @field_validator('vault_address', mode='before')
    @classmethod
    def validate_vault_address(cls, v: str) -> str:
        """Validate and checksum the vault address."""
        return validate_ethereum_address(v)


# Redeem From Vault Method
class RedeemFromVaultParams(BaseModel):
    """Parameters for redeeming from a vault."""
    vault_address: str = Field(..., alias="vaultAddress", description="Vault address")
    shares: str = Field(..., description="Number of shares to redeem")
    nonce: Optional[int] = Field(None, description="Transaction nonce")

    model_config = ConfigDict(populate_by_name=True)

    @field_validator('vault_address', mode='before')
    @classmethod
    def validate_vault_address(cls, v: str) -> str:
        """Validate and checksum the vault address."""
        return validate_ethereum_address(v)

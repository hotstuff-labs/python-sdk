"""Vault exchange method types."""
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator

from hotstuff.utils.address import validate_ethereum_address


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

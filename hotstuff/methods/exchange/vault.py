"""Vault exchange method types."""
from dataclasses import dataclass
from typing import Optional

from hotstuff.utils.address import validate_ethereum_address


# Deposit To Vault Method
@dataclass
class DepositToVaultParams:
    """Parameters for depositing to a vault."""
    vault_address: str
    amount: str
    nonce: Optional[int] = None
    
    def __post_init__(self):
        """Validate and checksum the vault address."""
        self.vault_address = validate_ethereum_address(self.vault_address)


# Redeem From Vault Method
@dataclass
class RedeemFromVaultParams:
    """Parameters for redeeming from a vault."""
    vault_address: str
    shares: str
    nonce: Optional[int] = None
    
    def __post_init__(self):
        """Validate and checksum the vault address."""
        self.vault_address = validate_ethereum_address(self.vault_address)

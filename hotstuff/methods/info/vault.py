"""Vault info method types."""
from dataclasses import dataclass
from typing import Optional

from hotstuff.utils.address import validate_ethereum_address


# Vaults Method
@dataclass
class VaultsParams:
    """Parameters for vaults query."""
    pass


@dataclass
class VaultsResponse:
    """Vaults response."""
    pass


# Sub Vaults Method
@dataclass
class SubVaultsParams:
    """Parameters for sub vaults query."""
    vault_address: str
    
    def __post_init__(self):
        """Validate and checksum the vault address."""
        self.vault_address = validate_ethereum_address(self.vault_address)


@dataclass
class SubVaultsResponse:
    """Sub vaults response."""
    pass


# Vault Balances Method
@dataclass
class VaultBalancesParams:
    """Parameters for vault balances query."""
    vault_address: str
    user: Optional[str] = None
    
    def __post_init__(self):
        """Validate and checksum Ethereum addresses."""
        self.vault_address = validate_ethereum_address(self.vault_address)
        if self.user:
            self.user = validate_ethereum_address(self.user)


@dataclass
class VaultBalancesResponse:
    """Vault balances response."""
    pass

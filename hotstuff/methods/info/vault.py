"""Vault info method types."""
from dataclasses import dataclass, field
from typing import List, Optional, Union

from hotstuff.utils.address import validate_ethereum_address


# Vaults Method
@dataclass
class VaultsParams:
    """Parameters for vaults query."""
    pass


@dataclass
class Vault:
    """Vault information."""
    vault_address: str
    vault_manager: str
    name: str
    symbol: str
    deposit_cap: str
    role: int
    underlying_asset_id: int
    lock_in_period: int
    commission: str
    min_share_of_vm: str
    created_at: int
    allow_deposits: bool
    always_close_on_withdraw: bool
    is_closed: bool
    updated_at: int


@dataclass
class VaultsResponse:
    """Vaults response."""
    vaults: List[Vault] = field(default_factory=list)


# Sub Vaults Method
@dataclass
class SubVaultsParams:
    """Parameters for sub vaults query."""
    vaultAddress: str
    
    def __post_init__(self):
        """Validate and checksum the vault address."""
        self.vaultAddress = validate_ethereum_address(self.vaultAddress)


@dataclass
class SubVault:
    """Sub vault information."""
    vault_address: str
    sub_vault_address: str
    manager: str
    created_at: int

# Note: sub vaults endpoint returns List[SubVault] directly
SubVaultsResponse = List[SubVault]


# Vault Balances Method
@dataclass
class VaultBalancesParams:
    """Parameters for vault balances query."""
    vaultAddress: str
    user: Optional[str] = None
    
    def __post_init__(self):
        """Validate and checksum Ethereum addresses."""
        self.vaultAddress = validate_ethereum_address(self.vaultAddress)
        if self.user:
            self.user = validate_ethereum_address(self.user)


@dataclass
class VaultBalance:
    """Vault balance entry."""
    vault_address: str
    account: str
    amount: str
    shares: str
    updated_at: int

# Note: vault balances endpoint returns VaultBalance if user is passed, List[VaultBalance] otherwise
VaultBalancesResponse = Union[VaultBalance, List[VaultBalance]]

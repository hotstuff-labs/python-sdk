"""Example: Vault data."""
import example_utils
from hotstuff import (
    VaultsParams,
    SubVaultsParams,
    VaultBalancesParams,
)

MAIN_ACCOUNT_ADDRESS = "0x42C183edba036906447372a7c81Eb89D0B9f2175"
VAULT_ADDRESS = "0xdE66c594AF8e4AD2C62DcFadCb6714F8b176A4ef"

def main():
    """Main example function."""
    print("--------------------------------\nGlobal trading data\n")
    info, _ = example_utils.setup_clients(is_testnet=True, main_account=False)
    
    # Get vaults
    print("Fetching vaults...")
    vaults = info.vaults(VaultsParams())
    print(f"Vaults: {vaults}\n")

    # Get sub vaults
    print("Fetching sub vaults...")
    sub_vaults = info.sub_vaults(SubVaultsParams(vaultAddress=VAULT_ADDRESS))
    print(f"Sub vaults: {sub_vaults}\n")

    # Get vault balances
    print("Fetching vault balances...")
    vault_balances = info.vault_balances(VaultBalancesParams(vaultAddress=VAULT_ADDRESS, user=MAIN_ACCOUNT_ADDRESS))
    print(f"Vault balances: {vault_balances}\n")

if __name__ == "__main__":
    main()

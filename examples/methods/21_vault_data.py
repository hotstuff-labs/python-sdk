"""Example: Vault data."""
from examples.utils.example_utils import setup_info_client
from hotstuff import (
    VaultsParams,
    SubVaultsParams,
    VaultBalancesParams,
)
from examples.utils.config import CONFIG

def main():
    """Main example function."""
    print("--------------------------------\nGlobal trading data\n")
    info, _, _, _ = setup_info_client()
    
    # Get vaults
    print("Fetching vaults...")
    vaults = info.vaults(VaultsParams())
    print(f"Vaults: {vaults}\n")

    # Get sub vaults
    print("Fetching sub vaults...")
    sub_vaults = info.sub_vaults(SubVaultsParams(vault_address=CONFIG["VAULT_ADDRESS"]))
    print(f"Sub vaults: {sub_vaults}\n")

    # Get vault balances
    print("Fetching vault balances...")
    vault_balances = info.vault_balances(VaultBalancesParams(vault_address=CONFIG["VAULT_ADDRESS"], user=CONFIG["MAIN_ACCOUNT_ADDRESS"]))
    print(f"Vault balances: {vault_balances}\n")

if __name__ == "__main__":
    main()

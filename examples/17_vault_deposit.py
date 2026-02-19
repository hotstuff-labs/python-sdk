"""Example: Vault deposit request."""
import json
import example_utils
from hotstuff import DepositToVaultParams


def main():
    """Main example function."""
    print("--------------------------------\nVault deposit request\n")
    _, exchange = example_utils.setup_clients(is_testnet=True, main_account=False)
        
    # Vault deposit request
    deposit_to_vault_params = DepositToVaultParams(
        vaultAddress="0xdE66c594AF8e4AD2C62DcFadCb6714F8b176A4ef",
        amount="100.0",
    )
    result = exchange.deposit_to_vault(deposit_to_vault_params)
        
    print(f"Vault deposit request successfully!\n\nResponse: {json.dumps(result, indent=2)}\n--------------------------------\n")
        
if __name__ == "__main__":
    main()

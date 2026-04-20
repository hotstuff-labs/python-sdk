"""Example: Vault deposit request."""
import json
from examples.utils.example_utils import setup_exchange_client
from examples.utils.config import ADDRESSES
from hotstuff import DepositToVaultParams


def main():
    """Main example function."""
    print("--------------------------------\nVault deposit request\n")
    exchange, _, _, _ = setup_exchange_client()
        
    # Vault deposit request
    deposit_to_vault_params = DepositToVaultParams(
        vaultAddress=ADDRESSES["VAULT_ADDRESS"],
        amount="100.0",
    )
    result = exchange.deposit_to_vault(deposit_to_vault_params)
        
    print(f"Vault deposit request successfully!\n\nResponse: {json.dumps(result, indent=2)}\n--------------------------------\n")
        
if __name__ == "__main__":
    main()

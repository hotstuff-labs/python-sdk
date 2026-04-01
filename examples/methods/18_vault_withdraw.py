"""Example: Vault withdraw request."""
import json
from examples.utils.example_utils import setup_exchange_client
from examples.utils.config import CONFIG
from hotstuff import RedeemFromVaultParams


def main():
    """Main example function."""
    print("--------------------------------\nVault withdraw request\n")
    exchange, _, _, _ = setup_exchange_client()
        
    # Vault withdraw request
    redeem_from_vault_params = RedeemFromVaultParams(
        vaultAddress=CONFIG["VAULT_ADDRESS"],
        shares="1",
    )
    result = exchange.redeem_from_vault(redeem_from_vault_params)
        
    print(f"Vault withdraw request successfully!\n\nResponse: {json.dumps(result, indent=2)}\n--------------------------------\n")
        
if __name__ == "__main__":
    main()

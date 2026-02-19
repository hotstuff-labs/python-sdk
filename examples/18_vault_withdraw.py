"""Example: Vault withdraw request."""
import json
import example_utils
from hotstuff import RedeemFromVaultParams


def main():
    """Main example function."""
    print("--------------------------------\nVault withdraw request\n")
    _, exchange = example_utils.setup_clients(is_testnet=True, main_account=False)
        
    # Vault withdraw request
    redeem_from_vault_params = RedeemFromVaultParams(
        vaultAddress="0xdE66c594AF8e4AD2C62DcFadCb6714F8b176A4ef",
        shares="1",
    )
    result = exchange.redeem_from_vault(redeem_from_vault_params)
        
    print(f"Vault withdraw request successfully!\n\nResponse: {json.dumps(result, indent=2)}\n--------------------------------\n")
        
if __name__ == "__main__":
    main()

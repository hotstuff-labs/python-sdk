"""Example: Spot withdraw request."""
import json
import example_utils
from hotstuff import AccountSpotWithdrawRequestParams


def main():
    """Main example function."""
    print("--------------------------------\nSpot withdraw request\n")
    _, exchange = example_utils.setup_clients(is_testnet=True, main_account=True)
        
    # Spot withdraw request
    spot_withdraw_request_params = AccountSpotWithdrawRequestParams(
        collateralId=1,
        amount="100.0",
        chainId=11155111,
    )
    result = exchange.account_spot_withdraw_request(spot_withdraw_request_params)
        
    print(f"Spot withdraw request successfully!\n\nResponse: {json.dumps(result, indent=2)}\n--------------------------------\n")
        
if __name__ == "__main__":
    main()

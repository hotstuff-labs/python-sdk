"""Example: Spot withdraw request."""
import json
from examples.utils.example_utils import setup_exchange_client
from hotstuff import AccountSpotWithdrawRequestParams


def main():
    """Main example function."""
    print("--------------------------------\nSpot withdraw request\n")
    exchange, _, _, _ = setup_exchange_client()
        
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

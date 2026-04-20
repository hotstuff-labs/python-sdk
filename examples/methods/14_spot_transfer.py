"""Example: Spot balance transfer request."""
import json
from examples.utils.example_utils import setup_exchange_client
from hotstuff import AccountSpotBalanceTransferRequestParams
from examples.utils.config import ADDRESSES

def main():
    """Main example function."""
    print("--------------------------------\nSpot balance transfer request\n")
    exchange, _, _, _ = setup_exchange_client()
        
    # Spot balance transfer request
    spot_balance_transfer_request_params = AccountSpotBalanceTransferRequestParams(
        collateralId=1,
        amount="100.0",
        destination=ADDRESSES["DESTINATION_ADDRESS"],
    )
    result = exchange.account_spot_balance_transfer_request(spot_balance_transfer_request_params)
        
    print(f"Spot balance transfer request successfully!\n\nResponse: {json.dumps(result, indent=2)}\n--------------------------------\n")
        
if __name__ == "__main__":
    main()

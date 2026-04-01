"""Example: Spot balance transfer request."""
import json
from examples.utils.example_utils import setup_exchange_client
from hotstuff import AccountSpotBalanceTransferRequestParams


def main():
    """Main example function."""
    print("--------------------------------\nSpot balance transfer request\n")
    exchange, _, _, _ = setup_exchange_client()
        
    # Spot balance transfer request
    spot_balance_transfer_request_params = AccountSpotBalanceTransferRequestParams(
        collateralId=1,
        amount="100.0",
        destination="0x78Deb9225c3F28D12922913Fec978e4dC90E1aa4",
    )
    result = exchange.account_spot_balance_transfer_request(spot_balance_transfer_request_params)
        
    print(f"Spot balance transfer request successfully!\n\nResponse: {json.dumps(result, indent=2)}\n--------------------------------\n")
        
if __name__ == "__main__":
    main()

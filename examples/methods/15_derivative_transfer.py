"""Example: Derivative balance transfer request."""
import json
from examples.utils.example_utils import setup_exchange_client
from hotstuff import AccountDerivativeBalanceTransferRequestParams
from examples.utils.config import ADDRESSES


def main():
    """Main example function."""
    print("--------------------------------\nDerivative balance transfer request\n")
    exchange, _, _, _ = setup_exchange_client()
        
    # Derivative balance transfer request
    derivative_balance_transfer_request_params = AccountDerivativeBalanceTransferRequestParams(
        collateralId=1,
        amount="100.0",
        destination=ADDRESSES["DESTINATION_ADDRESS"],
    )
    result = exchange.account_derivative_balance_transfer_request(derivative_balance_transfer_request_params)
        
    print(f"Derivative balance transfer request successfully!\n\nResponse: {json.dumps(result, indent=2)}\n--------------------------------\n")
        
if __name__ == "__main__":
    main()

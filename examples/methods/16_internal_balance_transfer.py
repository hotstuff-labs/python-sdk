"""Example: Internal balance transfer request."""
import json
from examples.utils.example_utils import setup_exchange_client
from hotstuff import AccountInternalBalanceTransferRequestParams


def main():
    """Main example function."""
    print("--------------------------------\nInternal balance transfer request\n")
    exchange, _, _, _ = setup_exchange_client()
        
    # Internal balance transfer request
    internal_balance_transfer_request_params = AccountInternalBalanceTransferRequestParams(
        collateralId=1,
        amount="100.0",
        toDerivativesAccount=False,
    )
    result = exchange.account_internal_balance_transfer_request(internal_balance_transfer_request_params)
        
    print(f"Internal balance transfer request successfully!\n\nResponse: {json.dumps(result, indent=2)}\n--------------------------------\n")
        
if __name__ == "__main__":
    main()

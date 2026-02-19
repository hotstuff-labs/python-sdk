"""Example: Internal balance transfer request."""
import json
import example_utils
from hotstuff import AccountInternalBalanceTransferRequestParams


def main():
    """Main example function."""
    print("--------------------------------\nInternal balance transfer request\n")
    _, exchange = example_utils.setup_clients(is_testnet=True, main_account=True)
        
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

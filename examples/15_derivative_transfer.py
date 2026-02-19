"""Example: Derivative balance transfer request."""
import json
import example_utils
from hotstuff import AccountDerivativeBalanceTransferRequestParams


def main():
    """Main example function."""
    print("--------------------------------\nDerivative balance transfer request\n")
    _, exchange = example_utils.setup_clients(is_testnet=True, main_account=True)
        
    # Derivative balance transfer request
    derivative_balance_transfer_request_params = AccountDerivativeBalanceTransferRequestParams(
        collateralId=1,
        amount="100.0",
        destination="0x78Deb9225c3F28D12922913Fec978e4dC90E1aa4",
    )
    result = exchange.account_derivative_balance_transfer_request(derivative_balance_transfer_request_params)
        
    print(f"Derivative balance transfer request successfully!\n\nResponse: {json.dumps(result, indent=2)}\n--------------------------------\n")
        
if __name__ == "__main__":
    main()

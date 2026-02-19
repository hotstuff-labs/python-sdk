"""Example: Derivative withdraw request."""
import json
import example_utils
from hotstuff import AccountDerivativeWithdrawRequestParams


def main():
    """Main example function."""
    print("--------------------------------\nDerivative withdraw request\n")
    _, exchange = example_utils.setup_clients(is_testnet=True, main_account=True)
        
    # Derivative withdraw request
    derivative_withdraw_request_params = AccountDerivativeWithdrawRequestParams(
        collateralId=1,
        amount="100.0",
        chainId=11155111,
    )
    result = exchange.account_derivative_withdraw_request(derivative_withdraw_request_params)
        
    print(f"Derivative withdraw request successfully!\n\nResponse: {json.dumps(result, indent=2)}\n--------------------------------\n")
        
if __name__ == "__main__":
    main()

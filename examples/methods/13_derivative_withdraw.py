"""Example: Derivative withdraw request."""
import json
from examples.utils.example_utils import setup_exchange_client
from hotstuff import AccountDerivativeWithdrawRequestParams


def main():
    """Main example function."""
    print("--------------------------------\nDerivative withdraw request\n")
    exchange, _, _, _ = setup_exchange_client()
        
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

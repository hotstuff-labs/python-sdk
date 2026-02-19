"""Example: Cancel all orders."""
import json
import example_utils
from hotstuff import CancelAllParams
import time


def main():
    """Main example function."""
    print("--------------------------------\nPlace orders\n")
    _, exchange = example_utils.setup_clients(is_testnet=True, main_account=False)
        
    # Cancel order by client order id
    cancel_all_params = CancelAllParams(
        expiresAfter=int(time.time() * 1000) + 3600000,
    )
    result = exchange.cancel_all(cancel_all_params)
        
    print(f"Client order cancelled successfully!\n\nResponse: {json.dumps(result, indent=2)}\n--------------------------------\n")
        
if __name__ == "__main__":
    main()

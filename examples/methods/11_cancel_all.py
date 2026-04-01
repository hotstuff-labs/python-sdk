"""Example: Cancel all orders."""
import json
from examples.utils.example_utils import setup_trading_client
from hotstuff import CancelAllParams
import time


def main():
    """Main example function."""
    print("--------------------------------\nCancel all orders\n")
    exchange, _, _, _ = setup_trading_client()
        
    # Cancel order by client order id
    cancel_all_params = CancelAllParams(
        expiresAfter=int(time.time() * 1000) + 3600000,
    )
    result = exchange.cancel_all(cancel_all_params)
        
    print(f"Client order cancelled successfully!\n\nResponse: {json.dumps(result, indent=2)}\n--------------------------------\n")
        
if __name__ == "__main__":
    main()

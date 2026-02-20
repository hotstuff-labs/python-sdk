"""Example: Cancel by order id."""
import json
import example_utils
from hotstuff import CancelByOidParams, UnitCancelByOrderId
import time


def main():
    """Main example function."""
    print("--------------------------------\nPlace orders\n")
    _, exchange = example_utils.setup_clients(is_testnet=True, main_account=False)
        
    # Cancel order by order id
    cancel_by_order_id_params = CancelByOidParams(
        cancels=[UnitCancelByOrderId(oid=1, instrumentId=1)],
        expiresAfter=int(time.time() * 1000) + 3600000,
    )
    result = exchange.cancel_by_oid(cancel_by_order_id_params)
        
    print(f"Order cancelled successfully!\n\nResponse: {json.dumps(result, indent=2)}\n--------------------------------\n")
        
if __name__ == "__main__":
    main()

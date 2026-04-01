"""Example: Cancel by client order id."""
import json
from examples.utils.example_utils import setup_trading_client
from hotstuff import CancelByCloidParams, UnitCancelByClOrderId
import time


def main():
    """Main example function."""
    print("--------------------------------\nCancel by client order id\n")
    exchange, _, _, _ = setup_trading_client()
        
    # Cancel order by client order id
    cancel_by_client_order_id_params = CancelByCloidParams(
        cancels=[UnitCancelByClOrderId(cloid="test-order-1", instrumentId=1)],
        expiresAfter=int(time.time() * 1000) + 3600000,
    )
    result = exchange.cancel_by_cloid(cancel_by_client_order_id_params)
        
    print(f"Client order cancelled successfully!\n\nResponse: {json.dumps(result, indent=2)}\n--------------------------------\n")
        
if __name__ == "__main__":
    main()

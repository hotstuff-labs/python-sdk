"""Example: Approve broker fee."""
import json
from examples.utils.example_utils import setup_exchange_client
from examples.utils.config import ADDRESSES
from hotstuff import ApproveBrokerFeeParams



def main():
    """Main example function."""
    print("--------------------------------\nApprove broker fee\n")
    exchange, _, _, _ = setup_exchange_client()
    
    result = exchange.approve_broker_fee(ApproveBrokerFeeParams(broker=ADDRESSES["BROKER_ADDRESS"], maxFeeRate="0.01"))
        
    print(f"Broker fee approved successfully!\n\nResponse: {json.dumps(result, indent=2)}\n--------------------------------\n")
        
if __name__ == "__main__":
    main()

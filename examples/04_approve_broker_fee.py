"""Example: Approve broker fee."""
import json
import example_utils
from hotstuff import ApproveBrokerFeeParams



def main():
    """Main example function."""
    print("--------------------------------\nApprove broker fee\n")
    _, exchange = example_utils.setup_clients(is_testnet=True, main_account=True)
    
    result = exchange.approve_broker_fee(ApproveBrokerFeeParams(broker="0x78Deb9225c3F28D12922913Fec978e4dC90E1aa4", maxFeeRate="0.01"))
        
    print(f"Broker fee approved successfully!\n\nResponse: {json.dumps(result, indent=2)}\n--------------------------------\n")
        
if __name__ == "__main__":
    main()

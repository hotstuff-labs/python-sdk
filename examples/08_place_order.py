"""Example: Place orders."""
import json
import example_utils
from hotstuff import PlaceOrderParams, UnitOrder
import time



def main():
    """Main example function."""
    print("--------------------------------\nPlace orders\n")
    _, exchange = example_utils.setup_clients(is_testnet=True, main_account=False)

    unit_order = UnitOrder(instrumentId=1, side="b", positionSide="BOTH", price="10000", size="1", tif="GTC", ro=False, po=False)
    expires_after = int(time.time() * 1000) + 3600000
    
    result = exchange.place_order(PlaceOrderParams(orders=[unit_order], expiresAfter=expires_after))
        
    print(f"Orders placed successfully!\n\nResponse: {json.dumps(result, indent=2)}\n--------------------------------\n")
        
if __name__ == "__main__":
    main()

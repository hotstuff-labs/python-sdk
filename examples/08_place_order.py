"""Example: Place orders."""
import json
import example_utils
from hotstuff import PlaceOrderParams, UnitOrder, BrokerConfig
import time



def main():
    """Main example function."""
    print("--------------------------------\nPlace orders\n")
    _, exchange = example_utils.setup_clients(is_testnet=True, main_account=False)

    unit_order = UnitOrder(
        instrumentId=1,
        side="b",
        positionSide="BOTH",
        price='100',
        size="0.01",
        tif="GTC",
        ro=False,
        po=False,
        # cloid='test-order-1',
        # triggerPx='',
        # isMarket=False,
        # tpsl='',
        # grouping='',
    )

    # broker_config = BrokerConfig(broker='', fee='0.001')

    expires_after = int(time.time() * 1000) + 3600000

    place_order_params = PlaceOrderParams(orders=[unit_order], expiresAfter=expires_after)
    
    result = exchange.place_order(place_order_params)
        
    print(f"Orders placed successfully!\n\nResponse: {json.dumps(result, indent=2)}\n--------------------------------\n")
        
if __name__ == "__main__":
    main()

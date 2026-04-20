"""Example: Place orders."""
import json
from examples.utils.example_utils import setup_trading_client
from hotstuff import PlaceOrderParams, UnitOrder, BrokerConfig
import time
from examples.utils.config import ADDRESSES

def place_order_payload():
    """Generate place order payload."""
    unit_order = UnitOrder(
        instrumentId=1,
        side="b",
        positionSide="BOTH",
        price='68508',
        size="0.001",
        tif="GTC",
        ro=False,
        po=False,
        # cloid='test-order-1',
        # triggerPx='',
        # isMarket=False,
        # tpsl='',
        # grouping='',
    )

    expires_after = int(time.time() * 1000) + 3600000

    place_order_params = PlaceOrderParams(orders=[unit_order], expiresAfter=expires_after)
    return place_order_params

def place_order_payload_with_nonce():
    """Generate place order payload."""
    unit_order = UnitOrder(
        instrumentId=1,
        side="b",
        positionSide="BOTH",
        price='68508',
        size="0.001",
        tif="GTC",
        ro=False,
        po=False,
        # cloid='test-order-1',
        # triggerPx='',
        # isMarket=False,
        # tpsl='',
        # grouping='',
    )

    nonce = 1234567890

    expires_after = int(time.time() * 1000) + 3600000

    place_order_params = PlaceOrderParams(orders=[unit_order], nonce=nonce, expiresAfter=expires_after)
    return place_order_params


def place_order_payload_with_broker_config():
    """Generate place order payload."""
    unit_order = UnitOrder(
        instrumentId=1,
        side="b",
        positionSide="BOTH",
        price='68508',
        size="0.001",
        tif="GTC",
        ro=False,
        po=False,
        # cloid='test-order-1',
        # triggerPx='',
        # isMarket=False,
        # tpsl='',
        # grouping='',
    )

    broker_config = BrokerConfig(broker=ADDRESSES["BROKER_ADDRESS"], fee='0.001')

    expires_after = int(time.time() * 1000) + 3600000

    place_order_params = PlaceOrderParams(orders=[unit_order], brokerConfig=broker_config, expiresAfter=expires_after)
    return place_order_params

def main():
    """Main example function."""
    print("--------------------------------\nPlace orders\n")
    exchange, _, _, _ = setup_trading_client()

    # Place order with no broker config
    # place_order_params = place_order_payload()
    # result = exchange.place_order(place_order_params)
        
    # Place order with broker config
    # place_order_params = place_order_payload_with_broker_config()
    # result = exchange.place_order(place_order_params)

    # Place order with nonce
    place_order_params = place_order_payload_with_nonce()
    result = exchange.place_order(place_order_params)
        
    print(f"Orders placed successfully!\n\nResponse: {json.dumps(result, indent=2)}\n--------------------------------\n")
        
if __name__ == "__main__":
    main()

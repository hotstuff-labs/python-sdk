"""Example: Trading with ExchangeClient."""
import asyncio
import time
import os
from hotstuff_sdk import (
    HttpTransport,
    ExchangeClient,
    InfoClient,
    HttpTransportOptions,
)
from eth_account import Account


async def main():
    """Main example function."""
    # Get private key from environment
    private_key = os.getenv("PRIVATE_KEY")
    if not private_key:
        print("ERROR: PRIVATE_KEY environment variable not set")
        return
    
    # Create HTTP transport for testnet
    transport = HttpTransport(
        HttpTransportOptions(is_testnet=True)
    )
    
    # Create account from private key
    account = Account.from_key(private_key)
    print(f"Trading account: {account.address}\n")
    
    # Create clients
    info = InfoClient(transport=transport)
    exchange = ExchangeClient(transport=transport, wallet=account)
    
    try:
        # Get current ticker
        print("Fetching current price...")
        ticker = await info.ticker({"symbol": "BTC-PERP"})
        current_price = ticker.get("last", 50000)
        print(f"Current BTC-PERP price: {current_price}\n")
        
        # Place a limit order
        print("Placing limit order...")
        order_result = await exchange.place_order({
            "orders": [{
                "instrumentId": 1,
                "side": "b",  # buy
                "positionSide": "LONG",
                "price": str(current_price * 0.95),  # 5% below market
                "size": "0.01",
                "tif": "GTC",
                "ro": False,
                "po": True,  # post-only
                "cloid": f"example-order-{int(time.time())}",
            }],
            "expiresAfter": int(time.time()) + 3600,  # 1 hour
        })
        print(f"Order result: {order_result}\n")
        
        # Get open orders
        print("Fetching open orders...")
        open_orders = await info.open_orders({"user": account.address})
        print(f"Open orders: {open_orders}\n")
        
        # Cancel all orders
        print("Cancelling all orders...")
        cancel_result = await exchange.cancel_all({
            "expiresAfter": int(time.time()) + 3600,
        })
        print(f"Cancel result: {cancel_result}\n")
        
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        # Clean up
        await transport.close()


if __name__ == "__main__":
    asyncio.run(main())


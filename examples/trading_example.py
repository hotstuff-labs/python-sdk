"""Example: Trading with ExchangeClient."""
import asyncio
import time
import os
from hotstuff import (
    CancelByOidParams,
    HttpTransport,
    ExchangeClient,
    InfoClient,
    HttpTransportOptions,
)
from eth_account import Account
import importlib

global_methods = importlib.import_module("hotstuff.methods.info.global")
TickerParams = global_methods.TickerParams

from hotstuff.methods.info.account import OpenOrdersParams
from hotstuff.methods.exchange.trading import (
    PlaceOrderParams,
    UnitOrder,
    BrokerConfig,
    CancelAllParams,
    UnitCancelByOrderId,
)


async def main():
    """Main example function."""
    # Get private key from environment
    private_key = os.getenv("AGENT_PRIVATE_KEY")
    if not private_key:
        print("ERROR: AGENT_PRIVATE_KEY environment variable must be set")
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
        ticker = await info.ticker(TickerParams(symbol="BTC-PERP"))
        # ticker returns a list with one element
        ticker_data = ticker[0] if ticker else None
        current_price = float(ticker_data.last_price) if ticker_data else 50000.0
        print(f"Current BTC-PERP price: {current_price}\n")
        
        # Place a limit order
        print("Placing limit order...")
        order_result = await exchange.place_order(
            PlaceOrderParams(
                orders=[
                    UnitOrder(
                        instrument_id=1,
                        side="b",  # buy
                        position_side="BOTH",
                        price= "65000",  
                        size="0.0005",
                        tif="GTC",
                        ro=False,
                        po=False,  # post-only
                        cloid="test-order-1",
                        trigger_px=None,
                        is_market=False,
                        tpsl="",
                        grouping="",
                    )
                ],
                expires_after=int(time.time() * 1000) + 3600000,  # 1 hour (in milliseconds)
            )
        )
        print(f"Order result: {order_result}\n")
        
        # # Get open orders
        print("Fetching open orders...")
        open_orders = await info.open_orders(OpenOrdersParams(user=account.address))
        print(f"Open orders: {open_orders}\n")


        # Cancel order by oid
        print("Cancelling order by oid...")
        cancel_result = await exchange.cancel_by_oid(
            CancelByOidParams(
                cancels=[UnitCancelByOrderId(oid=order_result["data"]["status"][0]["resting"]["order_id"], instrumentId=1)],
                expires_after=int(time.time() * 1000) + 3600000,
            )
        )
        print(f"Cancel result: {cancel_result}\n")
        
        # Cancel all orders
        # print("Cancelling all orders...")
        # cancel_result = await exchange.cancel_all(
        #     CancelAllParams(
        #         expires_after=int(time.time() * 1000) + 3600000,  # 1 hour (in milliseconds)
        #     )
        # )
        print(f"Cancel result: {cancel_result}\n")
        
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        # Clean up
        await transport.close()


if __name__ == "__main__":
    asyncio.run(main())

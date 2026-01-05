"""Example: WebSocket subscriptions."""
import asyncio
from hotstuff import (
    WebSocketTransport,
    SubscriptionClient,
    WebSocketTransportOptions,
)


async def main():
    """Main example function."""
    # Create WebSocket transport for testnet
    transport = WebSocketTransport(
        WebSocketTransportOptions(is_testnet=True)
    )
    
    # Create SubscriptionClient
    subscriptions = SubscriptionClient(transport=transport)
    
    try:
        # Subscribe to ticker updates
        def handle_ticker(data):
            print(f"Ticker update: {data.data}")
        
        print("Subscribing to BTC-PERP ticker...")
        ticker_sub = await subscriptions.ticker(
            {"symbol": "BTC-PERP"},
            handle_ticker
        )
        
        # Subscribe to trades
        def handle_trade(data):
            print(f"Trade: {data.data}")
        
        print("Subscribing to BTC-PERP trades...")
        trade_sub = await subscriptions.trade(
            {"symbol": "BTC-PERP"},
            handle_trade
        )
        
        # Run for 30 seconds
        print("\nListening to updates for 30 seconds...\n")
        await asyncio.sleep(30)
        
        # Unsubscribe
        print("\nUnsubscribing...")
        await ticker_sub["unsubscribe"]()
        await trade_sub["unsubscribe"]()
        
    finally:
        # Clean up
        await transport.disconnect()


if __name__ == "__main__":
    asyncio.run(main())


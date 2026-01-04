"""Example: Basic usage of the Hotstuff Python SDK."""
import asyncio
from hotstuff import (
    HttpTransport,
    InfoClient,
    HttpTransportOptions,
)


async def main():
    """Main example function."""
    # Create HTTP transport for testnet
    transport = HttpTransport(
        HttpTransportOptions(is_testnet=True)
    )
    
    # Create InfoClient
    info = InfoClient(transport=transport)
    
    try:
        # Get all instruments
        print("Fetching instruments...")
        instruments = await info.instruments({"type": "all"})
        print(f"Instruments: {instruments}\n")
        
        # Get ticker for BTC-PERP
        print("Fetching BTC-PERP ticker...")
        ticker = await info.ticker({"symbol": "BTC-PERP"})
        print(f"BTC-PERP Ticker: {ticker}\n")
        
        # Get orderbook
        print("Fetching orderbook...")
        orderbook = await info.orderbook({"symbol": "BTC-PERP", "depth": 10})
        print(f"Orderbook: {orderbook}\n")
        
        # Get recent trades
        print("Fetching recent trades...")
        trades = await info.trades({"symbol": "BTC-PERP", "limit": 5})
        print(f"Recent trades: {trades}\n")
        
    finally:
        # Clean up
        await transport.close()


if __name__ == "__main__":
    asyncio.run(main())


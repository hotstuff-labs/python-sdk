import asyncio
from hotstuff import (
    HttpTransport,
    InfoClient,
    HttpTransportOptions,
)
from hotstuff.methods.info.account import OrderHistoryParams, FundingHistoryParams, TradeHistoryParams


async def main():
    transport = HttpTransport(HttpTransportOptions(is_testnet=False))
    info = InfoClient(transport=transport)
    try:
        print("Fetching order history...")
        order_history = await info.order_history(
            OrderHistoryParams(user="0x3096E206da35141D5B23aE16C42C070f7df082a8", limit=10)
        )
        print(order_history)
        
        print("fetching funding history...")
        funding_history = await info.funding_history(
            FundingHistoryParams(user="0x3096E206da35141D5B23aE16C42C070f7df082a8", limit=10)
        )
        print(funding_history)
        
        print("fetching fills (trade history) ....")
        fills = await info.trade_history(
            TradeHistoryParams(user="0x3096E206da35141D5B23aE16C42C070f7df082a8")
        )
        print(fills)
        
    finally:
        await transport.close()


if __name__ == "__main__":
    asyncio.run(main())
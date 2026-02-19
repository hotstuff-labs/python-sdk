"""Example: Global trading data."""
import example_utils
import time
from hotstuff import (
    OracleParams,
    SupportedCollateralParams,
    InstrumentsParams,
    TickerParams,
    OrderbookParams,
    TradesParams,
    MidsParams,
    BBOParams,
    ChartParams,
)



def main():
    """Main example function."""
    print("--------------------------------\nGlobal trading data\n")
    info, _ = example_utils.setup_clients(is_testnet=True, main_account=False)
    
   # Get oracle prices
    print("Fetching oracle prices...")
    oracle = info.oracle(OracleParams(symbol="USDT/USDC"))
    print(f"Oracle prices: {oracle}\n")

    # Get supported collateral currencies
    print("Fetching supported collateral currencies...")
    supported_collateral = info.supported_collateral(SupportedCollateralParams())
    print(f"Supported collateral currencies: {supported_collateral}\n")
        
    # Get all instruments
    print("Fetching instruments...")
    instruments = info.instruments(InstrumentsParams(type="all"))
    print(f"Instruments: {instruments}\n")

    # Get ticker for BTC-PERP
    print("Fetching BTC-PERP ticker...")
    ticker = info.ticker(TickerParams(symbol="BTC-PERP"))
    print(f"BTC-PERP Ticker: {ticker}\n")

    # Get orderbook for BTC-PERP
    print("Fetching BTC-PERP orderbook...")
    orderbook = info.orderbook(OrderbookParams(symbol="BTC-PERP", depth=10))
    print(f"BTC-PERP Orderbook: {orderbook}\n")

    # Get recent trades for BTC-PERP
    print("Fetching recent trades for BTC-PERP...")
    trades = info.trades(TradesParams(symbol="BTC-PERP", limit=5))
    print(f"Recent trades: {trades}\n")

    # Get mid prices for all instruments
    print("Fetching mid prices for all instruments...")
    mids = info.mids(MidsParams())
    print(f"Mid prices: {mids}\n")

    # Get best bid/offer for BTC-PERP
    print("Fetching best bid/offer for BTC-PERP...")
    bbo = info.bbo(BBOParams(symbol="BTC-PERP"))
    print(f"BTC-PERP Best bid/offer: {bbo}\n")

    # Get chart data for BTC-PERP
    print("Fetching chart data for BTC-PERP...")
    chart = info.chart(ChartParams(symbol="1", chart_type="mark", resolution="5", from_=int(time.time()) - 1000, to=int(time.time())))
    print(f"BTC-PERP Chart data: {chart}\n")

if __name__ == "__main__":
    main()

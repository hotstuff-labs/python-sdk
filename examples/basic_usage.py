"""Example: Basic usage of the Hotstuff Python SDK."""
from hotstuff import (
    HttpTransport,
    InfoClient,
    HttpTransportOptions,
)

from hotstuff.methods.info.market import InstrumentsParams, TickerParams, OrderbookParams, TradesParams, SupportedCollateralParams
from hotstuff.methods.info.account import InstrumentLeverageParams, UserBalanceInfoParams, UserFeeInfoParams, AccountSummaryParams


def main():
    """Main example function."""
    # Create HTTP transport for testnet
    transport = HttpTransport(
        HttpTransportOptions(is_testnet=False)
    )
    
    # Create InfoClient
    info = InfoClient(transport=transport)
    
    try:
        # Get all instruments
        print("Fetching instruments...")
        instruments = info.instruments(InstrumentsParams(type="all"))
        print(f"Instruments: {instruments}\n")
        
        # Get supported collateral currencies
        print("Fetching supported collateral currencies...")
        supported_collateral = info.supported_collateral(SupportedCollateralParams())
        print(f"Supported collateral currencies: {supported_collateral}\n")
        
        # Get ticker for BTC-PERP
        print("Fetching BTC-PERP ticker...")
        ticker = info.ticker(TickerParams(symbol="BTC-PERP"))
        print(f"BTC-PERP Ticker: {ticker}\n")
        
        # Get orderbook
        print("Fetching orderbook...")
        orderbook = info.orderbook(OrderbookParams(symbol="BTC-PERP", depth=10))
        print(f"Orderbook: {orderbook}\n")
        
        # Get recent trades
        print("Fetching recent trades...")
        trades = info.trades(TradesParams(symbol="BTC-PERP", limit=5))
        print(f"Recent trades: {trades}\n")
        
        # Get instrument leverage for a user for a specific symbol
        print("Fetching instrument leverage...")
        leverage = info.instrument_leverage(InstrumentLeverageParams(user="0x3096E206da35141D5B23aE16C42C070f7df082a8", symbol="BTC-PERP"))
        print(f"Instrument leverage: {leverage}\n")
        
        # Get account balance info
        print("Fetching account balance info...")
        account_balance = info.user_balance(UserBalanceInfoParams(user="0x3096E206da35141D5B23aE16C42C070f7df082a8", type="all"))
        print(f"Account balance: {account_balance}\n")
        
        # Get user fee info
        print("Fetching user fee info...")
        user_fee = info.user_fee_info(UserFeeInfoParams(user="0x3096E206da35141D5B23aE16C42C070f7df082a8"))
        print(f"User fee: {user_fee}\n")
        
        # Get account summary info
        print("Fetching account summary info...")
        account_summary = info.account_summary(AccountSummaryParams(user="0x3096E206da35141D5B23aE16C42C070f7df082a8"))
        print(f"Account summary: {account_summary}\n")
        
    finally:
        # Clean up
        transport.close()


if __name__ == "__main__":
    main()

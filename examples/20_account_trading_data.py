"""Example: Account trading data."""
import example_utils
from hotstuff import (
  OpenOrdersParams,
  PositionsParams,
  AccountSummaryParams,
  AccountInfoParams,
  ReferralSummaryParams,
  UserFeeInfoParams,
  AccountHistoryParams,
  OrderHistoryParams,
  FillsParams,
  FundingHistoryParams,
  TransferHistoryParams,
  InstrumentLeverageParams,
  AgentsParams,
)

MAIN_ACCOUNT_ADDRESS = "0x42C183edba036906447372a7c81Eb89D0B9f2175"

def main():
    """Main example function."""
    print("--------------------------------\nAccount trading data\n")
    info, _ = example_utils.setup_clients(is_testnet=True, main_account=False)
    
    # # Get open orders
    print("Fetching open orders...")
    open_orders = info.open_orders(OpenOrdersParams(user=MAIN_ACCOUNT_ADDRESS))
    print(f"Open orders: {open_orders}\n")

    # # Get positions
    print("Fetching positions...")
    positions = info.positions(PositionsParams(user=MAIN_ACCOUNT_ADDRESS))
    print(f"Positions: {positions}\n")

    # Get account summary
    print("Fetching account summary...")
    account_summary = info.account_summary(AccountSummaryParams(user=MAIN_ACCOUNT_ADDRESS))
    print(f"Account summary: {account_summary}\n")

    # Get account info
    print("Fetching account info...")
    account_info = info.account_info(AccountInfoParams(user=MAIN_ACCOUNT_ADDRESS))
    print(f"Account info: {account_info}\n")

    # Get referral summary
    print("Fetching referral summary...")
    referral_summary = info.referral_summary(ReferralSummaryParams(user=MAIN_ACCOUNT_ADDRESS))
    print(f"Referral summary: {referral_summary}\n")

    # Get user fee info
    print("Fetching user fee info...")
    user_fee_info = info.user_fee_info(UserFeeInfoParams(user=MAIN_ACCOUNT_ADDRESS))
    print(f"User fee info: {user_fee_info}\n")

    # Get account history
    print("Fetching account history...")
    account_history = info.account_history(AccountHistoryParams(user=MAIN_ACCOUNT_ADDRESS))
    print(f"Account history: {account_history}\n")

    # Get order history
    print("Fetching order history...")
    order_history = info.order_history(OrderHistoryParams(user=MAIN_ACCOUNT_ADDRESS))
    print(f"Order history: {order_history}\n")

    # Get fills
    print("Fetching fills...")
    fills = info.fills(FillsParams(user=MAIN_ACCOUNT_ADDRESS))
    print(f"Fills: {fills}\n")


    # Get funding history
    print("Fetching funding history...")
    funding_history = info.funding_history(FundingHistoryParams(user=MAIN_ACCOUNT_ADDRESS))
    print(f"Funding history: {funding_history}\n")

    # # Get transfer history
    print("Fetching transfer history...")
    transfer_history = info.transfer_history(TransferHistoryParams(user=MAIN_ACCOUNT_ADDRESS))
    print(f"Transfer history: {transfer_history}\n")

    # Get instrument leverage
    print("Fetching instrument leverage...")
    instrument_leverage = info.instrument_leverage(InstrumentLeverageParams(user=MAIN_ACCOUNT_ADDRESS, symbol="BTC-PERP"))
    print(f"Instrument leverage: {instrument_leverage}\n")

    # Get agents
    print("Fetching agents...")
    agents = info.agents(AgentsParams(user=MAIN_ACCOUNT_ADDRESS))
    print(f"Agents: {agents}\n")

  
if __name__ == "__main__":
    main()

"""Example: Explorer data."""
import example_utils
from hotstuff import (
    BlocksParams,
    BlockDetailsParams,
    TransactionsParams,
    TransactionDetailsParams,
)

BLOCK_HEIGHT = 162778
TRANSACTION_HASH = "0x4cb07520655fd427da1574a0ac819b8d60e214b3e3a21fcbd07eee2f90b33029"

def main():
    """Main example function."""
    print("--------------------------------\nGlobal trading data\n")
    info, _ = example_utils.setup_clients(is_testnet=True, main_account=False)
    
    # Get blocks
    # print("Fetching blocks...")
    # blocks = info.blocks(BlocksParams(limit=10, offset=0))
    # print(f"Blocks: {blocks}\n")

    # Get block details
    print("Fetching block details...")
    block_details = info.block_details(BlockDetailsParams(block_height=BLOCK_HEIGHT))
    print(f"Block details: {block_details}\n")

    # Get transactions
    # print("Fetching transactions...")
    # transactions = info.transactions(TransactionsParams(blockNumber=BLOCK_NUMBER))
    # print(f"Transactions: {transactions}\n")

    # Get transaction details
    print("Fetching transaction details...")
    transaction_details = info.transaction_details(TransactionDetailsParams(tx_hash=TRANSACTION_HASH))
    print(f"Transaction details: {transaction_details}\n")

if __name__ == "__main__":
    main()

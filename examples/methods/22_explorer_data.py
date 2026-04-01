"""Example: Explorer data."""
from examples.utils.example_utils import setup_info_client
from hotstuff import (
    BlocksParams,
    BlockDetailsParams,
    TransactionsParams,
    TransactionDetailsParams,
)

def main():
    """Main example function."""
    print("--------------------------------\nGlobal trading data\n")
    info, _, _, _ = setup_info_client()
    
    # Get blocks
    print("Fetching blocks...")
    blocks = info.blocks(BlocksParams(limit=10, offset=0))
    print(f"Blocks: {blocks}\n")

    # Get block details
    print("Fetching block details...")
    block_details = info.block_details(BlockDetailsParams(block_height=162778))
    print(f"Block details: {block_details}\n")

    # Get transactions
    print("Fetching transactions...")
    transactions = info.transactions(TransactionsParams(blockNumber=162778))
    print(f"Transactions: {transactions}\n")

    # Get transaction details
    print("Fetching transaction details...")
    transaction_details = info.transaction_details(TransactionDetailsParams(tx_hash="0x4cb07520655fd427da1574a0ac819b8d60e214b3e3a21fcbd07eee2f90b33029"))
    print(f"Transaction details: {transaction_details}\n")

if __name__ == "__main__":
    main()

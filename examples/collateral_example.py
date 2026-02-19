"""Example: Collateral transfer operations with ExchangeClient."""
import os
from hotstuff import (
    HttpTransport,
    ExchangeClient,
    HttpTransportOptions,
)
from eth_account import Account
from hotstuff.methods.exchange.collateral import (
    AccountSpotWithdrawRequestParams,
    AccountDerivativeWithdrawRequestParams,
    AccountSpotBalanceTransferRequestParams,
    AccountDerivativeBalanceTransferRequestParams,
    AccountInternalBalanceTransferRequestParams,
)


def main():
    """Main example function demonstrating collateral transfer operations."""
    # Get private key from environment
    private_key = os.getenv("PRIVATE_KEY")
    if not private_key:
        print("ERROR: PRIVATE_KEY environment variable must be set")
        return
    
    # Create HTTP transport for testnet
    transport = HttpTransport(
        HttpTransportOptions(is_testnet=True)
    )
    
    # Create account from private key
    account = Account.from_key(private_key)
    print(f"Account: {account.address}\n")
    
    # Create exchange client
    exchange = ExchangeClient(transport=transport, wallet=account)
    
    try:
        # Example 1: Request spot collateral withdrawal to external chain
        print("Example 1: Spot Withdraw Request")
        print("-" * 40)
        result = exchange.account_spot_withdraw_request(
            AccountSpotWithdrawRequestParams(
                collateral_id=1,  # USDC
                amount="100.0",
                chain_id=1,  # Ethereum mainnet
            )
        )
        print(f"Spot withdraw request result: {result}\n")
        
        # Example 2: Request derivative collateral withdrawal to external chain
        print("Example 2: Derivative Withdraw Request")
        print("-" * 40)
        result = exchange.account_derivative_withdraw_request(
            AccountDerivativeWithdrawRequestParams(
                collateral_id=1,  # USDC
                amount="50.0",
                chain_id=1,  # Ethereum mainnet
            )
        )
        print(f"Derivative withdraw request result: {result}\n")
        
        # Example 3: Transfer spot balance to another address on Hotstuff
        print("Example 3: Spot Balance Transfer")
        print("-" * 40)
        recipient_address = "0x1234567890123456789012345678901234567890"  # Replace with actual address
        result = exchange.account_spot_balance_transfer_request(
            AccountSpotBalanceTransferRequestParams(
                collateral_id=1,  # USDC
                amount="25.0",
                destination=recipient_address,
            )
        )
        print(f"Spot balance transfer result: {result}\n")
        
        # Example 4: Transfer derivative balance to another address on Hotstuff
        print("Example 4: Derivative Balance Transfer")
        print("-" * 40)
        result = exchange.account_derivative_balance_transfer_request(
            AccountDerivativeBalanceTransferRequestParams(
                collateral_id=1,  # USDC
                amount="25.0",
                destination=recipient_address,
            )
        )
        print(f"Derivative balance transfer result: {result}\n")
        
        # Example 5: Internal transfer between spot and derivatives accounts
        print("Example 5: Internal Balance Transfer (Spot -> Derivatives)")
        print("-" * 40)
        result = exchange.account_internal_balance_transfer_request(
            AccountInternalBalanceTransferRequestParams(
                collateral_id=1,  # USDC
                amount="10.0",
                to_derivatives_account=True,  # Transfer from spot to derivatives
            )
        )
        print(f"Internal transfer (spot -> derivatives) result: {result}\n")
        
        # Example 6: Internal transfer from derivatives to spot
        print("Example 6: Internal Balance Transfer (Derivatives -> Spot)")
        print("-" * 40)
        result = exchange.account_internal_balance_transfer_request(
            AccountInternalBalanceTransferRequestParams(
                collateral_id=1,  # USDC
                amount="5.0",
                to_derivatives_account=False,  # Transfer from derivatives to spot
            )
        )
        print(f"Internal transfer (derivatives -> spot) result: {result}\n")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        transport.close()


if __name__ == "__main__":
    main()

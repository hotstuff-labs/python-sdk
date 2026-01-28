"""Example: Vault operations with ExchangeClient."""
import asyncio
import os
from hotstuff import (
    HttpTransport,
    ExchangeClient,
    InfoClient,
    HttpTransportOptions,
)
from eth_account import Account
from hotstuff.methods.exchange.vault import (
    DepositToVaultParams,
    RedeemFromVaultParams,
)


async def main():
    """Main example function demonstrating vault operations."""
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
    
    # Create clients
    info = InfoClient(transport=transport)
    exchange = ExchangeClient(transport=transport, wallet=account)
    
    # Example vault address (replace with actual vault address)
    vault_address = "0x1234567890123456789012345678901234567890"
    
    try:
        # Get available vaults
        print("Fetching available vaults...")
        print("-" * 40)
        # Uncomment when vaults endpoint is available:
        # vaults = await info.vaults({})
        # print(f"Available vaults: {vaults}\n")
        
        # Example 1: Deposit to a vault
        print("Example 1: Deposit to Vault")
        print("-" * 40)
        result = await exchange.deposit_to_vault(
            DepositToVaultParams(
                vault_address=vault_address,
                amount="1000.0",  # Amount to deposit
            )
        )
        print(f"Deposit result: {result}\n")
        
        # Example 2: Redeem shares from a vault
        print("Example 2: Redeem from Vault")
        print("-" * 40)
        result = await exchange.redeem_from_vault(
            RedeemFromVaultParams(
                vault_address=vault_address,
                shares="500.0",  # Number of shares to redeem
            )
        )
        print(f"Redeem result: {result}\n")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        await transport.close()


if __name__ == "__main__":
    asyncio.run(main())

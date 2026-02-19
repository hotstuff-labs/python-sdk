"""Example: Broker fee with agent trading flow.

This example demonstrates the full flow of:
1. Approving a broker fee from the main account
2. Creating an agent
3. Placing orders through the agent with broker configuration
"""
import time
import os
from hotstuff import (
    HttpTransport,
    ExchangeClient,
    HttpTransportOptions,
)
from eth_account import Account
from hotstuff.methods.exchange.account import (
    AddAgentParams,
    RevokeAgentParams,
    ApproveBrokerFeeParams,
)
from hotstuff.methods.exchange.trading import (
    PlaceOrderParams,
    UnitOrder,
    BrokerConfig,
)


def main():
    """Main example function demonstrating broker fee with agent trading."""
    # Get main account private key from environment
    main_private_key = os.getenv("PRIVATE_KEY")
    if not main_private_key:
        print("ERROR: PRIVATE_KEY environment variable must be set")
        return
    
    # Create HTTP transport for testnet
    transport = HttpTransport(
        HttpTransportOptions(is_testnet=True)
    )
    
    # Main account setup (the account that will approve broker fees and create agent)
    main_account = Account.from_key(main_private_key)
    print(f"Main account: {main_account.address}")
    
    # Create exchange client for main account
    main_exchange = ExchangeClient(transport=transport, wallet=main_account)
    
    # Broker address that will receive fees (replace with actual broker address)
    broker_address = "0x1234567890123456789012345678901234567890"
    
    try:
        # Step 1: Approve broker fee from main account
        print("\nStep 1: Approving broker fee...")
        print("-" * 40)
        result = main_exchange.approve_broker_fee(
            ApproveBrokerFeeParams(
                broker=broker_address,
                max_fee_rate="0.001",  # 0.1% max fee rate
            )
        )
        print(f"Broker fee approved! Result: {result}\n")
        
        # Step 2: Generate agent credentials and add agent
        print("Step 2: Creating and adding agent...")
        print("-" * 40)
        
        # Generate a new agent account
        agent_account = Account.create()
        agent_private_key = agent_account.key.hex()
        
        print(f"Agent address: {agent_account.address}")
        
        result = main_exchange.add_agent(
            AddAgentParams(
                agent_name="broker-trading-agent",
                agent=agent_account.address,
                for_account="",
                agent_private_key=agent_private_key,
                signer=main_account.address,
                valid_until=int(time.time() * 1000) + 86400000 * 30,  # Valid for 30 days (in milliseconds)
            )
        )
        print(f"Agent added! Result: {result}\n")
        
        # Step 3: Create exchange client for the agent
        print("Step 3: Setting up agent exchange client...")
        print("-" * 40)
        agent_exchange = ExchangeClient(transport=transport, wallet=agent_account)
        print("Agent exchange client created.\n")
        
        # Step 4: Place order from agent with broker config
        print("Step 4: Placing order with broker fee...")
        print("-" * 40)
        result = agent_exchange.place_order(
            PlaceOrderParams(
                orders=[
                    UnitOrder(
                        instrument_id=1,
                        side="b",  # buy
                        position_side="BOTH",
                        price="50000.00",
                        size="0.1",
                        tif="GTC",
                        ro=False,
                        po=False,
                        cloid=f"broker-order-{int(time.time())}",
                        trigger_px=None,
                        is_market=False,
                        tpsl="",
                        grouping="",
                    )
                ],
                broker_config=BrokerConfig(
                    broker=broker_address,
                    fee="0.0005",  # 0.05% fee (must be <= approved maxFeeRate)
                ),
                expires_after=int(time.time() * 1000) + 3600000,  # 1 hour (in milliseconds)
            )
        )
        print(f"Order placed with broker fee! Result: {result}\n")
        
        # Optional: Revoke agent when done
        print("Optional: Revoking agent...")
        print("-" * 40)
        # Uncomment to revoke the agent:
        # result = main_exchange.revoke_agent(
        #     RevokeAgentParams(
        #         agent=agent_account.address,
        #         for_account="",  # optional: sub-account address
        #     )
        # )
        # print(f"Agent revoked! Result: {result}\n")
        print("Skipped (uncomment to enable)\n")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        transport.close()


if __name__ == "__main__":
    main()

"""Example: Adding an agent with ExchangeClient."""
import asyncio
import time
import os
from hotstuff import (
    HttpTransport,
    ExchangeClient,
    InfoClient,
    HttpTransportOptions,
    AddAgentParams,
)
from eth_account import Account

async def main():
    """Main example function."""
    main_private_key = os.getenv("PRIVATE_KEY")
    agent_private_key = Account.create().key.hex()

    if not main_private_key or not agent_private_key:
        print("ERROR: PRIVATE_KEY and AGENT_PRIVATE_KEY environment variables must be set")
        return
    
    # Create HTTP transport for testnet
    transport = HttpTransport(
        HttpTransportOptions(is_testnet=True)
    )

    # Create accounts from private keys
    main_account = Account.from_key(main_private_key)
    agent_account = Account.from_key(agent_private_key)
    
    print(f"Main account: {main_account.address}")
    print(f"Agent account: {agent_account.address}\n")
    
    # Create exchange client with main account
    exchange = ExchangeClient(transport=transport, wallet=main_account)
    
    try:
        print("Adding agent...")
        agent_result = await exchange.add_agent(
            AddAgentParams(
                agent_name="my-trading-bot",  # Name for the agent
                agent=agent_account.address,  # Agent's Ethereum address
                for_account="",
                agent_private_key=agent_private_key,  # Agent's private key (for signing)
                signer=main_account.address,  # Signer address (usually the main account)
                valid_until=int(time.time() * 1000) + 3600000,  # Valid for 1 hour (in milliseconds)
            )
        )
        
        print(f"Agent added successfully!")
        print(f"Result: {agent_result}\n")
        
        # Optionally, verify the agent was added by checking all agents
        print("Verifying agent was added...")
        info = InfoClient(transport=transport)
        from hotstuff.methods.info.account import AgentsParams
        all_agents = await info.agents(
            AgentsParams(user=main_account.address)
        )
        print(f"All agents for account: {all_agents}\n")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        await transport.close()


if __name__ == "__main__":
    asyncio.run(main())

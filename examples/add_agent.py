"""Example: Adding an agent with ExchangeClient."""
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


def main():
    """Main example function."""
    # Get main account private key from environment or use default for testing
    main_private_key = os.getenv("PRIVATE_KEY")
    
    # Get agent private key from environment or create a new one
    agent_private_key = os.getenv("AGENT_PRIVATE_KEY")
    
    if not agent_private_key:
        # Create a new agent account if not provided
        agent_private_key = Account.create().key.hex()
        print("Note: Created a new agent account. Set AGENT_PRIVATE_KEY env var to use a specific agent.")
    
    # Validate that we have valid private keys
    if not main_private_key or not main_private_key.strip():
        print("ERROR: PRIVATE_KEY environment variable must be set or use the default")
        return
    
    if not agent_private_key or not agent_private_key.strip():
        print("ERROR: AGENT_PRIVATE_KEY is invalid")
        return
    
    # Create HTTP transport for testnet
    transport = HttpTransport(
        HttpTransportOptions(is_testnet=False)
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
        agent_result = exchange.add_agent(
            AddAgentParams(
                agent_name="my-agent",
                agent=agent_account.address,
                for_account="",
                agent_private_key=agent_private_key,
                signer=main_account.address,
                valid_until=int(time.time() * 1000) + 3600000,
            )
        )
        
        print(f"Agent added successfully!")
        print(f"Result: {agent_result}\n")
        
        # Optionally, verify the agent was added by checking all agents
        print("Verifying agent was added...")
        info = InfoClient(transport=transport)
        from hotstuff.methods.info.account import AgentsParams
        all_agents = info.agents(
            AgentsParams(user=main_account.address)
        )
        print(f"Found {len(all_agents)} agent(s) for account:")
        for agent in all_agents:
            agent_addr = agent.agent_address or 'N/A'
            agent_name = agent.agent_name or 'N/A'
            valid_until = agent.valid_until_timestamp or 'N/A'
            timestamp = agent.created_at_block_timestamp or 'N/A'
            print(f"  - Agent: {agent_addr}, Name: {agent_name}, Valid until: {valid_until}, Timestamp: {timestamp}")
        print()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        transport.close()


if __name__ == "__main__":
    main()

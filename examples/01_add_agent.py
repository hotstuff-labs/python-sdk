"""Example: Adding an agent"""
import time
import os
import json
import example_utils
from hotstuff import AddAgentParams
from eth_account import Account 


def main():
    """Main example function."""
    print("--------------------------------\nAdding Agent\n")
    _, exchange = example_utils.setup_clients(is_testnet=True, main_account=True)
    
    agent_account = Account.create()
    agent_private_key = agent_account.key.hex()
    main_account = Account.from_key(os.getenv("PRIVATE_KEY"))
    
    print(f"Main: {main_account.address}\nAgent: {agent_account.address}\nAgent Private Key: {agent_private_key}\n")

    result = exchange.add_agent(
            AddAgentParams(
                agent_name="python-sdk-demo-agent",
                agent=agent_account.address,
                for_account="",
                agent_private_key=agent_private_key,
                signer=main_account.address,
                valid_until=int(time.time() * 1000) + 3600000,
            )
        )
        
    print(f"Agent added successfully!\n\nResponse: {json.dumps(result, indent=2)}\n--------------------------------\n")
        
if __name__ == "__main__":
    main()

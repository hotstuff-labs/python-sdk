"""Example: Add Agent"""
import time
import json
from hotstuff import AddAgentParams
from examples.utils.example_utils import setup_exchange_client
from examples.utils.config import CREDENTIALS, CONFIG


def main():
    """Main example function."""
    print("--------------------------------\nAdding Agent\n")
    exchange, _, _, _ = setup_exchange_client()
    
    result = exchange.add_agent(
            AddAgentParams(
                agentName="python-sdk-demo-agent",
                agent=CONFIG["AGENT_ADDRESS"],
                forAccount="",
                agentPrivateKey=CREDENTIALS["AGENT_PRIVATE_KEY"],
                signer=CONFIG["MAIN_ACCOUNT_ADDRESS"],
                validUntil=int(time.time() * 1000) + 3600000,
            )
        )
        
    print(f"Agent added successfully!\n\nResponse: {json.dumps(result, indent=2)}\n--------------------------------\n")
        
if __name__ == "__main__":
    main()

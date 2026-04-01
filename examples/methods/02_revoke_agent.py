"""Example: Revoke Agent"""
import json
from examples.utils.example_utils import setup_exchange_client
from examples.utils.config import CONFIG
from hotstuff import RevokeAgentParams


def main():
    """Main example function."""
    print("--------------------------------\nRevoking Agent\n")
    exchange, _, _, _ = setup_exchange_client()
    
    result = exchange.revoke_agent(
            RevokeAgentParams(
                agent=CONFIG["AGENT_ADDRESS"],
                forAccount="",
            )
        )
        
    print(f"Agent revoked successfully!\n\nResponse: {json.dumps(result, indent=2)}\n--------------------------------\n")
        
if __name__ == "__main__":
    main()

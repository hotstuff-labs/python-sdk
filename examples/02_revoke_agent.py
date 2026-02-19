"""Example: Revoke Agent"""
import json
import example_utils
from hotstuff import RevokeAgentParams


def main():
    """Main example function."""
    print("--------------------------------\nRevoking Agent\n")
    _, exchange = example_utils.setup_clients(is_testnet=True, main_account=True)
    
    result = exchange.revoke_agent(
            RevokeAgentParams(
                agent="0x97C823F1915FC0b04ab15C32cBEec8ab9E2994fd",
                forAccount="",
            )
        )
        
    print(f"Agent revoked successfully!\n\nResponse: {json.dumps(result, indent=2)}\n--------------------------------\n")
        
if __name__ == "__main__":
    main()

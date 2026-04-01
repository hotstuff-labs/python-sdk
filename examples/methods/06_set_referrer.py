"""Example: Set referrer."""
import json
from examples.utils.example_utils import setup_exchange_client
from hotstuff import SetReferrerParams



def main():
    """Main example function."""
    print("--------------------------------\nSet referrer\n")
    exchange, _, _, _ = setup_exchange_client()
    
    result = exchange.set_referrer(SetReferrerParams(code="PY_SDK_DEMO_REFERRER"))
        
    print(f"Referrer set successfully!\n\nResponse: {json.dumps(result, indent=2)}\n--------------------------------\n")
        
if __name__ == "__main__":
    main()

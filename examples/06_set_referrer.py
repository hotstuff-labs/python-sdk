"""Example: Set referrer."""
import json
import example_utils
from hotstuff import SetReferrerParams



def main():
    """Main example function."""
    print("--------------------------------\nSet referrer\n")
    _, exchange = example_utils.setup_clients(is_testnet=True, main_account=False)
    
    result = exchange.set_referrer(SetReferrerParams(code="PY_SDK_DEMO_REFERRER"))
        
    print(f"Referrer set successfully!\n\nResponse: {json.dumps(result, indent=2)}\n--------------------------------\n")
        
if __name__ == "__main__":
    main()

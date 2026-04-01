"""Example: Create referral code."""
import json
from examples.utils.example_utils import setup_exchange_client
from hotstuff import CreateReferralCodeParams



def main():
    """Main example function."""
    print("--------------------------------\nCreate referral code\n")
    exchange, _, _, _ = setup_exchange_client()
    
    result = exchange.create_referral_code(CreateReferralCodeParams(code="1234567890"))
        
    print(f"Referral code created successfully!\n\nResponse: {json.dumps(result, indent=2)}\n--------------------------------\n")
        
if __name__ == "__main__":
    main()

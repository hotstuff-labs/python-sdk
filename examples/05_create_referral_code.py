"""Example: Create referral code."""
import json
import example_utils
from hotstuff import CreateReferralCodeParams



def main():
    """Main example function."""
    print("--------------------------------\nCreate referral code\n")
    _, exchange = example_utils.setup_clients(is_testnet=True, main_account=False)
    
    result = exchange.create_referral_code(CreateReferralCodeParams(code="1234567890"))
        
    print(f"Referral code created successfully!\n\nResponse: {json.dumps(result, indent=2)}\n--------------------------------\n")
        
if __name__ == "__main__":
    main()

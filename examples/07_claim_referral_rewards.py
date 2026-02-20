"""Example: Claim referral rewards."""
import json
import example_utils
from hotstuff import ClaimReferralRewardsParams



def main():
    """Main example function."""
    print("--------------------------------\nClaim referral rewards\n")
    _, exchange = example_utils.setup_clients(is_testnet=True, main_account=False)
    
    result = exchange.claim_referral_rewards(ClaimReferralRewardsParams(collateralId=1, spot=True))
        
    print(f"Referral rewards claimed successfully!\n\nResponse: {json.dumps(result, indent=2)}\n--------------------------------\n")
        
if __name__ == "__main__":
    main()

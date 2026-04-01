"""Example: Claim referral rewards."""
import json
from examples.utils.example_utils import setup_trading_client
from hotstuff import ClaimReferralRewardsParams



def main():
    """Main example function."""
    print("--------------------------------\nClaim referral rewards\n")
    exchange, _, _, _ = setup_trading_client()
    
    result = exchange.claim_referral_rewards(ClaimReferralRewardsParams(collateralId=1, spot=True))
        
    print(f"Referral rewards claimed successfully!\n\nResponse: {json.dumps(result, indent=2)}\n--------------------------------\n")
        
if __name__ == "__main__":
    main()

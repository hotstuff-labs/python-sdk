"""Account exchange method types."""
from dataclasses import dataclass
from typing import Optional

from hotstuff.utils.address import validate_ethereum_address


# Add Agent Method
@dataclass
class AddAgentParams:
    """Parameters for adding an agent."""
    agent_name: str
    agent: str
    for_account: str
    valid_until: int
    signature: Optional[str] = None
    nonce: Optional[int] = None
    agent_private_key: Optional[str] = None
    signer: Optional[str] = None
    
    def __post_init__(self):
        """Validate and checksum Ethereum addresses."""
        if self.agent:
            self.agent = validate_ethereum_address(self.agent)
        if self.signer:
            self.signer = validate_ethereum_address(self.signer)


# Revoke Agent Method
@dataclass
class RevokeAgentParams:
    """Parameters for revoking an agent."""
    agent: str
    for_account: Optional[str] = None
    nonce: Optional[int] = None
    
    def __post_init__(self):
        """Validate and checksum the agent address."""
        self.agent = validate_ethereum_address(self.agent)


# Update Perp Instrument Leverage Method
@dataclass
class UpdatePerpInstrumentLeverageParams:
    """Parameters for updating perp instrument leverage."""
    instrument_id: int
    leverage: int
    nonce: Optional[int] = None


# Approve Broker Fee Method
@dataclass
class ApproveBrokerFeeParams:
    """Parameters for approving broker fee."""
    broker: str
    max_fee_rate: str
    nonce: Optional[int] = None
    
    def __post_init__(self):
        """Validate and checksum the broker address."""
        self.broker = validate_ethereum_address(self.broker)


# Create Referral Code Method
@dataclass
class CreateReferralCodeParams:
    """Parameters for creating a referral code."""
    code: str
    nonce: Optional[int] = None


# Set Referrer Method
@dataclass
class SetReferrerParams:
    """Parameters for setting a referrer."""
    code: str
    nonce: Optional[int] = None


# Claim Referral Rewards Method
@dataclass
class ClaimReferralRewardsParams:
    """Parameters for claiming referral rewards."""
    collateral_id: int
    spot: bool
    nonce: Optional[int] = None

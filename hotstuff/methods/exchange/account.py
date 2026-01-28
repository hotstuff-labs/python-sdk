"""Account exchange method types."""
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator
from eth_utils import is_address, to_checksum_address


def validate_ethereum_address(value: str) -> str:
    """
    Validate and normalize an Ethereum address.
    
    Args:
        value: The address string to validate
        
    Returns:
        Checksummed address string
        
    Raises:
        ValueError: If the address is invalid
    """
    if not isinstance(value, str):
        raise ValueError(f"Address must be a string, got {type(value)}")
    
    if not is_address(value):
        raise ValueError(f"Invalid Ethereum address: {value}")
    
    # Return checksummed address (EIP-55)
    return to_checksum_address(value)


# Add Agent Method
class AddAgentParams(BaseModel):
    """Parameters for adding an agent."""
    agent_name: str = Field(..., alias="agentName", description="Agent name")
    agent: str = Field(..., description="Agent address")
    for_account: str = Field(..., alias="forAccount", description="Account to add agent for")
    signature: Optional[str] = Field(None, description="Agent signature")
    valid_until: int = Field(..., alias="validUntil", description="Validity expiration timestamp")
    nonce: Optional[int] = Field(None, description="Transaction nonce")
    agent_private_key: Optional[str] = Field(None, alias="agentPrivateKey", description="Agent private key")
    signer: Optional[str] = Field(None, description="Signer address")

    model_config = ConfigDict(populate_by_name=True)
    
    @field_validator('agent', 'signer', mode='before')
    @classmethod
    def validate_addresses(cls, v: Optional[str]) -> Optional[str]:
        """Validate and checksum Ethereum addresses."""
        if v is None or v == "":
            return v
        return validate_ethereum_address(v)


# Revoke Agent Method
class RevokeAgentParams(BaseModel):
    """Parameters for revoking an agent."""
    agent: str = Field(..., description="Agent address")
    for_account: Optional[str] = Field(None, alias="forAccount", description="Account to revoke agent for")
    nonce: Optional[int] = Field(None, description="Transaction nonce")

    model_config = ConfigDict(populate_by_name=True)

    @field_validator('agent', mode='before')
    @classmethod
    def validate_agent_address(cls, v: str) -> str:
        """Validate and checksum the agent address."""
        return validate_ethereum_address(v)


# Update Perp Instrument Leverage Method
class UpdatePerpInstrumentLeverageParams(BaseModel):
    """Parameters for updating perp instrument leverage."""
    instrument_id: int = Field(..., alias="instrumentId", description="Instrument ID")
    leverage: int = Field(..., description="Leverage value")
    nonce: Optional[int] = Field(None, description="Transaction nonce")

    model_config = ConfigDict(populate_by_name=True)


# Approve Broker Fee Method
class ApproveBrokerFeeParams(BaseModel):
    """Parameters for approving broker fee."""
    broker: str = Field(..., description="Broker address")
    max_fee_rate: str = Field(..., alias="maxFeeRate", description="Maximum fee rate")
    nonce: Optional[int] = Field(None, description="Transaction nonce")

    model_config = ConfigDict(populate_by_name=True)

    @field_validator('broker', mode='before')
    @classmethod
    def validate_broker_address(cls, v: str) -> str:
        """Validate and checksum the broker address."""
        return validate_ethereum_address(v)


# Create Referral Code Method
class CreateReferralCodeParams(BaseModel):
    """Parameters for creating a referral code."""
    code: str = Field(..., description="Referral code")
    nonce: Optional[int] = Field(None, description="Transaction nonce")

    model_config = ConfigDict(populate_by_name=True)


# Set Referrer Method
class SetReferrerParams(BaseModel):
    """Parameters for setting a referrer."""
    code: str = Field(..., description="Referral code")
    nonce: Optional[int] = Field(None, description="Transaction nonce")

    model_config = ConfigDict(populate_by_name=True)


# Claim Referral Rewards Method
class ClaimReferralRewardsParams(BaseModel):
    """Parameters for claiming referral rewards."""
    collateral_id: int = Field(..., alias="collateralId", description="Collateral ID")
    spot: bool = Field(..., description="Whether to claim from spot account")
    nonce: Optional[int] = Field(None, description="Transaction nonce")

    model_config = ConfigDict(populate_by_name=True)

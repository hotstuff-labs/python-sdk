"""Collateral exchange method types."""
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator

from hotstuff.utils.address import validate_ethereum_address


# Account Spot Withdraw Request Method
class AccountSpotWithdrawRequestParams(BaseModel):
    """Parameters for account spot withdraw request."""
    collateral_id: int = Field(..., alias="collateralId", description="Collateral ID")
    amount: str = Field(..., description="Withdrawal amount")
    chain_id: int = Field(..., alias="chainId", description="Chain ID")
    nonce: Optional[int] = Field(None, description="Transaction nonce")

    model_config = ConfigDict(populate_by_name=True)


# Account Derivative Withdraw Request Method
class AccountDerivativeWithdrawRequestParams(BaseModel):
    """Parameters for account derivative withdraw request."""
    collateral_id: int = Field(..., alias="collateralId", description="Collateral ID")
    amount: str = Field(..., description="Withdrawal amount")
    chain_id: int = Field(..., alias="chainId", description="Chain ID")
    nonce: Optional[int] = Field(None, description="Transaction nonce")

    model_config = ConfigDict(populate_by_name=True)


# Account Spot Balance Transfer Request Method
class AccountSpotBalanceTransferRequestParams(BaseModel):
    """Parameters for account spot balance transfer request."""
    collateral_id: int = Field(..., alias="collateralId", description="Collateral ID")
    amount: str = Field(..., description="Transfer amount")
    destination: str = Field(..., description="Destination address")
    nonce: Optional[int] = Field(None, description="Transaction nonce")

    model_config = ConfigDict(populate_by_name=True)

    @field_validator('destination', mode='before')
    @classmethod
    def validate_destination_address(cls, v: str) -> str:
        """Validate and checksum the destination address."""
        return validate_ethereum_address(v)


# Account Derivative Balance Transfer Request Method
class AccountDerivativeBalanceTransferRequestParams(BaseModel):
    """Parameters for account derivative balance transfer request."""
    collateral_id: int = Field(..., alias="collateralId", description="Collateral ID")
    amount: str = Field(..., description="Transfer amount")
    destination: str = Field(..., description="Destination address")
    nonce: Optional[int] = Field(None, description="Transaction nonce")

    model_config = ConfigDict(populate_by_name=True)

    @field_validator('destination', mode='before')
    @classmethod
    def validate_destination_address(cls, v: str) -> str:
        """Validate and checksum the destination address."""
        return validate_ethereum_address(v)


# Account Internal Balance Transfer Request Method
class AccountInternalBalanceTransferRequestParams(BaseModel):
    """Parameters for account internal balance transfer request."""
    collateral_id: int = Field(..., alias="collateralId", description="Collateral ID")
    amount: str = Field(..., description="Transfer amount")
    to_derivatives_account: bool = Field(..., alias="toDerivativesAccount", description="Transfer to derivatives account flag")
    nonce: Optional[int] = Field(None, description="Transaction nonce")

    model_config = ConfigDict(populate_by_name=True)

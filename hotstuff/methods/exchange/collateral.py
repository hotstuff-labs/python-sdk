"""Collateral exchange method types."""
from dataclasses import dataclass
from typing import Optional

from hotstuff.utils.address import validate_ethereum_address


# Account Spot Withdraw Request Method
@dataclass
class AccountSpotWithdrawRequestParams:
    """Parameters for account spot withdraw request."""
    collateralId: int
    amount: str
    chainId: int
    nonce: Optional[int] = None


# Account Derivative Withdraw Request Method
@dataclass
class AccountDerivativeWithdrawRequestParams:
    """Parameters for account derivative withdraw request."""
    collateralId: int
    amount: str
    chainId: int
    nonce: Optional[int] = None


# Account Spot Balance Transfer Request Method
@dataclass
class AccountSpotBalanceTransferRequestParams:
    """Parameters for account spot balance transfer request."""
    collateralId: int
    amount: str
    destination: str
    nonce: Optional[int] = None
    
    def __post_init__(self):
        """Validate and checksum the destination address."""
        self.destination = validate_ethereum_address(self.destination)


# Account Derivative Balance Transfer Request Method
@dataclass
class AccountDerivativeBalanceTransferRequestParams:
    """Parameters for account derivative balance transfer request."""
    collateralId: int
    amount: str
    destination: str
    nonce: Optional[int] = None
    
    def __post_init__(self):
        """Validate and checksum the destination address."""
        self.destination = validate_ethereum_address(self.destination)


# Account Internal Balance Transfer Request Method
@dataclass
class AccountInternalBalanceTransferRequestParams:
    """Parameters for account internal balance transfer request."""
    collateralId: int
    amount: str
    toDerivativesAccount: bool
    nonce: Optional[int] = None

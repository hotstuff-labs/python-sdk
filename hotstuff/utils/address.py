"""Ethereum address validation utilities."""
from typing import Annotated
from pydantic import Field, field_validator
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
    
    return to_checksum_address(value)


EthereumAddress = Annotated[
    str,
    Field(
        ...,
        description="Ethereum address (validated and checksummed)",
        examples=["0x1234567890123456789012345678901234567890"],
    ),
    field_validator('*', mode='before')(validate_ethereum_address),
]

"""Ethereum address validation utilities."""
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
    if not is_address(value):
        raise ValueError(f"Invalid Ethereum address: {value}")
    
    return to_checksum_address(value)

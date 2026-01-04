"""Signing utilities for EIP-712 typed data."""
import msgpack
from eth_account import Account
from eth_account.messages import encode_structured_data
from eth_utils import keccak


EXCHANGE_OP_CODES = {
    "placeOrder": 1,
    "cancelByOid": 2,
    "cancelByCloid": 3,
    "cancelAll": 4,
    "addAgent": 5,
}


async def sign_action(
    wallet: Account,
    action: dict,
    tx_type: int,
    is_testnet: bool = False
) -> str:
    """
    Sign an action using EIP-712.
    
    Args:
        wallet: The account to sign with
        action: The action data
        tx_type: The transaction type code
        is_testnet: Whether this is for testnet
        
    Returns:
        str: The signature
    """
    # Encode action to msgpack
    action_bytes = msgpack.packb(action)
    
    # Hash the payload
    payload_hash = keccak(action_bytes)
    
    # EIP-712 domain
    domain = {
        "name": "HotstuffCore",
        "version": "1",
        "chainId": 1,
        "verifyingContract": "0x1234567890123456789012345678901234567890",
    }
    
    # EIP-712 types
    types = {
        "EIP712Domain": [
            {"name": "name", "type": "string"},
            {"name": "version", "type": "string"},
            {"name": "chainId", "type": "uint256"},
            {"name": "verifyingContract", "type": "address"},
        ],
        "Action": [
            {"name": "source", "type": "string"},
            {"name": "hash", "type": "bytes32"},
            {"name": "txType", "type": "uint16"},
        ],
    }
    
    # Message
    message = {
        "source": "Testnet" if is_testnet else "Mainnet",
        "hash": payload_hash,
        "txType": tx_type,
    }
    
    # Create structured data
    structured_data = {
        "types": types,
        "primaryType": "Action",
        "domain": domain,
        "message": message,
    }
    
    # Encode and sign
    encoded_data = encode_structured_data(structured_data)
    signed_message = wallet.sign_message(encoded_data)
    
    return signed_message.signature.hex()


"""Signing utilities for EIP-712 typed data."""
import msgpack
from eth_account import Account
from eth_utils import keccak
from hotstuff.methods.exchange.op_codes import EXCHANGE_OP_CODES


def sign_action(
    wallet: Account,
    action: dict,
    tx_type: int,
    is_testnet: bool = False
) -> str:
    """
    Sign an action using EIP-712.
    
    This is a synchronous function that generates an EIP-712 signature
    for the given action data.
    
    Args:
        wallet: The account to sign with
        action: The action data
        tx_type: The transaction type code
        is_testnet: Whether this is for testnet
        
    Returns:
        str: The signature (hex string)
    """
    # Canonicalize key order so msgpack bytes match backend (deterministic signing)
    canonical_action = canonicalize_for_signing(action)
    # Encode action to msgpack
    action_bytes = msgpack.packb(canonical_action)
    
    # Hash the payload
    payload_hash = keccak(action_bytes)
    
    # EIP-712 domain
    domain = {
        "name": "HotstuffCore",
        "version": "1",
        "chainId": 1,
        "verifyingContract": "0x1234567890123456789012345678901234567890",
    }
    
    # EIP-712 message types (without EIP712Domain for new API)
    message_types = {
        "Action": [
            {"name": "source", "type": "string"},
            {"name": "hash", "type": "bytes32"},
            {"name": "txType", "type": "uint16"},
        ],
    }
    
    # Message data
    message = {
        "source": "Testnet" if is_testnet else "Mainnet",
        "hash": payload_hash,
        "txType": tx_type,
    }
    
    if _USE_NEW_API:
        # New API (eth-account >= 0.9): use 3-argument form
        encoded_data = encode_typed_data(
            domain_data=domain,
            message_types=message_types,
            message_data=message,
        )
    else:
        # Legacy API (eth-account < 0.9): use full_message form
        # Include EIP712Domain in types for legacy API
        types_with_domain = {
            "EIP712Domain": [
                {"name": "name", "type": "string"},
                {"name": "version", "type": "string"},
                {"name": "chainId", "type": "uint256"},
                {"name": "verifyingContract", "type": "address"},
            ],
            **message_types,
        }
        structured_data = {
            "types": types_with_domain,
            "primaryType": "Action",
            "domain": domain,
            "message": message,
        }
        encoded_data = encode_structured_data(structured_data)
    
    signed_message = wallet.sign_message(encoded_data)
    
    return signed_message.signature.hex()


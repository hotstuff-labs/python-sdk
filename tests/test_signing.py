"""Test signing and canonicalization."""
import msgpack
import pytest
from hotstuff.utils.signing import canonicalize_for_signing, sign_action
from eth_account import Account


class TestCanonicalizeForSigning:
    """Test canonical key ordering for deterministic msgpack."""

    def test_canonicalize_sorts_top_level_keys(self):
        """Different key order produces same canonical dict."""
        a = {"cancels": [{"oid": 1, "instrumentId": 2}], "expiresAfter": 1000, "nonce": 99}
        b = {"nonce": 99, "cancels": [{"oid": 1, "instrumentId": 2}], "expiresAfter": 1000}
        ca = canonicalize_for_signing(a)
        cb = canonicalize_for_signing(b)
        assert ca == cb
        assert list(ca.keys()) == ["cancels", "expiresAfter", "nonce"]
        assert list(ca["cancels"][0].keys()) == ["instrumentId", "oid"]

    def test_canonicalize_produces_deterministic_msgpack(self):
        """Same logical payload with different key order -> same msgpack bytes."""
        payload1 = {"cancels": [{"oid": 123, "instrumentId": 1}], "expiresAfter": 1769692246080, "nonce": 1769688646080}
        payload2 = {"nonce": 1769688646080, "expiresAfter": 1769692246080, "cancels": [{"instrumentId": 1, "oid": 123}]}
        bytes1 = msgpack.packb(canonicalize_for_signing(payload1))
        bytes2 = msgpack.packb(canonicalize_for_signing(payload2))
        assert bytes1 == bytes2

    def test_sign_action_deterministic(self):
        """Same payload with different key order -> same signature."""
        wallet = Account.create()
        params1 = {"cancels": [{"oid": 1, "instrumentId": 1}], "expiresAfter": 1769692246080, "nonce": 1769688646080}
        params2 = {"nonce": 1769688646080, "expiresAfter": 1769692246080, "cancels": [{"instrumentId": 1, "oid": 1}]}
        sig1 = sign_action(wallet=wallet, action=params1, tx_type=1302, is_testnet=True)
        sig2 = sign_action(wallet=wallet, action=params2, tx_type=1302, is_testnet=True)
        assert sig1 == sig2

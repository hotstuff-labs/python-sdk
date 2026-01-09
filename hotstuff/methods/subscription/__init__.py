"""Subscription method types."""
import importlib

GlobalSubscriptionMethods = importlib.import_module("hotstuff.methods.subscription.global")

__all__ = [
    "GlobalSubscriptionMethods",
]

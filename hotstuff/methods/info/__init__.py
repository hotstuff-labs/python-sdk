"""Info method types organized by category."""
import importlib

GlobalInfoMethods = importlib.import_module("hotstuff.methods.info.global")
AccountInfoMethods = importlib.import_module("hotstuff.methods.info.account")
VaultInfoMethods = importlib.import_module("hotstuff.methods.info.vault")
ExplorerInfoMethods = importlib.import_module("hotstuff.methods.info.explorer")

__all__ = [
    "GlobalInfoMethods",
    "AccountInfoMethods",
    "VaultInfoMethods",
    "ExplorerInfoMethods",
]

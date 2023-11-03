"""Initializes the octoai module."""
from importlib.metadata import version

from . import clients, errors, types, utils

__version__ = version("octoai-sdk")
__all__ = ["clients", "client", "errors", "server", "service", "types", "utils"]

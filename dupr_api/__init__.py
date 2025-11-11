"""
DUPR API Client
A Python client library for interacting with the DUPR (Dynamic Universal Pickleball Rating) API.
"""

from .client import DUPRClient
from .exceptions import (
    DUPRAPIError,
    AuthenticationError,
    ValidationError,
    NotFoundError,
    RateLimitError,
)

__version__ = "0.1.1"
__all__ = [
    "DUPRClient",
    "DUPRAPIError",
    "AuthenticationError",
    "ValidationError",
    "NotFoundError",
    "RateLimitError",
]

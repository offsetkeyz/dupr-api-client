"""Base API class for all endpoint implementations."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import DUPRClient


class BaseAPI:
    """Base class for all API endpoint implementations."""

    def __init__(self, client: "DUPRClient"):
        self.client = client
        self.version = client.version

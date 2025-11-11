"""
Exception classes for DUPR API client.
"""


class DUPRAPIError(Exception):
    """Base exception for all DUPR API errors."""

    def __init__(self, message, status_code=None, response=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response = response


class AuthenticationError(DUPRAPIError):
    """Raised when authentication fails."""
    pass


class ValidationError(DUPRAPIError):
    """Raised when request validation fails."""
    pass


class NotFoundError(DUPRAPIError):
    """Raised when a resource is not found (404)."""
    pass


class RateLimitError(DUPRAPIError):
    """Raised when API rate limit is exceeded."""
    pass


class ServerError(DUPRAPIError):
    """Raised when server returns 5xx error."""
    pass

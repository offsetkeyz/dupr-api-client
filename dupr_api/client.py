"""
Main DUPR API client implementation.
"""

import requests
from typing import Optional, Dict, Any
from .exceptions import (
    DUPRAPIError,
    AuthenticationError,
    ValidationError,
    NotFoundError,
    RateLimitError,
    ServerError,
)
from .api.user import UserAPI
from .api.matches import MatchesAPI
from .api.clubs import ClubsAPI
from .api.events import EventsAPI
from .api.brackets import BracketsAPI
from .api.admin import AdminAPI
from .api.players import PlayersAPI


class DUPRClient:
    """
    Main client for interacting with the DUPR API.

    Args:
        bearer_token: Optional bearer token for authentication
        base_url: Base URL for the API (default: https://backend.mydupr.com)
        version: API version (default: v1.0)
        timeout: Request timeout in seconds (default: 30)

    Example:
        >>> client = DUPRClient(bearer_token="your_token")
        >>> profile = client.user.get_profile()
        >>> matches = client.matches.search(player_id=12345)
    """

    def __init__(
        self,
        bearer_token: Optional[str] = None,
        base_url: str = "https://backend.mydupr.com",
        version: str = "v1.0",
        timeout: int = 30,
    ):
        self.bearer_token = bearer_token
        self.base_url = base_url.rstrip("/")
        self.version = version
        self.timeout = timeout
        self.session = requests.Session()

        # Initialize API namespaces
        self.user = UserAPI(self)
        self.matches = MatchesAPI(self)
        self.clubs = ClubsAPI(self)
        self.events = EventsAPI(self)
        self.brackets = BracketsAPI(self)
        self.admin = AdminAPI(self)
        self.players = PlayersAPI(self)

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers including authentication."""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if self.bearer_token:
            headers["Authorization"] = f"Bearer {self.bearer_token}"
        return headers

    def _make_request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to the DUPR API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            path: API endpoint path
            params: Query parameters
            json_data: JSON request body
            files: Files for multipart upload
            **kwargs: Additional arguments to pass to requests

        Returns:
            Response data as dictionary

        Raises:
            AuthenticationError: If authentication fails (401)
            ValidationError: If request validation fails (400)
            NotFoundError: If resource not found (404)
            RateLimitError: If rate limit exceeded (429)
            ServerError: If server error occurs (5xx)
            DUPRAPIError: For other API errors
        """
        url = f"{self.base_url}{path}"
        headers = self._get_headers()

        # Remove Content-Type for file uploads
        if files:
            headers.pop("Content-Type", None)

        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=json_data,
                files=files,
                timeout=self.timeout,
                **kwargs,
            )

            # Handle different status codes
            if response.status_code == 401:
                raise AuthenticationError(
                    "Authentication failed. Please check your bearer token.",
                    status_code=401,
                    response=response,
                )
            elif response.status_code == 400:
                raise ValidationError(
                    f"Validation error: {response.text}",
                    status_code=400,
                    response=response,
                )
            elif response.status_code == 404:
                raise NotFoundError(
                    f"Resource not found: {url}",
                    status_code=404,
                    response=response,
                )
            elif response.status_code == 429:
                raise RateLimitError(
                    "Rate limit exceeded. Please try again later.",
                    status_code=429,
                    response=response,
                )
            elif response.status_code >= 500:
                raise ServerError(
                    f"Server error: {response.status_code}",
                    status_code=response.status_code,
                    response=response,
                )
            elif response.status_code >= 400:
                raise DUPRAPIError(
                    f"API error: {response.status_code} - {response.text}",
                    status_code=response.status_code,
                    response=response,
                )

            # Parse JSON response
            if response.content:
                return response.json()
            return {}

        except requests.exceptions.Timeout:
            raise DUPRAPIError(f"Request timeout after {self.timeout} seconds")
        except requests.exceptions.ConnectionError as e:
            raise DUPRAPIError(f"Connection error: {str(e)}")
        except requests.exceptions.RequestException as e:
            raise DUPRAPIError(f"Request error: {str(e)}")

    def get(self, path: str, **kwargs) -> Dict[str, Any]:
        """Make a GET request."""
        return self._make_request("GET", path, **kwargs)

    def post(self, path: str, **kwargs) -> Dict[str, Any]:
        """Make a POST request."""
        return self._make_request("POST", path, **kwargs)

    def put(self, path: str, **kwargs) -> Dict[str, Any]:
        """Make a PUT request."""
        return self._make_request("PUT", path, **kwargs)

    def delete(self, path: str, **kwargs) -> Dict[str, Any]:
        """Make a DELETE request."""
        return self._make_request("DELETE", path, **kwargs)

    def set_bearer_token(self, token: str):
        """Set or update the bearer token for authentication."""
        self.bearer_token = token

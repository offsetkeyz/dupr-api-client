"""Unit tests for DUPRClient."""

import pytest
import requests
from unittest.mock import Mock, patch, MagicMock
from dupr_api import DUPRClient
from dupr_api.exceptions import (
    AuthenticationError,
    ValidationError,
    NotFoundError,
    RateLimitError,
    ServerError,
    DUPRAPIError,
)


class TestDUPRClient:
    """Test suite for DUPRClient class."""

    def test_client_initialization(self):
        """Test client initialization with default parameters."""
        client = DUPRClient(bearer_token="test_token")

        assert client.bearer_token == "test_token"
        assert client.base_url == "https://backend.mydupr.com"
        assert client.version == "v1.0"
        assert client.timeout == 30
        assert isinstance(client.session, requests.Session)

    def test_client_custom_parameters(self):
        """Test client initialization with custom parameters."""
        client = DUPRClient(
            bearer_token="custom_token",
            base_url="https://custom.api.com",
            version="v2.0",
            timeout=60,
        )

        assert client.bearer_token == "custom_token"
        assert client.base_url == "https://custom.api.com"
        assert client.version == "v2.0"
        assert client.timeout == 60

    def test_get_headers_with_token(self):
        """Test header generation with bearer token."""
        client = DUPRClient(bearer_token="test_token")
        headers = client._get_headers()

        assert headers["Authorization"] == "Bearer test_token"
        assert headers["Content-Type"] == "application/json"
        assert headers["Accept"] == "application/json"

    def test_get_headers_without_token(self):
        """Test header generation without bearer token."""
        client = DUPRClient()
        headers = client._get_headers()

        assert "Authorization" not in headers
        assert headers["Content-Type"] == "application/json"
        assert headers["Accept"] == "application/json"

    def test_set_bearer_token(self):
        """Test updating bearer token."""
        client = DUPRClient()
        assert client.bearer_token is None

        client.set_bearer_token("new_token")
        assert client.bearer_token == "new_token"

    @patch("dupr_api.client.requests.Session.request")
    def test_successful_get_request(self, mock_request):
        """Test successful GET request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": "success"}
        mock_response.content = b'{"result": "success"}'
        mock_request.return_value = mock_response

        client = DUPRClient(bearer_token="test_token")
        result = client.get("/test/endpoint")

        assert result == {"result": "success"}
        mock_request.assert_called_once()

    @patch("dupr_api.client.requests.Session.request")
    def test_successful_post_request(self, mock_request):
        """Test successful POST request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": "created"}
        mock_response.content = b'{"result": "created"}'
        mock_request.return_value = mock_response

        client = DUPRClient(bearer_token="test_token")
        result = client.post("/test/endpoint", json_data={"key": "value"})

        assert result == {"result": "created"}

    @patch("dupr_api.client.requests.Session.request")
    def test_authentication_error_401(self, mock_request):
        """Test 401 authentication error handling."""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_request.return_value = mock_response

        client = DUPRClient(bearer_token="invalid_token")

        with pytest.raises(AuthenticationError) as exc_info:
            client.get("/test/endpoint")

        assert exc_info.value.status_code == 401

    @patch("dupr_api.client.requests.Session.request")
    def test_validation_error_400(self, mock_request):
        """Test 400 validation error handling."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        mock_request.return_value = mock_response

        client = DUPRClient(bearer_token="test_token")

        with pytest.raises(ValidationError) as exc_info:
            client.post("/test/endpoint", json_data={"invalid": "data"})

        assert exc_info.value.status_code == 400

    @patch("dupr_api.client.requests.Session.request")
    def test_not_found_error_404(self, mock_request):
        """Test 404 not found error handling."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_request.return_value = mock_response

        client = DUPRClient(bearer_token="test_token")

        with pytest.raises(NotFoundError) as exc_info:
            client.get("/test/nonexistent")

        assert exc_info.value.status_code == 404

    @patch("dupr_api.client.requests.Session.request")
    def test_rate_limit_error_429(self, mock_request):
        """Test 429 rate limit error handling."""
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.text = "Too Many Requests"
        mock_request.return_value = mock_response

        client = DUPRClient(bearer_token="test_token")

        with pytest.raises(RateLimitError) as exc_info:
            client.get("/test/endpoint")

        assert exc_info.value.status_code == 429

    @patch("dupr_api.client.requests.Session.request")
    def test_server_error_500(self, mock_request):
        """Test 500 server error handling."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_request.return_value = mock_response

        client = DUPRClient(bearer_token="test_token")

        with pytest.raises(ServerError) as exc_info:
            client.get("/test/endpoint")

        assert exc_info.value.status_code == 500

    @patch("dupr_api.client.requests.Session.request")
    def test_connection_error(self, mock_request):
        """Test connection error handling."""
        mock_request.side_effect = requests.exceptions.ConnectionError("Connection failed")

        client = DUPRClient(bearer_token="test_token")

        with pytest.raises(DUPRAPIError) as exc_info:
            client.get("/test/endpoint")

        assert "Connection error" in str(exc_info.value)

    @patch("dupr_api.client.requests.Session.request")
    def test_timeout_error(self, mock_request):
        """Test timeout error handling."""
        mock_request.side_effect = requests.exceptions.Timeout("Request timeout")

        client = DUPRClient(bearer_token="test_token", timeout=5)

        with pytest.raises(DUPRAPIError) as exc_info:
            client.get("/test/endpoint")

        assert "timeout" in str(exc_info.value).lower()

    @patch("dupr_api.client.requests.Session.request")
    def test_empty_response(self, mock_request):
        """Test handling of empty response."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b""
        mock_request.return_value = mock_response

        client = DUPRClient(bearer_token="test_token")
        result = client.get("/test/endpoint")

        assert result == {}

    def test_api_namespaces_initialized(self):
        """Test that all API namespaces are properly initialized."""
        client = DUPRClient(bearer_token="test_token")

        assert client.user is not None
        assert client.matches is not None
        assert client.clubs is not None
        assert client.events is not None
        assert client.brackets is not None
        assert client.admin is not None
        assert client.players is not None

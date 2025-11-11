"""Unit tests for User API."""

import pytest
from unittest.mock import Mock, patch
from dupr_api import DUPRClient


class TestUserAPI:
    """Test suite for User API endpoints."""

    @pytest.fixture
    def client(self):
        """Create a test client."""
        return DUPRClient(bearer_token="test_token")

    @patch("dupr_api.client.requests.Session.request")
    def test_get_profile(self, mock_request, client):
        """Test getting user profile."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": {
                "userId": 12345,
                "fullName": "John Doe",
                "email": "john@example.com"
            }
        }
        mock_response.content = b'{"result": {}}'
        mock_request.return_value = mock_response

        result = client.user.get_profile()

        assert "result" in result
        assert result["result"]["userId"] == 12345
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"] == "https://backend.mydupr.com/user/v1.0/profile"
        assert kwargs["method"] == "GET"

    @patch("dupr_api.client.requests.Session.request")
    def test_update_profile(self, mock_request, client):
        """Test updating user profile."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": {
                "fullName": "John Updated"
            }
        }
        mock_response.content = b'{"result": {}}'
        mock_request.return_value = mock_response

        profile_data = {"fullName": "John Updated"}
        result = client.user.update_profile(profile_data)

        assert "result" in result
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"] == "https://backend.mydupr.com/user/v1.0/profile"
        assert kwargs["method"] == "PUT"
        assert kwargs["json"] == profile_data

    @patch("dupr_api.client.requests.Session.request")
    def test_get_settings(self, mock_request, client):
        """Test getting user settings."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": {
                "emailNotifications": True,
                "privacyMode": "public"
            }
        }
        mock_response.content = b'{"result": {}}'
        mock_request.return_value = mock_response

        result = client.user.get_settings()

        assert "result" in result
        mock_request.assert_called_once()

    @patch("dupr_api.client.requests.Session.request")
    def test_update_settings(self, mock_request, client):
        """Test updating user settings."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True}
        mock_response.content = b'{"success": true}'
        mock_request.return_value = mock_response

        settings = {"emailNotifications": False}
        result = client.user.update_settings(settings)

        assert result["success"] is True
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["json"] == settings

    @patch("dupr_api.client.requests.Session.request")
    def test_update_preferences(self, mock_request, client):
        """Test updating user preferences."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True}
        mock_response.content = b'{"success": true}'
        mock_request.return_value = mock_response

        preferences = {"preferredFormat": "doubles"}
        result = client.user.update_preferences(preferences)

        assert result["success"] is True
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["url"] == "https://backend.mydupr.com/user/v1.0/preferences"

    @patch("dupr_api.client.requests.Session.request")
    def test_get_activities(self, mock_request, client):
        """Test getting user activities."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": [
                {"activityType": "match", "timestamp": "2024-01-01T00:00:00Z"}
            ]
        }
        mock_response.content = b'{"result": []}'
        mock_request.return_value = mock_response

        result = client.user.get_activities(player_id=12345, limit=10)

        assert "result" in result
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert "12345" in kwargs["url"]
        assert kwargs["params"]["limit"] == 10

    @patch("dupr_api.client.requests.Session.request")
    def test_custom_version(self, mock_request, client):
        """Test using custom API version."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": {}}
        mock_response.content = b'{"result": {}}'
        mock_request.return_value = mock_response

        result = client.user.get_profile(version="v2.0")

        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert "v2.0" in kwargs["url"]

"""Unit tests for Matches API."""

import pytest
from unittest.mock import Mock, patch
from dupr_api import DUPRClient


class TestMatchesAPI:
    """Test suite for Matches API endpoints."""

    @pytest.fixture
    def client(self):
        """Create a test client."""
        return DUPRClient(bearer_token="test_token")

    @patch("dupr_api.client.requests.Session.request")
    def test_save_match(self, mock_request, client):
        """Test saving a new match."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": 12345}
        mock_response.content = b'{"result": 12345}'
        mock_request.return_value = mock_response

        match_data = {
            "format": "singles",
            "team1": [{"playerId": 123}],
            "team2": [{"playerId": 456}],
            "scores": [{"team1": 11, "team2": 5}]
        }
        result = client.matches.save_match(match_data)

        assert result["result"] == 12345
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["method"] == "PUT"
        assert kwargs["json"] == match_data
        assert "/match/v1.0/save" in kwargs["url"]

    @patch("dupr_api.client.requests.Session.request")
    def test_get_match(self, mock_request, client):
        """Test getting match details."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": {
                "matchId": 789,
                "format": "doubles",
                "status": "COMPLETED"
            }
        }
        mock_response.content = b'{"result": {}}'
        mock_request.return_value = mock_response

        result = client.matches.get_match(match_id=789)

        assert result["result"]["matchId"] == 789
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert "789" in kwargs["url"]

    @patch("dupr_api.client.requests.Session.request")
    def test_search_matches(self, mock_request, client):
        """Test searching for matches."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": [
                {"matchId": 1, "format": "singles"},
                {"matchId": 2, "format": "doubles"}
            ]
        }
        mock_response.content = b'{"result": []}'
        mock_request.return_value = mock_response

        result = client.matches.search_matches(
            player_id=12345,
            limit=10,
            offset=0
        )

        assert len(result["result"]) == 2
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["method"] == "POST"
        assert kwargs["json"]["playerId"] == 12345
        assert kwargs["json"]["limit"] == 10

    @patch("dupr_api.client.requests.Session.request")
    def test_search_matches_with_filters(self, mock_request, client):
        """Test searching matches with multiple filters."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": []}
        mock_response.content = b'{"result": []}'
        mock_request.return_value = mock_response

        result = client.matches.search_matches(
            player_id=12345,
            club_id=100,
            event_id=500,
            limit=20
        )

        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        json_data = kwargs["json"]
        assert json_data["playerId"] == 12345
        assert json_data["clubId"] == 100
        assert json_data["eventId"] == 500

    @patch("dupr_api.client.requests.Session.request")
    def test_update_match(self, mock_request, client):
        """Test updating a match."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": {"matchId": 789, "updated": True}
        }
        mock_response.content = b'{"result": {}}'
        mock_request.return_value = mock_response

        match_data = {
            "matchId": 789,
            "scores": [{"team1": 11, "team2": 8}]
        }
        result = client.matches.update_match(match_data)

        assert result["result"]["updated"] is True
        mock_request.assert_called_once()

    @patch("dupr_api.client.requests.Session.request")
    def test_save_verified_match(self, mock_request, client):
        """Test saving a verified match."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True}
        mock_response.content = b'{"success": true}'
        mock_request.return_value = mock_response

        match_data = {
            "format": "doubles",
            "verificationSource": "tournament"
        }
        result = client.matches.save_verified_match(match_data)

        assert result["success"] is True
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert "/match/verified/v1.0/save" in kwargs["url"]

    @patch("dupr_api.client.requests.Session.request")
    def test_delete_match(self, mock_request, client):
        """Test deleting a match."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True}
        mock_response.content = b'{"success": true}'
        mock_request.return_value = mock_response

        result = client.matches.delete_match(match_id=789)

        assert result["success"] is True
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["method"] == "DELETE"
        assert "789" in kwargs["url"]

    @patch("dupr_api.client.requests.Session.request")
    def test_get_match_rating_impact(self, mock_request, client):
        """Test getting match rating impact simulation."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": {
                "team1Impact": 0.05,
                "team2Impact": -0.05
            }
        }
        mock_response.content = b'{"result": {}}'
        mock_request.return_value = mock_response

        match_data = {
            "team1": [{"playerId": 123, "rating": 4.5}],
            "team2": [{"playerId": 456, "rating": 4.2}]
        }
        result = client.matches.get_match_rating_impact(match_data)

        assert "result" in result
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert "/match/v1.0/rating-simulator" in kwargs["url"]

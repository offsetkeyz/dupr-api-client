"""Integration tests with API mocking."""

import pytest
import responses
from dupr_api import DUPRClient
from dupr_api.exceptions import AuthenticationError, NotFoundError


class TestIntegration:
    """Integration tests with mocked API responses."""

    @pytest.fixture
    def client(self):
        """Create a test client."""
        return DUPRClient(bearer_token="test_token")

    @responses.activate
    def test_complete_user_workflow(self, client):
        """Test a complete user workflow: get profile, update, get again."""
        base_url = "https://backend.mydupr.com"

        # Mock initial profile fetch
        responses.add(
            responses.GET,
            f"{base_url}/user/v1.0/profile",
            json={
                "result": {
                    "userId": 12345,
                    "fullName": "John Doe",
                    "rating": 4.5
                }
            },
            status=200,
        )

        # Mock profile update
        responses.add(
            responses.PUT,
            f"{base_url}/user/v1.0/profile",
            json={
                "result": {
                    "userId": 12345,
                    "fullName": "John Updated",
                    "rating": 4.5
                }
            },
            status=200,
        )

        # Mock second profile fetch
        responses.add(
            responses.GET,
            f"{base_url}/user/v1.0/profile",
            json={
                "result": {
                    "userId": 12345,
                    "fullName": "John Updated",
                    "rating": 4.5
                }
            },
            status=200,
        )

        # Execute workflow
        profile = client.user.get_profile()
        assert profile["result"]["fullName"] == "John Doe"

        updated = client.user.update_profile({"fullName": "John Updated"})
        assert updated["result"]["fullName"] == "John Updated"

        profile_after = client.user.get_profile()
        assert profile_after["result"]["fullName"] == "John Updated"

    @responses.activate
    def test_match_creation_and_retrieval(self, client):
        """Test match creation and retrieval workflow."""
        base_url = "https://backend.mydupr.com"

        # Mock match creation
        responses.add(
            responses.PUT,
            f"{base_url}/match/v1.0/save",
            json={"result": 99999},
            status=200,
        )

        # Mock match retrieval
        responses.add(
            responses.GET,
            f"{base_url}/match/v1.0/99999",
            json={
                "result": {
                    "matchId": 99999,
                    "format": "singles",
                    "status": "COMPLETED",
                    "team1": [{"playerId": 123}],
                    "team2": [{"playerId": 456}]
                }
            },
            status=200,
        )

        # Create match
        match_data = {
            "format": "singles",
            "team1": [{"playerId": 123}],
            "team2": [{"playerId": 456}],
            "scores": [{"team1": 11, "team2": 5}]
        }
        created = client.matches.save_match(match_data)
        match_id = created["result"]
        assert match_id == 99999

        # Retrieve match
        match = client.matches.get_match(match_id)
        assert match["result"]["matchId"] == 99999
        assert match["result"]["format"] == "singles"

    @responses.activate
    def test_player_search_and_details(self, client):
        """Test player search and getting player details."""
        base_url = "https://backend.mydupr.com"

        # Mock player search
        responses.add(
            responses.POST,
            f"{base_url}/player/v1.0/search",
            json={
                "result": [
                    {"playerId": 12345, "fullName": "John Doe", "rating": 4.5}
                ]
            },
            status=200,
        )

        # Mock player details
        responses.add(
            responses.GET,
            f"{base_url}/player/v1.0/12345",
            json={
                "result": {
                    "playerId": 12345,
                    "fullName": "John Doe",
                    "rating": 4.5,
                    "matchCount": 100
                }
            },
            status=200,
        )

        # Search for player
        search_results = client.players.search_players(query="John Doe")
        assert len(search_results["result"]) == 1
        player_id = search_results["result"][0]["playerId"]

        # Get player details
        player = client.players.get_player(player_id)
        assert player["result"]["playerId"] == 12345
        assert player["result"]["matchCount"] == 100

    @responses.activate
    def test_club_membership_workflow(self, client):
        """Test club membership workflow."""
        base_url = "https://backend.mydupr.com"

        # Mock club search
        responses.add(
            responses.POST,
            f"{base_url}/club/v1.0/search",
            json={
                "result": [
                    {"clubId": 100, "name": "Downtown Pickleball"}
                ]
            },
            status=200,
        )

        # Mock join request
        responses.add(
            responses.PUT,
            f"{base_url}/club/100/members/v1.0/join",
            json={"success": True},
            status=200,
        )

        # Mock get club members
        responses.add(
            responses.GET,
            f"{base_url}/club/v1.0/100/members",
            json={
                "result": [
                    {"userId": 12345, "role": "PLAYER"},
                    {"userId": 67890, "role": "DIRECTOR"}
                ]
            },
            status=200,
        )

        # Search for club
        clubs = client.clubs.search_clubs(query="Downtown")
        club_id = clubs["result"][0]["clubId"]

        # Join club
        join_result = client.clubs.join_club(club_id)
        assert join_result["success"] is True

        # Get club members
        members = client.clubs.get_club_members(club_id)
        assert len(members["result"]) == 2

    @responses.activate
    def test_authentication_failure(self, client):
        """Test handling of authentication failure."""
        base_url = "https://backend.mydupr.com"

        responses.add(
            responses.GET,
            f"{base_url}/user/v1.0/profile",
            json={"error": "Unauthorized"},
            status=401,
        )

        with pytest.raises(AuthenticationError):
            client.user.get_profile()

    @responses.activate
    def test_resource_not_found(self, client):
        """Test handling of 404 errors."""
        base_url = "https://backend.mydupr.com"

        responses.add(
            responses.GET,
            f"{base_url}/match/v1.0/99999",
            json={"error": "Match not found"},
            status=404,
        )

        with pytest.raises(NotFoundError):
            client.matches.get_match(99999)

    @responses.activate
    def test_pagination_workflow(self, client):
        """Test pagination with multiple requests."""
        base_url = "https://backend.mydupr.com"

        # Mock first page
        responses.add(
            responses.POST,
            f"{base_url}/match/v1.0/search",
            json={
                "result": [{"matchId": i} for i in range(20)]
            },
            status=200,
        )

        # Mock second page
        responses.add(
            responses.POST,
            f"{base_url}/match/v1.0/search",
            json={
                "result": [{"matchId": i} for i in range(20, 40)]
            },
            status=200,
        )

        # Fetch first page
        page1 = client.matches.search_matches(player_id=12345, limit=20, offset=0)
        assert len(page1["result"]) == 20
        assert page1["result"][0]["matchId"] == 0

        # Fetch second page
        page2 = client.matches.search_matches(player_id=12345, limit=20, offset=20)
        assert len(page2["result"]) == 20
        assert page2["result"][0]["matchId"] == 20

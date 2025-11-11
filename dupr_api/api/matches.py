"""Matches API endpoints."""

from typing import Dict, Any, Optional, List
from .base import BaseAPI


class MatchesAPI(BaseAPI):
    """
    Match-related API endpoints.

    Handles match creation, updates, searches, and verification.
    """

    def save_match(
        self, match_data: Dict[str, Any], version: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Save a new match.

        Args:
            match_data: Match details including players, scores, format, etc.
            version: API version (default: client version)

        Returns:
            Match ID in response

        Example:
            >>> match = client.matches.save_match({
            ...     "format": "singles",
            ...     "team1": [{"playerId": 123}],
            ...     "team2": [{"playerId": 456}],
            ...     "scores": [{"team1": 11, "team2": 5}]
            ... })
        """
        version = version or self.version
        return self.client.put(f"/match/{version}/save", json_data=match_data)

    def update_match(
        self, match_data: Dict[str, Any], version: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update an existing match.

        Args:
            match_data: Match data with match ID and updated fields
            version: API version (default: client version)

        Returns:
            Updated match response

        Example:
            >>> updated = client.matches.update_match({
            ...     "matchId": 789,
            ...     "scores": [{"team1": 11, "team2": 8}]
            ... })
        """
        version = version or self.version
        return self.client.put(
            f"/admin/{version}/panel/match/{version}/update", json_data=match_data
        )

    def get_match(
        self, match_id: int, version: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get match details by ID.

        Args:
            match_id: Match ID
            version: API version (default: client version)

        Returns:
            Match details

        Example:
            >>> match = client.matches.get_match(match_id=789)
        """
        version = version or self.version
        return self.client.get(f"/match/{version}/{match_id}")

    def search_matches(
        self,
        player_id: Optional[int] = None,
        club_id: Optional[int] = None,
        event_id: Optional[int] = None,
        limit: int = 20,
        offset: int = 0,
        version: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Search for matches with various filters.

        Args:
            player_id: Filter by player ID
            club_id: Filter by club ID
            event_id: Filter by event ID
            limit: Number of results to return
            offset: Pagination offset
            version: API version (default: client version)

        Returns:
            List of matches

        Example:
            >>> matches = client.matches.search_matches(player_id=12345, limit=10)
        """
        version = version or self.version
        search_data = {"limit": limit, "offset": offset}

        if player_id:
            search_data["playerId"] = player_id
        if club_id:
            search_data["clubId"] = club_id
        if event_id:
            search_data["eventId"] = event_id

        return self.client.post(f"/match/{version}/search", json_data=search_data)

    def save_verified_match(
        self, match_data: Dict[str, Any], version: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Save a verified match (requires verification privileges).

        Args:
            match_data: Verified match details
            version: API version (default: client version)

        Returns:
            Response wrapper

        Example:
            >>> verified = client.matches.save_verified_match({
            ...     "format": "doubles",
            ...     "verificationSource": "tournament",
            ...     "teams": [...]
            ... })
        """
        version = version or self.version
        return self.client.put(
            f"/match/verified/{version}/save", json_data=match_data
        )

    def delete_match(
        self, match_id: int, version: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Delete a match.

        Args:
            match_id: Match ID to delete
            version: API version (default: client version)

        Returns:
            Response wrapper

        Example:
            >>> client.matches.delete_match(match_id=789)
        """
        version = version or self.version
        return self.client.delete(f"/match/{version}/{match_id}")

    def get_match_rating_impact(
        self, match_data: Dict[str, Any], version: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Simulate rating impact before saving a match.

        Args:
            match_data: Match data to simulate
            version: API version (default: client version)

        Returns:
            Expected rating changes for each player

        Example:
            >>> impact = client.matches.get_match_rating_impact({
            ...     "team1": [{"playerId": 123, "rating": 4.5}],
            ...     "team2": [{"playerId": 456, "rating": 4.2}]
            ... })
        """
        version = version or self.version
        return self.client.post(
            f"/match/{version}/rating-simulator", json_data=match_data
        )

    def get_unauthenticated_history(
        self,
        player_id: int,
        limit: int = 10,
        offset: int = 0,
        version: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get public match history for a player without authentication.

        Args:
            player_id: Player ID
            limit: Number of matches to return (max 10 per request)
            offset: Pagination offset
            version: API version (default: client version)

        Returns:
            List of player's matches

        Example:
            >>> history = client.matches.get_unauthenticated_history(
            ...     player_id=12345,
            ...     limit=10
            ... )
        """
        version = version or self.version
        # API has strict limits - max 10 per request
        if limit > 10:
            limit = 10

        params = {'limit': limit, 'offset': offset}
        return self.client.get(
            f"/match/{version}/history/unauthenticated/{player_id}", params=params
        )

    def get_match_details(
        self, match_id: int, version: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get full match details by match ID.

        Args:
            match_id: Match ID
            version: API version (not used for this endpoint)

        Returns:
            Complete match details

        Example:
            >>> match = client.matches.get_match_details(match_id=789)
        """
        return self.client.get(f"/match/{match_id}")

    def get_pending_matches(self, version: Optional[str] = None) -> Dict[str, Any]:
        """
        Get pending matches (requiring confirmation).

        Args:
            version: API version (default: client version)

        Returns:
            List of pending matches

        Example:
            >>> pending = client.matches.get_pending_matches()
        """
        version = version or self.version
        return self.client.get(f"/match/{version}/pending")

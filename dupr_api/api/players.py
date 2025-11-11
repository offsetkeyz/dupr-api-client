"""Players API endpoints."""

from typing import Dict, Any, Optional, List
from .base import BaseAPI


class PlayersAPI(BaseAPI):
    """
    Player search and information endpoints.

    Handles player searches, ratings, and claims.
    """

    def search_players(
        self,
        query: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
        include_unclaimed: bool = True,
        version: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Search for players.

        Args:
            query: Search query (player name)
            limit: Number of results to return (max 25)
            offset: Pagination offset
            include_unclaimed: Include unclaimed player profiles
            version: API version (default: client version)

        Returns:
            List of matching players

        Example:
            >>> players = client.players.search_players(
            ...     query="John Doe",
            ...     limit=10
            ... )
        """
        version = version or self.version

        # DUPR API has max limit of 25 for search
        if limit > 25:
            limit = 25

        search_data = {
            "query": query or "",
            "limit": limit,
            "offset": offset,
            "includeUnclaimedPlayers": include_unclaimed,
            "filter": {}  # Empty filter, using query instead
        }

        return self.client.post(f"/player/{version}/search", json_data=search_data)

    def get_player(self, player_id: int, version: Optional[str] = None) -> Dict[str, Any]:
        """
        Get player information by ID.

        Args:
            player_id: Player ID
            version: API version (default: client version)

        Returns:
            Player details including rating, history, etc.

        Example:
            >>> player = client.players.get_player(player_id=12345)
            >>> print(player['result']['rating'])
        """
        version = version or self.version
        return self.client.get(f"/player/{version}/{player_id}")

    def get_player_rating_history(
        self,
        player_id: int,
        match_type: Optional[str] = None,
        format_type: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        sort_by: str = "desc",
        version: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get player's rating history over time.

        Args:
            player_id: Player ID
            match_type: "SINGLES" or "DOUBLES" (preferred parameter name)
            format_type: Alias for match_type (deprecated, use match_type)
            limit: Maximum number of rating entries
            offset: Pagination offset
            start_date: Start date in YYYY-MM-DD format (optional)
            end_date: End date in YYYY-MM-DD format (optional)
            sort_by: Sort order "asc" or "desc"
            version: API version (default: client version)

        Returns:
            Rating history with dates and values

        Example:
            >>> history = client.players.get_player_rating_history(
            ...     player_id=12345,
            ...     match_type="DOUBLES",
            ...     limit=50
            ... )
        """
        version = version or self.version

        # Support both match_type and format_type (backward compatibility)
        rating_type = match_type or format_type or "DOUBLES"

        data = {
            'type': rating_type,
            'limit': limit,
            'offset': offset,
            'sortBy': sort_by
        }

        if start_date:
            data['startDate'] = start_date

        if end_date:
            data['endDate'] = end_date

        return self.client.post(
            f"/player/{version}/{player_id}/rating-history", json_data=data
        )

    def get_player_matches(
        self,
        player_id: int,
        limit: int = 20,
        offset: int = 0,
        version: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get matches for a specific player.

        Args:
            player_id: Player ID
            limit: Number of matches to return
            offset: Pagination offset
            version: API version (default: client version)

        Returns:
            List of player's matches

        Example:
            >>> matches = client.players.get_player_matches(player_id=12345, limit=10)
        """
        version = version or self.version
        params = {"limit": limit, "offset": offset}
        return self.client.get(f"/player/{version}/{player_id}/matches", params=params)

    def get_player_history(
        self,
        player_id: int,
        limit: int = 10,
        offset: int = 0,
        version: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get player's match history.

        Args:
            player_id: Player ID
            limit: Number of history items to return
            offset: Pagination offset
            version: API version (default: client version)

        Returns:
            Player's match history

        Example:
            >>> history = client.players.get_player_history(player_id=12345, limit=10)
        """
        version = version or self.version
        data = {"limit": limit, "offset": offset}
        return self.client.post(f"/player/{version}/{player_id}/history", json_data=data)

    def claim_player(
        self, player_id: int, claim_data: Dict[str, Any], version: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Claim an unclaimed player profile.

        Args:
            player_id: Player ID to claim
            claim_data: Claim verification data
            version: API version (default: client version)

        Returns:
            Response wrapper

        Example:
            >>> client.players.claim_player(
            ...     player_id=12345,
            ...     claim_data={"verificationMethod": "email", "code": "123456"}
            ... )
        """
        version = version or self.version
        return self.client.post(
            f"/player/{version}/{player_id}/claim", json_data=claim_data
        )

    def get_expected_score(
        self,
        team1_players: List[int],
        team2_players: List[int],
        version: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Calculate expected match score based on player IDs.

        Args:
            team1_players: List of player IDs for team 1
            team2_players: List of player IDs for team 2
            version: API version (default: client version)

        Returns:
            Expected score and win probability

        Example:
            >>> expected = client.players.get_expected_score(
            ...     team1_players=[12345],
            ...     team2_players=[67890]
            ... )
        """
        version = version or self.version
        data = {
            "team1": team1_players,
            "team2": team2_players,
        }
        return self.client.post(f"/match/{version}/expected-score", json_data=data)

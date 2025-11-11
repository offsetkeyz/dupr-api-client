"""Brackets API endpoints."""

from typing import Dict, Any, Optional
from .base import BaseAPI


class BracketsAPI(BaseAPI):
    """
    Tournament brackets API endpoints.

    Handles bracket creation, seeding, and tournament management.
    """

    def save_bracket(
        self, bracket_data: Dict[str, Any], version: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new tournament bracket.

        Args:
            bracket_data: Bracket configuration (format, seeding, participants, etc.)
            version: API version (default: client version)

        Returns:
            Created bracket response

        Example:
            >>> bracket = client.brackets.save_bracket({
            ...     "name": "Championship Bracket",
            ...     "format": "single_elimination",
            ...     "participants": [...]
            ... })
        """
        version = version or self.version
        return self.client.put(f"/brackets/{version}/save", json_data=bracket_data)

    def edit_bracket(
        self, bracket_data: Dict[str, Any], version: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Edit an existing bracket.

        Args:
            bracket_data: Updated bracket data with bracket ID
            version: API version (default: client version)

        Returns:
            Updated bracket response

        Example:
            >>> updated = client.brackets.edit_bracket({
            ...     "bracketId": 300,
            ...     "name": "Championship Bracket - Final"
            ... })
        """
        version = version or self.version
        return self.client.put(f"/brackets/{version}/edit", json_data=bracket_data)

    def get_bracket(
        self, bracket_id: int, version: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get bracket details.

        Args:
            bracket_id: Bracket ID
            version: API version (default: client version)

        Returns:
            Bracket details including matches and standings

        Example:
            >>> bracket = client.brackets.get_bracket(bracket_id=300)
        """
        version = version or self.version
        return self.client.get(f"/brackets/{version}/{bracket_id}")

    def update_bracket_status(
        self,
        league_id: int,
        bracket_id: int,
        club_id: int,
        status: str,
        version: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Update bracket status.

        Args:
            league_id: League ID
            bracket_id: Bracket ID
            club_id: Club ID
            status: New status (ACTIVE, INACTIVE, IN_PROGRESS, COMPLETE, etc.)
            version: API version (default: client version)

        Returns:
            Response wrapper

        Example:
            >>> client.brackets.update_bracket_status(
            ...     league_id=500,
            ...     bracket_id=300,
            ...     club_id=100,
            ...     status="IN_PROGRESS"
            ... )
        """
        version = version or self.version
        params = {
            "leagueId": league_id,
            "bracketId": bracket_id,
            "clubId": club_id,
            "status": status,
        }
        return self.client.put(
            f"/brackets/director/{version}/edit/bracket_status", params=params
        )

    def get_bracket_matches(
        self,
        bracket_id: int,
        limit: int = 50,
        offset: int = 0,
        version: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get matches in a bracket.

        Args:
            bracket_id: Bracket ID
            limit: Number of matches to return
            offset: Pagination offset
            version: API version (default: client version)

        Returns:
            List of bracket matches

        Example:
            >>> matches = client.brackets.get_bracket_matches(bracket_id=300)
        """
        version = version or self.version
        params = {"limit": limit, "offset": offset}
        return self.client.get(
            f"/brackets/{version}/{bracket_id}/matches", params=params
        )

    def seed_bracket(
        self,
        bracket_id: int,
        seeding_data: Dict[str, Any],
        version: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Seed a tournament bracket.

        Args:
            bracket_id: Bracket ID
            seeding_data: Seeding configuration and player placements
            version: API version (default: client version)

        Returns:
            Seeded bracket response

        Example:
            >>> client.brackets.seed_bracket(
            ...     bracket_id=300,
            ...     seeding_data={"seedingMethod": "rating", "participants": [...]}
            ... )
        """
        version = version or self.version
        return self.client.post(
            f"/brackets/{version}/{bracket_id}/seed", json_data=seeding_data
        )

"""Clubs API endpoints."""

from typing import Dict, Any, Optional, BinaryIO
from .base import BaseAPI


class ClubsAPI(BaseAPI):
    """
    Club-related API endpoints.

    Handles club management, membership, and club matches.
    """

    def add_club(
        self, club_data: Dict[str, Any], version: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new club.

        Args:
            club_data: Club information (name, location, description, etc.)
            version: API version (default: client version)

        Returns:
            Response wrapper

        Example:
            >>> club = client.clubs.add_club({
            ...     "name": "Downtown Pickleball Club",
            ...     "location": "New York, NY",
            ...     "description": "Premier pickleball facility"
            ... })
        """
        version = version or self.version
        return self.client.put(f"/club/{version}/add", json_data=club_data)

    def get_club(self, club_id: int, version: Optional[str] = None) -> Dict[str, Any]:
        """
        Get club information.

        Args:
            club_id: Club ID
            version: API version (default: client version)

        Returns:
            Club details

        Example:
            >>> club = client.clubs.get_club(club_id=100)
        """
        version = version or self.version
        return self.client.get(f"/club/{version}/{club_id}")

    def search_clubs(
        self,
        query: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
        version: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Search for clubs.

        Args:
            query: Search query (filter string)
            limit: Number of results to return
            offset: Pagination offset
            version: API version (default: client version)

        Returns:
            List of matching clubs

        Example:
            >>> clubs = client.clubs.search_clubs(query="New York")
        """
        version = version or self.version
        search_data = {"limit": limit, "offset": offset}
        if query:
            search_data["filter"] = query

        return self.client.post(f"/club/{version}/all", json_data=search_data)

    def add_member(
        self,
        club_id: int,
        member_data: Dict[str, Any],
        version: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Add a member to a club (admin).

        Args:
            club_id: Club ID
            member_data: Member information
            version: API version (default: client version)

        Returns:
            Response wrapper

        Example:
            >>> client.clubs.add_member(
            ...     club_id=100,
            ...     member_data={"userId": 12345, "role": "PLAYER"}
            ... )
        """
        version = version or self.version
        return self.client.put(
            f"/club/{club_id}/members/{version}/add", json_data=member_data
        )

    def add_members_bulk(
        self,
        club_id: int,
        members_data: Dict[str, Any],
        version: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Add multiple members to a club (admin).

        Args:
            club_id: Club ID
            members_data: List of members to add
            version: API version (default: client version)

        Returns:
            Response with added members

        Example:
            >>> client.clubs.add_members_bulk(
            ...     club_id=100,
            ...     members_data={"members": [{"userId": 123}, {"userId": 456}]}
            ... )
        """
        version = version or self.version
        return self.client.put(
            f"/club/{club_id}/members/{version}/multiple/add", json_data=members_data
        )

    def join_club(
        self, club_id: int, version: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Request to join a club.

        Args:
            club_id: Club ID
            version: API version (default: client version)

        Returns:
            Response wrapper

        Example:
            >>> client.clubs.join_club(club_id=100)
        """
        version = version or self.version
        return self.client.put(f"/club/{club_id}/members/{version}/join")

    def invite_member(
        self,
        club_id: int,
        invite_data: Dict[str, Any],
        version: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Invite a member to a club.

        Args:
            club_id: Club ID
            invite_data: Invitation details (email, userId, etc.)
            version: API version (default: client version)

        Returns:
            Invitation response

        Example:
            >>> client.clubs.invite_member(
            ...     club_id=100,
            ...     invite_data={"email": "player@example.com"}
            ... )
        """
        version = version or self.version
        return self.client.put(
            f"/club/{club_id}/members/{version}/invite", json_data=invite_data
        )

    def get_club_members(
        self,
        club_id: int,
        limit: int = 50,
        offset: int = 0,
        version: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get club members.

        Args:
            club_id: Club ID
            limit: Number of members to return
            offset: Pagination offset
            version: API version (default: client version)

        Returns:
            List of club members

        Example:
            >>> members = client.clubs.get_club_members(club_id=100)
        """
        version = version or self.version
        params = {"limit": limit, "offset": offset}
        return self.client.get(f"/club/{version}/{club_id}/members", params=params)

    def get_staff_members(
        self, club_id: int, version: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get club staff members.

        Args:
            club_id: Club ID
            version: API version (default: client version)

        Returns:
            Staff members list

        Example:
            >>> staff = client.clubs.get_staff_members(club_id=100)
        """
        version = version or self.version
        return self.client.get(f"/club/{club_id}/members/{version}/staff")

    def update_staff_members(
        self,
        club_id: int,
        staff_data: Dict[str, Any],
        version: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Update club staff members.

        Args:
            club_id: Club ID
            staff_data: Staff member updates
            version: API version (default: client version)

        Returns:
            Response wrapper

        Example:
            >>> client.clubs.update_staff_members(
            ...     club_id=100,
            ...     staff_data={"staff": [{"userId": 123, "role": "DIRECTOR"}]}
            ... )
        """
        version = version or self.version
        return self.client.put(
            f"/club/{club_id}/members/{version}/staff", json_data=staff_data
        )

    def save_club_match(
        self,
        club_id: int,
        match_data: Dict[str, Any],
        version: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Save a match for a club.

        Args:
            club_id: Club ID
            match_data: Match details
            version: API version (default: client version)

        Returns:
            Match response

        Example:
            >>> match = client.clubs.save_club_match(
            ...     club_id=100,
            ...     match_data={"format": "doubles", "teams": [...]}
            ... )
        """
        version = version or self.version
        return self.client.put(
            f"/club/{club_id}/match/{version}/save", json_data=match_data
        )

    def get_club_matches(
        self,
        club_id: int,
        limit: int = 20,
        offset: int = 0,
        version: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get matches for a club.

        Args:
            club_id: Club ID
            limit: Number of matches to return
            offset: Pagination offset
            version: API version (default: client version)

        Returns:
            List of club matches

        Example:
            >>> matches = client.clubs.get_club_matches(club_id=100)
        """
        version = version or self.version
        params = {"limit": limit, "offset": offset}
        return self.client.get(f"/club/{version}/{club_id}/matches", params=params)

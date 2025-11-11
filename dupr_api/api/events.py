"""Events and Leagues API endpoints."""

from typing import Dict, Any, Optional
from .base import BaseAPI


class EventsAPI(BaseAPI):
    """
    Events and leagues API endpoints.

    Handles event/league creation, registration, and management.
    """

    def create_league(
        self, league_data: Dict[str, Any], version: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new league/event.

        Args:
            league_data: League details (name, dates, format, etc.)
            version: API version (default: client version)

        Returns:
            Created league response

        Example:
            >>> league = client.events.create_league({
            ...     "name": "Summer League 2024",
            ...     "startDate": "2024-06-01",
            ...     "endDate": "2024-08-31",
            ...     "format": "doubles"
            ... })
        """
        version = version or self.version
        return self.client.post(f"/event/{version}/save", json_data=league_data)

    def edit_league(
        self, league_data: Dict[str, Any], version: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Edit an existing league/event.

        Args:
            league_data: Updated league data with league ID
            version: API version (default: client version)

        Returns:
            Updated league response

        Example:
            >>> updated = client.events.edit_league({
            ...     "leagueId": 500,
            ...     "name": "Summer League 2024 - Updated"
            ... })
        """
        version = version or self.version
        return self.client.put(f"/event/{version}/edit", json_data=league_data)

    def get_event(self, event_id: int, version: Optional[str] = None) -> Dict[str, Any]:
        """
        Get event/league details.

        Args:
            event_id: Event ID
            version: API version (default: client version)

        Returns:
            Event details

        Example:
            >>> event = client.events.get_event(event_id=500)
        """
        version = version or self.version
        return self.client.get(f"/event/{version}/{event_id}")

    def search_events(
        self,
        query: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
        version: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Search for events/leagues.

        Args:
            query: Search query
            limit: Number of results to return
            offset: Pagination offset
            version: API version (default: client version)

        Returns:
            List of matching events

        Example:
            >>> events = client.events.search_events(query="Summer League")
        """
        version = version or self.version
        search_data = {"limit": limit, "offset": offset}
        if query:
            search_data["query"] = query

        return self.client.post(f"/event/{version}/search", json_data=search_data)

    def register_for_event(
        self,
        event_id: int,
        registration_data: Dict[str, Any],
        version: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Register for an event.

        Args:
            event_id: Event ID
            registration_data: Registration details
            version: API version (default: client version)

        Returns:
            Registration response

        Example:
            >>> client.events.register_for_event(
            ...     event_id=500,
            ...     registration_data={"format": "doubles", "partnerId": 12345}
            ... )
        """
        version = version or self.version
        return self.client.post(
            f"/event/{version}/{event_id}/register", json_data=registration_data
        )

    def get_event_participants(
        self,
        event_id: int,
        limit: int = 50,
        offset: int = 0,
        version: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get event participants.

        Args:
            event_id: Event ID
            limit: Number of participants to return
            offset: Pagination offset
            version: API version (default: client version)

        Returns:
            List of participants

        Example:
            >>> participants = client.events.get_event_participants(event_id=500)
        """
        version = version or self.version
        params = {"limit": limit, "offset": offset}
        return self.client.get(
            f"/event/{version}/{event_id}/participants", params=params
        )

    def update_open_play(
        self,
        open_play_id: int,
        update_data: Dict[str, Any],
        version: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Update an open play event.

        Args:
            open_play_id: Open play ID
            update_data: Updated details
            version: API version (default: client version)

        Returns:
            Response wrapper

        Example:
            >>> client.events.update_open_play(
            ...     open_play_id=200,
            ...     update_data={"maxParticipants": 20}
            ... )
        """
        version = version or self.version
        return self.client.put(
            f"/event/{version}/open-play/{open_play_id}/{version}/update",
            json_data=update_data,
        )

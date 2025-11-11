"""User API endpoints."""

from typing import Dict, Any, Optional
from .base import BaseAPI


class UserAPI(BaseAPI):
    """
    User-related API endpoints.

    Handles user profile, settings, and preferences management.
    """

    def get_profile(self, version: Optional[str] = None) -> Dict[str, Any]:
        """
        Get the current user's profile.

        Args:
            version: API version (default: client version)

        Returns:
            User profile data

        Example:
            >>> profile = client.user.get_profile()
            >>> print(profile['result']['fullName'])
        """
        version = version or self.version
        return self.client.get(f"/user/{version}/profile")

    def update_profile(
        self, profile_data: Dict[str, Any], version: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update the current user's profile.

        Args:
            profile_data: Profile data to update
            version: API version (default: client version)

        Returns:
            Updated user profile

        Example:
            >>> updated = client.user.update_profile({
            ...     "fullName": "John Doe",
            ...     "location": "New York, NY"
            ... })
        """
        version = version or self.version
        return self.client.put(f"/user/{version}/profile", json_data=profile_data)

    def get_settings(self, version: Optional[str] = None) -> Dict[str, Any]:
        """
        Get user settings.

        Args:
            version: API version (default: client version)

        Returns:
            User settings as dictionary

        Example:
            >>> settings = client.user.get_settings()
        """
        version = version or self.version
        return self.client.get(f"/user/{version}/settings")

    def update_settings(
        self, settings: Dict[str, Any], version: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update user settings.

        Args:
            settings: Settings to update
            version: API version (default: client version)

        Returns:
            Response wrapper

        Example:
            >>> client.user.update_settings({
            ...     "emailNotifications": True,
            ...     "privacyMode": "public"
            ... })
        """
        version = version or self.version
        return self.client.put(f"/user/{version}/settings", json_data=settings)

    def update_preferences(
        self, preferences: Dict[str, Any], version: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update user preferences.

        Args:
            preferences: Preferences to update
            version: API version (default: client version)

        Returns:
            Response wrapper

        Example:
            >>> client.user.update_preferences({
            ...     "preferredFormat": "singles",
            ...     "skillLevel": "intermediate"
            ... })
        """
        version = version or self.version
        return self.client.put(f"/user/{version}/preferences", json_data=preferences)

    def get_activities(
        self,
        player_id: int,
        limit: int = 20,
        offset: int = 0,
        version: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get user activities/newsfeed.

        Args:
            player_id: Player ID
            limit: Number of activities to return
            offset: Pagination offset
            version: API version (default: client version)

        Returns:
            List of activities

        Example:
            >>> activities = client.user.get_activities(player_id=12345)
        """
        version = version or self.version
        params = {"limit": limit, "offset": offset}
        return self.client.get(
            f"/player/{version}/{player_id}/activities", params=params
        )

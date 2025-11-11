"""Admin API endpoints."""

from typing import Dict, Any, Optional
from .base import BaseAPI


class AdminAPI(BaseAPI):
    """
    Admin API endpoints.

    Handles administrative functions like user management, ratings updates,
    and system operations. Requires admin privileges.
    """

    def get_user_profile(
        self, user_id: int, version: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get user profile (admin).

        Args:
            user_id: User ID
            version: API version (default: client version)

        Returns:
            User profile data

        Example:
            >>> profile = client.admin.get_user_profile(user_id=12345)
        """
        version = version or self.version
        params = {"userId": user_id}
        return self.client.get(f"/admin/{version}/panel/user/profile", params=params)

    def update_user_profile(
        self,
        user_id: int,
        profile_data: Dict[str, Any],
        version: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Update user profile (admin).

        Args:
            user_id: User ID
            profile_data: Profile data to update
            version: API version (default: client version)

        Returns:
            Updated user profile

        Example:
            >>> client.admin.update_user_profile(
            ...     user_id=12345,
            ...     profile_data={"fullName": "John Doe Updated"}
            ... )
        """
        version = version or self.version
        params = {"userId": user_id}
        return self.client.put(
            f"/admin/{version}/panel/user/profile",
            params=params,
            json_data=profile_data,
        )

    def signup_user(
        self, signup_data: Dict[str, Any], version: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new user account (admin).

        Args:
            signup_data: User registration data
            version: API version (default: client version)

        Returns:
            Created user token

        Example:
            >>> client.admin.signup_user({
            ...     "email": "newuser@example.com",
            ...     "fullName": "New User",
            ...     "password": "securepass123"
            ... })
        """
        version = version or self.version
        return self.client.put(
            f"/admin/{version}/panel/user/signup", json_data=signup_data
        )

    def delete_user(
        self, user_identifier: str, version: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Delete a user account (admin).

        Args:
            user_identifier: User email or ID
            version: API version (default: client version)

        Returns:
            Response wrapper

        Example:
            >>> client.admin.delete_user(user_identifier="user@example.com")
        """
        version = version or self.version
        params = {"request": user_identifier}
        return self.client.put(f"/admin/{version}/panel/user/delete", params=params)

    def update_player_rating(
        self,
        player_id: int,
        rating_data: Dict[str, Any],
        version: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Update a player's rating (admin).

        Args:
            player_id: Player ID
            rating_data: Rating update data (singles/doubles ratings)
            version: API version (default: client version)

        Returns:
            Response wrapper

        Example:
            >>> client.admin.update_player_rating(
            ...     player_id=12345,
            ...     rating_data={"singlesRating": 4.5, "doublesRating": 4.7}
            ... )
        """
        version = version or self.version
        return self.client.put(
            f"/admin/{version}/rating/{player_id}", json_data=rating_data
        )

    def batch_update_ratings(
        self, ratings_data: Dict[str, Any], version: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Batch update player ratings (admin).

        Args:
            ratings_data: Batch ratings update data
            version: API version (default: client version)

        Returns:
            Response wrapper

        Example:
            >>> client.admin.batch_update_ratings({
            ...     "updates": [
            ...         {"playerId": 123, "singlesRating": 4.5},
            ...         {"playerId": 456, "doublesRating": 4.2}
            ...     ]
            ... })
        """
        version = version or self.version
        return self.client.put(
            f"/admin/{version}/rating/batch", json_data=ratings_data
        )

    def get_club_settings(
        self, club_id: int, version: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get club settings (admin).

        Args:
            club_id: Club ID
            version: API version (default: client version)

        Returns:
            Club settings including auto-approve and invite limits

        Example:
            >>> settings = client.admin.get_club_settings(club_id=100)
        """
        version = version or self.version
        request_data = {"clubId": club_id}
        return self.client.post(
            f"/admin/{version}/clubs/settings", json_data=request_data
        )

    def set_club_settings(
        self,
        club_id: int,
        settings_data: Dict[str, Any],
        version: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Set club settings (admin).

        Args:
            club_id: Club ID
            settings_data: Settings to update (autoApproveJoinRequests, maxOutstandingWebInvites)
            version: API version (default: client version)

        Returns:
            Response wrapper

        Example:
            >>> client.admin.set_club_settings(
            ...     club_id=100,
            ...     settings_data={
            ...         "clubId": 100,
            ...         "autoApproveJoinRequests": True,
            ...         "maxOutstandingWebInvites": 50
            ...     }
            ... )
        """
        version = version or self.version
        settings_data["clubId"] = club_id
        return self.client.put(
            f"/admin/{version}/clubs/settings", json_data=settings_data
        )

    def get_club_restrictions(
        self, club_id: int, version: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get club restrictions (admin).

        Args:
            club_id: Club ID
            version: API version (default: client version)

        Returns:
            Club restrictions

        Example:
            >>> restrictions = client.admin.get_club_restrictions(club_id=100)
        """
        version = version or self.version
        request_data = {"clubId": club_id}
        return self.client.post(
            f"/admin/{version}/clubs/restrictions", json_data=request_data
        )

    def set_club_restrictions(
        self,
        club_id: int,
        restrictions_data: Dict[str, Any],
        version: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Set club restrictions (admin).

        Args:
            club_id: Club ID
            restrictions_data: Restrictions to set
            version: API version (default: client version)

        Returns:
            Response wrapper

        Example:
            >>> client.admin.set_club_restrictions(
            ...     club_id=100,
            ...     restrictions_data={"clubId": 100, "restrictions": [...]}
            ... )
        """
        version = version or self.version
        restrictions_data["clubId"] = club_id
        return self.client.put(
            f"/admin/{version}/clubs/restrictions", json_data=restrictions_data
        )

    def change_email(
        self, email_change_data: Dict[str, Any], version: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Change user email (admin).

        Args:
            email_change_data: Email change request (userId, newEmail)
            version: API version (default: client version)

        Returns:
            Response wrapper

        Example:
            >>> client.admin.change_email({
            ...     "userId": 12345,
            ...     "newEmail": "newemail@example.com"
            ... })
        """
        version = version or self.version
        return self.client.put(
            f"/admin/{version}/panel/email/change", json_data=email_change_data
        )

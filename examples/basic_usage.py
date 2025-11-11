"""
Basic usage examples for DUPR API client.
"""

from dupr_api import DUPRClient
from dupr_api.exceptions import AuthenticationError, DUPRAPIError

def main():
    """Demonstrate basic client usage."""

    # Initialize the client with your bearer token
    # In production, store your token securely (e.g., environment variable)
    bearer_token = "your_bearer_token_here"
    client = DUPRClient(bearer_token=bearer_token)

    try:
        # Get user profile
        print("Fetching user profile...")
        profile = client.user.get_profile()
        user_data = profile['result']
        print(f"User: {user_data.get('fullName', 'N/A')}")
        print(f"Email: {user_data.get('email', 'N/A')}")
        print(f"User ID: {user_data.get('userId', 'N/A')}")

        # Get user settings
        print("\nFetching user settings...")
        settings = client.user.get_settings()
        print(f"Settings: {settings['result']}")

        # Search for players
        print("\nSearching for players...")
        players = client.players.search_players(
            query="John",
            limit=5
        )
        print(f"Found {len(players.get('result', []))} players")
        for player in players.get('result', [])[:3]:
            print(f"  - {player.get('fullName')} (Rating: {player.get('rating', 'N/A')})")

    except AuthenticationError:
        print("Authentication failed. Please check your bearer token.")
    except DUPRAPIError as e:
        print(f"API Error: {e.message}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")


if __name__ == "__main__":
    main()

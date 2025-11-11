"""
Match management examples for DUPR API client.
"""

from dupr_api import DUPRClient
from dupr_api.exceptions import DUPRAPIError


def create_singles_match(client):
    """Create a singles match."""
    print("Creating a singles match...")

    match_data = {
        "format": "singles",
        "team1": [{"playerId": 12345}],
        "team2": [{"playerId": 67890}],
        "scores": [
            {"team1": 11, "team2": 5},
            {"team1": 11, "team2": 8}
        ],
        "matchDate": "2024-01-15",
        "location": "Downtown Courts"
    }

    try:
        result = client.matches.save_match(match_data)
        match_id = result['result']
        print(f"Match created successfully! Match ID: {match_id}")
        return match_id
    except DUPRAPIError as e:
        print(f"Error creating match: {e.message}")
        return None


def create_doubles_match(client):
    """Create a doubles match."""
    print("\nCreating a doubles match...")

    match_data = {
        "format": "doubles",
        "team1": [
            {"playerId": 12345},
            {"playerId": 12346}
        ],
        "team2": [
            {"playerId": 67890},
            {"playerId": 67891}
        ],
        "scores": [
            {"team1": 11, "team2": 9}
        ],
        "matchDate": "2024-01-15"
    }

    try:
        result = client.matches.save_match(match_data)
        match_id = result['result']
        print(f"Doubles match created successfully! Match ID: {match_id}")
        return match_id
    except DUPRAPIError as e:
        print(f"Error creating match: {e.message}")
        return None


def get_match_details(client, match_id):
    """Retrieve match details."""
    print(f"\nFetching match details for ID {match_id}...")

    try:
        match = client.matches.get_match(match_id)
        match_data = match['result']
        print(f"Match Format: {match_data.get('format', 'N/A')}")
        print(f"Status: {match_data.get('status', 'N/A')}")
        print(f"Date: {match_data.get('matchDate', 'N/A')}")
        return match_data
    except DUPRAPIError as e:
        print(f"Error fetching match: {e.message}")
        return None


def search_player_matches(client, player_id):
    """Search for a player's matches."""
    print(f"\nSearching matches for player {player_id}...")

    try:
        matches = client.matches.search_matches(
            player_id=player_id,
            limit=10,
            offset=0
        )
        match_list = matches.get('result', [])
        print(f"Found {len(match_list)} matches")

        for match in match_list[:5]:
            print(f"  Match ID: {match.get('matchId')}, "
                  f"Format: {match.get('format')}, "
                  f"Date: {match.get('matchDate', 'N/A')}")

        return match_list
    except DUPRAPIError as e:
        print(f"Error searching matches: {e.message}")
        return []


def simulate_rating_impact(client):
    """Simulate the rating impact of a potential match."""
    print("\nSimulating rating impact...")

    match_data = {
        "team1": [{"playerId": 12345, "rating": 4.5}],
        "team2": [{"playerId": 67890, "rating": 4.2}],
        "format": "singles"
    }

    try:
        impact = client.matches.get_match_rating_impact(match_data)
        print(f"Expected rating changes: {impact.get('result', {})}")
        return impact
    except DUPRAPIError as e:
        print(f"Error simulating rating impact: {e.message}")
        return None


def main():
    """Run match management examples."""
    bearer_token = "your_bearer_token_here"
    client = DUPRClient(bearer_token=bearer_token)

    # Create matches
    singles_match_id = create_singles_match(client)
    doubles_match_id = create_doubles_match(client)

    # Get match details
    if singles_match_id:
        get_match_details(client, singles_match_id)

    # Search player matches
    search_player_matches(client, player_id=12345)

    # Simulate rating impact
    simulate_rating_impact(client)


if __name__ == "__main__":
    main()

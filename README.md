# DUPR API Client

A comprehensive, fully-tested Python client library for interacting with the DUPR (Dynamic Universal Pickleball Rating) API.

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Features

- **Complete API Coverage**: All major DUPR API endpoints including users, matches, clubs, events, brackets, players, and admin functions
- **Type Hints**: Full type annotations for better IDE support and code clarity
- **Error Handling**: Comprehensive exception handling with specific error types
- **Authentication**: Simple bearer token authentication
- **Testing**: Extensive unit and integration test suite
- **Documentation**: Detailed docstrings and usage examples

## Installation

```bash
pip install dupr-api-client
```

Or install from source:

```bash
git clone https://github.com/offsetkeyz/dupr-api-client.git
cd dupr-api-client
pip install -e .
```

## Quick Start

```python
from dupr_api import DUPRClient

# Initialize the client with your bearer token
client = DUPRClient(bearer_token="your_bearer_token_here")

# Get your user profile
profile = client.user.get_profile()
print(f"User: {profile['result']['fullName']}")

# Search for players
players = client.players.search_players(query="John Doe")
for player in players['result']:
    print(f"{player['fullName']} - Rating: {player['rating']}")

# Save a match
match_data = {
    "format": "singles",
    "team1": [{"playerId": 123}],
    "team2": [{"playerId": 456}],
    "scores": [{"team1": 11, "team2": 5}]
}
match_id = client.matches.save_match(match_data)
print(f"Match saved with ID: {match_id['result']}")
```

## API Modules

The client is organized into logical modules:

### User API (`client.user`)
Manage user profiles, settings, and preferences.

```python
# Get profile
profile = client.user.get_profile()

# Update profile
client.user.update_profile({"fullName": "New Name"})

# Update settings
client.user.update_settings({"emailNotifications": True})

# Get user activities
activities = client.user.get_activities(player_id=12345)
```

### Matches API (`client.matches`)
Create, update, search, and manage matches.

```python
# Save a match
match = client.matches.save_match({
    "format": "doubles",
    "team1": [{"playerId": 123}, {"playerId": 124}],
    "team2": [{"playerId": 456}, {"playerId": 457}],
    "scores": [{"team1": 11, "team2": 9}]
})

# Search matches
matches = client.matches.search_matches(player_id=12345, limit=10)

# Get match details
match = client.matches.get_match(match_id=789)

# Get rating impact simulation
impact = client.matches.get_match_rating_impact(match_data)
```

### Players API (`client.players`)
Search for players and retrieve player information.

```python
# Search players
players = client.players.search_players(
    query="John Doe",
    filter_by={"minRating": 4.0, "maxRating": 5.0}
)

# Get player details
player = client.players.get_player(player_id=12345)

# Get rating history
history = client.players.get_player_rating_history(
    player_id=12345,
    format_type="doubles"
)

# Get player matches
matches = client.players.get_player_matches(player_id=12345)

# Get expected score
expected = client.players.get_expected_score(
    team1_ratings=[4.5],
    team2_ratings=[4.2],
    format_type="singles"
)
```

### Clubs API (`client.clubs`)
Manage clubs, memberships, and club matches.

```python
# Search clubs
clubs = client.clubs.search_clubs(query="New York")

# Get club details
club = client.clubs.get_club(club_id=100)

# Join a club
client.clubs.join_club(club_id=100)

# Get club members
members = client.clubs.get_club_members(club_id=100)

# Save a club match
match = client.clubs.save_club_match(
    club_id=100,
    match_data={"format": "doubles", ...}
)
```

### Events API (`client.events`)
Create and manage events, leagues, and tournaments.

```python
# Create a league
league = client.events.create_league({
    "name": "Summer League 2024",
    "startDate": "2024-06-01",
    "endDate": "2024-08-31"
})

# Search events
events = client.events.search_events(query="Summer League")

# Register for an event
client.events.register_for_event(
    event_id=500,
    registration_data={"format": "doubles"}
)

# Get event participants
participants = client.events.get_event_participants(event_id=500)
```

### Brackets API (`client.brackets`)
Create and manage tournament brackets.

```python
# Create a bracket
bracket = client.brackets.save_bracket({
    "name": "Championship Bracket",
    "format": "single_elimination"
})

# Update bracket status
client.brackets.update_bracket_status(
    league_id=500,
    bracket_id=300,
    club_id=100,
    status="IN_PROGRESS"
)

# Seed bracket
client.brackets.seed_bracket(
    bracket_id=300,
    seeding_data={"seedingMethod": "rating"}
)
```

### Admin API (`client.admin`)
Administrative functions (requires admin privileges).

```python
# Get user profile (admin)
profile = client.admin.get_user_profile(user_id=12345)

# Update player rating
client.admin.update_player_rating(
    player_id=12345,
    rating_data={"singlesRating": 4.5}
)

# Get/set club settings
settings = client.admin.get_club_settings(club_id=100)
client.admin.set_club_settings(
    club_id=100,
    settings_data={"autoApproveJoinRequests": True}
)
```

## Error Handling

The client provides specific exception types for different error scenarios:

```python
from dupr_api import DUPRClient
from dupr_api.exceptions import (
    AuthenticationError,
    ValidationError,
    NotFoundError,
    RateLimitError,
    ServerError,
    DUPRAPIError
)

client = DUPRClient(bearer_token="token")

try:
    profile = client.user.get_profile()
except AuthenticationError:
    print("Authentication failed - check your token")
except NotFoundError:
    print("Resource not found")
except RateLimitError:
    print("Rate limit exceeded - try again later")
except ValidationError as e:
    print(f"Validation error: {e.message}")
except ServerError:
    print("Server error - try again later")
except DUPRAPIError as e:
    print(f"API error: {e.message}")
```

## Configuration

You can customize the client configuration:

```python
client = DUPRClient(
    bearer_token="your_token",
    base_url="https://backend.mydupr.com",  # Custom API URL
    version="v1.0",                         # API version
    timeout=30                              # Request timeout in seconds
)

# Update bearer token
client.set_bearer_token("new_token")
```

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/offsetkeyz/dupr-api-client.git
cd dupr-api-client

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=dupr_api --cov-report=html

# Run specific test file
pytest tests/unit/test_client.py

# Run integration tests only
pytest tests/integration/
```

### Code Quality

```bash
# Format code with black
black dupr_api tests

# Run type checking
mypy dupr_api

# Run linting
flake8 dupr_api tests
```

## Examples

See the `examples/` directory for more detailed usage examples:

- `examples/basic_usage.py` - Basic client usage
- `examples/match_management.py` - Match creation and management
- `examples/player_search.py` - Player search and information
- `examples/club_management.py` - Club operations

## API Reference

Full API documentation is available in the `docs/` directory.

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure tests pass (`pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Issues**: Report bugs or request features via [GitHub Issues](https://github.com/offsetkeyz/dupr-api-client/issues)
- **Documentation**: [Full documentation](https://dupr-api-client.readthedocs.io/)
- **DUPR API**: [Official DUPR API Documentation](https://backend.mydupr.com/swagger-ui/index.html)

## Acknowledgments

- Built for the DUPR (Dynamic Universal Pickleball Rating) system
- Based on the official DUPR API OpenAPI specification

## Changelog

### Version 0.1.0 (2025)
- Initial release
- Complete API coverage for all major endpoints
- Comprehensive test suite
- Full documentation

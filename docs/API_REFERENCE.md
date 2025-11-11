# DUPR API Client - Complete API Reference

## Table of Contents

- [Client Initialization](#client-initialization)
- [User API](#user-api)
- [Matches API](#matches-api)
- [Players API](#players-api)
- [Clubs API](#clubs-api)
- [Events API](#events-api)
- [Brackets API](#brackets-api)
- [Admin API](#admin-api)
- [Exception Handling](#exception-handling)

## Client Initialization

### DUPRClient

```python
DUPRClient(
    bearer_token: Optional[str] = None,
    base_url: str = "https://backend.mydupr.com",
    version: str = "v1.0",
    timeout: int = 30
)
```

**Parameters:**
- `bearer_token`: OAuth bearer token for authentication
- `base_url`: Base URL of the DUPR API
- `version`: Default API version to use
- `timeout`: Request timeout in seconds

**Example:**
```python
from dupr_api import DUPRClient

client = DUPRClient(
    bearer_token="your_token",
    timeout=60
)
```

## User API

Access via `client.user`

### get_profile()

Get the authenticated user's profile.

```python
profile = client.user.get_profile(version: Optional[str] = None)
```

**Returns:** Dictionary containing user profile data

**Example:**
```python
profile = client.user.get_profile()
print(profile['result']['fullName'])
```

### update_profile()

Update the authenticated user's profile.

```python
result = client.user.update_profile(
    profile_data: Dict[str, Any],
    version: Optional[str] = None
)
```

**Parameters:**
- `profile_data`: Dictionary with profile fields to update
  - `fullName`: User's full name
  - `location`: User's location
  - `bio`: User biography
  - etc.

**Example:**
```python
client.user.update_profile({
    "fullName": "John Doe",
    "location": "New York, NY"
})
```

### get_settings()

Get user settings.

```python
settings = client.user.get_settings(version: Optional[str] = None)
```

### update_settings()

Update user settings.

```python
client.user.update_settings(
    settings: Dict[str, Any],
    version: Optional[str] = None
)
```

**Example:**
```python
client.user.update_settings({
    "emailNotifications": True,
    "privacyMode": "public"
})
```

### update_preferences()

Update user preferences.

```python
client.user.update_preferences(
    preferences: Dict[str, Any],
    version: Optional[str] = None
)
```

### get_activities()

Get user activities/newsfeed.

```python
activities = client.user.get_activities(
    player_id: int,
    limit: int = 20,
    offset: int = 0,
    version: Optional[str] = None
)
```

## Matches API

Access via `client.matches`

### save_match()

Save a new match.

```python
result = client.matches.save_match(
    match_data: Dict[str, Any],
    version: Optional[str] = None
)
```

**Match Data Structure:**
```python
{
    "format": "singles" | "doubles",
    "team1": [{"playerId": int}],
    "team2": [{"playerId": int}],
    "scores": [
        {"team1": int, "team2": int}
    ],
    "matchDate": "YYYY-MM-DD",
    "location": "string"
}
```

**Example:**
```python
match_id = client.matches.save_match({
    "format": "singles",
    "team1": [{"playerId": 123}],
    "team2": [{"playerId": 456}],
    "scores": [{"team1": 11, "team2": 5}]
})
```

### get_match()

Get match details by ID.

```python
match = client.matches.get_match(
    match_id: int,
    version: Optional[str] = None
)
```

### search_matches()

Search for matches with filters.

```python
matches = client.matches.search_matches(
    player_id: Optional[int] = None,
    club_id: Optional[int] = None,
    event_id: Optional[int] = None,
    limit: int = 20,
    offset: int = 0,
    version: Optional[str] = None
)
```

**Example:**
```python
matches = client.matches.search_matches(
    player_id=12345,
    limit=10
)
for match in matches['result']:
    print(f"Match {match['matchId']}: {match['format']}")
```

### update_match()

Update an existing match.

```python
result = client.matches.update_match(
    match_data: Dict[str, Any],
    version: Optional[str] = None
)
```

### save_verified_match()

Save a verified match (requires verification privileges).

```python
result = client.matches.save_verified_match(
    match_data: Dict[str, Any],
    version: Optional[str] = None
)
```

### delete_match()

Delete a match.

```python
result = client.matches.delete_match(
    match_id: int,
    version: Optional[str] = None
)
```

### get_match_rating_impact()

Simulate rating impact before saving a match.

```python
impact = client.matches.get_match_rating_impact(
    match_data: Dict[str, Any],
    version: Optional[str] = None
)
```

## Players API

Access via `client.players`

### search_players()

Search for players.

```python
players = client.players.search_players(
    query: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    filter_by: Optional[Dict[str, Any]] = None,
    version: Optional[str] = None
)
```

**Example:**
```python
players = client.players.search_players(
    query="John Doe",
    filter_by={
        "minRating": 4.0,
        "maxRating": 5.0
    }
)
```

### get_player()

Get player information by ID.

```python
player = client.players.get_player(
    player_id: int,
    version: Optional[str] = None
)
```

### get_player_rating_history()

Get player's rating history.

```python
history = client.players.get_player_rating_history(
    player_id: int,
    format_type: str = "singles",
    limit: int = 50,
    version: Optional[str] = None
)
```

### get_player_matches()

Get matches for a specific player.

```python
matches = client.players.get_player_matches(
    player_id: int,
    limit: int = 20,
    offset: int = 0,
    version: Optional[str] = None
)
```

### claim_player()

Claim an unclaimed player profile.

```python
result = client.players.claim_player(
    player_id: int,
    claim_data: Dict[str, Any],
    version: Optional[str] = None
)
```

### get_expected_score()

Calculate expected match score based on ratings.

```python
expected = client.players.get_expected_score(
    team1_ratings: List[float],
    team2_ratings: List[float],
    format_type: str = "singles",
    version: Optional[str] = None
)
```

## Clubs API

Access via `client.clubs`

### add_club()

Create a new club.

```python
result = client.clubs.add_club(
    club_data: Dict[str, Any],
    version: Optional[str] = None
)
```

### get_club()

Get club information.

```python
club = client.clubs.get_club(
    club_id: int,
    version: Optional[str] = None
)
```

### search_clubs()

Search for clubs.

```python
clubs = client.clubs.search_clubs(
    query: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    version: Optional[str] = None
)
```

### add_member()

Add a member to a club (admin).

```python
result = client.clubs.add_member(
    club_id: int,
    member_data: Dict[str, Any],
    version: Optional[str] = None
)
```

### join_club()

Request to join a club.

```python
result = client.clubs.join_club(
    club_id: int,
    version: Optional[str] = None
)
```

### invite_member()

Invite a member to a club.

```python
result = client.clubs.invite_member(
    club_id: int,
    invite_data: Dict[str, Any],
    version: Optional[str] = None
)
```

### get_club_members()

Get club members.

```python
members = client.clubs.get_club_members(
    club_id: int,
    limit: int = 50,
    offset: int = 0,
    version: Optional[str] = None
)
```

## Events API

Access via `client.events`

### create_league()

Create a new league/event.

```python
league = client.events.create_league(
    league_data: Dict[str, Any],
    version: Optional[str] = None
)
```

### get_event()

Get event/league details.

```python
event = client.events.get_event(
    event_id: int,
    version: Optional[str] = None
)
```

### search_events()

Search for events/leagues.

```python
events = client.events.search_events(
    query: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    version: Optional[str] = None
)
```

### register_for_event()

Register for an event.

```python
result = client.events.register_for_event(
    event_id: int,
    registration_data: Dict[str, Any],
    version: Optional[str] = None
)
```

## Brackets API

Access via `client.brackets`

### save_bracket()

Create a new tournament bracket.

```python
bracket = client.brackets.save_bracket(
    bracket_data: Dict[str, Any],
    version: Optional[str] = None
)
```

### edit_bracket()

Edit an existing bracket.

```python
result = client.brackets.edit_bracket(
    bracket_data: Dict[str, Any],
    version: Optional[str] = None
)
```

### get_bracket()

Get bracket details.

```python
bracket = client.brackets.get_bracket(
    bracket_id: int,
    version: Optional[str] = None
)
```

### update_bracket_status()

Update bracket status.

```python
result = client.brackets.update_bracket_status(
    league_id: int,
    bracket_id: int,
    club_id: int,
    status: str,
    version: Optional[str] = None
)
```

**Valid Status Values:**
- `ACTIVE`
- `INACTIVE`
- `IN_PROGRESS`
- `COMPLETE`
- `CANCELLED`

## Admin API

Access via `client.admin`

**Note:** All admin methods require admin privileges.

### get_user_profile()

Get user profile (admin).

```python
profile = client.admin.get_user_profile(
    user_id: int,
    version: Optional[str] = None
)
```

### update_user_profile()

Update user profile (admin).

```python
result = client.admin.update_user_profile(
    user_id: int,
    profile_data: Dict[str, Any],
    version: Optional[str] = None
)
```

### signup_user()

Create a new user account (admin).

```python
result = client.admin.signup_user(
    signup_data: Dict[str, Any],
    version: Optional[str] = None
)
```

### delete_user()

Delete a user account (admin).

```python
result = client.admin.delete_user(
    user_identifier: str,
    version: Optional[str] = None
)
```

### update_player_rating()

Update a player's rating (admin).

```python
result = client.admin.update_player_rating(
    player_id: int,
    rating_data: Dict[str, Any],
    version: Optional[str] = None
)
```

### batch_update_ratings()

Batch update player ratings (admin).

```python
result = client.admin.batch_update_ratings(
    ratings_data: Dict[str, Any],
    version: Optional[str] = None
)
```

## Exception Handling

### Exception Hierarchy

```
DUPRAPIError (base exception)
├── AuthenticationError (401)
├── ValidationError (400)
├── NotFoundError (404)
├── RateLimitError (429)
└── ServerError (5xx)
```

### Exception Attributes

All exceptions have:
- `message`: Error message
- `status_code`: HTTP status code (if applicable)
- `response`: Original response object (if applicable)

### Example

```python
from dupr_api.exceptions import (
    AuthenticationError,
    NotFoundError,
    DUPRAPIError
)

try:
    profile = client.user.get_profile()
except AuthenticationError as e:
    print(f"Auth failed: {e.message}")
except NotFoundError as e:
    print(f"Not found: {e.message}")
except DUPRAPIError as e:
    print(f"API error {e.status_code}: {e.message}")
```

## Rate Limiting

The DUPR API may implement rate limiting. When rate limits are exceeded, a `RateLimitError` will be raised. Implement appropriate retry logic with exponential backoff:

```python
import time
from dupr_api.exceptions import RateLimitError

max_retries = 3
for attempt in range(max_retries):
    try:
        result = client.matches.search_matches(player_id=123)
        break
    except RateLimitError:
        if attempt < max_retries - 1:
            time.sleep(2 ** attempt)  # Exponential backoff
        else:
            raise
```

## Pagination

Many list endpoints support pagination via `limit` and `offset` parameters:

```python
# Fetch all matches in batches
all_matches = []
offset = 0
limit = 50

while True:
    batch = client.matches.search_matches(
        player_id=12345,
        limit=limit,
        offset=offset
    )
    matches = batch.get('result', [])
    if not matches:
        break
    all_matches.extend(matches)
    offset += limit
```

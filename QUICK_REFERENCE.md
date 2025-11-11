# DUPR API Client - Quick Reference Card

## Installation & Verification

```bash
# Install package
cd /home/offsetkeyz/scripts/dupr-api-client
pip install -e .

# Verify installation
python verify_install.py

# Quick import test
python3 -c "from dupr_api import DUPRClient; print('✅ OK')"
```

## Command-Line Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=dupr_api --cov-report=html

# Run interactive CLI tool
python cli_test.py --interactive

# Run specific test
python cli_test.py --test namespaces
```

## Basic Usage

```python
from dupr_api import DUPRClient

# Initialize client
client = DUPRClient(bearer_token="your_token")

# Get user profile
profile = client.user.get_profile()

# Search players
players = client.players.search_players(query="John", limit=10)

# Save a match
match = client.matches.save_match({
    "format": "singles",
    "team1": [{"playerId": 123}],
    "team2": [{"playerId": 456}],
    "scores": [{"team1": 11, "team2": 5}]
})
```

## API Namespaces

```python
client.user       # User profile, settings, preferences
client.matches    # Match creation, search, updates
client.players    # Player search, ratings, history
client.clubs      # Club management, membership
client.events     # Events, leagues, registration
client.brackets   # Tournament brackets, seeding
client.admin      # Admin functions (requires privileges)
```

## Error Handling

```python
from dupr_api.exceptions import (
    AuthenticationError,  # 401 - Invalid token
    ValidationError,      # 400 - Bad request
    NotFoundError,        # 404 - Resource not found
    RateLimitError,       # 429 - Rate limit exceeded
    ServerError,          # 5xx - Server error
)

try:
    profile = client.user.get_profile()
except AuthenticationError:
    print("Invalid bearer token")
except DUPRAPIError as e:
    print(f"API error: {e.message}")
```

## Common Operations

### User Operations
```python
# Get profile
profile = client.user.get_profile()

# Update profile
client.user.update_profile({"fullName": "John Doe"})

# Get settings
settings = client.user.get_settings()

# Update settings
client.user.update_settings({"emailNotifications": True})
```

### Match Operations
```python
# Save a singles match
match = client.matches.save_match({
    "format": "singles",
    "team1": [{"playerId": 123}],
    "team2": [{"playerId": 456}],
    "scores": [{"team1": 11, "team2": 5}]
})

# Search matches
matches = client.matches.search_matches(
    player_id=123,
    limit=20
)

# Get match details
match = client.matches.get_match(match_id=789)
```

### Player Operations
```python
# Search players
players = client.players.search_players(
    query="John",
    limit=10
)

# Get player details
player = client.players.get_player(player_id=123)

# Get rating history
history = client.players.get_player_rating_history(
    player_id=123,
    format_type="doubles"
)
```

### Club Operations
```python
# Search clubs
clubs = client.clubs.search_clubs(query="Downtown")

# Get club details
club = client.clubs.get_club(club_id=100)

# Join a club
client.clubs.join_club(club_id=100)

# Get club members
members = client.clubs.get_club_members(club_id=100)
```

## Testing Commands Reference

```bash
# Verification
python verify_install.py

# All tests
pytest

# Specific test suite
pytest tests/unit/
pytest tests/integration/

# With coverage
pytest --cov=dupr_api

# Interactive CLI
python cli_test.py -i

# With authentication
export DUPR_BEARER_TOKEN="your_token"
python cli_test.py
```

## Configuration Options

```python
# Custom configuration
client = DUPRClient(
    bearer_token="token",
    base_url="https://backend.mydupr.com",  # Custom API URL
    version="v1.0",                         # API version
    timeout=30                              # Request timeout (seconds)
)

# Update token later
client.set_bearer_token("new_token")
```

## Pagination Pattern

```python
# Fetch all matches in batches
all_matches = []
offset = 0
limit = 50

while True:
    batch = client.matches.search_matches(
        player_id=123,
        limit=limit,
        offset=offset
    )
    matches = batch.get('result', [])
    if not matches:
        break
    all_matches.extend(matches)
    offset += limit
```

## File Locations

```
/home/offsetkeyz/scripts/dupr-api-client/
├── dupr_api/              # Main package
├── tests/                 # Test suite
├── examples/              # Usage examples
├── docs/                  # Documentation
├── README.md              # Quick start
├── API_REFERENCE.md       # Complete API docs
├── TESTING.md            # Testing guide
├── verify_install.py     # Installation check
└── cli_test.py           # CLI testing tool
```

## Environment Variables

```bash
# Set bearer token
export DUPR_BEARER_TOKEN="your_token_here"

# Use in scripts
python cli_test.py  # Automatically uses token from env
```

## Package Information

```bash
# Show package info
pip show dupr-api-client

# Check version
python3 -c "import dupr_api; print(dupr_api.__version__)"

# List all methods
python3 -c "from dupr_api import DUPRClient; c = DUPRClient(); print(dir(c.user))"
```

## Build & Distribution

```bash
# Build package
python -m build

# Install from wheel
pip install dist/dupr_api_client-0.1.0-py3-none-any.whl

# Upload to PyPI (when ready)
python -m twine upload dist/*
```

## Help & Documentation

```bash
# CLI tool help
python cli_test.py --help

# View README
cat README.md

# View API reference
cat docs/API_REFERENCE.md

# View testing guide
cat TESTING.md
```

## Common Issues & Solutions

**Import Error:**
```bash
pip install -e .  # Reinstall in editable mode
```

**Authentication Error:**
```bash
export DUPR_BEARER_TOKEN="your_valid_token"
```

**Test Failures:**
```bash
pytest -vv  # Verbose output to see what failed
```

**Missing Dependencies:**
```bash
pip install -r requirements-dev.txt
```

## Quick Links

- Main docs: `README.md`
- API reference: `docs/API_REFERENCE.md`
- Testing guide: `TESTING.md`
- Command-line testing: `COMMAND_LINE_TESTING.md`
- Project summary: `PROJECT_SUMMARY.md`
- DUPR API Docs: https://backend.mydupr.com/swagger-ui/index.html

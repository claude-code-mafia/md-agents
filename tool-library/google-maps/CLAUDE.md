# Google Maps CLI - AI Instructions

## When to Use This Tool

Use the Google Maps CLI when the user:
- Asks for directions or routes between locations
- Needs to convert addresses to coordinates (geocoding)
- Wants to find places like restaurants, hotels, or businesses
- Requests distance or travel time calculations
- Needs timezone or elevation information for a location
- Mentions "map", "location", "directions", "places", or "navigate"

## Key Commands

### Most Common Operations

```bash
# Get directions
google-maps directions "origin" "destination"

# Search for places
google-maps place-search "query" --near "location"

# Convert address to coordinates
google-maps geocode "address"

# Calculate distance/time
google-maps distance "origin" "destination"
```

### Integration Patterns

```bash
# For JSON processing
google-maps geocode "Times Square NYC" --json | jq '.results[0].geometry.location'

# Chain with other tools
PLACE_ID=$(google-maps place-search "best coffee" --near "Seattle" --json | jq -r '.results[0].place_id')
google-maps place-details "$PLACE_ID"
```

## Automatic Usage Scenarios

1. **Travel Planning**: When user asks about routes, directions, or trip planning
2. **Location Information**: When user needs coordinates, timezone, or elevation
3. **Business Search**: When looking for restaurants, shops, or services
4. **Distance Queries**: When user asks "how far" or "how long to drive"

## Output Formats

- Default: Human-readable text format
- JSON: Use `--json` flag for structured data
- Place IDs: Can be used for detailed lookups

## Important Notes

1. **API Key Required**: Tool will fail without valid Google Maps API key
2. **Location Formats**: Accepts addresses, place names, or "lat,lng" coordinates
3. **Place IDs**: Use place-search first to get IDs for place-details
4. **Travel Modes**: driving (default), walking, bicycling, transit

## Common Workflows

### Finding and Getting to a Place
```bash
# Search for place
google-maps place-search "restaurant" --near "user location" --type restaurant

# Get details
google-maps place-details "PLACE_ID"

# Get directions
google-maps directions "current location" "place address"
```

### Location Analysis
```bash
# Get all location data
ADDR="Empire State Building"
google-maps geocode "$ADDR" --json
google-maps timezone 40.7484 -73.9857
google-maps elevation 40.7484 -73.9857
```

### Trip Planning
```bash
# Multi-stop route
google-maps directions "Start" "End" --waypoints "Stop1" "Stop2" --alternatives

# Distance matrix for multiple destinations
google-maps distance "Origin" "Destination" --mode transit
```

## Error Handling

- No API key: Direct user to setup instructions
- Invalid location: Suggest alternatives or ask for clarification
- API quota exceeded: Inform user about rate limits

## Tips

- Use `--near` with place-search for location-specific results
- Add `--alternatives` to directions for route options
- Specify `--fields` with place-details to reduce API usage
- Use coordinates (lat,lng) for precise locations
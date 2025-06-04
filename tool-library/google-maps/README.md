# Google Maps CLI

A command-line interface for Google Maps API operations including geocoding, directions, place search, and more.

## Features

- **Geocoding**: Convert addresses to coordinates and vice versa
- **Directions**: Get turn-by-turn directions between locations
- **Distance**: Calculate distance and travel time between places
- **Place Search**: Find places by name, type, or location
- **Place Details**: Get detailed information about specific places
- **Timezone**: Get timezone information for any location
- **Elevation**: Get elevation data for coordinates

## Installation

```bash
# From the tool-library directory
./install-tool.sh google-maps

# Or manually set up API key first
export GOOGLE_MAPS_API_KEY="your-api-key-here"
```

## Setup

You'll need a Google Maps API key. Get one from:
https://developers.google.com/maps/documentation/javascript/get-api-key

Then either:
1. Set environment variable: `export GOOGLE_MAPS_API_KEY="your-key"`
2. Run the setup script: `./setup.sh` (in google-maps directory)

## Usage

### Geocoding

Convert address to coordinates:
```bash
google-maps geocode "1600 Amphitheatre Parkway, Mountain View, CA"
```

Convert coordinates to address:
```bash
google-maps reverse-geocode 37.4224764 -122.0842499
```

### Directions

Get driving directions:
```bash
google-maps directions "San Francisco, CA" "Los Angeles, CA"
```

With options:
```bash
# Walking directions with waypoints
google-maps directions "Union Square, SF" "Golden Gate Bridge" \
  --mode walking \
  --waypoints "Fisherman's Wharf" "Crissy Field"

# Show alternative routes
google-maps directions "Berkeley" "San Jose" --alternatives
```

### Distance Calculation

```bash
google-maps distance "New York" "Boston"

# With travel mode and units
google-maps distance "London" "Paris" --mode transit --units imperial
```

### Place Search

Search for places:
```bash
# Basic search
google-maps place-search "coffee shops"

# Search near a location
google-maps place-search "restaurants" --near "Times Square, NYC" --radius 1000

# Filter by type
google-maps place-search "pizza" --near "37.7749,-122.4194" --type restaurant
```

### Place Details

Get detailed information about a place:
```bash
# Using a Place ID from search results
google-maps place-details "ChIJN1t_tDeuEmsRUsoyG83frY4"

# Get specific fields only
google-maps place-details "ChIJN1t_tDeuEmsRUsoyG83frY4" \
  --fields name rating formatted_phone_number website
```

### Timezone

Get timezone for a location:
```bash
google-maps timezone 40.7128 -74.0060
```

### Elevation

Get elevation data:
```bash
google-maps elevation 37.4224764 -122.0842499
```

## JSON Output

All commands support JSON output for scripting:
```bash
google-maps geocode "NYC" --json
google-maps place-search "hotels" --json
```

## Examples

### Find nearby restaurants and get directions
```bash
# Search for restaurants
google-maps place-search "italian restaurant" --near "Chicago" --limit 3

# Get place details
google-maps place-details "ChIJ..." 

# Get directions to the restaurant
google-maps directions "current location" "restaurant address"
```

### Plan a trip with multiple stops
```bash
# Get directions with waypoints
google-maps directions "San Francisco" "Los Angeles" \
  --waypoints "Monterey" "Santa Barbara" \
  --alternatives
```

### Analyze location data
```bash
# Get coordinates
COORDS=$(google-maps geocode "Statue of Liberty" --json | jq -r '.results[0].geometry.location')

# Get timezone
google-maps timezone $(echo $COORDS | jq -r '.lat') $(echo $COORDS | jq -r '.lng')

# Get elevation
google-maps elevation $(echo $COORDS | jq -r '.lat') $(echo $COORDS | jq -r '.lng')
```

## API Key Configuration

The tool looks for your API key in this order:
1. `GOOGLE_MAPS_API_KEY` environment variable
2. `~/.google-maps/config.json` file

To save your API key permanently:
```bash
mkdir -p ~/.google-maps
echo '{"api_key": "your-key-here"}' > ~/.google-maps/config.json
chmod 600 ~/.google-maps/config.json
```

## Rate Limits

Google Maps API has usage quotas. For details see:
https://developers.google.com/maps/documentation/javascript/usage-and-billing

## Error Handling

The tool provides clear error messages for common issues:
- Invalid API key
- Quota exceeded
- Invalid locations
- Network errors

## Required APIs

Enable these APIs in Google Cloud Console:
- Geocoding API
- Directions API
- Distance Matrix API
- Places API
- Time Zone API
- Elevation API
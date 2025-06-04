#!/bin/bash

set -e

echo "Google Maps CLI Setup"
echo "===================="
echo

# Check if API key is already configured
if [ -n "$GOOGLE_MAPS_API_KEY" ]; then
    echo "✓ API key found in environment variable"
    exit 0
fi

CONFIG_DIR="$HOME/.google-maps"
CONFIG_FILE="$CONFIG_DIR/config.json"

if [ -f "$CONFIG_FILE" ]; then
    echo "✓ Configuration file already exists at $CONFIG_FILE"
    exit 0
fi

# Prompt for API key
echo "To use Google Maps CLI, you need a Google Maps API key."
echo
echo "Get one from: https://developers.google.com/maps/documentation/javascript/get-api-key"
echo
echo "Required APIs to enable in Google Cloud Console:"
echo "  - Geocoding API"
echo "  - Directions API" 
echo "  - Distance Matrix API"
echo "  - Places API"
echo "  - Time Zone API"
echo "  - Elevation API"
echo
read -p "Enter your Google Maps API key: " API_KEY

if [ -z "$API_KEY" ]; then
    echo "Error: No API key provided"
    exit 1
fi

# Create config directory
mkdir -p "$CONFIG_DIR"

# Save API key
cat > "$CONFIG_FILE" << EOF
{
  "api_key": "$API_KEY"
}
EOF

# Secure the config file
chmod 600 "$CONFIG_FILE"

echo
echo "✓ Configuration saved to $CONFIG_FILE"
echo
echo "You can also set the API key as an environment variable:"
echo "  export GOOGLE_MAPS_API_KEY=\"$API_KEY\""
echo
echo "Setup complete! You can now use the google-maps command."
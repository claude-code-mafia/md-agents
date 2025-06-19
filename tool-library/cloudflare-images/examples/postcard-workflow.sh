#!/bin/bash
# Example: Complete postcard generation workflow
# This script demonstrates the full flow from generation to web URL

set -e

# Configuration
LOCATION="${1:-Paris}"
THEME="${2:-vintage}"
TIMESTAMP=$(date +%s)
OUTPUT_DIR="./postcards"

# Create output directory
mkdir -p "$OUTPUT_DIR"

echo "🎨 Generating postcard for $LOCATION in $THEME style..."

# Step 1: Generate the postcard image
PROMPT="Beautiful ${LOCATION} postcard in ${THEME} style, scenic view, high quality"
LOCAL_FILE="$OUTPUT_DIR/postcard-${LOCATION,,}-${THEME,,}-${TIMESTAMP}.png"

if command -v image-gen &> /dev/null; then
    image-gen "$PROMPT" --output "$LOCAL_FILE" --size 1024x768
else
    echo "⚠️  image-gen tool not found, creating placeholder..."
    # Create a placeholder image for testing
    convert -size 1024x768 \
        -background white \
        -fill black \
        -gravity center \
        -pointsize 72 \
        label:"$LOCATION\n$THEME" \
        "$LOCAL_FILE" 2>/dev/null || {
        echo "❌ Neither image-gen nor ImageMagick available"
        exit 1
    }
fi

echo "✅ Image generated: $LOCAL_FILE"

# Step 2: Upload to Cloudflare Images
echo "☁️  Uploading to Cloudflare Images..."

CF_IMAGE_ID="postcards/${LOCATION,,}/${THEME,,}/${TIMESTAMP}"
METADATA=$(cat <<EOF
{
    "location": "$LOCATION",
    "theme": "$THEME",
    "created": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "prompt": "$PROMPT"
}
EOF
)

# Upload and capture result
UPLOAD_RESULT=$(cf-images upload "$LOCAL_FILE" \
    --id "$CF_IMAGE_ID" \
    --metadata "$METADATA" \
    --format json)

# Extract URL from result
IMAGE_URL=$(echo "$UPLOAD_RESULT" | jq -r '.url')
IMAGE_ID=$(echo "$UPLOAD_RESULT" | jq -r '.id')

if [ "$IMAGE_URL" = "null" ] || [ -z "$IMAGE_URL" ]; then
    echo "❌ Upload failed:"
    echo "$UPLOAD_RESULT" | jq .
    exit 1
fi

echo "✅ Image uploaded successfully!"
echo "   ID: $IMAGE_ID"
echo "   URL: $IMAGE_URL"

# Step 3: Save result to JSON file
RESULT_FILE="$OUTPUT_DIR/postcard-${LOCATION,,}-${THEME,,}-${TIMESTAMP}.json"
cat > "$RESULT_FILE" <<EOF
{
    "id": "$IMAGE_ID",
    "url": "$IMAGE_URL",
    "location": "$LOCATION",
    "theme": "$THEME",
    "timestamp": $TIMESTAMP,
    "created": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "local_file": "$LOCAL_FILE",
    "prompt": "$PROMPT"
}
EOF

echo "📄 Result saved to: $RESULT_FILE"

# Step 4: Optional - Update database (if convex tool is available)
if command -v convex &> /dev/null && [ -n "$POSTCARD_ID" ]; then
    echo "🔄 Updating Convex database..."
    convex save-postcard \
        --id "$POSTCARD_ID" \
        --image-path "$LOCAL_FILE" \
        --location "$LOCATION" \
        --theme "$THEME"
fi

# Step 5: Display summary
echo ""
echo "🎉 Postcard generation complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Location:    $LOCATION"
echo "Theme:       $THEME"
echo "Image URL:   $IMAGE_URL"
echo "Local file:  $LOCAL_FILE"
echo "Result JSON: $RESULT_FILE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Optional: Open in browser
if command -v open &> /dev/null; then
    echo ""
    echo "Press Enter to open in browser, or Ctrl+C to skip..."
    read -r
    open "$IMAGE_URL"
elif command -v xdg-open &> /dev/null; then
    echo ""
    echo "Press Enter to open in browser, or Ctrl+C to skip..."
    read -r
    xdg-open "$IMAGE_URL"
fi
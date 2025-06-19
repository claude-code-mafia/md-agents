#!/bin/bash
# Example: Batch upload multiple images with organized structure

set -e

# Configuration
BATCH_NAME="${1:-batch-$(date +%Y%m%d-%H%M%S)}"
SOURCE_DIR="${2:-.}"

echo "📦 Batch Upload: $BATCH_NAME"
echo "📁 Source directory: $SOURCE_DIR"
echo ""

# Find all image files
IMAGE_FILES=$(find "$SOURCE_DIR" -maxdepth 1 -type f \( -iname "*.png" -o -iname "*.jpg" -o -iname "*.jpeg" \))

if [ -z "$IMAGE_FILES" ]; then
    echo "❌ No image files found in $SOURCE_DIR"
    exit 1
fi

# Count files
FILE_COUNT=$(echo "$IMAGE_FILES" | wc -l)
echo "Found $FILE_COUNT image file(s) to upload"
echo ""

# Upload counter
SUCCESS_COUNT=0
FAIL_COUNT=0

# Results array
RESULTS_FILE="batch-results-${BATCH_NAME}.json"
echo "[" > "$RESULTS_FILE"
FIRST_ENTRY=true

# Process each file
while IFS= read -r FILE; do
    if [ -z "$FILE" ]; then
        continue
    fi
    
    FILENAME=$(basename "$FILE")
    BASENAME="${FILENAME%.*}"
    
    echo "⬆️  Uploading: $FILENAME"
    
    # Create structured ID
    CF_ID="batch/$BATCH_NAME/$BASENAME"
    
    # Upload with error handling
    if RESULT=$(cf-images upload "$FILE" --id "$CF_ID" --format json 2>&1); then
        URL=$(echo "$RESULT" | jq -r '.url' 2>/dev/null || echo "")
        
        if [ -n "$URL" ] && [ "$URL" != "null" ]; then
            echo "   ✅ Success: $URL"
            ((SUCCESS_COUNT++))
            
            # Add to results file
            if [ "$FIRST_ENTRY" = true ]; then
                FIRST_ENTRY=false
            else
                echo "," >> "$RESULTS_FILE"
            fi
            
            # Append result
            cat >> "$RESULTS_FILE" <<EOF
  {
    "filename": "$FILENAME",
    "id": "$CF_ID",
    "url": "$URL",
    "status": "success"
  }
EOF
        else
            echo "   ❌ Failed: Invalid response"
            ((FAIL_COUNT++))
        fi
    else
        echo "   ❌ Failed: $RESULT"
        ((FAIL_COUNT++))
        
        # Add failure to results
        if [ "$FIRST_ENTRY" = true ]; then
            FIRST_ENTRY=false
        else
            echo "," >> "$RESULTS_FILE"
        fi
        
        cat >> "$RESULTS_FILE" <<EOF
  {
    "filename": "$FILENAME",
    "id": "$CF_ID",
    "status": "failed",
    "error": "Upload failed"
  }
EOF
    fi
    
    echo ""
done <<< "$IMAGE_FILES"

# Close results JSON
echo "]" >> "$RESULTS_FILE"

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Batch Upload Complete"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Successful: $SUCCESS_COUNT"
echo "❌ Failed:     $FAIL_COUNT"
echo "📄 Results:    $RESULTS_FILE"
echo ""

# Show uploaded images
if [ "$SUCCESS_COUNT" -gt 0 ]; then
    echo "📷 Uploaded images:"
    cf-images list --limit "$SUCCESS_COUNT" --format json | \
        jq -r '.images[] | select(.id | startswith("batch/'$BATCH_NAME'")) | "   - \(.id): \(.variants[0])"'
fi
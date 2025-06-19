# Cloudflare Images Tool Package

## Package Contents

```
cloudflare-images-tool/
├── cf-images              # Main executable tool
├── README.md             # User documentation
├── CLAUDE.md             # AI-specific instructions
├── setup.sh              # Installation script
├── test_cf_images.py     # Test suite
├── PACKAGE.md            # This file
└── examples/             # Example scripts
    ├── postcard-workflow.sh    # Complete postcard generation example
    └── batch-upload.sh         # Batch upload example
```

## Tool Information

- **Name**: cf-images
- **Version**: 1.0.0
- **Purpose**: Upload images to Cloudflare Images and retrieve web-accessible URLs
- **Language**: Python 3
- **Dependencies**: requests

## Key Features

1. **Simple Upload**: `cf-images upload image.png --id custom-id`
2. **JSON Output**: Perfect for automation and scripting
3. **Custom IDs**: Organize images with path-like structure
4. **Metadata Support**: Attach searchable JSON metadata
5. **Batch Operations**: Process multiple images efficiently
6. **List/Delete**: Manage uploaded images

## Installation

### Quick Install
```bash
curl -O https://raw.githubusercontent.com/peteknowsai/cells-tool-registry/main/tools/bin/cf-images
chmod +x cf-images
sudo mv cf-images /usr/local/bin/
```

### Using Setup Script
```bash
./setup.sh
```

## Configuration

Set environment variables:
```bash
export CLOUDFLARE_ACCOUNT_ID="your-account-id"
export CLOUDFLARE_API_TOKEN="your-api-token"
```

## Integration Example

```bash
# Generate image
image-gen "Beautiful sunset" --output sunset.png

# Upload and get URL
result=$(cf-images upload sunset.png --id "postcards/sunset" --format json)
url=$(echo "$result" | jq -r '.url')

echo "Image available at: $url"
```

## Testing

Run the test suite:
```bash
python3 test_cf_images.py
```

All tests should pass:
- ✓ Help command works
- ✓ Upload help works
- ✓ Properly handles missing credentials
- ✓ File validation works
- ✓ JSON format option accepted
- ✓ Metadata parsing validated

## API Limits

- Max file size: 10MB
- Max dimensions: 12,000px
- Max area: 100 megapixels
- Supported formats: PNG, JPEG, GIF, WebP, SVG

## Publishing to Registry

To publish to the cells-tool-registry:

1. Fork https://github.com/peteknowsai/cells-tool-registry
2. Copy files:
   ```bash
   cp cf-images ../cells-tool-registry/tools/bin/
   mkdir -p ../cells-tool-registry/tools/cloudflare-images
   cp README.md CLAUDE.md ../cells-tool-registry/tools/cloudflare-images/
   ```
3. Create pull request

## Support

For issues or improvements:
- Check error messages for API-specific issues
- Verify credentials and permissions
- Ensure image meets size/format requirements
- Review Cloudflare Images documentation
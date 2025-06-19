# Cloudflare Images Tool Package

## Contents
- `cf-images` - Main executable script
- `README.md` - User documentation
- `CLAUDE.md` - AI assistant instructions
- `setup.sh` - Installation script
- `test_cf_images.py` - Test suite

## Installation

### Quick Install
```bash
./setup.sh
```

### Manual Install
```bash
# Copy to tool-library
cp cf-images ~/Projects/tool-library/bin/
chmod +x ~/Projects/tool-library/bin/cf-images

# Install dependencies
pip install requests

# Set environment variables
export CLOUDFLARE_ACCOUNT_ID="your-account-id"
export CLOUDFLARE_API_TOKEN="your-api-token"
```

## Key Features
- Upload images with custom IDs
- Support for metadata
- JSON output for automation
- List and delete operations
- Integration with image-gen tool

## Version
1.0.0 - Initial release
EOF < /dev/null

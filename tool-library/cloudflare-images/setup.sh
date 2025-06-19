#\!/bin/bash
# Setup script for cf-images tool

echo "Setting up Cloudflare Images CLI tool..."

# Check if tool-library directory exists
TOOL_DIR="$HOME/Projects/tool-library"
if [ \! -d "$TOOL_DIR" ]; then
    echo "Error: tool-library not found at $TOOL_DIR"
    echo "Please ensure you have the tool-library repository cloned."
    exit 1
fi

# Create directories if needed
mkdir -p "$TOOL_DIR/bin"
mkdir -p "$TOOL_DIR/cloudflare-images"

# Copy files
echo "Installing cf-images..."
cp cf-images "$TOOL_DIR/bin/"
chmod +x "$TOOL_DIR/bin/cf-images"

cp README.md "$TOOL_DIR/cloudflare-images/"
cp CLAUDE.md "$TOOL_DIR/cloudflare-images/"

# Check Python dependencies
echo "Checking Python dependencies..."
if \! python3 -c "import requests" 2>/dev/null; then
    echo "Installing requests library..."
    pip install requests
fi

# Add to PATH if not already there
if \! echo "$PATH"  < /dev/null |  grep -q "$TOOL_DIR/bin"; then
    echo ""
    echo "Add the following to your shell configuration (.bashrc, .zshrc, etc.):"
    echo "export PATH=\"\$PATH:$TOOL_DIR/bin\""
fi

# Check for environment variables
echo ""
echo "Configuration:"
echo "Set the following environment variables:"
echo "  export CLOUDFLARE_ACCOUNT_ID='your-account-id'"
echo "  export CLOUDFLARE_API_TOKEN='your-api-token'"
echo ""
echo "Get these from:"
echo "  - Account ID: Cloudflare Dashboard > Right sidebar"
echo "  - API Token: My Profile > API Tokens > Create Token"
echo "    (needs 'Cloudflare Images:Edit' permission)"

echo ""
echo "✓ Installation complete\!"
echo ""
echo "Test with: cf-images --help"

#!/bin/bash
# Setup script to add tool-library commands to PATH

TOOL_LIB_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BIN_DIR="$TOOL_LIB_DIR/bin"

echo "Setting up tool-library commands..."

# Detect shell
if [ -n "$ZSH_VERSION" ]; then
    SHELL_RC="$HOME/.zshrc"
    SHELL_NAME="zsh"
elif [ -n "$BASH_VERSION" ]; then
    SHELL_RC="$HOME/.bashrc"
    SHELL_NAME="bash"
else
    echo "Unsupported shell. Please add $BIN_DIR to your PATH manually."
    exit 1
fi

# Check if PATH already contains our bin directory
if echo "$PATH" | grep -q "$BIN_DIR"; then
    echo "tool-library/bin is already in PATH"
else
    echo "Adding tool-library/bin to PATH in $SHELL_RC"
    echo "" >> "$SHELL_RC"
    echo "# Tool Library Commands" >> "$SHELL_RC"
    echo "export PATH=\"$BIN_DIR:\$PATH\"" >> "$SHELL_RC"
    echo "Added to $SHELL_RC"
fi

echo ""
echo "Available commands:"
echo "  gmail          - Gmail CLI (list, read, send emails)"
echo "  gmail-advanced - Advanced Gmail features (analyze, export)"
echo "  grok           - Grok AI chat and X/Twitter analysis"
echo "  image-gen      - Generate images with DALL-E"
echo "  current-time   - Get accurate network time"
echo "  typefully      - Twitter/X content creation"
echo "  tiktok         - TikTok CLI (trends, search, user info)"
echo ""
echo "To use immediately, run: source $SHELL_RC"
echo "Or start a new terminal session."
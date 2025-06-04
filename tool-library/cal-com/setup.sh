#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Setting up Cal.com CLI tool..."

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv "$SCRIPT_DIR/venv"

# Activate and install dependencies
echo "Installing dependencies..."
source "$SCRIPT_DIR/venv/bin/activate"
pip install -r "$SCRIPT_DIR/requirements.txt" >/dev/null 2>&1

echo "✓ Cal.com CLI setup complete"
echo ""
echo "To authenticate, run: cal-com auth"
echo "Then enter your Cal.com API key from Settings > Security"
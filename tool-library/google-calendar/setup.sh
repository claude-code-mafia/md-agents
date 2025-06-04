#!/bin/bash

# Setup script for Google Calendar CLI

set -e

echo "Setting up Google Calendar CLI..."

# Get the directory of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv "$DIR/venv"

# Activate virtual environment
source "$DIR/venv/bin/activate"

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing dependencies..."
pip install -r "$DIR/requirements.txt"

# Update shebang in gcal_cli.py to use virtual environment
echo "Updating shebang..."
sed -i '' "1s|.*|#!$DIR/venv/bin/python|" "$DIR/gcal_cli.py"

# Create config directory
CONFIG_DIR="$HOME/.gcal-cli"
mkdir -p "$CONFIG_DIR"

echo ""
echo "✅ Google Calendar CLI setup complete!"
echo ""
echo "⚠️  Important: Before using the tool, you need to:"
echo "1. Go to https://console.cloud.google.com/"
echo "2. Create a new project or select an existing one"
echo "3. Enable the Google Calendar API"
echo "4. Create OAuth 2.0 credentials (Desktop application type)"
echo "5. Download credentials.json to $CONFIG_DIR/credentials.json"
echo ""
echo "The tool will guide you through authentication on first use."
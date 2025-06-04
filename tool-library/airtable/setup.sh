#!/bin/bash
# Setup script for Airtable CLI

echo "Setting up Airtable CLI..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Setup complete!"
echo ""
echo "To use the Airtable CLI, you need to set your Personal Access Token:"
echo "  export AIRTABLE_PAT='your-personal-access-token'"
echo ""
echo "Get your token from: https://airtable.com/create/tokens"
echo ""
echo "Note: API keys (starting with 'key') are deprecated as of Feb 2024."
echo "Please use Personal Access Tokens instead."
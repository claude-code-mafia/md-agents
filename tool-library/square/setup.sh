#!/bin/bash

echo "Setting up Square CLI..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Square CLI setup complete!"
echo ""
echo "To use the Square CLI, you need to set your access token:"
echo "export SQUARE_ACCESS_TOKEN='your-access-token'"
echo ""
echo "Get your access token from: https://developer.squareup.com/apps"
echo ""
echo "For sandbox testing, also set:"
echo "export SQUARE_ENVIRONMENT='sandbox'"
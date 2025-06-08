#!/bin/bash

echo "Setting up Raycast CLI..."

# Create virtual environment
python3 -m venv venv

# Activate and install dependencies
source venv/bin/activate
pip install -r requirements.txt

echo "Setup complete!"
echo "Install globally with: ../install-tool.sh raycast-cli"
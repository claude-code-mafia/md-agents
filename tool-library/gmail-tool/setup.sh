#!/bin/bash

# Gmail CLI Tool Setup Script

echo "Gmail CLI Tool Setup"
echo "==================="
echo

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
if [[ -z "$python_version" ]]; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

echo "✓ Python version: $python_version"

# Create virtual environment (optional but recommended)
read -p "Create virtual environment? (recommended) [Y/n]: " create_venv
if [[ "$create_venv" != "n" && "$create_venv" != "N" ]]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✓ Virtual environment created and activated"
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"

# Create config directory
echo "Creating configuration directory..."
mkdir -p ~/.gmail-cli
echo "✓ Configuration directory created at ~/.gmail-cli/"

# Check for credentials
if [[ ! -f ~/.gmail-cli/credentials.json ]]; then
    echo
    echo "⚠️  credentials.json not found!"
    echo
    echo "To complete setup, you need to:"
    echo "1. Go to https://console.cloud.google.com/"
    echo "2. Create a new project or select existing"
    echo "3. Enable Gmail API"
    echo "4. Create OAuth 2.0 credentials (Desktop application)"
    echo "5. Download credentials.json"
    echo "6. Move it to ~/.gmail-cli/credentials.json"
    echo
    read -p "Open Google Cloud Console now? [Y/n]: " open_console
    if [[ "$open_console" != "n" && "$open_console" != "N" ]]; then
        open "https://console.cloud.google.com/" 2>/dev/null || xdg-open "https://console.cloud.google.com/" 2>/dev/null || echo "Please open https://console.cloud.google.com/ in your browser"
    fi
else
    echo "✓ credentials.json found"
fi

# Create convenient aliases
echo
read -p "Add convenient aliases to your shell? [Y/n]: " add_aliases
if [[ "$add_aliases" != "n" && "$add_aliases" != "N" ]]; then
    # Detect shell
    if [[ -n "$ZSH_VERSION" ]]; then
        shell_rc="$HOME/.zshrc"
    elif [[ -n "$BASH_VERSION" ]]; then
        shell_rc="$HOME/.bashrc"
    else
        shell_rc="$HOME/.profile"
    fi
    
    # Add aliases
    echo "" >> "$shell_rc"
    echo "# Gmail CLI aliases" >> "$shell_rc"
    echo "alias gmail='python3 $(pwd)/gmail_cli.py'" >> "$shell_rc"
    echo "alias gmail-advanced='python3 $(pwd)/gmail_advanced.py'" >> "$shell_rc"
    
    echo "✓ Aliases added to $shell_rc"
    echo "  Run 'source $shell_rc' or restart your terminal to use them"
fi

# Test authentication
echo
read -p "Test Gmail authentication now? [Y/n]: " test_auth
if [[ "$test_auth" != "n" && "$test_auth" != "N" ]]; then
    echo "Testing authentication..."
    python3 gmail_cli.py list -n 1
fi

echo
echo "Setup complete!"
echo
echo "Quick start:"
echo "  gmail list                    # List recent emails"
echo "  gmail read MESSAGE_ID         # Read a specific email"
echo "  gmail send to@example.com \"Subject\" \"Body\""
echo
echo "Advanced features:"
echo "  gmail-advanced analyze        # Analyze inbox patterns"
echo "  gmail-advanced export \"query\" # Export search results"
echo
echo "For full documentation, see README.md"
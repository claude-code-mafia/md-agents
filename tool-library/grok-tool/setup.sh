#!/bin/bash

# Grok CLI Tool Setup Script

echo "Grok CLI Tool Setup"
echo "=================="
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
mkdir -p ~/.grok-cli
mkdir -p ~/.grok-cli/sessions
echo "✓ Configuration directory created at ~/.grok-cli/"

# Check for API key
if [[ -z "$GROK_API_KEY" ]] && [[ ! -f ~/.grok-cli/config.json ]]; then
    echo
    echo "⚠️  No API key found!"
    echo
    echo "To complete setup, you need to:"
    echo "1. Go to https://console.x.ai/"
    echo "2. Sign up or log in to create an account"
    echo "3. Navigate to API Keys section"
    echo "4. Generate a new API key"
    echo "5. Set it as environment variable:"
    echo "   export GROK_API_KEY='your-key-here'"
    echo "   Or it will be saved in ~/.grok-cli/config.json on first use"
    echo
    echo "Note: You get $25 of free API credits per month!"
    echo
    read -p "Open xAI Console now? [Y/n]: " open_console
    if [[ "$open_console" != "n" && "$open_console" != "N" ]]; then
        open "https://console.x.ai/" 2>/dev/null || xdg-open "https://console.x.ai/" 2>/dev/null || echo "Please open https://console.x.ai/ in your browser"
    fi
else
    echo "✓ API key configuration found"
fi

# Make the main script executable
chmod +x grok_cli.py
echo "✓ Made grok_cli.py executable"

# Create convenient aliases
echo
read -p "Add convenient alias to your shell? [Y/n]: " add_alias
if [[ "$add_alias" != "n" && "$add_alias" != "N" ]]; then
    # Detect shell
    if [[ -n "$ZSH_VERSION" ]]; then
        shell_rc="$HOME/.zshrc"
    elif [[ -n "$BASH_VERSION" ]]; then
        shell_rc="$HOME/.bashrc"
    else
        shell_rc="$HOME/.profile"
    fi
    
    # Add alias
    echo "" >> "$shell_rc"
    echo "# Grok CLI alias" >> "$shell_rc"
    echo "alias grok='$(pwd)/grok_cli.py'" >> "$shell_rc"
    
    echo "✓ Alias added to $shell_rc"
    echo "  Run 'source $shell_rc' or restart your terminal to use it"
fi

# Test API connection
echo
read -p "Test Grok API connection now? [Y/n]: " test_api
if [[ "$test_api" != "n" && "$test_api" != "N" ]]; then
    if [[ -z "$GROK_API_KEY" ]]; then
        echo "Please set GROK_API_KEY first:"
        echo "export GROK_API_KEY='your-key-here'"
    else
        echo "Testing API connection..."
        python3 grok_cli.py chat "Hello, Grok! Tell me a joke in one line."
    fi
fi

echo
echo "Setup complete!"
echo
echo "Quick start:"
echo "  grok chat \"What's happening on X today?\""
echo "  grok analyze \"https://x.com/user/status/123\""
echo "  grok trending --category tech"
echo "  grok image \"cyberpunk cat\""
echo
echo "For Claude integration:"
echo "  grok [any-command] --json"
echo
echo "For full documentation, see README.md"
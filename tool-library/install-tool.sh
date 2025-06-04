#!/bin/bash
# Standardized tool installation script for tool-library

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BIN_DIR="$SCRIPT_DIR/bin"

# Default to global installation
INSTALL_SCOPE="global"

# Function to print colored output
print_color() {
    color=$1
    shift
    echo -e "${color}$@${NC}"
}

# Function to show usage
usage() {
    echo "Usage: $0 <tool-name> [options]"
    echo ""
    echo "Options:"
    echo "  --project    Update project CLAUDE.md instead of global"
    echo "  --help       Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 my-tool           # Install globally (default)"
    echo "  $0 my-tool --project # Update project CLAUDE.md"
    exit 1
}

# Parse arguments
if [ $# -eq 0 ]; then
    usage
fi

TOOL_NAME=$1
shift

while [[ $# -gt 0 ]]; do
    case $1 in
        --project)
            INSTALL_SCOPE="project"
            shift
            ;;
        --help|-h)
            usage
            ;;
        *)
            print_color $RED "Unknown option: $1"
            usage
            ;;
    esac
done

# Validate tool exists
TOOL_DIR="$SCRIPT_DIR/$TOOL_NAME"
if [ ! -d "$TOOL_DIR" ]; then
    print_color $RED "Error: Tool directory '$TOOL_DIR' not found"
    exit 1
fi

print_color $GREEN "Installing $TOOL_NAME..."

# Step 1: Find the main executable
EXECUTABLE=""
if [ -f "$TOOL_DIR/$TOOL_NAME.py" ]; then
    EXECUTABLE="$TOOL_DIR/$TOOL_NAME.py"
    # Check if there's a virtual environment
    if [ -f "$TOOL_DIR/venv/bin/python" ]; then
        WRAPPER_CONTENT="#!/bin/bash
# $TOOL_NAME CLI wrapper
exec $TOOL_DIR/venv/bin/python $EXECUTABLE \"\$@\""
    else
        WRAPPER_CONTENT="#!/bin/bash
# $TOOL_NAME CLI wrapper
exec python3 $EXECUTABLE \"\$@\""
    fi
elif [ -f "$TOOL_DIR/$TOOL_NAME.sh" ]; then
    EXECUTABLE="$TOOL_DIR/$TOOL_NAME.sh"
    WRAPPER_CONTENT="#!/bin/bash
# $TOOL_NAME CLI wrapper
exec $EXECUTABLE \"\$@\""
elif [ -f "$TOOL_DIR/$TOOL_NAME" ]; then
    EXECUTABLE="$TOOL_DIR/$TOOL_NAME"
    WRAPPER_CONTENT="#!/bin/bash
# $TOOL_NAME CLI wrapper
exec $EXECUTABLE \"\$@\""
else
    # Look for any executable file
    EXECUTABLE=$(find "$TOOL_DIR" -maxdepth 1 -type f -perm +111 | grep -v -E '(setup\.sh|venv|__pycache__|\.pyc)' | head -1)
    if [ -z "$EXECUTABLE" ]; then
        print_color $RED "Error: No executable found in $TOOL_DIR"
        exit 1
    fi
    # Determine if it's Python or shell
    if head -1 "$EXECUTABLE" | grep -q python; then
        # Check if there's a virtual environment
        if [ -f "$TOOL_DIR/venv/bin/python" ]; then
            WRAPPER_CONTENT="#!/bin/bash
# $TOOL_NAME CLI wrapper
exec $TOOL_DIR/venv/bin/python $EXECUTABLE \"\$@\""
        else
            WRAPPER_CONTENT="#!/bin/bash
# $TOOL_NAME CLI wrapper
exec python3 $EXECUTABLE \"\$@\""
        fi
    else
        WRAPPER_CONTENT="#!/bin/bash
# $TOOL_NAME CLI wrapper
exec $EXECUTABLE \"\$@\""
    fi
fi

print_color $YELLOW "Found executable: $EXECUTABLE"

# Step 2: Create bin directory if it doesn't exist
mkdir -p "$BIN_DIR"

# Step 3: Create wrapper script
WRAPPER_PATH="$BIN_DIR/$TOOL_NAME"
echo "$WRAPPER_CONTENT" > "$WRAPPER_PATH"
chmod +x "$WRAPPER_PATH"
print_color $GREEN "Created wrapper: $WRAPPER_PATH"

# Step 4: Add bin to PATH if not already there
PATH_LINE="export PATH=\"$BIN_DIR:\$PATH\""
PATH_ADDED=false

# Add to .bashrc if it exists
if [ -f "$HOME/.bashrc" ]; then
    if ! grep -q "Tool Library Commands" "$HOME/.bashrc"; then
        echo "" >> "$HOME/.bashrc"
        echo "# Tool Library Commands" >> "$HOME/.bashrc"
        echo "$PATH_LINE" >> "$HOME/.bashrc"
        print_color $GREEN "Added $BIN_DIR to PATH in ~/.bashrc"
        PATH_ADDED=true
    fi
fi

# Add to .zshrc if it exists
if [ -f "$HOME/.zshrc" ]; then
    if ! grep -q "Tool Library Commands" "$HOME/.zshrc"; then
        echo "" >> "$HOME/.zshrc"
        echo "# Tool Library Commands" >> "$HOME/.zshrc"
        echo "$PATH_LINE" >> "$HOME/.zshrc"
        print_color $GREEN "Added $BIN_DIR to PATH in ~/.zshrc"
        PATH_ADDED=true
    fi
fi

# Export for current session
if ! echo "$PATH" | grep -q "$BIN_DIR"; then
    export PATH="$BIN_DIR:$PATH"
fi

if [ "$PATH_ADDED" = false ]; then
    print_color $YELLOW "bin directory already in PATH"
fi

# Step 5: Update CLAUDE.md
update_claude_md() {
    local claude_file=$1
    local tool_name=$2
    
    # Read tool's README for description
    local description="CLI tool"
    if [ -f "$TOOL_DIR/README.md" ]; then
        description=$(head -3 "$TOOL_DIR/README.md" | tail -1 | sed 's/^[[:space:]]*//')
    fi
    
    # Check if tool is already documented
    if grep -q "^$tool_name " "$claude_file" 2>/dev/null || grep -q "^### $tool_name" "$claude_file" 2>/dev/null; then
        print_color $YELLOW "Tool $tool_name already documented in $claude_file"
        return
    fi
    
    # Find the Available CLI Tools section and add the new tool
    if grep -q "## Available CLI Tools" "$claude_file" 2>/dev/null; then
        # Create temporary file with new content
        local temp_file=$(mktemp)
        local in_tools_section=false
        local added=false
        
        while IFS= read -r line; do
            echo "$line" >> "$temp_file"
            
            if [[ "$line" == "## Available CLI Tools"* ]]; then
                in_tools_section=true
            elif [[ "$in_tools_section" == true ]] && [[ "$line" == "### "* ]] && [[ "$added" == false ]]; then
                # Add before the first tool subsection
                echo "" >> "$temp_file"
                echo "### $tool_name" >> "$temp_file"
                echo "\`\`\`bash" >> "$temp_file"
                echo "$tool_name [options] arguments" >> "$temp_file"
                echo "\`\`\`" >> "$temp_file"
                echo "$description" >> "$temp_file"
                echo "" >> "$temp_file"
                added=true
            elif [[ "$in_tools_section" == true ]] && [[ "$line" == "## "* ]] && [[ ! "$line" == "## Available CLI Tools"* ]]; then
                # End of tools section
                if [[ "$added" == false ]]; then
                    # Add at the end of tools section
                    echo "" >> "$temp_file"
                    echo "### $tool_name" >> "$temp_file"
                    echo "\`\`\`bash" >> "$temp_file"
                    echo "$tool_name [options] arguments" >> "$temp_file"
                    echo "\`\`\`" >> "$temp_file"
                    echo "$description" >> "$temp_file"
                    added=true
                fi
                in_tools_section=false
            fi
        done < "$claude_file"
        
        mv "$temp_file" "$claude_file"
        print_color $GREEN "Updated $claude_file with $tool_name"
    else
        print_color $YELLOW "Could not find '## Available CLI Tools' section in $claude_file"
    fi
}

if [ "$INSTALL_SCOPE" == "global" ]; then
    CLAUDE_FILE="$HOME/.claude/CLAUDE.md"
    if [ -f "$CLAUDE_FILE" ]; then
        update_claude_md "$CLAUDE_FILE" "$TOOL_NAME"
    else
        print_color $YELLOW "Global CLAUDE.md not found at $CLAUDE_FILE"
    fi
else
    # Project scope - look for CLAUDE.md in current directory or project root
    CLAUDE_FILE="./CLAUDE.md"
    if [ ! -f "$CLAUDE_FILE" ]; then
        CLAUDE_FILE="$SCRIPT_DIR/CLAUDE.md"
    fi
    
    if [ -f "$CLAUDE_FILE" ]; then
        update_claude_md "$CLAUDE_FILE" "$TOOL_NAME"
    else
        print_color $YELLOW "Project CLAUDE.md not found"
    fi
fi

# Step 6: Run tool-specific setup if exists
if [ -f "$TOOL_DIR/setup.sh" ]; then
    print_color $YELLOW "Running tool-specific setup..."
    cd "$TOOL_DIR"
    bash setup.sh
    cd - > /dev/null
fi

print_color $GREEN "✓ Installation complete!"
print_color $GREEN "You can now use: $TOOL_NAME"

# Test the command
if command -v "$TOOL_NAME" &> /dev/null; then
    print_color $GREEN "✓ Command is available in current session"
else
    print_color $YELLOW "Command will be available in new terminal sessions"
    print_color $YELLOW "Or run: source ~/.bashrc (or ~/.zshrc)"
fi
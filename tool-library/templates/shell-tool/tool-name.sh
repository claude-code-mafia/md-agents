#!/bin/bash
# Tool Name - Brief description
#
# This tool does X, Y, and Z.

set -e  # Exit on error

# Default values
OUTPUT=""
JSON_OUTPUT=false
VERBOSE=false
VERSION="1.0.0"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_color() {
    local color=$1
    shift
    [ "$JSON_OUTPUT" = false ] && echo -e "${color}$@${NC}" >&2
}

# Function to show usage
usage() {
    cat << EOF
Usage: $(basename "$0") [OPTIONS] [INPUT]

Brief tool description

Options:
    -o, --output FILE    Output to file (default: stdout)
    --json              Output as JSON
    -v, --verbose       Enable verbose output
    --version          Show version
    -h, --help         Show this help message

Examples:
    $(basename "$0") input.txt
    $(basename "$0") --json data.csv
    $(basename "$0") --output results.txt input.txt

EOF
    exit 0
}

# Function to output JSON
output_json() {
    local status=$1
    local message=$2
    local data=$3
    
    cat << EOF
{
  "status": "$status",
  "message": "$message",
  "data": $data
}
EOF
}

# Parse command line arguments
INPUT=""
while [[ $# -gt 0 ]]; do
    case $1 in
        -o|--output)
            OUTPUT="$2"
            shift 2
            ;;
        --json)
            JSON_OUTPUT=true
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        --version)
            echo "$(basename "$0") version $VERSION"
            exit 0
            ;;
        -h|--help)
            usage
            ;;
        -*)
            echo "Unknown option: $1" >&2
            usage
            ;;
        *)
            INPUT="$1"
            shift
            ;;
    esac
done

# Main logic
main() {
    [ "$VERBOSE" = true ] && print_color "$YELLOW" "Processing input: ${INPUT:-stdin}"
    
    # Check if input file exists (if provided)
    if [ -n "$INPUT" ] && [ ! -f "$INPUT" ]; then
        if [ "$JSON_OUTPUT" = true ]; then
            output_json "error" "File not found: $INPUT" "null"
        else
            print_color "$RED" "Error: File not found: $INPUT"
        fi
        exit 1
    fi
    
    # Process input (TODO: Implement actual logic)
    local result="Tool executed successfully"
    
    # Output results
    if [ "$JSON_OUTPUT" = true ]; then
        output_json "success" "$result" '{"processed": true}'
    else
        print_color "$GREEN" "Status: success"
        echo "Message: $result"
    fi
}

# Run main function and handle output
if [ -n "$OUTPUT" ]; then
    main > "$OUTPUT"
    [ "$VERBOSE" = true ] && print_color "$GREEN" "Output written to: $OUTPUT"
else
    main
fi
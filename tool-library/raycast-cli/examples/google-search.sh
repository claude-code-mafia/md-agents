#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Google Search
# @raycast.mode silent

# Optional parameters:
# @raycast.icon 🔍
# @raycast.packageName Web Search
# @raycast.argument1 { "type": "text", "placeholder": "Search query" }

# Documentation:
# @raycast.description Search Google from Raycast
# @raycast.author Pete
# @raycast.authorURL https://github.com/pete

query="$1"
encoded_query=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$query'))")
open "https://www.google.com/search?q=$encoded_query"
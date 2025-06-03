#!/bin/bash

# Preview the MD Agents documentation site locally

cd "$(dirname "$0")/../docs-site" || exit 1

echo "🚀 Starting MD Agents documentation preview..."
echo ""

# Check if bundle is installed
if ! command -v bundle &> /dev/null; then
    echo "❌ Ruby bundler not found. Please install Ruby and bundler first:"
    echo "   gem install bundler"
    exit 1
fi

# Install dependencies if needed
if [ ! -f "Gemfile.lock" ]; then
    echo "📦 Installing dependencies..."
    bundle install
    echo ""
fi

# Build and serve
echo "🔨 Building site..."
echo "📡 Starting local server..."
echo ""
echo "➡️  View docs at: http://localhost:4000/md-agents/"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

bundle exec jekyll serve --baseurl "/md-agents"
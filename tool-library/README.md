# Tool Library

A collection of useful command-line tools for various tasks.

## Tools

### 1. [Image Generation Tool](./image-gen-tool/)
A simple Python script for generating images using OpenAI's image generation API with sensible defaults.

### 2. [Gmail CLI Tool](./gmail-tool/)
Comprehensive command-line interface for Gmail with advanced features like bulk operations and inbox analysis.

### 3. [Time Tool](./time-tool/)
Network-based accurate time retrieval tool that fetches current time from reliable sources.

### 4. [Grok CLI Tool](./grok-tool/)
Command-line interface for xAI's Grok API, specialized for X/Twitter analysis and uncensored content generation.

## Structure

```
tool-library/
├── README.md                 # This file
├── gmail-tool/              # Gmail CLI with advanced features
│   ├── README.md
│   ├── gmail_cli.py
│   ├── gmail_advanced.py
│   └── setup.sh
├── grok-tool/               # Grok AI CLI for X analysis
│   ├── README.md
│   ├── grok_cli.py
│   └── setup.sh
├── image-gen-tool/          # Image generation tool
│   ├── README.md
│   ├── generate_image.py
│   └── examples/
└── time-tool/               # Current time retrieval
    ├── README.md
    └── get-current-time.sh
```

## Requirements

- Python 3.6+
- OpenAI API key set as environment variable `OPENAI_API_KEY`

## Contributing

Each tool should have:
1. Its own directory
2. A README with usage instructions
3. Minimal dependencies (prefer standard library)
4. Clear error messages
5. Example outputs where applicable
# Grok CLI Tool

A command-line interface for xAI's Grok API, optimized for X/Twitter analysis, Grok's unique personality, and uncensored image generation.

## Purpose

This tool provides direct access to Grok's unique capabilities:
- Real-time X (Twitter) data analysis
- Grok's distinctive, witty personality
- Less restrictive image generation
- Perfect for integration with Claude Code

## Installation

1. Run the setup script:
   ```bash
   ./setup.sh
   ```

2. Set your xAI API key:
   ```bash
   export GROK_API_KEY="your-key-here"
   ```
   
   Get your API key from https://console.x.ai/ (includes $25 free monthly credits)

## Usage

### Basic Chat
```bash
grok chat "What's your take on the latest AI drama?"
grok chat "Roast corporate buzzwords" --style maximum

# Use specific models
grok chat "Explain quantum computing" --model grok-3-mini-fast
```

### X/Twitter Analysis
```bash
# Analyze specific tweets or threads
grok analyze "https://x.com/user/status/123"

# Track real-time discussions
grok track "AI safety" --duration 5m

# Get sentiment analysis
grok sentiment "new iPhone" --posts 100

# Find trending topics
grok trending --category tech
```

### Image Analysis (Vision)
```bash
# Analyze local images with Grok Vision
grok analyze /path/to/image.jpg
grok analyze screenshot.png --json
```

### Image Generation
```bash
# Generate images ($0.07 each) - saves to Desktop by default
grok image "cyberpunk philosopher portrait"

# Multiple variations
grok image "futuristic city" --variations 4

# Save with specific name (still on Desktop)
grok image "mars colony" --output mars.png

# Save to different location
grok image "sunset" --output /path/to/sunset.png
```

### Claude Integration
```bash
# JSON output for easy parsing
grok chat "What's trending?" --json
grok analyze @elonmusk --json
grok trending --json --limit 10
```

### Session Management
```bash
# Maintain conversation context
grok chat "Tell me about X drama" --session myproject
grok chat "What about the responses?" --session myproject
grok session list
grok session clear myproject
```

## Output Examples

### Standard Output
```
$ grok chat "Sum up today's tech news"
╭─ Grok Response ──────────────────────────────╮
│ Oh boy, where do I start? Today's tech news │
│ is like watching a soap opera written by     │
│ robots. We've got [actual summary here]...   │
╰──────────────────────────────────────────────╯
```

### JSON Output (for automation)
```json
{
  "response": "Today's tech drama includes...",
  "model": "grok-beta",
  "usage": {
    "prompt_tokens": 15,
    "completion_tokens": 127,
    "total_tokens": 142
  }
}
```

## Configuration

The tool stores configuration in `~/.grok-cli/`:
- `config.json` - API key and default settings
- `sessions/` - Conversation history for context

Default settings can be modified:
```bash
grok config set default-model grok-beta
grok config set default-style witty
grok config show
```

## Technical Details

- **API**: xAI Grok API (OpenAI-compatible)
- **Available Models**:
  - `grok-2-1212` - Standard Grok 2 model
  - `grok-2-vision-1212` - Vision-enabled (text + image input)
  - `grok-3` - Latest Grok 3 model (default)
  - `grok-3-fast` - Fast variant of Grok 3
  - `grok-3-mini` - Smaller Grok 3 model
  - `grok-3-mini-fast` - Fast variant of mini Grok 3
- **Image Generation**: `grok-2-image-1212` ($0.07 per image)
- **Rate Limits**: 1 request/second, 60-1200 requests/hour
- **Context**: 128,000 tokens
- **Dependencies**: Minimal Python packages for reliability

## Error Handling

The tool handles common errors gracefully:
- Missing API key prompts for setup
- Rate limits trigger automatic retry
- Network errors show clear messages
- Invalid URLs/tweets are validated

## Cost Awareness

- **Chat**: ~$3/million input tokens, $15/million output
- **Free tier**: $25/month during public beta
- **Images**: Pricing varies by size/model

## Integration with Claude Code

This tool is designed to complement Claude Code:
- Use `--json` flag for structured output
- Grok provides real-time X data that Claude can't access
- Combine Claude's reasoning with Grok's current information
- Let Grok generate images that Claude can then analyze
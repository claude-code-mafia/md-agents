# Image Generation Tool

A simple, fast command-line tool for generating images using OpenAI's image generation API.

## Features

- **Single parameter**: Just provide the prompt
- **Opinionated defaults**: Optimized for speed and cost
- **Auto-naming**: Files are timestamped automatically
- **No dependencies**: Uses only Python standard library

## Installation

1. Ensure you have Python 3.6+ installed
2. Set your OpenAI API key:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

## Usage

```bash
python generate_image.py "your image description here"
```

### Examples

```bash
# Generate a sunset
python generate_image.py "a beautiful sunset over the ocean"

# Generate a logo
python generate_image.py "minimalist tech company logo"

# Generate art
python generate_image.py "abstract watercolor painting in blue and gold"
```

## Configuration

The tool uses these opinionated defaults:
- **Model**: `gpt-image-1` (fastest model)
- **Quality**: `low` (optimized for speed and cost)
- **Size**: `1024x1024`
- **Output**: PNG format in current directory

## Output

Images are saved with the naming pattern: `generated_YYYYMMDD_HHMMSS.png`

## Error Handling

The script provides clear error messages for:
- Missing API key
- Network issues
- API errors
- Invalid responses

## Cost Optimization

This tool is configured for maximum efficiency:
- Uses the fastest model (`gpt-image-1`)
- Low quality setting reduces cost by ~50%
- Single image generation per call

## Future Enhancements

Potential improvements while keeping simplicity:
- [ ] Add `--quality` flag for occasional high-quality needs
- [ ] Add `--output` flag for custom filenames
- [ ] Add batch generation support
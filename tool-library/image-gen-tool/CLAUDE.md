# Image Generation Tool Instructions

## Tool Purpose
This tool provides fast, low-cost image generation using OpenAI's API. It's designed for quick prototyping and testing rather than production-quality images.

## Usage Guidelines

### When to Use Automatically
- User requests "quick image", "test image", or mentions cost consciousness
- Prototyping visual concepts
- Generating placeholder images
- Multiple images needed (due to low cost)

### When to Suggest Alternatives
- User needs "high quality" or "production" images → Suggest MCP OpenAI server
- User needs specific dimensions beyond 1024x1024 → Mention limitation

## Tool Maintenance

### Code Standards
- Keep it simple - single file, minimal dependencies
- Maintain Python 3 compatibility (3.8+)
- Use only standard library + OpenAI SDK
- Clear error messages for common failures (API key, network, etc.)

### Configuration
- Model: `dall-e-2` (hardcoded for cost efficiency)
- Size: `1024x1024` (optimal cost/quality balance)
- Quality: `standard` (not configurable in DALL-E 2)
- Never change these without discussing cost implications

### Error Handling
Current error scenarios handled:
- Missing OPENAI_API_KEY
- Network failures
- API quota exceeded
- Invalid prompts

## Output Conventions
- Filename format: `generated_YYYYMMDD_HHMMSS.png`
- Always save to current directory (controlled by CLAUDE.md global instruction)
- Print only the filename on success
- Print clear error messages on failure

## Integration Notes
- This tool is meant to be composed with other Unix tools
- Output is designed for piping: `generate_image.py "cat" | xargs open`
- Exits with proper codes: 0 for success, 1 for failure

## Testing Requirements
When modifying:
1. Test with various prompt lengths (1 word to 100+ words)
2. Test without API key set
3. Test with invalid API key
4. Ensure filename format remains consistent

## Cost Awareness
- DALL-E 2: ~$0.02 per image
- DALL-E 3: ~$0.04-0.08 per image (not used here)
- Always inform user this is the "low-cost" option

## Future Considerations
If upgrading to DALL-E 3:
- Update cost documentation
- Add size parameter options
- Consider quality parameter
- Maintain backward compatibility
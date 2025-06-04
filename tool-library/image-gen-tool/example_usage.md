# Example Usage from Claude Code

When you want to generate an image through Claude Code, simply say something like:

- "Generate an image of a sunset"
- "Create an image of a red apple"
- "Make me a picture of a futuristic city"

Claude Code will then run:
```bash
python ~/Projects/tool-library/image-gen-tool/generate_image.py "your description"
```

The image will be saved in the current directory with a timestamp.

## Quick Test

To test the tool is working:
```bash
python ~/Projects/tool-library/image-gen-tool/generate_image.py "test image: simple geometric shapes"
```
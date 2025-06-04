#!/usr/bin/env python3
"""
Simple image generator with opinionated defaults.
Usage: python generate_image.py "your prompt here"
"""

import os
import sys
import json
import base64
import urllib.request
import urllib.error
from datetime import datetime

def generate_image(prompt):
    """Generate an image with sensible defaults"""
    
    # Get API key from environment
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        sys.exit(1)
    
    # Opinionated defaults - optimized for speed and cost
    payload = {
        "model": "gpt-image-1",
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024",
        "quality": "low"  # Fast and cheap
    }
    
    # Make the API call
    try:
        # Prepare the request
        url = "https://api.openai.com/v1/images/generations"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        # Convert payload to JSON
        data = json.dumps(payload).encode('utf-8')
        
        # Create and send request
        req = urllib.request.Request(url, data=data, headers=headers)
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
        
        # Extract base64 image
        image_b64 = result["data"][0]["b64_json"]
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"generated_{timestamp}.png"
        
        # Save to current directory
        with open(filename, "wb") as f:
            f.write(base64.b64decode(image_b64))
        
        print(f"Image saved: {filename}")
        return filename
        
    except urllib.error.HTTPError as e:
        print(f"Error generating image: HTTP {e.code} - {e.reason}")
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Error connecting to API: {e.reason}")
        sys.exit(1)
    except KeyError:
        print("Error: Unexpected API response format")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Get prompt from command line arguments
    if len(sys.argv) < 2:
        print("Usage: python generate_image.py \"your prompt here\"")
        sys.exit(1)
    
    prompt = " ".join(sys.argv[1:])
    generate_image(prompt)
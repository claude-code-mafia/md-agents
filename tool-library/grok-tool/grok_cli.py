#!/Users/pete/Projects/tool-library/grok-tool/venv/bin/python
"""
Grok CLI Tool - Command-line interface for xAI's Grok API
Optimized for X/Twitter analysis, unique personality, and image generation
"""

import os
import sys
import json
import time
import click
import httpx
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any
from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Rich console
console = Console()

# Configuration
CONFIG_DIR = Path.home() / ".grok-cli"
CONFIG_FILE = CONFIG_DIR / "config.json"
SESSIONS_DIR = CONFIG_DIR / "sessions"
API_BASE_URL = "https://api.x.ai/v1"
# Available models based on xAI dashboard
TEXT_MODELS = {
    "grok-2-1212": "Standard Grok 2 model",
    "grok-2-vision-1212": "Vision-enabled Grok 2 (text + image input)",
    "grok-3": "Latest Grok 3 model",
    "grok-3-fast": "Fast variant of Grok 3",
    "grok-3-mini": "Smaller Grok 3 model",
    "grok-3-mini-fast": "Fast variant of mini Grok 3"
}

DEFAULT_MODEL = "grok-3"
DEFAULT_IMAGE_MODEL = "grok-2-image-1212"  # $0.07 per image
DESKTOP_PATH = Path.home() / "Desktop"

class GrokCLI:
    """Main Grok CLI class"""
    
    def __init__(self):
        self.config = self.load_config()
        self.api_key = self.get_api_key()
        self.client = None
        if self.api_key:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=API_BASE_URL
            )
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        return {
            "default_model": DEFAULT_MODEL,
            "default_style": "witty",
            "image_size": "1024x1024"
        }
    
    def save_config(self):
        """Save configuration to file"""
        CONFIG_DIR.mkdir(exist_ok=True)
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get_api_key(self) -> Optional[str]:
        """Get API key from environment or config"""
        # First check environment
        api_key = os.getenv("GROK_API_KEY")
        if api_key:
            return api_key
        
        # Then check config file
        if "api_key" in self.config:
            return self.config["api_key"]
        
        return None
    
    def setup_api_key(self) -> str:
        """Interactive API key setup"""
        console.print("\n[yellow]No API key found![/yellow]")
        console.print("Get your API key from https://console.x.ai/")
        console.print("You get $25 of free API credits per month!\n")
        
        api_key = click.prompt("Enter your Grok API key", hide_input=True)
        
        # Test the API key
        test_client = OpenAI(api_key=api_key, base_url=API_BASE_URL)
        try:
            test_client.chat.completions.create(
                model=DEFAULT_MODEL,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5
            )
            console.print("[green]✓ API key validated successfully![/green]")
            
            # Save to config
            self.config["api_key"] = api_key
            self.save_config()
            console.print(f"[green]✓ API key saved to {CONFIG_FILE}[/green]")
            
            return api_key
            
        except Exception as e:
            console.print(f"[red]✗ Invalid API key: {e}[/red]")
            sys.exit(1)
    
    def ensure_client(self):
        """Ensure API client is initialized"""
        if not self.client:
            if not self.api_key:
                self.api_key = self.setup_api_key()
            self.client = OpenAI(api_key=self.api_key, base_url=API_BASE_URL)
    
    def load_session(self, session_name: str) -> List[Dict[str, str]]:
        """Load conversation session"""
        SESSIONS_DIR.mkdir(exist_ok=True)
        session_file = SESSIONS_DIR / f"{session_name}.json"
        
        if session_file.exists():
            with open(session_file, 'r') as f:
                return json.load(f)
        return []
    
    def save_session(self, session_name: str, messages: List[Dict[str, str]]):
        """Save conversation session"""
        SESSIONS_DIR.mkdir(exist_ok=True)
        session_file = SESSIONS_DIR / f"{session_name}.json"
        
        # Keep only last 10 messages for context
        messages = messages[-20:]  # 10 user + 10 assistant
        
        with open(session_file, 'w') as f:
            json.dump(messages, f, indent=2)
    
    def stream_chat(self, messages: List[Dict[str, str]], model: str = None) -> str:
        """Stream chat completion"""
        self.ensure_client()
        
        model = model or self.config.get("default_model", DEFAULT_MODEL)
        
        try:
            stream = self.client.chat.completions.create(
                model=model,
                messages=messages,
                stream=True,
                temperature=0.7
            )
            
            response_text = ""
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    response_text += content
                    console.print(content, end="")
            
            return response_text
            
        except Exception as e:
            if "rate_limit" in str(e).lower():
                console.print("\n[yellow]Rate limit hit. Waiting 2 seconds...[/yellow]")
                time.sleep(2)
                return self.stream_chat(messages, model)
            else:
                raise e


# Create CLI app
cli = GrokCLI()

@click.group()
def main():
    """Grok CLI - Access xAI's Grok for X analysis, chat, and images"""
    pass

@main.command()
@click.argument('prompt')
@click.option('--style', default=None, help='Response style (witty, serious, maximum)')
@click.option('--session', default=None, help='Session name for context')
@click.option('--json', 'output_json', is_flag=True, help='Output as JSON')
@click.option('--model', default=None, type=click.Choice(list(TEXT_MODELS.keys())), help='Model to use')
def chat(prompt: str, style: str, session: str, output_json: bool, model: str):
    """Chat with Grok"""
    
    messages = []
    
    # Load session if specified
    if session:
        messages = cli.load_session(session)
    
    # Add system message for style
    if style or cli.config.get("default_style"):
        style = style or cli.config.get("default_style")
        style_prompts = {
            "witty": "Be witty, sarcastic, and clever. Don't hold back on the sass.",
            "serious": "Be direct and professional. Skip the jokes.",
            "maximum": "Turn the sass up to 11. Roast everything playfully."
        }
        if style in style_prompts:
            messages.insert(0, {"role": "system", "content": style_prompts[style]})
    
    # Use vision model if specified
    if model == "grok-2-vision-1212":
        console.print("[yellow]Note: Vision model selected. To analyze images, include image URLs in your prompt.[/yellow]")
    
    # Add user message
    messages.append({"role": "user", "content": prompt})
    
    if output_json:
        # Non-streaming for JSON output
        cli.ensure_client()
        response = cli.client.chat.completions.create(
            model=model or cli.config.get("default_model", DEFAULT_MODEL),
            messages=messages,
            temperature=0.7
        )
        
        result = {
            "response": response.choices[0].message.content,
            "model": response.model,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
        }
        
        if session:
            messages.append({"role": "assistant", "content": result["response"]})
            cli.save_session(session, messages)
        
        print(json.dumps(result, indent=2))
    else:
        # Streaming output with Rich formatting
        console.print(Panel.fit("Grok Response", style="cyan"))
        response_text = cli.stream_chat(messages, model)
        console.print()  # New line after streaming
        
        if session:
            messages.append({"role": "assistant", "content": response_text})
            cli.save_session(session, messages)

@main.command()
@click.argument('input_path')
@click.option('--json', 'output_json', is_flag=True, help='Output as JSON')
def analyze(input_path: str, output_json: bool):
    """Analyze a tweet/X thread OR an image file"""
    
    # Check if it's a file path or URL
    path = Path(input_path)
    
    if path.exists() and path.is_file():
        # It's an image file - use vision model
        if path.suffix.lower() not in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
            console.print("[red]Error: Only image files (jpg, png, gif, webp) are supported[/red]")
            sys.exit(1)
        
        # Read and encode image
        import base64
        with open(path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')
        
        prompt = "Analyze this image and describe what you see in detail."
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/{path.suffix[1:]};base64,{image_data}"}}
                ]
            }
        ]
        
        model = "grok-2-vision-1212"  # Use vision model for images
        
        if output_json:
            cli.ensure_client()
            response = cli.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.3
            )
            
            result = {
                "file": str(path),
                "analysis": response.choices[0].message.content,
                "model": model,
                "timestamp": datetime.now().isoformat()
            }
            print(json.dumps(result, indent=2))
        else:
            console.print(Panel.fit(f"Analyzing Image: {path.name}", style="cyan"))
            cli.stream_chat(messages, model)
            console.print()
    
    elif input_path.startswith("https://x.com/") or input_path.startswith("https://twitter.com/"):
        # It's a Twitter/X URL
        url = input_path
        
        prompt = f"""Analyze this X/Twitter post: {url}

1. Summary of the content
2. Key points or arguments made
3. Overall sentiment (positive/negative/neutral)
4. Engagement metrics interpretation (if visible)
5. Notable replies or quote tweets (if it's a thread)

Be concise but thorough."""

        messages = [
            {"role": "system", "content": "You are analyzing X (Twitter) content. You have access to real-time X data."},
            {"role": "user", "content": prompt}
        ]
        
        if output_json:
            cli.ensure_client()
            response = cli.client.chat.completions.create(
                model=cli.config.get("default_model", DEFAULT_MODEL),
                messages=messages,
                temperature=0.3  # Lower temp for analysis
            )
            
            # Parse response into structured format
            content = response.choices[0].message.content
            result = {
                "url": url,
                "analysis": content,
                "model": response.model,
                "timestamp": datetime.now().isoformat()
            }
            print(json.dumps(result, indent=2))
        else:
            console.print(Panel.fit(f"Analyzing: {url}", style="cyan"))
            cli.stream_chat(messages)
            console.print()
    else:
        console.print("[red]Error: Please provide a valid X/Twitter URL or image file path[/red]")
        sys.exit(1)

@main.command()
@click.option('--category', default=None, help='Category (tech, news, crypto, etc.)')
@click.option('--limit', default=10, help='Number of trends to show')
@click.option('--json', 'output_json', is_flag=True, help='Output as JSON')
def trending(category: str, limit: int, output_json: bool):
    """Get trending topics on X"""
    
    prompt = f"What's trending on X (Twitter) right now"
    if category:
        prompt += f" in the {category} category"
    prompt += f"? Give me the top {limit} trending topics with brief context for each."
    
    messages = [
        {"role": "system", "content": "You have real-time access to X trending data. Be specific and current."},
        {"role": "user", "content": prompt}
    ]
    
    if output_json:
        cli.ensure_client()
        response = cli.client.chat.completions.create(
            model=cli.config.get("default_model", DEFAULT_MODEL),
            messages=messages,
            temperature=0.3
        )
        
        result = {
            "trends": response.choices[0].message.content,
            "category": category,
            "limit": limit,
            "timestamp": datetime.now().isoformat()
        }
        print(json.dumps(result, indent=2))
    else:
        console.print(Panel.fit(f"X Trending" + (f" - {category}" if category else ""), style="cyan"))
        cli.stream_chat(messages)
        console.print()

@main.command()
@click.argument('keyword')
@click.option('--duration', default="5m", help='Duration to track (e.g., 5m, 1h)')
@click.option('--json', 'output_json', is_flag=True, help='Output as JSON')
def track(keyword: str, duration: str, output_json: bool):
    """Track real-time discussions about a keyword"""
    
    prompt = f"""Track real-time discussions about "{keyword}" on X over the last {duration}.

Provide:
1. Volume of posts
2. Key influencers discussing it
3. Overall sentiment
4. Main themes or arguments
5. Any breaking news or developments"""

    messages = [
        {"role": "system", "content": "You have real-time access to X data. Focus on the most recent and relevant posts."},
        {"role": "user", "content": prompt}
    ]
    
    if output_json:
        cli.ensure_client()
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True
        ) as progress:
            progress.add_task(description=f"Tracking '{keyword}'...", total=None)
            
            response = cli.client.chat.completions.create(
                model=cli.config.get("default_model", DEFAULT_MODEL),
                messages=messages,
                temperature=0.3
            )
        
        result = {
            "keyword": keyword,
            "duration": duration,
            "analysis": response.choices[0].message.content,
            "timestamp": datetime.now().isoformat()
        }
        print(json.dumps(result, indent=2))
    else:
        console.print(Panel.fit(f"Tracking: {keyword}", style="cyan"))
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True
        ) as progress:
            progress.add_task(description="Analyzing real-time data...", total=None)
            time.sleep(1)  # Simulate processing
        
        cli.stream_chat(messages)
        console.print()

@main.command()
@click.argument('topic')
@click.option('--posts', default=100, help='Number of posts to analyze')
@click.option('--json', 'output_json', is_flag=True, help='Output as JSON')
def sentiment(topic: str, posts: int, output_json: bool):
    """Analyze sentiment around a topic"""
    
    prompt = f"""Analyze the sentiment around "{topic}" on X based on approximately {posts} recent posts.

Provide:
1. Overall sentiment breakdown (positive/negative/neutral percentages)
2. Key positive themes
3. Key negative themes  
4. Notable opinions or hot takes
5. Influencer sentiment vs general public"""

    messages = [
        {"role": "system", "content": "You have access to real-time X sentiment data. Be data-driven and specific."},
        {"role": "user", "content": prompt}
    ]
    
    if output_json:
        cli.ensure_client()
        response = cli.client.chat.completions.create(
            model=cli.config.get("default_model", DEFAULT_MODEL),
            messages=messages,
            temperature=0.3
        )
        
        result = {
            "topic": topic,
            "posts_analyzed": posts,
            "sentiment_analysis": response.choices[0].message.content,
            "timestamp": datetime.now().isoformat()
        }
        print(json.dumps(result, indent=2))
    else:
        console.print(Panel.fit(f"Sentiment Analysis: {topic}", style="cyan"))
        cli.stream_chat(messages)
        console.print()

@main.command()
@click.argument('prompt')
@click.option('--variations', default=1, help='Number of variations')
@click.option('--size', default="1024x1024", help='Image size (default: 1024x1024)')
@click.option('--output', default=None, help='Output filename (default: saves to Desktop)')
@click.option('--json', 'output_json', is_flag=True, help='Output as JSON')
def image(prompt: str, variations: int, size: str, output: str, output_json: bool):
    """Generate images with Grok-2 ($0.07 per image)"""
    
    cli.ensure_client()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Default to Desktop if no output specified
    if not output:
        output_path = DESKTOP_PATH / f"grok_image_{timestamp}.png"
    else:
        # If output is just a filename, save to Desktop
        output_path = Path(output)
        if not output_path.is_absolute():
            output_path = DESKTOP_PATH / output
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True
        ) as progress:
            progress.add_task(description="Generating image...", total=None)
            
            # Using the image generation endpoint
            response = httpx.post(
                f"{API_BASE_URL}/images/generations",
                headers={
                    "Authorization": f"Bearer {cli.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": DEFAULT_IMAGE_MODEL,
                    "prompt": prompt,
                    "n": variations
                },
                timeout=60.0
            )
            
            if response.status_code != 200:
                error_data = response.json()
                raise Exception(f"API Error: {error_data}")
            
            result = response.json()
        
        # Download and save images regardless of output mode
        saved_paths = []
        for i, img_data in enumerate(result.get("data", [])):
            if "url" in img_data:
                # Download image
                img_response = httpx.get(img_data["url"])
                if img_response.status_code == 200:
                    if variations == 1:
                        save_path = output_path
                    else:
                        # Multiple variations: add index
                        save_path = output_path.parent / f"{output_path.stem}_{i+1}{output_path.suffix}"
                    
                    save_path.write_bytes(img_response.content)
                    saved_paths.append(str(save_path))
                    if not output_json:
                        console.print(f"Saved: {save_path}")
            elif "b64_json" in img_data:
                # Base64 encoded image
                import base64
                img_bytes = base64.b64decode(img_data["b64_json"])
                if variations == 1:
                    save_path = output_path
                else:
                    save_path = output_path.parent / f"{output_path.stem}_{i+1}{output_path.suffix}"
                
                save_path.write_bytes(img_bytes)
                saved_paths.append(str(save_path))
                if not output_json:
                    console.print(f"Saved: {save_path}")
        
        if output_json:
            output_result = {
                "prompt": prompt,
                "variations": variations,
                "size": size,
                "model": DEFAULT_IMAGE_MODEL,
                "cost": f"${0.07 * variations:.2f}",
                "images": result.get("data", []),
                "saved_files": saved_paths,
                "output_path": str(output_path) if variations == 1 else str(DESKTOP_PATH)
            }
            print(json.dumps(output_result, indent=2))
        else:
            console.print(Panel.fit("Image Generation Complete", style="green"))
            console.print(f"Model: {DEFAULT_IMAGE_MODEL} ($0.07 per image)")
            console.print(f"Generated {variations} image(s)")
            console.print(f"Total cost: ${0.07 * variations:.2f}")
    
    except Exception as e:
        if output_json:
            error_result = {
                "error": str(e),
                "prompt": prompt,
                "model": DEFAULT_IMAGE_MODEL
            }
            print(json.dumps(error_result, indent=2))
        else:
            console.print(f"[red]Error generating image: {e}[/red]")

@main.group()
def session():
    """Manage conversation sessions"""
    pass

@session.command('list')
def session_list():
    """List all sessions"""
    SESSIONS_DIR.mkdir(exist_ok=True)
    sessions = list(SESSIONS_DIR.glob("*.json"))
    
    if not sessions:
        console.print("No sessions found.")
        return
    
    console.print(Panel.fit("Conversation Sessions", style="cyan"))
    for session_file in sessions:
        name = session_file.stem
        modified = datetime.fromtimestamp(session_file.stat().st_mtime)
        console.print(f"  • {name} (modified: {modified.strftime('%Y-%m-%d %H:%M')})")

@session.command('clear')
@click.argument('name')
def session_clear(name: str):
    """Clear a session"""
    session_file = SESSIONS_DIR / f"{name}.json"
    if session_file.exists():
        session_file.unlink()
        console.print(f"[green]✓ Session '{name}' cleared[/green]")
    else:
        console.print(f"[yellow]Session '{name}' not found[/yellow]")

@main.group()
def config():
    """Manage configuration"""
    pass

@config.command('set')
@click.argument('key')
@click.argument('value')
def config_set(key: str, value: str):
    """Set a configuration value"""
    cli.config[key] = value
    cli.save_config()
    console.print(f"[green]✓ Set {key} = {value}[/green]")

@config.command('show')
def config_show():
    """Show current configuration"""
    console.print(Panel.fit("Grok CLI Configuration", style="cyan"))
    
    # Don't show the API key
    safe_config = cli.config.copy()
    if "api_key" in safe_config:
        safe_config["api_key"] = "***" + safe_config["api_key"][-4:]
    
    for key, value in safe_config.items():
        console.print(f"  {key}: {value}")

if __name__ == '__main__':
    main()
"""Authentication handling for Typefully CLI."""

import click
from typing import Optional

from .config import Config
from .api import TypefullyAPI


def setup_auth(api_key: Optional[str] = None) -> bool:
    """Set up authentication with Typefully API.
    
    Args:
        api_key: API key to use. If None, will prompt user.
    
    Returns:
        True if authentication was successful, False otherwise.
    """
    config = Config()
    
    if not api_key:
        # Check if we already have a key
        existing_key = config.get_api_key()
        if existing_key:
            click.echo("Found existing API key.")
            if not click.confirm("Do you want to replace it?"):
                return True
        
        # Prompt for API key
        click.echo("\nTo get your Typefully API key:")
        click.echo("1. Log in to https://typefully.com")
        click.echo("2. Go to Settings > API & Integrations")
        click.echo("3. Generate or copy your API key\n")
        
        api_key = click.prompt("Enter your API key", hide_input=True)
    
    if not api_key or not api_key.strip():
        click.echo("Error: API key cannot be empty.", err=True)
        return False
    
    # Validate the API key by making a test request
    api = TypefullyAPI(api_key.strip())
    
    click.echo("Validating API key...")
    if api.validate_key():
        config.set_api_key(api_key.strip())
        click.echo("✓ Authentication successful!")
        return True
    else:
        click.echo("✗ Invalid API key. Please check your key and try again.", err=True)
        return False


def get_api_client() -> Optional[TypefullyAPI]:
    """Get an authenticated API client.
    
    Returns:
        TypefullyAPI instance if authenticated, None otherwise.
    """
    config = Config()
    api_key = config.get_api_key()
    
    if not api_key:
        click.echo("Error: No API key found. Please run 'typefully auth' first.", err=True)
        return None
    
    return TypefullyAPI(api_key)
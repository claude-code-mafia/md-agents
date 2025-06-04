#!/usr/bin/env python3
"""Typefully CLI - Command-line interface for Typefully API."""

import sys
import warnings
from typing import Optional

# Suppress urllib3 warnings about OpenSSL
warnings.filterwarnings('ignore', message='urllib3 v2 only supports OpenSSL')

import click
import requests

from typefully import __version__
from typefully.auth import setup_auth, get_api_client
from typefully.config import Config
from typefully.utils import (
    output_json, output_drafts_table, output_notifications_table,
    handle_api_error, parse_schedule_date
)


@click.group()
@click.version_option(version=__version__, prog_name='typefully')
@click.pass_context
def cli(ctx):
    """Typefully CLI - Create and manage Twitter/X content from the command line."""
    ctx.ensure_object(dict)


@cli.command()
@click.option('--key', '-k', help='API key (will prompt if not provided)')
def auth(key: Optional[str]):
    """Set up authentication with Typefully API."""
    success = setup_auth(key)
    sys.exit(0 if success else 1)


@cli.command()
@click.argument('content', required=False)
@click.option('--stdin', is_flag=True, help='Read content from stdin')
@click.option('--threadify', is_flag=True, help='Auto-split long content into thread')
@click.option('--share', is_flag=True, help='Generate a share URL')
@click.option('--schedule', help='Schedule date/time or "next" for next slot')
@click.option('--auto-retweet', is_flag=True, help='Enable auto-retweet')
@click.option('--auto-plug', is_flag=True, help='Enable auto-plug')
@click.option('--platform', type=click.Choice(['twitter', 'linkedin']), help='Target platform (experimental)')
@click.option('--json', 'output_json_flag', is_flag=True, help='Output as JSON')
def create(content: Optional[str], stdin: bool, threadify: bool, share: bool,
          schedule: Optional[str], auto_retweet: bool, auto_plug: bool,
          platform: Optional[str], output_json_flag: bool):
    """Create a new draft tweet or thread.
    
    Examples:
    
        # Simple tweet
        typefully create "Hello from the CLI!"
        
        # Thread (use 4 newlines)
        typefully create "First tweet
        
        
        
        Second tweet"
        
        # Auto-threadify long content
        typefully create "Very long content..." --threadify
        
        # Schedule for specific time
        typefully create "Scheduled tweet" --schedule "2025-01-07 10:00"
        
        # Schedule to next available slot
        typefully create "Auto-scheduled" --schedule next
        
        # Read from stdin
        echo "Tweet content" | typefully create --stdin
    """
    # Get content from stdin if requested
    if stdin:
        content = sys.stdin.read().strip()
    
    if not content:
        click.echo("Error: No content provided. Use --stdin or provide content as argument.", err=True)
        sys.exit(1)
    
    # Get API client
    api = get_api_client()
    if not api:
        sys.exit(1)
    
    try:
        # Parse schedule date if provided
        schedule_date = None
        if schedule:
            schedule_date = parse_schedule_date(schedule)
        
        # Create draft
        result = api.create_draft(
            content=content,
            threadify=threadify,
            share=share,
            schedule_date=schedule_date,
            auto_retweet_enabled=auto_retweet,
            auto_plug_enabled=auto_plug,
            platform=platform
        )
        
        if output_json_flag:
            output_json(result)
        else:
            click.echo("✓ Draft created successfully!")
            
            if result.get('id'):
                click.echo(f"  ID: {result['id']}")
            
            if result.get('share_url'):
                click.echo(f"  Share URL: {result['share_url']}")
            
            if schedule:
                if schedule.lower() == 'next':
                    click.echo("  Scheduled to next available slot")
                else:
                    click.echo(f"  Scheduled for: {schedule}")
    
    except ValueError as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)
    except requests.HTTPError as e:
        handle_api_error(e)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@cli.group()
def list():
    """List drafts (scheduled or published)."""
    pass


@list.command('scheduled')
@click.option('--filter', 'content_filter', type=click.Choice(['threads', 'tweets']),
              help='Filter by content type')
@click.option('--json', 'output_json_flag', is_flag=True, help='Output as JSON')
def list_scheduled(content_filter: Optional[str], output_json_flag: bool):
    """List recently scheduled drafts."""
    api = get_api_client()
    if not api:
        sys.exit(1)
    
    try:
        drafts = api.get_scheduled_drafts(content_filter)
        
        if output_json_flag:
            output_json(drafts)
        else:
            output_drafts_table(drafts, "Scheduled Drafts")
    
    except requests.HTTPError as e:
        handle_api_error(e)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@list.command('published')
@click.option('--json', 'output_json_flag', is_flag=True, help='Output as JSON')
def list_published(output_json_flag: bool):
    """List recently published drafts."""
    api = get_api_client()
    if not api:
        sys.exit(1)
    
    try:
        drafts = api.get_published_drafts()
        
        if output_json_flag:
            output_json(drafts)
        else:
            output_drafts_table(drafts, "Published Drafts")
    
    except requests.HTTPError as e:
        handle_api_error(e)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@cli.group()
def notifications():
    """Manage notifications."""
    pass


@notifications.command('view')
@click.option('--kind', type=click.Choice(['inbox', 'activity']),
              help='Filter by notification type')
@click.option('--json', 'output_json_flag', is_flag=True, help='Output as JSON')
def notifications_view(kind: Optional[str], output_json_flag: bool):
    """View notifications."""
    api = get_api_client()
    if not api:
        sys.exit(1)
    
    try:
        notifs = api.get_notifications(kind)
        
        if output_json_flag:
            output_json(notifs)
        else:
            output_notifications_table(notifs)
    
    except requests.HTTPError as e:
        handle_api_error(e)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@notifications.command('mark-read')
@click.option('--kind', type=click.Choice(['inbox', 'activity']),
              help='Filter by notification type')
@click.option('--username', help='Filter by specific username')
def notifications_mark_read(kind: Optional[str], username: Optional[str]):
    """Mark all notifications as read."""
    api = get_api_client()
    if not api:
        sys.exit(1)
    
    try:
        api.mark_notifications_read(kind, username)
        click.echo("✓ Notifications marked as read.")
    
    except requests.HTTPError as e:
        handle_api_error(e)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@cli.group()
def config():
    """Manage configuration settings."""
    pass


@config.command('get')
@click.argument('key', required=False)
def config_get(key: Optional[str]):
    """Get configuration value(s)."""
    cfg = Config()
    
    if key:
        value = cfg.get(key)
        if value is not None:
            click.echo(f"{key}: {value}")
        else:
            click.echo(f"Key '{key}' not found.", err=True)
            sys.exit(1)
    else:
        # Show all config (excluding sensitive data)
        config_data = cfg._config.copy()
        if 'api_key' in config_data:
            config_data['api_key'] = '***' + config_data['api_key'][-4:]
        output_json(config_data)


@config.command('set')
@click.argument('key')
@click.argument('value')
def config_set(key: str, value: str):
    """Set configuration value."""
    if key == 'api_key':
        click.echo("Error: Use 'typefully auth' to set API key.", err=True)
        sys.exit(1)
    
    cfg = Config()
    cfg.set(key, value)
    click.echo(f"✓ Set {key} = {value}")


@config.command('clear')
@click.confirmation_option(prompt='Are you sure you want to clear all configuration?')
def config_clear():
    """Clear all configuration."""
    cfg = Config()
    cfg.clear()
    click.echo("✓ Configuration cleared.")


# Convenience shortcuts for common commands
@cli.command('scheduled', hidden=True)
@click.pass_context
def scheduled_shortcut(ctx):
    """Shortcut for 'list scheduled'."""
    ctx.invoke(list_scheduled)


@cli.command('published', hidden=True)
@click.pass_context
def published_shortcut(ctx):
    """Shortcut for 'list published'."""
    ctx.invoke(list_published)


if __name__ == '__main__':
    cli()
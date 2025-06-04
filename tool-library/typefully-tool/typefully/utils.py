"""Utility functions for Typefully CLI."""

import json
import sys
from datetime import datetime
from typing import Any, List, Dict

import click
from dateutil import parser as date_parser
from rich.console import Console
from rich.table import Table
from rich.text import Text


console = Console()


def format_date(date_string: str) -> str:
    """Format ISO date string to human-readable format.
    
    Args:
        date_string: ISO format date string
    
    Returns:
        Human-readable date string
    """
    try:
        dt = date_parser.parse(date_string)
        return dt.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return date_string


def truncate_text(text: str, max_length: int = 50) -> str:
    """Truncate text with ellipsis if too long.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
    
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def output_json(data: Any):
    """Output data as JSON to stdout.
    
    Args:
        data: Data to output as JSON
    """
    click.echo(json.dumps(data, indent=2, default=str))


def output_drafts_table(drafts: List[Dict[str, Any]], title: str = "Drafts"):
    """Output drafts as a formatted table.
    
    Args:
        drafts: List of draft dictionaries
        title: Table title
    """
    if not drafts:
        click.echo(f"No {title.lower()} found.")
        return
    
    table = Table(title=title, show_lines=True)
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Content", style="white")
    table.add_column("Type", style="yellow")
    table.add_column("Scheduled", style="green")
    table.add_column("Status", style="magenta")
    
    for draft in drafts:
        # Extract content preview
        content = draft.get('content', '')
        content_preview = truncate_text(content.replace('\n', ' '), 60)
        
        # Determine type
        is_thread = '\n\n\n\n' in content or draft.get('is_thread', False)
        draft_type = "Thread" if is_thread else "Tweet"
        
        # Format scheduled date
        scheduled_at = draft.get('scheduled_at', '')
        if scheduled_at:
            scheduled_at = format_date(scheduled_at)
        
        # Status
        status = draft.get('status', 'unknown')
        
        table.add_row(
            str(draft.get('id', 'N/A')),
            content_preview,
            draft_type,
            scheduled_at or 'Not scheduled',
            status
        )
    
    console.print(table)


def output_notifications_table(notifications: List[Dict[str, Any]]):
    """Output notifications as a formatted table.
    
    Args:
        notifications: List of notification dictionaries
    """
    if not notifications:
        click.echo("No notifications found.")
        return
    
    table = Table(title="Notifications", show_lines=True)
    table.add_column("Type", style="cyan", no_wrap=True)
    table.add_column("From", style="yellow")
    table.add_column("Message", style="white")
    table.add_column("Time", style="green")
    
    for notif in notifications:
        notif_type = notif.get('type', 'unknown')
        from_user = notif.get('from_username', 'System')
        message = truncate_text(notif.get('message', ''), 60)
        created_at = format_date(notif.get('created_at', ''))
        
        table.add_row(
            notif_type,
            from_user,
            message,
            created_at
        )
    
    console.print(table)


def handle_api_error(error: Exception):
    """Handle API errors with user-friendly messages.
    
    Args:
        error: The exception that occurred
    """
    if hasattr(error, 'response') and error.response is not None:
        status_code = error.response.status_code
        
        if status_code == 401:
            click.echo("Error: Invalid API key. Please run 'typefully auth' to update.", err=True)
        elif status_code == 403:
            click.echo("Error: Access forbidden. Check your API permissions.", err=True)
        elif status_code == 404:
            click.echo("Error: Resource not found.", err=True)
        elif status_code == 429:
            click.echo("Error: Rate limit exceeded. Please try again later.", err=True)
        elif status_code >= 500:
            click.echo(f"Error: Typefully server error ({status_code}). Please try again later.", err=True)
        else:
            try:
                error_data = error.response.json()
                message = error_data.get('message', 'Unknown error')
                click.echo(f"Error: {message}", err=True)
            except Exception:
                click.echo(f"Error: HTTP {status_code}", err=True)
    else:
        click.echo(f"Error: {str(error)}", err=True)


def parse_schedule_date(schedule_str: str) -> str:
    """Parse schedule date string to ISO format.
    
    Args:
        schedule_str: Date string or 'next' for next-free-slot
    
    Returns:
        ISO format date string or 'next-free-slot'
    
    Raises:
        ValueError: If date cannot be parsed
    """
    if schedule_str.lower() == 'next':
        return 'next-free-slot'
    
    try:
        # Parse the date and convert to ISO format
        dt = date_parser.parse(schedule_str)
        return dt.isoformat()
    except Exception as e:
        raise ValueError(f"Invalid date format: {schedule_str}") from e
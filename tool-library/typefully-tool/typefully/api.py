"""Typefully API client wrapper."""

import json
from typing import Dict, Any, Optional, List
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class TypefullyAPI:
    """Wrapper for Typefully API v1."""
    
    BASE_URL = "https://api.typefully.com/v1/"
    
    def __init__(self, api_key: str):
        """Initialize API client with authentication.
        
        Args:
            api_key: Typefully API key
        """
        self.api_key = api_key
        self.session = self._create_session()
    
    def _create_session(self) -> requests.Session:
        """Create a requests session with retry logic."""
        session = requests.Session()
        
        # Set authentication header
        session.headers.update({
            'X-API-KEY': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        })
        
        # Configure retries for network errors
        retry = Retry(
            total=3,
            backoff_factor=0.3,
            status_forcelist=[500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        
        return session
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make an API request.
        
        Args:
            method: HTTP method
            endpoint: API endpoint (relative to base URL)
            **kwargs: Additional arguments for requests
        
        Returns:
            Response data as dictionary
            
        Raises:
            requests.HTTPError: For API errors
        """
        url = urljoin(self.BASE_URL, endpoint)
        
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        
        # Some endpoints might return empty responses
        if response.text:
            return response.json()
        return {}
    
    def validate_key(self) -> bool:
        """Validate the API key by making a test request.
        
        Returns:
            True if key is valid, False otherwise
        """
        try:
            # Try to get notifications as a validation request
            self._request('GET', 'notifications/')
            return True
        except Exception:
            return False
    
    def create_draft(self, 
                    content: str,
                    threadify: bool = False,
                    share: bool = False,
                    schedule_date: Optional[str] = None,
                    auto_retweet_enabled: bool = False,
                    auto_plug_enabled: bool = False,
                    platform: Optional[str] = None) -> Dict[str, Any]:
        """Create a new draft.
        
        Args:
            content: The content of the draft (use 4 newlines for threads)
            threadify: Whether to auto-split long content into threads
            share: Whether to generate a share URL
            schedule_date: ISO date string or "next-free-slot"
            auto_retweet_enabled: Enable auto-retweet
            auto_plug_enabled: Enable auto-plug
        
        Returns:
            API response with draft details
        """
        payload = {
            'content': content
        }
        
        if threadify:
            payload['threadify'] = True
        if share:
            payload['share'] = True
        if schedule_date:
            payload['schedule-date'] = schedule_date
        if auto_retweet_enabled:
            payload['auto_retweet_enabled'] = True
        if auto_plug_enabled:
            payload['auto_plug_enabled'] = True
        if platform:
            payload['platform'] = platform
        
        return self._request('POST', 'drafts/', json=payload)
    
    def get_scheduled_drafts(self, content_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get recently scheduled drafts.
        
        Args:
            content_filter: Filter by 'threads' or 'tweets'
        
        Returns:
            List of scheduled drafts
        """
        params = {}
        if content_filter:
            params['content_filter'] = content_filter
        
        response = self._request('GET', 'drafts/recently-scheduled/', params=params)
        return response.get('drafts', [])
    
    def get_published_drafts(self) -> List[Dict[str, Any]]:
        """Get recently published drafts.
        
        Returns:
            List of published drafts
        """
        response = self._request('GET', 'drafts/recently-published/')
        return response.get('drafts', [])
    
    def get_notifications(self, kind: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get notifications.
        
        Args:
            kind: Filter by 'inbox' or 'activity'
        
        Returns:
            List of notifications
        """
        params = {}
        if kind:
            params['kind'] = kind
        
        response = self._request('GET', 'notifications/', params=params)
        return response.get('notifications', [])
    
    def mark_notifications_read(self, kind: Optional[str] = None, username: Optional[str] = None) -> Dict[str, Any]:
        """Mark all notifications as read.
        
        Args:
            kind: Filter by 'inbox' or 'activity'
            username: Filter by specific username
        
        Returns:
            API response
        """
        payload = {}
        if kind:
            payload['kind'] = kind
        if username:
            payload['username'] = username
        
        return self._request('POST', 'notifications/mark-all-read/', json=payload)
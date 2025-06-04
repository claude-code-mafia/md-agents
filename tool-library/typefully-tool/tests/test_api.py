#!/usr/bin/env python3
"""Tests for Typefully API client."""

import unittest
from unittest.mock import Mock, patch, MagicMock
import requests

from typefully.api import TypefullyAPI


class TestTypefullyAPI(unittest.TestCase):
    """Test cases for TypefullyAPI class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.api_key = "test_api_key_123"
        self.api = TypefullyAPI(self.api_key)
    
    def test_initialization(self):
        """Test API client initialization."""
        self.assertEqual(self.api.api_key, self.api_key)
        self.assertIsNotNone(self.api.session)
        self.assertEqual(
            self.api.session.headers['X-API-KEY'],
            f'Bearer {self.api_key}'
        )
    
    @patch('requests.Session.request')
    def test_validate_key_success(self, mock_request):
        """Test successful API key validation."""
        mock_response = Mock()
        mock_response.text = '{"notifications": []}'
        mock_response.json.return_value = {"notifications": []}
        mock_request.return_value = mock_response
        
        result = self.api.validate_key()
        self.assertTrue(result)
    
    @patch('requests.Session.request')
    def test_validate_key_failure(self, mock_request):
        """Test failed API key validation."""
        mock_request.side_effect = requests.HTTPError()
        
        result = self.api.validate_key()
        self.assertFalse(result)
    
    @patch('requests.Session.request')
    def test_create_draft_basic(self, mock_request):
        """Test basic draft creation."""
        mock_response = Mock()
        mock_response.text = '{"id": "123", "content": "Test tweet"}'
        mock_response.json.return_value = {"id": "123", "content": "Test tweet"}
        mock_request.return_value = mock_response
        
        result = self.api.create_draft("Test tweet")
        
        self.assertEqual(result["id"], "123")
        self.assertEqual(result["content"], "Test tweet")
        
        # Check request was made correctly
        mock_request.assert_called_once()
        call_args = mock_request.call_args
        self.assertEqual(call_args[0][0], 'POST')
        self.assertTrue(call_args[0][1].endswith('/drafts/'))
        self.assertEqual(call_args[1]['json']['content'], 'Test tweet')
    
    @patch('requests.Session.request')
    def test_create_draft_with_options(self, mock_request):
        """Test draft creation with all options."""
        mock_response = Mock()
        mock_response.text = '{"id": "123"}'
        mock_response.json.return_value = {"id": "123"}
        mock_request.return_value = mock_response
        
        self.api.create_draft(
            "Test content",
            threadify=True,
            share=True,
            schedule_date="2025-01-07T10:00:00",
            auto_retweet_enabled=True,
            auto_plug_enabled=True
        )
        
        # Check all parameters were included
        call_args = mock_request.call_args[1]['json']
        self.assertEqual(call_args['content'], 'Test content')
        self.assertTrue(call_args['threadify'])
        self.assertTrue(call_args['share'])
        self.assertEqual(call_args['schedule-date'], '2025-01-07T10:00:00')
        self.assertTrue(call_args['auto_retweet_enabled'])
        self.assertTrue(call_args['auto_plug_enabled'])
    
    @patch('requests.Session.request')
    def test_get_scheduled_drafts(self, mock_request):
        """Test getting scheduled drafts."""
        mock_response = Mock()
        mock_response.text = '{"drafts": [{"id": "1"}, {"id": "2"}]}'
        mock_response.json.return_value = {"drafts": [{"id": "1"}, {"id": "2"}]}
        mock_request.return_value = mock_response
        
        result = self.api.get_scheduled_drafts()
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["id"], "1")
    
    @patch('requests.Session.request')
    def test_get_scheduled_drafts_with_filter(self, mock_request):
        """Test getting scheduled drafts with filter."""
        mock_response = Mock()
        mock_response.text = '{"drafts": []}'
        mock_response.json.return_value = {"drafts": []}
        mock_request.return_value = mock_response
        
        self.api.get_scheduled_drafts(content_filter="threads")
        
        call_args = mock_request.call_args
        self.assertEqual(call_args[1]['params']['content_filter'], 'threads')


if __name__ == '__main__':
    unittest.main()
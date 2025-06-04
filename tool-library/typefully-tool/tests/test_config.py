#!/usr/bin/env python3
"""Tests for configuration management."""

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from typefully.config import Config


class TestConfig(unittest.TestCase):
    """Test cases for Config class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create temporary directory for testing
        self.temp_dir = tempfile.mkdtemp()
        self.config_dir = Path(self.temp_dir) / '.typefully'
        self.config_file = self.config_dir / 'config.json'
        
        # Patch CONFIG_DIR and related paths
        self.patcher = patch.multiple(
            'typefully.config',
            CONFIG_DIR=self.config_dir,
            CONFIG_FILE=self.config_file,
            CACHE_DIR=self.config_dir / 'cache'
        )
        self.patcher.start()
    
    def tearDown(self):
        """Clean up test fixtures."""
        self.patcher.stop()
        # Clean up temporary directory
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_init_creates_directories(self):
        """Test that initialization creates required directories."""
        config = Config()
        
        self.assertTrue(self.config_dir.exists())
        self.assertTrue((self.config_dir / 'cache').exists())
    
    def test_get_set_value(self):
        """Test getting and setting configuration values."""
        config = Config()
        
        # Test default value
        self.assertIsNone(config.get('test_key'))
        self.assertEqual(config.get('test_key', 'default'), 'default')
        
        # Test setting value
        config.set('test_key', 'test_value')
        self.assertEqual(config.get('test_key'), 'test_value')
        
        # Verify it was saved to file
        self.assertTrue(self.config_file.exists())
        with open(self.config_file) as f:
            data = json.load(f)
        self.assertEqual(data['test_key'], 'test_value')
    
    def test_api_key_from_config(self):
        """Test getting API key from configuration."""
        config = Config()
        config.set_api_key('test_api_key_123')
        
        self.assertEqual(config.get_api_key(), 'test_api_key_123')
    
    @patch.dict(os.environ, {'TYPEFULLY_API_KEY': 'env_api_key'})
    def test_api_key_from_environment(self):
        """Test that environment variable takes precedence."""
        config = Config()
        config.set_api_key('config_api_key')
        
        # Environment should take precedence
        self.assertEqual(config.get_api_key(), 'env_api_key')
    
    def test_clear_config(self):
        """Test clearing configuration."""
        config = Config()
        config.set('test_key', 'test_value')
        config.set_api_key('test_api_key')
        
        # Verify config exists
        self.assertTrue(self.config_file.exists())
        
        # Clear config
        config.clear()
        
        # Verify file is removed and values are cleared
        self.assertFalse(self.config_file.exists())
        self.assertIsNone(config.get('test_key'))
        self.assertIsNone(config.get('api_key'))
    
    def test_file_permissions(self):
        """Test that config file has restricted permissions."""
        config = Config()
        config.set('test_key', 'test_value')
        
        # Check file permissions (should be 0o600)
        stat_info = self.config_file.stat()
        mode = stat_info.st_mode & 0o777
        self.assertEqual(mode, 0o600)


if __name__ == '__main__':
    unittest.main()
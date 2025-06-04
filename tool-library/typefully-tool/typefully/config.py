"""Configuration management for Typefully CLI."""

import json
import os
from pathlib import Path
from typing import Optional, Dict, Any

CONFIG_DIR = Path.home() / '.typefully'
CONFIG_FILE = CONFIG_DIR / 'config.json'
CACHE_DIR = CONFIG_DIR / 'cache'


class Config:
    """Manage Typefully CLI configuration."""
    
    def __init__(self):
        self._ensure_dirs()
        self._config = self._load_config()
    
    def _ensure_dirs(self):
        """Create configuration directories if they don't exist."""
        CONFIG_DIR.mkdir(mode=0o700, exist_ok=True)
        CACHE_DIR.mkdir(mode=0o700, exist_ok=True)
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, 'r') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}
    
    def save(self):
        """Save configuration to file."""
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self._config, f, indent=2)
        # Ensure file has restricted permissions
        CONFIG_FILE.chmod(0o600)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set configuration value."""
        self._config[key] = value
        self.save()
    
    def get_api_key(self) -> Optional[str]:
        """Get API key from config or environment."""
        # Environment variable takes precedence
        env_key = os.environ.get('TYPEFULLY_API_KEY')
        if env_key:
            return env_key
        return self.get('api_key')
    
    def set_api_key(self, api_key: str):
        """Set API key in configuration."""
        self.set('api_key', api_key)
    
    def clear(self):
        """Clear all configuration."""
        self._config = {}
        if CONFIG_FILE.exists():
            CONFIG_FILE.unlink()
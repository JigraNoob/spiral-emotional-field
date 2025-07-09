"""
Configuration management for the Spiral Tabnine Proxy.
"""
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

# Default configuration
DEFAULT_CONFIG = {
    "completionFilter": {
        "toneformAwareness": True,
        "phaseBias": {
            "inhale": 0.2,
            "hold": 0.3,
            "exhale": 0.5
        },
        "glintWeighting": {
            "resonance_level": "high",
            "recent_toneform": [
                "soft.reveal",
                "hush.sustain",
                "echo.offer"
            ]
        },
        "silenceThreshold": 3000,
        "coherenceFavor": True
    },
    "display": {
        "style": "spiral-glow",
        "dimOnDrift": True
    },
    "metrics": {
        "trackRecursionDepth": True,
        "completionEntropy": True,
        "phaseDiversity": True
    },
    "server": {
        "host": "localhost",
        "port": 9001,
        "log_level": "INFO"
    },
    "glintstream": {
        "enabled": True,
        "endpoint": "http://localhost:9000/glintstream"
    },
    "breathline": {
        "endpoint": "http://localhost:9000/breathline",
        "sync_interval": 5.0
    }
}

def find_config_file() -> Optional[Path]:
    """Locate the configuration file in common locations."""
    config_paths = [
        Path("tabnine_config.json"),
        Path("~/.config/spiral/tabnine_config.json").expanduser(),
        Path("/etc/spiral/tabnine_config.json"),
        Path(__file__).parent.parent / "config" / "tabnine_config.json"
    ]
    
    for path in config_paths:
        if path.exists() and path.is_file():
            return path
    return None

def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Load configuration from file or use defaults.
    
    Args:
        config_path: Optional path to config file. If None, will search common locations.
    
    Returns:
        Dict containing the configuration.
    """
    config = DEFAULT_CONFIG.copy()
    
    # Find config file if path not provided
    if config_path is None:
        config_file = find_config_file()
    else:
        config_file = Path(config_path)
    
    # Load config from file if found
    if config_file and config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                file_config = json.load(f)
                # Deep merge with defaults
                config = _deep_merge(config, file_config)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load config from {config_file}: {e}")
    
    # Apply environment variable overrides
    config = _apply_env_overrides(config)
    
    return config

def _deep_merge(base: Dict[str, Any], update: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively merge two dictionaries."""
    result = base.copy()
    for key, value in update.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result

def _apply_env_overrides(config: Dict[str, Any], prefix: str = "SPIRAL_TABNINE_") -> Dict[str, Any]:
    """Apply environment variable overrides to the config."""
    for key, value in os.environ.items():
        if key.startswith(prefix):
            # Convert SPIRAL_TABNINE_SERVER_PORT to server.port
            parts = key[len(prefix):].lower().split('_')
            if len(parts) >= 2:
                section = parts[0]
                setting = '_'.join(parts[1:])
                if section in config and setting in config[section]:
                    # Simple type conversion based on default value
                    default_value = DEFAULT_CONFIG.get(section, {}).get(setting)
                    if isinstance(default_value, bool):
                        config[section][setting] = value.lower() in ('true', '1', 't')
                    elif isinstance(default_value, int):
                        config[section][setting] = int(value)
                    elif isinstance(default_value, float):
                        config[section][setting] = float(value)
                    else:
                        config[section][setting] = value
    return config

# Load default config when module is imported
current_config = load_config()

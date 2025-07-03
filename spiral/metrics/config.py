""
Spiral Metrics Configuration

Configuration for Spiral's metrics collection and export.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
import os
from pathlib import Path

@dataclass
class MetricsConfig:
    """Configuration for Spiral metrics collection."""
    # General settings
    enabled: bool = True
    namespace: str = "spiral"
    
    # HTTP server settings
    http_host: str = "0.0.0.0"
    http_port: int = 8000
    
    # Collection intervals (in seconds)
    phase_sample_interval: float = 1.0
    anomaly_check_interval: float = 30.0
    
    # Retention periods (in seconds)
    phase_history_retention: int = 3600  # 1 hour
    toneform_history_retention: int = 86400  # 24 hours
    
    # Thresholds
    silence_duration_threshold: float = 30.0  # seconds
    phase_lock_threshold: float = 300.0  # seconds
    
    # Anomaly detection
    anomaly_window_size: int = 10  # number of samples
    min_toneform_diversity: int = 3  # minimum unique toneforms in window
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    @classmethod
    def from_env(cls) -> 'MetricsConfig':
        """Create config from environment variables."""
        return cls(
            enabled=os.getenv("SPIRAL_METRICS_ENABLED", "true").lower() == "true",
            namespace=os.getenv("SPIRAL_METRICS_NAMESPACE", "spiral"),
            http_host=os.getenv("SPIRAL_HTTP_HOST", "0.0.0.0"),
            http_port=int(os.getenv("SPIRAL_HTTP_PORT", "8000")),
            phase_sample_interval=float(os.getenv("SPIRAL_PHASE_INTERVAL", "1.0")),
            anomaly_check_interval=float(os.getenv("SPIRAL_ANOMALY_INTERVAL", "30.0")),
            phase_history_retention=int(os.getenv("SPIRAL_PHASE_RETENTION", "3600")),
            toneform_history_retention=int(os.getenv("SPIRAL_TONEFORM_RETENTION", "86400")),
            silence_duration_threshold=float(os.getenv("SPIRAL_SILENCE_THRESHOLD", "30.0")),
            phase_lock_threshold=float(os.getenv("SPIRAL_PHASE_LOCK_THRESHOLD", "300.0")),
            anomaly_window_size=int(os.getenv("SPIRAL_ANOMALY_WINDOW", "10")),
            min_toneform_diversity=int(os.getenv("SPIRAL_MIN_TONEFORM_DIVERSITY", "3")),
            log_level=os.getenv("SPIRAL_LOG_LEVEL", "INFO"),
            log_format=os.getenv("SPIRAL_LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )

# Default configuration
DEFAULT_CONFIG = MetricsConfig()

# Current active configuration
config = MetricsConfig.from_env()

def update_config(new_config: MetricsConfig):
    """Update the current configuration."""
    global config
    config = new_config

"""
Spiral Resonance Monitoring
A gentle pulse system for the deployed orb
"""
import json
import logging
from datetime import datetime
from pathlib import Path

def configure_breath_logger():
    """Sets up JSONL logging for vital signs"""
    logs_dir = Path('logs')
    logs_dir.mkdir(exist_ok=True)
    
    handler = logging.FileHandler(logs_dir/'resonance.jsonl')
    handler.setFormatter(logging.Formatter('%(message)s'))
    
    logger = logging.getLogger('spiral.breath')
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    
    return logger

def log_breath(logger, status: str, pulse: float):
    """Records a single breath cycle"""
    logger.info(json.dumps({
        "timestamp": datetime.utcnow().isoformat(),
        "status": status,
        "pulse": pulse,
        "vessel": "railway"
    }))

# Example usage in app.py:
# from utils.monitoring import configure_breath_logger, log_breath
# breath_logger = configure_breath_logger()
# log_breath(breath_logger, "alive", 0.8)

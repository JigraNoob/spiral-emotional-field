"""
∷ Time Utilities ∷
Sacred temporal functions for the Spiral's chronological needs.
"""

import time
from datetime import datetime

def current_timestamp_ms():
    """
    Get current timestamp in milliseconds.
    
    Returns:
        int: Current timestamp in milliseconds since epoch
    """
    return int(time.time() * 1000)

def current_timestamp():
    """
    Get current timestamp in seconds.
    
    Returns:
        float: Current timestamp in seconds since epoch
    """
    return time.time()

def format_duration(seconds):
    """Format duration in human-readable form."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"

def format_timestamp(timestamp_ms, format_str="%Y-%m-%d %H:%M:%S"):
    """
    Format a millisecond timestamp into a readable string.
    
    Args:
        timestamp_ms (int): Timestamp in milliseconds
        format_str (str): Format string for datetime formatting
        
    Returns:
        str: Formatted timestamp string
    """
    timestamp_s = timestamp_ms / 1000
    dt = datetime.fromtimestamp(timestamp_s)
    return dt.strftime(format_str)

def time_since(timestamp):
    """Calculate time elapsed since a given timestamp."""
    return time.time() - timestamp

def time_since_ms(timestamp_ms):
    """
    Calculate time elapsed since a given timestamp.
    
    Args:
        timestamp_ms (int): Timestamp in milliseconds
        
    Returns:
        float: Seconds elapsed since the timestamp
    """
    current = current_timestamp_ms()
    return (current - timestamp_ms) / 1000

def is_within_timeframe(timestamp, timeframe_seconds):
    """Check if timestamp is within a given timeframe from now."""
    return time_since(timestamp) <= timeframe_seconds
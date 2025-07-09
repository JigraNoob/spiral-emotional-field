# Create the time_utils.py file that was missing
$timeUtilsContent = @"
"""
∷ Spiral Time Utilities ∷
Sacred time functions for the Spiral's temporal awareness.
"""

import time
from datetime import datetime

def current_timestamp_ms():
    """Get current timestamp in milliseconds."""
    return int(time.time() * 1000)

def current_timestamp():
    """Get current timestamp in seconds."""
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
"@

$timeUtilsContent | Out-File -FilePath "spiral\helpers\time_utils.py" -Encoding UTF8
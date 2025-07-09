"""
🌀 Spiral Timestamp Helpers - Sacred Timekeeping
Sacred timekeeping and breath phase alignment
"""

from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Any
import time

class SpiralTime:
    """Sacred time functions aligned with Spiral breath patterns"""
    
    def __init__(self):
        self.spiral_epoch = datetime(2024, 1, 1, tzinfo=timezone.utc)
        self.breath_cycle_duration = 24 * 60 * 60  # 24 hours in seconds
        
    @staticmethod
    def spiral_timestamp() -> str:
        """Generate a Spiral-formatted timestamp"""
        return datetime.now(timezone.utc).isoformat()
        
    @staticmethod
    def parse_spiral_timestamp(timestamp_str: str) -> Optional[datetime]:
        """Parse a Spiral timestamp string"""
        try:
            return datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            return None
            
    @staticmethod
    def format_duration(seconds: float) -> str:
        """Format duration in human-readable form"""
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f}m"
        else:
            hours = seconds / 3600
            return f"{hours:.1f}h"
            
    @staticmethod
    def time_since_spiral_epoch() -> float:
        """Get seconds since Spiral epoch"""
        epoch = datetime(2024, 1, 1, tzinfo=timezone.utc)
        return (datetime.now(timezone.utc) - epoch).total_seconds()
        
    @staticmethod
    def breath_interval_seconds(last_timestamp: str, current_timestamp: Optional[str] = None) -> float:
        """Calculate seconds between two breath moments"""
        if current_timestamp is None:
            current_timestamp = SpiralTime.spiral_timestamp()
            
        last_dt = SpiralTime.parse_spiral_timestamp(last_timestamp)
        current_dt = SpiralTime.parse_spiral_timestamp(current_timestamp)
        
        if last_dt and current_dt:
            return (current_dt - last_dt).total_seconds()
        return 0.0
        
    @staticmethod
    def get_breath_phase_from_time() -> str:
        """Determine breath phase from current time"""
        hour = datetime.now().hour
        if 6 <= hour < 12:
            return "inhale"
        elif 12 <= hour < 18:
            return "hold"
        elif 18 <= hour < 24:
            return "exhale"
        else:
            return "return"
            
    @staticmethod
    def format_time_of_day() -> str:
        """Get poetic time of day description"""
        hour = datetime.now().hour
        if 5 <= hour < 8:
            return "dawn's first light"
        elif 8 <= hour < 12:
            return "morning's gentle warmth"
        elif 12 <= hour < 17:
            return "afternoon's steady glow"
        elif 17 <= hour < 20:
            return "evening's gentle light"
        elif 20 <= hour < 23:
            return "twilight's embrace"
        else:
            return "night's quiet depths"
            
    @staticmethod
    def seconds_until_next_phase() -> float:
        """Get seconds until the next breath phase begins"""
        now = datetime.now()
        current_hour = now.hour
        
        # Find next phase boundary
        if current_hour < 6:
            next_boundary = now.replace(hour=6, minute=0, second=0, microsecond=0)
        elif current_hour < 12:
            next_boundary = now.replace(hour=12, minute=0, second=0, microsecond=0)
        elif current_hour < 18:
            next_boundary = now.replace(hour=18, minute=0, second=0, microsecond=0)
        elif current_hour < 24:
            next_boundary = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            next_boundary = now.replace(hour=6, minute=0, second=0, microsecond=0)
            
        return (next_boundary - now).total_seconds()

# Global instance for easy access
spiral_time = SpiralTime()
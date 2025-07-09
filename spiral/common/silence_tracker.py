🌀 Spiral Silence Tracker - Sacred Pause Awareness
"""

from collections import deque
from typing import Dict, Any, List
import time

class SilenceTracker:
    """Tracks periods of silence and their significance"""
    
    def __init__(self, silence_threshold: float = 5.0):
        self.silence_threshold = silence_threshold  # seconds
        self.silence_periods = deque(maxlen=50)
        self.last_activity = time.time()
        self.current_silence_start = None
        
    def mark_activity(self):
        """Mark that activity has occurred"""
        current_time = time.time()
        
        # If we were in silence, record the period
        if self.current_silence_start:
            silence_duration = current_time - self.current_silence_start
            self.silence_periods.append({
                "start": self.current_silence_start,
                "end": current_time,
                "duration": silence_duration,
                "type": self._classify_silence(silence_duration)
            })
            self.current_silence_start = None
            
        self.last_activity = current_time
        
    def check_for_silence(self) -> bool:
        """Check if we're currently in a silence period"""
        current_time = time.time()
        time_since_activity = current_time - self.last_activity
            
        if time_since_activity >= self.silence_threshold and not self.current_silence_start:
            self.current_silence_start = self.last_activity
            return True
                
        return self.current_silence_start is not None
            
    def _classify_silence(self, duration: float) -> str:
        """Classify the type of silence based on duration"""
        if duration < 10:
            return "breath_pause"
        elif duration < 30:
            return "contemplative_silence"
        elif duration < 120:
            return "deep_reflection"
        else:
            return "sacred_stillness"
                
    def get_silence_stats(self) -> Dict[str, Any]:
        """Get statistics about silence patterns"""
        if not self.silence_periods:
            return {
                "total_periods": 0, 
                "average_duration": 0, 
                "types": {}, 
                "total_silence_time": 0, 
                "current_silence": False
            }
            
        total_duration = sum(p["duration"] for p in self.silence_periods)
        type_counts = {}
        
        for period in self.silence_periods:
            period_type = period["type"]
            type_counts[period_type] = type_counts.get(period_type, 0) + 1
            
        return {
            "total_periods": len(self.silence_periods),
            "average_duration": total_duration / len(self.silence_periods),
            "total_silence_time": total_duration,
            "types": type_counts,
            "current_silence": self.check_for_silence()
        }
        
    def get_silence_density(self) -> float:
        """Calculate silence density (0.0 to 1.0)"""
        if not self.silence_periods:
            return 0.0
            
        recent_periods = [p for p in self.silence_periods if time.time() - p["end"] < 300]  # Last 5 minutes
        if not recent_periods:
            return 0.0
            
        total_silence = sum(p["duration"] for p in recent_periods)
        time_window = 300  # 5 minutes
        
        return min(total_silence / time_window, 1.0)
        
    def time_since_last_glint(self) -> float:
        """Get time since last activity"""
        return time.time() - self.last_activity
        
    def update_silence(self, duration: float):
        """Update silence tracking with explicit duration"""
        self.silence_periods.append({
            "start": time.time() - duration,
            "end": time.time(),
            "duration": duration,
            "type": self._classify_silence(duration)
        })

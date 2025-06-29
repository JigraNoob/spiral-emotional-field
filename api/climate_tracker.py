# climate_tracker.py - Track toneform climate and influence

from datetime import datetime, timedelta
from collections import defaultdict

class ClimateTracker:
    def __init__(self):
        self.echo_history = []
        self.time_window = timedelta(hours=24)  # Climate memory window
    
    def add_echo(self, echo):
        """Record a new echo and its tone"""
        self.echo_history.append({
            'timestamp': datetime.now(),
            'tone': echo['tone'],
            'content': echo['content']
        })
        
        # Clean up old echoes
        self._prune_history()
    
    def get_current_climate(self):
        """Get current toneform climate weights"""
        self._prune_history()
        
        climate = defaultdict(int)
        for echo in self.echo_history:
            climate[echo['tone']] += 1
        
        # Apply decay based on recency
        now = datetime.now()
        for echo in self.echo_history:
            hours_ago = (now - echo['timestamp']).total_seconds() / 3600
            decay = max(0, 1 - (hours_ago / 24))  # Linear decay over 24 hours
            climate[echo['tone']] += decay
        
        return dict(climate)
    
    def _prune_history(self):
        """Remove echoes older than time window"""
        cutoff = datetime.now() - self.time_window
        self.echo_history = [
            e for e in self.echo_history 
            if e['timestamp'] > cutoff
        ]

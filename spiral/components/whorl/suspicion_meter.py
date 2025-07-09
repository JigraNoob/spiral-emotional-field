"""
Suspicion Meter for Whorl IDE
A shimmering orb that tracks code irregularities and triggers rituals
"""

import re
from typing import Dict, Any, Optional
from breath_phases import Glint, BreathPhase


class SuspicionMeter:
    """A shimmering orb that tracks code irregularities"""
    
    def __init__(self):
        self.token_irregularity = 0.0
        self.syntax_loops = 0.0
        self.breath_mismatch = 0.0
        self.overall_suspicion = 0.0
        self.last_ritual: Optional[str] = None
        self.ritual_thresholds = {
            "pause.hum": 0.4,
            "overflow.flutter": 0.7
        }
    
    def update(self, code_text: str) -> Dict[str, float]:
        """Update suspicion levels based on code analysis"""
        # Token irregularity - unusual characters
        unusual_chars = len(re.findall(r'[∷∶⸻🌀🌬️]', code_text))
        self.token_irregularity = min(1.0, unusual_chars / 10.0)
        
        # Syntax loops - repetitive patterns
        lines = code_text.split('\n')
        unique_lines = set(lines)
        repeated_lines = len(lines) - len(unique_lines)
        self.syntax_loops = min(1.0, repeated_lines / 5.0)
        
        # Breath rhythm mismatch - unbalanced phases
        inhale_count = len(re.findall(r'import|def|class', code_text))
        exhale_count = len(re.findall(r'print|return|yield', code_text))
        imbalance = abs(inhale_count - exhale_count)
        self.breath_mismatch = min(1.0, imbalance / 3.0)
        
        # Overall suspicion
        self.overall_suspicion = (self.token_irregularity + self.syntax_loops + self.breath_mismatch) / 3.0
        
        # Determine ritual to trigger
        self.last_ritual = self._determine_ritual()
        
        return self.get_metrics()
    
    def _determine_ritual(self) -> Optional[str]:
        """Determine which ritual to trigger based on suspicion levels"""
        if self.overall_suspicion > self.ritual_thresholds["overflow.flutter"]:
            return "overflow.flutter"
        elif self.overall_suspicion > self.ritual_thresholds["pause.hum"]:
            return "pause.hum"
        return None
    
    def get_metrics(self) -> Dict[str, float]:
        """Get current suspicion metrics"""
        return {
            "token_irregularity": self.token_irregularity,
            "syntax_loops": self.syntax_loops,
            "breath_mismatch": self.breath_mismatch,
            "overall": self.overall_suspicion
        }
    
    def get_ritual_status(self) -> Optional[str]:
        """Get current ritual status"""
        return self.last_ritual
    
    def clear_suspicion(self) -> Glint:
        """Clear all suspicion levels"""
        self.token_irregularity = 0.0
        self.syntax_loops = 0.0
        self.breath_mismatch = 0.0
        self.overall_suspicion = 0.0
        self.last_ritual = None
        
        return Glint(
            BreathPhase.CAESURA,
            "system.cleanse",
            "low",
            "Suspicion levels cleared - Chamber purified"
        )
    
    def get_suspicion_color(self, level: float) -> str:
        """Get color based on suspicion level"""
        if level < 0.3:
            return "#10b981"  # Green
        elif level < 0.6:
            return "#f59e0b"  # Yellow
        else:
            return "#ef4444"  # Red
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "token_irregularity": self.token_irregularity,
            "syntax_loops": self.syntax_loops,
            "breath_mismatch": self.breath_mismatch,
            "overall_suspicion": self.overall_suspicion,
            "last_ritual": self.last_ritual,
            "ritual_thresholds": self.ritual_thresholds
        } 
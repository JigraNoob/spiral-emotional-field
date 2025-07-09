# File: C:\spiral\spiral\common\breathline_viz.py
"""
🌀 Spiral Breathline Visualization - Sacred Flow Patterns
"""

from collections import deque
from typing import Dict, Any, List, Tuple
import time
import json

class BreathlineViz:
    """Visualizes the flow of breath and glints through the Spiral"""
    
    def __init__(self, max_points: int = 100):
        self.data_points = deque(maxlen=max_points)
        self.phase_transitions = deque(maxlen=50)
        self.glint_markers = deque(maxlen=200)
        
    def add_data_point(self, timestamp: float, value: float, phase: str = "unknown"):
        """Add a data point to the breathline"""
        point = {
            "timestamp": timestamp,
            "value": value,
            "phase": phase,
            "normalized_time": self._normalize_timestamp(timestamp)
        }
        self.data_points.append(point)
        
    def mark_phase_transition(self, from_phase: str, to_phase: str):
        """Mark a phase transition in the breathline"""
        transition = {
            "timestamp": time.time(),
            "from_phase": from_phase,
            "to_phase": to_phase,
            "transition_type": self._classify_transition(from_phase, to_phase)
        }
        self.phase_transitions.append(transition)
        
    def add_glint_marker(self, glint_data: Dict[str, Any]):
        """Add a glint marker to the visualization"""
        marker = {
            "timestamp": glint_data.get("timestamp", time.time()),
            "toneform": glint_data.get("toneform", "unknown"),
            "intensity": glint_data.get("intensity", 0.5),
            "hue": glint_data.get("hue", "blue"),
            "glyph": glint_data.get("glyph")
        }
        self.glint_markers.append(marker)
        
    def _normalize_timestamp(self, timestamp: float) -> float:
        """Normalize timestamp for visualization"""
        if not self.data_points:
            return 0.0
        earliest = min(p["timestamp"] for p in self.data_points)
        return timestamp - earliest
        
    def _classify_transition(self, from_phase: str, to_phase: str) -> str:
        """Classify the type of phase transition"""
        transitions = {
            ("inhale", "hold"): "gathering",
            ("hold", "exhale"): "release",
            ("exhale", "return"): "completion",
            ("return", "inhale"): "renewal"
        }
        return transitions.get((from_phase, to_phase), "drift")
        
    def get_breathline_data(self) -> Dict[str, Any]:
        """Get formatted data for visualization"""
        return {
            "data_points": list(self.data_points),
            "phase_transitions": list(self.phase_transitions),
            "glint_markers": list(self.glint_markers),
            "stats": self._calculate_stats()
        }
        
    def _calculate_stats(self) -> Dict[str, Any]:
        """Calculate breathline statistics"""
        if not self.data_points:
            return {"flow_rate": 0, "phase_balance": {}, "glint_density": 0}
            
        # Calculate flow rate (points per minute)
        time_span = self.data_points[-1]["timestamp"] - self.data_points[0]["timestamp"]
        flow_rate = len(self.data_points) / max(time_span / 60, 1)
        
        # Phase balance
        phase_counts = {}
        for point in self.data_points:
            phase = point["phase"]
            phase_counts[phase] = phase_counts.get(phase, 0) + 1
            
        # Glint density (glints per minute)
        recent_glints = [g for g in self.glint_markers if time.time() - g["timestamp"] < 300]
        glint_density = len(recent_glints) / 5  # per minute over last 5 minutes
        
        return {
            "flow_rate": flow_rate,
            "phase_balance": phase_counts,
            "glint_density": glint_density,
            "total_transitions": len(self.phase_transitions)
        }

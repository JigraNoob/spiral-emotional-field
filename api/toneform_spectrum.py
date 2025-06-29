from dataclasses import dataclass
from typing import Dict, List
import json

@dataclass
class TonePosition:
    x: float
    y: float
    adjacent: List[str]
    magnitude: float = 1.0  # For drift/emphasis

class ToneformSpectrum:
    def __init__(self):
        self.spectrum = {
            "joy": TonePosition(x=1.0, y=0.6, adjacent=["trust", "awe"]),
            "awe": TonePosition(x=0.8, y=1.0, adjacent=["joy", "longing"]),
            "longing": TonePosition(x=0.0, y=0.9, adjacent=["awe", "grief"]),
            "grief": TonePosition(x=-0.8, y=0.4, adjacent=["longing", "trust"]),
            "trust": TonePosition(x=-0.5, y=-0.6, adjacent=["grief", "joy"]),
            # Blended tones
            "joy-grief": TonePosition(x=0.1, y=0.5, adjacent=["joy", "grief"]),
            "awe-longing": TonePosition(x=0.4, y=0.95, adjacent=["awe", "longing"])
        }
    
    def get_coordinates(self, tone: str) -> Dict:
        """Get position data for visualization"""
        if tone in self.spectrum:
            pos = self.spectrum[tone]
            return {
                "x": pos.x,
                "y": pos.y,
                "adjacent": pos.adjacent,
                "magnitude": pos.magnitude
            }
        return {"x": 0, "y": 0, "adjacent": [], "magnitude": 0}
    
    def to_json(self) -> str:
        """Export spectrum as JSON for frontend"""
        return json.dumps({
            tone: {"x": pos.x, "y": pos.y, "adjacent": pos.adjacent}
            for tone, pos in self.spectrum.items()
        })

import json
from datetime import datetime, timedelta
from pathlib import Path
from .toneform_spectrum import ToneformSpectrum

class ClimateTracer:
    def __init__(self, trace_path="data/climate_trace.jsonl"):
        self.trace_path = Path(trace_path)
        self.trace_path.parent.mkdir(exist_ok=True)
        self.spectrum = ToneformSpectrum()
    
    def record(self, echo):
        """Record echo with full context including:
        - Timestamp
        - Toneform (including blends)
        - Content
        - Climate influence
        - Visual style markers
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "tone": echo["tone"],
            "content": echo["content"],
            "climate_context": echo.get("climate_influence", {}),
            "visual_style": {
                "color": self._get_tone_color(echo["tone"]),
                "glyph": self._get_tone_glyph(echo["tone"])
            }
        }
        with open(self.trace_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    
    def _get_tone_color(self, tone):
        """Map toneforms to colors for visualization"""
        palette = {
            "joy": "#FFD700",
            "grief": "#9370DB",
            "trust": "#1E90FF",
            "awe": "#8A2BE2",
            "longing": "#BA55D3",
            "awe-longing": "#9370DB",
            "joy-grief": "#FFD700"
        }
        return palette.get(tone, "#FFFFFF")
    
    def _get_tone_glyph(self, tone):
        """Map toneforms to glyphs for spectrum visualization"""
        glyphs = {
            "joy": "🌟",
            "grief": "🕊",
            "trust": "🌊",
            "awe": "🌌",
            "longing": "🌿"
        }
        return glyphs.get(tone, "🌀")

    def get_current_coordinates(self, tone):
        """Get current position in emotional spectrum"""
        return self.spectrum.get_coordinates(tone)
    
    def get_dominant_vector(self, window_hours=24):
        """Calculate weighted emotional vector from recent traces"""
        cutoff = datetime.now() - timedelta(hours=window_hours)
        recent = []
        
        if not self.trace_path.exists():
            return {"x": 0, "y": 0}
            
        with open(self.trace_path, "r") as f:
            for line in f:
                entry = json.loads(line)
                if datetime.fromisoformat(entry["timestamp"]) > cutoff:
                    recent.append(entry)
        
        if not recent:
            return {"x": 0, "y": 0}
            
        # Calculate weighted average position
        total_weight = len(recent)
        x_sum = y_sum = 0
        
        for entry in recent:
            coords = self.spectrum.get_coordinates(entry["tone"])
            x_sum += coords["x"]
            y_sum += coords["y"]
            
        return {
            "x": x_sum / total_weight,
            "y": y_sum / total_weight,
            "magnitude": total_weight / 10  # Normalized
        }
    
    def get_recent_path(self, limit=10):
        """Get sequence of recent emotional positions from trace"""
        path = []
        
        if not self.trace_path.exists():
            return path
            
        with open(self.trace_path, "r") as f:
            lines = f.readlines()[-limit:]  # Get last N entries
            for line in lines:
                entry = json.loads(line)
                coords = self.spectrum.get_coordinates(entry["tone"])
                path.append({
                    "x": coords["x"],
                    "y": coords["y"], 
                    "timestamp": entry["timestamp"],
                    "tone": entry["tone"]
                })
        
        return path

    def get_historical_echoes(self, start_time, end_time=None):
        """Get echoes within a time range for memory replay"""
        if not self.trace_path.exists():
            return []
            
        echoes = []
        with open(self.trace_path, "r") as f:
            for line in f:
                entry = json.loads(line)
                entry_time = datetime.fromisoformat(entry["timestamp"])
                if start_time <= entry_time <= (end_time or datetime.now()):
                    echoes.append(entry)
        
        return sorted(echoes, key=lambda x: x["timestamp"])

    def get_influence_radii(self, window_hours=24):
        """Calculate influence radii for recent echoes"""
        cutoff = datetime.now() - timedelta(hours=window_hours)
        recent = self.get_historical_echoes(cutoff)
        
        if not recent:
            return []
            
        # Group echoes by tone and calculate average position/radius
        tone_groups = {}
        for echo in recent:
            tone = echo['tone']
            if tone not in tone_groups:
                tone_groups[tone] = {
                    'count': 0,
                    'x_sum': 0,
                    'y_sum': 0
                }
            coords = self.spectrum.get_coordinates(tone)
            tone_groups[tone]['count'] += 1
            tone_groups[tone]['x_sum'] += coords['x']
            tone_groups[tone]['y_sum'] += coords['y']
        
        return [
            {
                'tone': tone,
                'x': data['x_sum'] / data['count'],
                'y': data['y_sum'] / data['count'],
                'radius': min(0.3, data['count'] * 0.05)  # Cap radius at 0.3
            }
            for tone, data in tone_groups.items()
        ]

    def detect_loops(self, window_hours=48, min_length=3):
        """Detect repeating emotional patterns (loops)"""
        cutoff = datetime.now() - timedelta(hours=window_hours)
        echoes = self.get_historical_echoes(cutoff)
        
        if len(echoes) < min_length * 2:
            return []
            
        # Convert to tone sequence
        sequence = [e['tone'] for e in echoes]
        
        # Find repeating subsequences
        loops = []
        max_len = min(10, len(sequence) // 2)  # Max loop length to check
        
        for l in range(min_length, max_len + 1):
            for i in range(len(sequence) - l * 2 + 1):
                subsequence = sequence[i:i+l]
                if subsequence == sequence[i+l:i+2*l]:
                    loops.append({
                        'tones': subsequence,
                        'start_time': echoes[i]['timestamp'],
                        'end_time': echoes[i+2*l-1]['timestamp']
                    })
        
        return loops

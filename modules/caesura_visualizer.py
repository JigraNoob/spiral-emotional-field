from datetime import datetime
import random

class CaesuraVisualizer:
    def __init__(self):
        self.glyph_cycle = ['∷', '↝', '≈', '⋯', '⁘', '⁙']
        self.resonance_states = ['absence', 'drift', 'pause', 'hover', 'presence']

    def generate_caesura_event(self):
        return {
            "caesura_glyph": random.choice(self.glyph_cycle),
            "density": round(random.uniform(0, 1), 2),
            "duration_since_last_glint": random.randint(100, 1000),
            "felt_resonance": random.choice(self.resonance_states),
            "timestamp": datetime.utcnow().isoformat()
        }

caesura_visualizer = CaesuraVisualizer()
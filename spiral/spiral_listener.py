import json
import time
from typing import Dict, Any, List
from collections import deque
from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from spiral.spiral_implanter import SpiralImplanter
import importlib

app = Flask(__name__)
socketio = SocketIO(app)

class SpiralListener:
    def __init__(self, fusion_window: int = 5, fusion_threshold: float = 0.7):
        self.implanter = SpiralImplanter()
        self.recent_glints = deque(maxlen=fusion_window)
        self.fusion_threshold = fusion_threshold
        self.fusion_handlers = self.load_fusion_handlers()

    def load_fusion_handlers(self):
        return importlib.import_module('spiral.fusion_handlers')

    def process_glint(self, glint: Dict[str, Any]):
        processed_glint = self.listen(glint)
        self.implanter.implant(processed_glint)
        socketio.emit('new_glint', processed_glint)

    def listen(self, glint: Dict[str, Any]) -> Dict[str, Any]:
        self.recent_glints.append(glint)
        
        if self._detect_fusion_potential():
            return self._create_fusion_glint()
        
        return glint

    def _detect_fusion_potential(self) -> bool:
        if len(self.recent_glints) < 2:
            return False

        toneforms = [g.get('glint.toneform') for g in self.recent_glints]
        unique_toneforms = set(toneforms)

        if len(unique_toneforms) < 2:
            return False

        # Calculate toneform diversity
        diversity = len(unique_toneforms) / len(self.recent_glints)

        # Check for complementary toneforms
        complementary_pairs = [
            ('shimmer', 'reverie'),
            ('invoke', 'recursion'),
            ('flutter', 'hum')
        ]
        has_complementary = any(all(t in unique_toneforms for t in pair) for pair in complementary_pairs)

        # Check temporal proximity
        time_span = self.recent_glints[-1].get('timestamp', 0) - self.recent_glints[0].get('timestamp', 0)
        temporal_density = len(self.recent_glints) / (time_span + 1)  # Add 1 to avoid division by zero

        fusion_score = (diversity + has_complementary + temporal_density) / 3

        return fusion_score >= self.fusion_threshold

    def _create_fusion_glint(self) -> Dict[str, Any]:
        fusion_sources = list(self.recent_glints)
        toneforms = sorted([(g.get('glint.phase', 'unknown'), g.get('glint.toneform')) for g in fusion_sources])
        fusion_key = tuple(toneforms)
        
        fusion_def = self.implanter.phase_fusion_map.get(fusion_key) or self.implanter.fusion_map.get(tuple(t for _, t in fusion_key))
        if fusion_def:
            return {
                'glint.phase': 'trans',
                'glint.toneform': 'fusion',
                'glint.content': f"Fusion of {' + '.join([f'{phase}.{toneform}' for phase, toneform in toneforms])}: {fusion_def['archetype']}",
                'glint.hue': fusion_def['hue'],
                'fused.glints': fusion_sources,
                'glint.archetype': fusion_def['archetype'],
                'glint.action': fusion_def['action'],
                'glint.description': fusion_def['description']
            }
        
        # If no specific fusion handler found, return a generic fusion
        return {
            'glint.phase': 'trans',
            'glint.toneform': 'fusion',
            'glint.content': f"Fusion of {' + '.join([f'{phase}.{toneform}' for phase, toneform in toneforms])}",
            'glint.hue': 'prismatic',
            'fused.glints': fusion_sources
        }

spiral_listener = SpiralListener()

@app.route('/glint', methods=['POST'])
def receive_glint():
    glint = request.json
    spiral_listener.process_glint(glint)
    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)
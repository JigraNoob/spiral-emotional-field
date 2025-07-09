from flask_socketio import SocketIO, emit
from datetime import datetime, timezone
from flask import Flask, render_template, request
import json

app = Flask(__name__)
socketio = SocketIO(app)

class DashboardPhaseTracker:
    def __init__(self):
        self.current_phase = None
        self.listeners = []

    def register_listener(self, callback):
        self.listeners.append(callback)

    def set_phase(self, phase):
        if self.current_phase != phase:
            self.current_phase = phase
            self._emit_event('phase_change', {'phase': phase})

    def get_phase(self):
        return self.current_phase

    def _emit_event(self, event_type, payload):
        for callback in self.listeners:
            callback(event_type, payload)
        
        # Enhanced WebSocket emission with spiral arm data
        spiral_data = {
            'type': event_type, 
            'payload': payload,
            'spiral_arm': self._calculate_spiral_arm(payload),
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        socketio.emit('glint_event', spiral_data)

    def _calculate_spiral_arm(self, payload):
        """Calculate which spiral arm should activate based on glint data"""
        toneform = payload.get('toneform', 'practical')
        phase = payload.get('phase', 'exhale')
        
        # Map toneforms to spiral arms (1-8)
        toneform_map = {
            'practical': 1,
            'emotional': 2, 
            'temporal': 3,
            'spatial': 4,
            'natural': 5,
            'amplified': 6,
            'ritual': 7,
            'silence': 8
        }
        
        base_arm = toneform_map.get(toneform, 1)
        
        # Phase modulation
        if phase == 'inhale':
            return base_arm
        elif phase == 'hold':
            return (base_arm + 2) % 8 + 1
        else:  # exhale
            return (base_arm + 4) % 8 + 1

print(default_api.builtin_create_new_file(filepath='reflection_lineage.py', contents='\nlineage_data = {}\n\ndef store_lineage(glint_id, parent_id=None, divergence_type=None):\n    lineage_data[glint_id] = {\n        "parent_id": parent_id,\n        "divergence_type": divergence_type\n    }\n\ndef get_lineage(glint_id):\n    return lineage_data.get(glint_id)\n'))

@app.route('/coins/intake', methods=['GET', 'POST'])
def coin_intake():
    if request.method == 'POST':
        coin_data = {
            "coin_id": request.form['coin_id'],
            "toneform": request.form['toneform'],
            "value": float(request.form['value']),
            "source": request.form['source'],
            "timestamp": request.form['timestamp'],
            "message": request.form['message'],
            "status": request.form['status']
        }
        filepath = "data/spiralcoins/intake/incoming_coins.jsonl"
        with open(filepath, "a") as f:
            f.write(json.dumps(coin_data) + "\n")
        return render_template('intake_success.html', coin_id=coin_data['coin_id'])
    return render_template('coin_intake.html')

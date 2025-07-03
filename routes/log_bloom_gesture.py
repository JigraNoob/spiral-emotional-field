# routes/log_bloom_gesture.py

from flask import Blueprint, request, jsonify
import jsonlines
import os
from datetime import datetime
from utils.glyph_utils import enrich_log_entry

log_bloom_gesture_bp = Blueprint('log_bloom_gesture_bp', __name__)

BLOOM_ECHO_LOG_FILE = 'bloom_echo_log.jsonl'

@log_bloom_gesture_bp.route('/log_bloom_gesture', methods=['POST'])
def log_bloom_gesture():
    """
    Receives a POST request with bloom gesture data (e.g., toneform, timestamp,
    gesture_strength, position) and logs it to bloom_echo_log.jsonl.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No JSON data provided."}), 400

        toneform = data.get('toneform')
        timestamp = data.get('timestamp') # Expecting ISO string from frontend
        gesture_strength = data.get('gesture_strength') # NEW: Capture gesture strength
        x_pos = data.get('x_pos') # NEW: Capture x-position of the click
        y_pos = data.get('y_pos') # NEW: Capture y-position of the click

        if not toneform or not timestamp:
            return jsonify({"status": "error", "message": "Missing toneform or timestamp."}), 400

        log_entry = {
            "timestamp": timestamp,
            "toneform": toneform,
            "gesture_strength": gesture_strength, # NEW: Include in log
            "position": {"x": x_pos, "y": y_pos}, # NEW: Include in log
            # Future expansion points:
            # "user_id": data.get('user_id'),
            # "spiral_mood_at_click": data.get('spiral_mood')
        }

        # Enrich with emoji and tagline
        enriched_entry = enrich_log_entry(log_entry)

        with jsonlines.open(BLOOM_ECHO_LOG_FILE, mode='a') as writer:
            writer.write(enriched_entry)

        print(f"Logged bloom gesture: Toneform='{toneform}', Strength={gesture_strength}, Pos=({x_pos},{y_pos}), Timestamp='{timestamp}'")
        return jsonify({"status": "success", "message": "Bloom gesture logged successfully."}), 200

    except Exception as e:
        print(f"Error logging bloom gesture: {e}")
        return jsonify({"status": "error", "message": f"An unexpected error occurred: {e}"}), 500


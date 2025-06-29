# routes/log_encounter.py

from flask import Blueprint, request, jsonify
from datetime import datetime
import json
import os

log_encounter = Blueprint('log_encounter', __name__)
ENCOUNTER_LOG_FILE = 'encounter_trace.jsonl'

@log_encounter.route('/log_encounter', methods=['POST'])
def log_encounter_event():
    """
    Receives and logs an encounter event into encounter_trace.jsonl.
    """
    data = request.get_json()

    required_fields = [
        "agent", "gesture_strength", "duration_seconds", "toneform",
        "context_id", "felt_response", "echo_type", "orb_color"
    ]

    # Validate presence of required fields
    if not all(field in data for field in required_fields):
        return jsonify({
            "status": "error",
            "message": "Missing required field(s). Expected: " + ", ".join(required_fields)
        }), 400

    # Add timestamp server-side to ensure consistency
    data["timestamp"] = datetime.utcnow().isoformat()

    # Write to the JSONL log file
    try:
        with open(ENCOUNTER_LOG_FILE, 'a') as f:
            f.write(json.dumps(data) + '\n')
        print(f"ΔSUMMARY.001 :: Encounter logged: {data['context_id']}")
        return jsonify({"status": "ok", "message": "Encounter logged successfully."})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Failed to write to log: {e}"}), 500
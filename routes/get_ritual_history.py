# routes/get_ritual_history.py

from flask import Blueprint, jsonify
import json
import os

get_ritual_history_bp = Blueprint('get_ritual_history_bp', __name__)

ENCOUNTER_LOG_FILE = 'encounter_trace.jsonl' # Path to your encounter log file

@get_ritual_history_bp.route('/get_ritual_history', methods=['GET'])
def get_ritual_history():
    """
    Reads the encounter_trace.jsonl file and returns its contents as a JSON array.
    Each line in the file is expected to be a JSON object representing an event.
    """
    history_data = []
    if os.path.exists(ENCOUNTER_LOG_FILE):
        try:
            with open(ENCOUNTER_LOG_FILE, 'r') as f:
                for line in f:
                    try:
                        history_data.append(json.loads(line.strip()))
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON from line in {ENCOUNTER_LOG_FILE}: {line.strip()} - {e}")
                        # Optionally, skip problematic lines or log them for later inspection
        except Exception as e:
            print(f"Error reading {ENCOUNTER_LOG_FILE}: {e}")
            return jsonify({"status": "error", "message": "Failed to read ritual history."}), 500
    
    # History data is returned as-is; sorting will be handled by the frontend for replay order
    return jsonify(history_data)


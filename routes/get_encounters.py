# routes/get_encounters.py

from flask import Blueprint, jsonify
import json
import os

get_encounters_bp = Blueprint('get_encounters_bp', __name__, url_prefix='/encounters')
ENCOUNTER_LOG_FILE = 'encounter_trace.jsonl'

@get_encounters_bp.route('/encounters', methods=['GET'])
@get_encounters_bp.route('/', methods=['GET'])
def get_all_encounters():
    """
    Returns all encounter events from encounter_trace.jsonl as JSON.
    """
    encounters = []
    if os.path.exists(ENCOUNTER_LOG_FILE):
        try:
            with open(ENCOUNTER_LOG_FILE, 'r') as f:
                for line in f:
                    encounters.append(json.loads(line))
        except Exception as e:
            return jsonify({"status": "error", "message": f"Failed to read encounter log: {e}"}), 500
    
    return jsonify(encounters)
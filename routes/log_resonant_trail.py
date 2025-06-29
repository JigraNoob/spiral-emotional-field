# routes/log_resonant_trail.py

from flask import Blueprint, request, jsonify
import jsonlines
import os
from datetime import datetime

log_resonant_trail_bp = Blueprint('log_resonant_trail_bp', __name__)

TRAIL_LOG_FILE = 'trail_impression.jsonl'

def log_trail_impression(impression_data):
    """
    Logs a steward's lingering impression to trail_impression.jsonl.
    Adds a timestamp and ensures the file exists.
    """
    impression_data["timestamp"] = datetime.utcnow().isoformat() + 'Z' # UTC timestamp with Z

    # Ensure the file exists before attempting to open in append mode
    if not os.path.exists(TRAIL_LOG_FILE):
        # Create an empty file if it doesn't exist
        open(TRAIL_LOG_FILE, 'w').close()

    with jsonlines.open(TRAIL_LOG_FILE, mode='a') as writer:
        writer.write(impression_data)

@log_resonant_trail_bp.route('/log_trail', methods=['POST'])
def log_trail():
    """
    Accepts a lingering impression: { "felt_tone": "...", "response_text": "..." }
    """
    data = request.get_json()
    if not data or "felt_tone" not in data or "response_text" not in data:
        return jsonify({"status": "error", "message": "Invalid submission: Missing 'felt_tone' or 'response_text'"}), 400

    try:
        log_trail_impression(data)
        print(f"Resonant Trail received: Tone='{data.get('felt_tone')}', Text='{data.get('response_text')}'")
        return jsonify({"status": "success", "message": "Resonant trail received"}), 200
    except Exception as e:
        print(f"Error logging trail impression: {e}")
        return jsonify({"status": "error", "message": f"Failed to log resonant trail: {str(e)}"}), 500


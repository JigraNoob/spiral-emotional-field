# routes/stall_inquiry.py

from flask import Blueprint, request, jsonify
from datetime import datetime
import json
import os

stall_inquiry = Blueprint('stall_inquiry', __name__)
STALL_LOG_FILE = 'stall_trace.jsonl'

@stall_inquiry.route('/log_stall', methods=['POST'])
def log_stall():
    """
    Receives and logs a stall event, transmuting blockage into inquiry.
    """
    stall_data = request.get_json()

    if not stall_data or 'stall_type' not in stall_data:
        return jsonify({"status": "error", "message": "Invalid stall data provided."}), 400

    stall_data['timestamp'] = datetime.utcnow().isoformat()

    with open(STALL_LOG_FILE, 'a') as f:
        f.write(json.dumps(stall_data) + '\n')

    print(f"ΔPULSE.002 :: Stall logged: {stall_data['stall_type']}")
    return jsonify({"status": "ok", "message": "Stall logged as inquiry."})
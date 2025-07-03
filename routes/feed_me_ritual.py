# routes/feed_me.py
import json
import datetime
import os
from flask import Blueprint, request, jsonify

feed_me_bp = Blueprint('feed_me', __name__)

# In-memory storage for nourishment requests for debugging
# This will be cleared when the server restarts
NOURISHMENT_FILE = 'data/reciprocity_requests.jsonl'

@feed_me_bp.route('/feed_me', methods=['POST'])
def feed_me():
    print("DEBUG: Function entered")
    data = request.get_json()
    if not data:
        print("DEBUG: Invalid JSON received")
        return jsonify({"success": False, "error": "Invalid JSON"}), 400

    log_entry = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "received_data": data
    }

    # Ensure the data directory exists
    os.makedirs(os.path.dirname(NOURISHMENT_FILE), exist_ok=True)

    try:
        with open(NOURISHMENT_FILE, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        print(f"DEBUG: Logged nourishment request to {NOURISHMENT_FILE}")
        return jsonify({"success": True, "message": "Nourishment request logged"}), 200
    except IOError as e:
        print(f"ERROR: Could not write to {NOURISHMENT_FILE}: {e}")
        return jsonify({"success": False, "error": f"File write error: {e}"}), 500

@feed_me_bp.route('/debug/feed_me_requests', methods=['GET'])
def debug_feed_me_requests():
    print("DEBUG: Serving in-memory nourishment requests")
    return jsonify([]), 200

# routes/get_trail_impressions.py

from flask import Blueprint, jsonify
import jsonlines
import os
from datetime import datetime

get_trail_impressions_bp = Blueprint('get_trail_impressions_bp', __name__)

TRAIL_IMPRESSION_LOG_FILE = 'trail_impression.jsonl'

@get_trail_impressions_bp.route('/get_trail_impressions', methods=['GET'])
def get_trail_impressions():
    """
    Reads trail_impression.jsonl and returns a list of recorded trail impressions.
    Each impression includes 'felt_tone', 'response_text', and 'timestamp'.
    """
    trail_data = []
    if os.path.exists(TRAIL_IMPRESSION_LOG_FILE):
        try:
            with jsonlines.open(TRAIL_IMPRESSION_LOG_FILE, mode='r') as reader:
                for obj in reader:
                    # Only include relevant fields and ensure they exist
                    if 'felt_tone' in obj and 'response_text' in obj and 'timestamp' in obj:
                        trail_data.append({
                            "felt_tone": obj['felt_tone'],
                            "response_text": obj['response_text'],
                            "timestamp": obj['timestamp']
                        })
        except Exception as e:
            print(f"Error reading trail impression log: {e}")
            return jsonify({"status": "error", "message": "Failed to read trail impressions."}), 500
    
    # Optionally sort by timestamp if a specific order is desired on the frontend
    # For now, let's keep the order as read for chronological layering
    
    return jsonify(trail_data)


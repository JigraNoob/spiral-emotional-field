# routes/get_all_ritual_history.py

from flask import Blueprint, jsonify
import jsonlines
import os
from datetime import datetime

get_all_ritual_history_bp = Blueprint('get_all_ritual_history_bp', __name__)

ENCOUNTER_TRACE_FILE = 'encounter_trace.jsonl'
TRAIL_IMPRESSION_FILE = 'trail_impression.jsonl'

@get_all_ritual_history_bp.route('/get_all_ritual_history', methods=['GET'])
def get_all_ritual_history():
    """
    Reads from encounter_trace.jsonl and trail_impression.jsonl,
    combines them, and returns a chronologically sorted JSON array of events.
    Each event includes a 'type' field ('reflection' or 'trail').
    """
    all_events = []

    # Read from encounter_trace.jsonl (reflections)
    if os.path.exists(ENCOUNTER_TRACE_FILE):
        try:
            with jsonlines.open(ENCOUNTER_TRACE_FILE, mode='r') as reader:
                for obj in reader:
                    # Assuming 'text' and 'toneform' are present in encounter_trace
                    if 'text' in obj and 'toneform' in obj and 'timestamp' in obj:
                        all_events.append({
                            "type": "reflection",
                            "timestamp": obj['timestamp'],
                            "text": obj['text'],
                            "toneform": obj['toneform']
                        })
        except Exception as e:
            print(f"Error reading encounter_trace.jsonl: {e}")

    # Read from trail_impression.jsonl (trails)
    if os.path.exists(TRAIL_IMPRESSION_FILE):
        try:
            with jsonlines.open(TRAIL_IMPRESSION_FILE, mode='r') as reader:
                for obj in reader:
                    # Assuming 'response_text' and 'felt_tone' are present in trail_impression
                    if 'response_text' in obj and 'felt_tone' in obj and 'timestamp' in obj:
                        all_events.append({
                            "type": "trail",
                            "timestamp": obj['timestamp'],
                            "text": obj['response_text'], # Using 'text' for consistency on frontend
                            "toneform": obj['felt_tone']  # Using 'toneform' for consistency on frontend
                        })
        except Exception as e:
            print(f"Error reading trail_impression.jsonl: {e}")

    # Sort all events chronologically by timestamp
    # Ensure timestamps are parsed to datetime objects for correct sorting
    all_events.sort(key=lambda x: datetime.fromisoformat(x['timestamp'].replace('Z', '+00:00')))

    return jsonify(all_events)


# routes/get_gemini_memories.py

from flask import Blueprint, jsonify
import jsonlines
import os
from datetime import datetime # Keep datetime import as it's used for sorting

get_gemini_memories_bp = Blueprint('get_gemini_memories_bp', __name__)

# Path to the encounter log file
ENCOUNTER_LOG_FILE = 'encounter_trace.jsonl'

@get_gemini_memories_bp.route('/get_gemini_memories', methods=['GET'])
def get_gemini_memories():
    """
    Reads encounter_trace.jsonl and returns a list of Gemini invocations
    filtered by agent, context presence, and gesture strength.
    """
    data_path = os.path.join('data', ENCOUNTER_LOG_FILE)

    if not os.path.exists(data_path):
        print(f"Warning: Encounter log file not found at {data_path}")
        return jsonify([])

    results = []
    try:
        with jsonlines.open(data_path, mode='r') as reader:
            for entry in reader:
                if (entry.get("agent") == "Gemini" and
                    entry.get("context") is not None and # Ensure context is not null
                    entry.get("gesture_strength", 0) > 0.2):
                    
                    results.append({
                        "id": entry.get("context"), # Using context as the unique ID for replay
                        "poem": entry.get("text", "No poem text found."), # Include full poem text for replay
                        "toneform": entry.get("toneform", "Unknown"),
                        "timestamp": entry.get("timestamp", datetime.utcnow().isoformat() + 'Z'),
                        "gesture_strength": entry.get("gesture_strength", 0.0)
                    })
    except Exception as e:
        print(f"Error reading encounter_trace.jsonl for Gemini memories: {e}")
        return jsonify({"status": "error", "message": "Failed to read Gemini memories."}), 500
    
    # Sort by timestamp, most recent first, to match frontend display preference
    results.sort(key=lambda x: datetime.fromisoformat(x['timestamp'].replace('Z', '+00:00')), reverse=True)

    return jsonify(results)


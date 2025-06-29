# routes/get_toneform_blooms.py

from flask import Blueprint, jsonify
import jsonlines
import os
from collections import defaultdict

get_toneform_blooms_bp = Blueprint('get_toneform_blooms_bp', __name__)

TRAIL_IMPRESSION_FILE = 'trail_impression.jsonl'
if not os.path.exists(TRAIL_IMPRESSION_FILE):
    with open(TRAIL_IMPRESSION_FILE, 'w') as f:
        pass
@get_toneform_blooms_bp.route('/get_toneform_blooms', methods=['GET'])
def get_toneform_blooms():
    """
    Reads trail_impression.jsonl, groups data by 'felt_tone' (toneform),
    and returns summarized data for each toneform to represent blooms.
    The response includes toneform, count of impressions, and average gesture strength.
    """
    toneform_data = defaultdict(lambda: {"count": 0, "total_strength": 0})
    
    if os.path.exists(TRAIL_IMPRESSION_FILE):
        try:
            with jsonlines.open(TRAIL_IMPRESSION_FILE, mode='r') as reader:
                for obj in reader:
                    felt_tone = obj.get('felt_tone')
                    # Assuming gesture_strength is logged in trail_impression or default to 0.5
                    gesture_strength = obj.get('gesture_strength', 0.5) 
                    
                    if felt_tone:
                        toneform_data[felt_tone]["count"] += 1
                        toneform_data[felt_tone]["total_strength"] += gesture_strength
        except Exception as e:
            print(f"Error reading trail_impression.jsonl for blooms: {e}")
            return jsonify({"status": "error", "message": "Failed to read trail impressions for blooms."}), 500
    
    blooms_output = []
    for toneform, data in toneform_data.items():
        avg_strength = data["total_strength"] / data["count"] if data["count"] > 0 else 0.5
        blooms_output.append({
            "toneform": toneform,
            "count": data["count"],
            "average_strength": avg_strength
            # Frontend will determine random coordinates
        })
    
    return jsonify(blooms_output)


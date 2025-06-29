from flask import Blueprint, jsonify
from datetime import datetime, timedelta
import json

echo_bp = Blueprint('echo', __name__, url_prefix='/echo')

@echo_bp.route('/responses/<offering_id>')
def get_echo_responses(offering_id):
    """Returns echo responses for a Still Offering"""
    try:
        # Load echo data from JSONL (mock implementation)
        echoes = []
        with open(f'data/echo_responses_{offering_id}.jsonl') as f:
            for line in f:
                echoes.append(json.loads(line))
                
        return jsonify({
            "offering_id": offering_id,
            "echoes": echoes,
            "summary": {
                "count": len(echoes),
                "last_echo": max(e['timestamp'] for e in echoes) if echoes else None,
                "toneform_distribution": {
                    t: sum(1 for e in echoes if e['toneform'] == t)
                    for t in set(e['toneform'] for e in echoes)
                }
            }
        })
    except FileNotFoundError:
        return jsonify({"error": "No echoes found"}), 404

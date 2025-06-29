from flask import Blueprint, jsonify, current_app
from datetime import datetime, timedelta
import json
import os

echo_bp = Blueprint('echo', __name__, url_prefix='/echo')

@echo_bp.route('/responses/<offering_id>')
def get_echo_responses(offering_id):
    """Returns echo responses for a Still Offering"""
    try:
        # Verify data directory exists
        data_dir = os.path.join(current_app.root_path, 'data')
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            
        data_file = os.path.join(data_dir, f'echo_responses_{offering_id}.jsonl')
        
        if not os.path.exists(data_file):
            return jsonify({"error": "No echoes found", "hint": "Sample data not deployed"}), 404
            
        # Load echo data from JSONL
        echoes = []
        with open(data_file) as f:
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
    except Exception as e:
        current_app.logger.error(f"Error loading echoes: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

from flask import Blueprint, jsonify, current_app
from datetime import datetime, timedelta
import json
import os

echo_bp = Blueprint('echo', __name__, url_prefix='/echo')

@echo_bp.route('/responses/<offering_id>')
def get_echo_responses(offering_id):
    """Returns echo responses for a Still Offering"""
    current_app.logger.info(f"Echo tracker request for offering: {offering_id}")
    
    try:
        # Verify data directory exists
        data_dir = os.path.join(current_app.root_path, 'data')
        current_app.logger.info(f"Checking data directory: {data_dir}")
        
        if not os.path.exists(data_dir):
            current_app.logger.info("Creating data directory")
            os.makedirs(data_dir)
            
        data_file = os.path.join(data_dir, f'echo_responses_{offering_id}.jsonl')
        current_app.logger.info(f"Looking for data file: {data_file}")
        
        if not os.path.exists(data_file):
            current_app.logger.warning(f"Data file not found: {data_file}")
            return jsonify({
                "error": "No echoes found", 
                "hint": "Sample data not deployed",
                "data_dir": data_dir,
                "data_file": data_file
            }), 404
            
        current_app.logger.info("Loading echo data")
        echoes = []
        with open(data_file) as f:
            for line in f:
                echoes.append(json.loads(line))
                
        current_app.logger.info(f"Returning {len(echoes)} echoes")
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
        current_app.logger.error(f"Error loading echoes: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

@echo_bp.route('/health')
def echo_health():
    """Verify blueprint is registered"""
    return jsonify({
        "status": "active",
        "blueprint": "echo",
        "url_prefix": echo_bp.url_prefix
    })

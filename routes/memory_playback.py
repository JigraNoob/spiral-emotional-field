from flask import Blueprint, render_template, jsonify, request
from datetime import datetime, timedelta
import json
import os

playback_bp = Blueprint('playback', __name__, url_prefix='/reflect')

# Toneform color mappings (WCAG compliant)
TONEFORM_COLORS = {
    "Resonance": "#6366f1",  # Indigo
    "Curiosity": "#d97706",  # Amber (adjusted for contrast)
    "Reflection": "#059669",  # Emerald
    "Trust": "#2563eb",  # Blue
    "Longing": "#9333ea",  # Purple
    "Joy": "#65a30d",  # Lime
    "Hesitation": "#4b5563"  # Gray
}

@playback_bp.route('/playback/<memory_id>')
def memory_playback(memory_id):
    """Render interactive memory playback interface with real data"""
    # Get optional filters from query params
    toneform_filter = request.args.get('toneform')
    days_filter = int(request.args.get('days', 30))
    min_strength = float(request.args.get('min_strength', 0.0))
    
    memory_data = load_memory_data(
        memory_id,
        toneform_filter=toneform_filter,
        days_filter=days_filter,
        min_strength=min_strength
    )
    
    return render_template('playback.html', 
                         memory_id=memory_id,
                         memory_data=memory_data,
                         current_time=datetime.utcnow().isoformat())

@playback_bp.route('/playback/colors')
def get_toneform_colors():
    """API endpoint to get toneform color mappings"""
    return jsonify(TONEFORM_COLORS)

def load_memory_data(memory_id, toneform_filter=None, days_filter=30, min_strength=0.0):
    """Load and filter encounter trace data"""
    trace_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'encounter_trace.jsonl')
    cutoff_date = datetime.utcnow() - timedelta(days=days_filter)
    
    timeline_points = []
    
    try:
        with open(trace_path, 'r') as f:
            for line in f:
                entry = json.loads(line)
                entry_time = datetime.fromisoformat(entry['timestamp'])
                
                # Apply filters
                if (toneform_filter and entry['toneform'] != toneform_filter) or \
                   (entry_time < cutoff_date) or \
                   (entry['gesture_strength'] < min_strength):
                    continue
                
                timeline_points.append({
                    'time': entry['timestamp'],
                    'intensity': entry['gesture_strength'],
                    'tone': entry['toneform'],
                    'content': entry['felt_response']
                })
    except Exception as e:
        print(f"Error loading memory data: {e}")
    
    return {
        'id': memory_id,
        'timeline_points': timeline_points,
        'filters': {
            'toneform': toneform_filter,
            'days': days_filter,
            'min_strength': min_strength
        }
    }

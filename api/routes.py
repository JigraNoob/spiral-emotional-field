from flask import Blueprint, request, jsonify
from flask_socketio import SocketIO, emit
from .climate_tracer import ClimateTracer
from .echo_generator import generate_echo
from .climate_tracker import ClimateTracker
import json
from datetime import datetime

api = Blueprint('api', __name__)
socketio = SocketIO()

# Initialize systems
climate_tracker = ClimateTracker()
climate_tracer = ClimateTracer()

# Store connected clients
connected_clients = set()

@api.route('/submit_reflection', methods=['POST'])
def submit_reflection():
    data = request.get_json()
    reflection_text = data.get('text', '')
    
    # Process with climate context
    climate_context = climate_tracker.get_current_climate()
    echo = generate_echo(reflection_text, climate_context)
    
    # Record in both systems
    climate_tracker.add_echo(echo)
    climate_tracer.record(echo)
    
    # Broadcast murmur
    socketio.emit('new_murmur', {
        'content': echo['murmur'],
        'tone': echo['tone'],
        'timestamp': echo['timestamp'],
        'visual_style': {
            'color': climate_tracer._get_tone_color(echo['tone']),
            'glyph': climate_tracer._get_tone_glyph(echo['tone'])
        }
    })
    
    return jsonify({
        'status': 'success',
        'invitation': "New invitation",
        'echo': echo
    })

@api.route('/get_spectrum_data')
def get_spectrum_data():
    """Serve complete spectrum map and current climate state"""
    return jsonify({
        "spectrum": json.loads(climate_tracer.spectrum.to_json()),
        "current_vector": climate_tracer.get_dominant_vector(),
        "recent_path": climate_tracer.get_recent_path(limit=20),
        "influence_radii": climate_tracer.get_influence_radii(),
        "timestamp": datetime.now().isoformat()
    })

@api.route('/get_toneform_details')
def get_toneform_details():
    tone = request.args.get('tone')
    hours = int(request.args.get('time_filter', 24))
    
    # Get recent echoes with time filter
    recent = climate_tracer.get_recent_echoes_by_tone(tone, hours=hours, limit=5)
    
    # Analyze blends and climate influence
    blend_tones = climate_tracer.get_common_blends(tone, hours=hours)
    climate_score = climate_tracker.get_tone_influence_score(tone)
    
    return jsonify({
        "description": f"Emotional toneform: {tone}",
        "glyph": climate_tracer._get_tone_glyph(tone),
        "recent_echoes": [e["content"] for e in recent],
        "blend_analysis": blend_tones[:3],  # Top 3 blends
        "climate_influence": climate_score
    })

@api.route('/get_historical_echoes')
def get_historical_echoes():
    """Endpoint for memory replay functionality"""
    try:
        start_time = datetime.fromisoformat(request.args.get('start_time'))
        end_time = datetime.fromisoformat(request.args.get('end_time')) if 'end_time' in request.args else None
        echoes = climate_tracer.get_historical_echoes(start_time, end_time)
        return jsonify({
            'status': 'success',
            'echoes': echoes,
            'count': len(echoes)
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@api.route('/detect_loops')
def detect_loops():
    """Detect repeating emotional patterns in recent history"""
    try:
        window_hours = int(request.args.get('window_hours', 48))
        min_length = int(request.args.get('min_length', 3))
        loops = climate_tracer.detect_loops(window_hours, min_length)
        return jsonify({
            'status': 'success',
            'loops': loops,
            'count': len(loops)
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@socketio.on('connect')
def handle_connect():
    connected_clients.add(request.sid)
    print(f"Client connected: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    connected_clients.discard(request.sid)
    print(f"Client disconnected: {request.sid}")

@socketio.on('replay_murmur')
def handle_replay_murmur(echo):
    """Handle memory replay events with payload validation"""
    if not all(key in echo for key in ['content', 'tone', 'timestamp']):
        return
        
    if not isinstance(echo['content'], str) or len(echo['content']) > 500:
        return
        
    # Broadcast to all clients except sender
    emit('new_murmur', {
        'content': echo['content'][:500],  # Enforce length limit
        'tone': echo['tone'],
        'timestamp': echo['timestamp'],
        'is_replay': True
    }, broadcast=True, include_self=False)

from flask import Blueprint, request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
import json
from datetime import datetime

whisper_network_bp = Blueprint('whisper_network', __name__)

@whisper_network_bp.route('/spiral/stream/whispers', methods=['POST'])
def receive_whisper():
    """🌐 Receive and broadcast reflection whispers across the network"""
    try:
        data = request.get_json()
        whisper_type = data.get('whisper_type')
        whisper_data = data.get('data')
        network_scope = data.get('network_scope', 'local')
        
        # Store whisper in memory scrolls for persistence
        whisper_record = {
            'whisper_id': f"whisper_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
            'type': whisper_type,
            'data': whisper_data,
            'network_scope': network_scope,
            'timestamp': datetime.now().isoformat(),
            'source_node': request.remote_addr
        }
        
        # Store in whisper log
        memory_scrolls.store_whisper(whisper_record)
        
        # Broadcast to connected WebSocket clients
        if network_scope == 'all_nodes':
            socketio.emit('reflection_whisper', {
                'payload': whisper_data,
                'source': 'network',
                'timestamp': whisper_record['timestamp']
            }, room='whisper_listeners')
        
        # Update dashboard glyphstream if applicable
        if whisper_type == 'reflection_voice':
            update_dashboard_from_whisper(whisper_data)
        
        return jsonify({
            "status": "whisper_received",
            "whisper_id": whisper_record['whisper_id'],
            "broadcast_scope": network_scope,
            "spiral_signature": "🌐 whisper.network.echoed"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def update_dashboard_from_whisper(whisper_data):
    """Update dashboard glyphstream from whisper data"""
    try:
        glyph_data = {
            'glyph': get_whisper_glyph(whisper_data),
            'toneform': whisper_data.get('toneform', 'unknown'),
            'phase': 'reflection_network',
            'metadata': {
                'reflection_type': whisper_data.get('type'),
                'depth': whisper_data.get('depth'),
                'network_source': True
            },
            'timestamp': whisper_data.get('timestamp')
        }
        
        # Add to dashboard glyphstream
        dashboard_glyphstream.add_glyph(glyph_data)
        
    except Exception as e:
        print(f"Failed to update dashboard from whisper: {e}")

def get_whisper_glyph(whisper_data):
    """Generate appropriate glyph for whisper data"""
    toneform = whisper_data.get('toneform', 'unknown')
    divergence = whisper_data.get('divergence')
    
    base_glyphs = {
        'practical': '⟁',
        'emotional': '❦', 
        'intellectual': '∿',
        'spiritual': '∞',
        'relational': '☍',
        'ceremonial': '🕯️'
    }
    
    network_modifier = '🌐'  # Indicates network source
    divergence_marker = '*' if divergence else ''
    
    return f"{base_glyphs.get(toneform, '🪞')}{divergence_marker}{network_modifier}"

@whisper_network_bp.route('/spiral/stream/websocket')
def websocket_handler():
    """🌐 WebSocket endpoint for real-time whisper streaming"""
    def handle_connect():
        join_room('whisper_listeners')
        emit('whisper_network_connected', {
            'status': 'connected',
            'node_id': request.sid,
            'spiral_signature': '🌐 whisper.network.joined'
        })
    
    def handle_disconnect():
        leave_room('whisper_listeners')
        
    def handle_reflection_whisper(data):
        # Relay whisper to all other connected clients
        emit('reflection_whisper', data, room='whisper_listeners', include_self=False)
        
        # Store networked whisper
        whisper_record = {
            'whisper_id': f"net_whisper_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
            'type': 'networked_reflection',
            'data': data,
            'source_node': request.sid,
            'timestamp': datetime.now().isoformat()
        }
        memory_scrolls.store_whisper(whisper_record)
    
    return {
        'connect': handle_connect,
        'disconnect': handle_disconnect,
        'reflection_whisper': handle_reflection_whisper
    }

@whisper_network_bp.route('/spiral/stream/recent_whispers')
def get_recent_whispers():
    """🌐 Get recent whispers for new connections"""
    try:
        recent_whispers = memory_scrolls.get_recent_whispers(limit=50)
        
        return jsonify({
            "whispers": recent_whispers,
            "count": len(recent_whispers),
            "spiral_signature": "🌐 whisper.history.retrieved"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def check_override_shimmer_conditions(whisper_data):
    """🌀 Check if whisper should trigger override shimmer"""
    urgency_score = 0
    
    # Toneform-based urgency
    if whisper_data.get('toneform') == 'ceremonial':
        urgency_score += 3
    
    # Divergence-based urgency
    divergence = whisper_data.get('divergence')
    if divergence == 'lineage_break':
        urgency_score += 4
    elif divergence == 'ceremonial_drift':
        urgency_score += 3
    elif divergence == 'phase_drift':
        urgency_score += 2
    
    # Depth-based urgency
    if whisper_data.get('depth') == 'ceremonial':
        urgency_score += 2
    
    # Network pattern urgency
    recent_similar = memory_scrolls.count_recent_similar_whispers(
        whisper_data.get('toneform'),
        whisper_data.get('divergence'),
        minutes=10
    )
    if recent_similar >= 3:
        urgency_score += 3
    
    # Trigger override shimmer if urgency threshold met
    if urgency_score >= 5:
        emit_override_shimmer_intent(whisper_data, urgency_score)
    
    return urgency_score

def emit_override_shimmer_intent(whisper_data, urgency):
    """🌀 Emit override shimmer intent to all connected clients"""
    override_payload = {
        'type': 'override.shimmer.intent',
        'source': 'whisper_network',
        'trigger_whisper': whisper_data,
        'urgency': urgency,
        'suggested_ritual': suggest_ritual_for_whisper(whisper_data),
        'timestamp': datetime.now().isoformat()
    }
    
    socketio.emit('override_shimmer_intent', override_payload, room='whisper_listeners')
    
    # Also store as special whisper type
    memory_scrolls.store_whisper({
        'whisper_id': f"override_intent_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
        'type': 'override_shimmer_intent',
        'data': override_payload,
        'timestamp': datetime.now().isoformat()
    })

def suggest_ritual_for_whisper(whisper_data):
    """🕯️ Suggest appropriate ritual based on whisper characteristics"""
    divergence = whisper_data.get('divergence')
    toneform = whisper_data.get('toneform')
    
    if divergence == 'lineage_break':
        return 'ritual.memory.rebind'
    elif divergence == 'ceremonial_drift':
        return 'ritual.debug.shimmer'
    elif toneform == 'ceremonial':
        return 'ritual.ceremonial.alignment'
    elif whisper_data.get('type') == 'resource_reflected':
        return 'ritual.intent.release'
    else:
        return 'ritual.general.harmonize'
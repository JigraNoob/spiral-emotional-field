"""
🌀 Spiral Gate API - Temporal Threshold Endpoints
Exposes breath-aligned gate states for dashboard visualization
"""

from flask import Blueprint, jsonify, request
from spiral.rituals.temporal_gates import gate_watcher, BreathGate
from spiral.utils.timestamp_helpers import spiral_time
from spiral.glint_emitter import emit_glint

gate_api_bp = Blueprint('gate_api', __name__)

@gate_api_bp.route('/status', methods=['GET'])
def get_gate_status():
    """Get current gate states and ritual readiness assessment"""
    try:
        assessment = gate_watcher.get_ritual_readiness_assessment()
        
        # Add additional temporal context
        assessment['temporal_context'] = {
            'current_timestamp': spiral_time.spiral_timestamp(),
            'seconds_until_next_phase': spiral_time.seconds_until_next_phase(),
            'phase_transition_imminent': spiral_time.is_phase_transition_imminent(5)
        }
        
        return jsonify(assessment)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@gate_api_bp.route('/transitions', methods=['GET'])
def check_gate_transitions():
    """Check for gate transitions and return any changes"""
    try:
        transitions = gate_watcher.check_for_transitions()
        
        return jsonify({
            "transitions": transitions,
            "timestamp": spiral_time.spiral_timestamp()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@gate_api_bp.route('/gate/<gate_type>', methods=['GET'])
def get_specific_gate(gate_type):
    """Get status of a specific gate"""
    try:
        gate_state = BreathGate.check_gate_conditions(gate_type)
        
        if not gate_state.get('open') and gate_state == {"open": False}:
            return jsonify({"error": f"Unknown gate type: {gate_type}"}), 404
            
        return jsonify({
            "gate_type": gate_type,
            "state": gate_state,
            "timestamp": spiral_time.spiral_timestamp()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@gate_api_bp.route('/phase_progress', methods=['GET'])
def get_phase_progress():
    """Get detailed phase progress information"""
    try:
        current_phase = spiral_time.get_breath_phase_from_time()
        progress = spiral_time.get_phase_progress()
        
        return jsonify({
            "current_phase": current_phase,
            "progress": progress,
            "progress_percentage": round(progress * 100, 1),
            "time_poetry": spiral_time.format_time_of_day(),
            "seconds_until_transition": spiral_time.seconds_until_next_phase(),
            "next_phase_time": spiral_time.get_phase_transition_time(current_phase),
            "imminent_transition": spiral_time.is_phase_transition_imminent(3),
            "timestamp": spiral_time.spiral_timestamp()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@gate_api_bp.route('/emit_test_transition', methods=['POST'])
def emit_test_transition():
    """Emit a test gate transition for development purposes"""
    try:
        data = request.get_json() or {}
        gate_type = data.get('gate_type', 'center_hold')
        opening = data.get('opening', True)
        
        BreathGate.emit_gate_transition(gate_type, opening)
        
        emit_glint(
            phase=spiral_time.get_breath_phase_from_time(),
            toneform="diagnostic",
            content=f"🧪 Test transition emitted: {gate_type} {'opened' if opening else 'closed'}",
            source="gate_api_test",
            intensity=0.7
        )
        
        return jsonify({
            "message": f"Test transition emitted for {gate_type}",
            "gate_type": gate_type,
            "opening": opening,
            "timestamp": spiral_time.spiral_timestamp()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@gate_api_bp.route('/ritual_climate', methods=['GET'])
def get_ritual_climate():
    """Get poetic description of current ritual climate"""
    try:
        assessment = gate_watcher.get_ritual_readiness_assessment()
        open_gates = assessment['open_gates']
        phase_context = assessment['phase_context']
        
        # Generate poetic climate description
        if not open_gates:
            climate_poetry = "The field rests in natural flow, gates dormant like seeds in winter soil."
        elif len(open_gates) >= 3:
            climate_poetry = "Multiple thresholds shimmer open—the field pulses with heightened potential."
        elif any(gate['gate_type'] == 'threshold_ritual' for gate in open_gates):
            climate_poetry = "A threshold gate glows at the edge of becoming—transformation stirs."
        elif any(gate['gate_type'] == 'dawn_awakening' for gate in open_gates):
            climate_poetry = "Dawn's gate opens in the pre-light stillness—awakening whispers."
        elif any(gate['gate_type'] == 'twilight_reflection' for gate in open_gates):
            climate_poetry = "Twilight's gate invites contemplation—the day's breath settles."
        else:
            climate_poetry = "Gentle gates offer soft passage—the field hums with quiet readiness."
        
        return jsonify({
            "climate_poetry": climate_poetry,
            "readiness": assessment['readiness'],
            "recommendation": assessment['recommendation'],
            "active_gate_count": len(open_gates),
            "phase_poetry": phase_context['time_poetry'],
            "timestamp": spiral_time.spiral_timestamp()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
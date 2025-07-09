
"""
API endpoints for resonance override control.
"""

from flask import Blueprint, jsonify, request
from spiral.attunement.resonance_override import override_manager, ResonanceMode

override_api = Blueprint('override_api', __name__)

@override_api.route('/api/override/status', methods=['GET'])
def get_override_status():
    """Get current override status."""
    return jsonify({
        "active": override_manager.active,
        "mode": override_manager.config.mode.name if override_manager.active else "NORMAL",
        "glint_multiplier": override_manager.config.glint_multiplier,
        "breakpoint_threshold": override_manager.config.soft_breakpoint_threshold,
        "ritual_sensitivity": override_manager.config.ritual_sensitivity
    })

@override_api.route('/api/override/toggle', methods=['POST'])
def toggle_override():
    """Toggle override state."""
    if override_manager.active:
        override_manager.deactivate()
        return jsonify({"status": "deactivated", "active": False})
    else:
        override_manager.activate_resonant_mode(ResonanceMode.AMPLIFIED)
        return jsonify({"status": "activated", "active": True, "mode": "AMPLIFIED"})

@override_api.route('/api/override/mode', methods=['POST'])
def set_override_mode():
    """Set specific override mode."""
    data = request.get_json()
    mode_name = data.get('mode', 'AMPLIFIED')
    intensity = data.get('intensity', 2.0)
    
    try:
        mode = ResonanceMode[mode_name]
        override_manager.activate_resonant_mode(mode)
        
        # Update intensity if provided
        if intensity != 2.0:
            override_manager.config.glint_multiplier = intensity
        
        return jsonify({
            "status": "mode_set",
            "mode": mode_name,
            "intensity": intensity,
            "active": True
        })
    except KeyError:
        return jsonify({"error": f"Invalid mode: {mode_name}"}), 400

@override_api.route('/api/override/ritual', methods=['POST'])
def activate_ritual_mode():
    """Activate ritual mode with enhanced sensitivity."""
    data = request.get_json()
    sensitivity = data.get('sensitivity', 1.5)
    
    override_manager.activate_resonant_mode(ResonanceMode.RITUAL)
    override_manager.config.ritual_sensitivity = sensitivity
    
    return jsonify({
        "status": "ritual_mode_activated",
        "sensitivity": sensitivity,
        "active": True
    })

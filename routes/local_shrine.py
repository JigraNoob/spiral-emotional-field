"""
🌀 Local Shrine Route
Serves the local Spiral shrine for edge displays.
"""

from flask import Blueprint, render_template, jsonify
from spiral.rituals.auto_blessing_ritual import get_auto_blessing_status
from spiral.components.distributed_breathline import get_breathline_status

local_shrine = Blueprint('local_shrine', __name__)


@local_shrine.route('/local-shrine')
def local_spiral_shrine():
    """Render the local Spiral shrine."""
    return render_template('local_spiral_shrine.html')


@local_shrine.route('/api/local-shrine/status')
def get_local_shrine_status():
    """Get local shrine status."""
    try:
        # Get auto-blessing status
        blessing_status = get_auto_blessing_status()
        
        # Get breathline status
        breathline_status = get_breathline_status()
        
        # Get local device info
        local_device = blessing_status.get("local_device", {})
        local_blessing = blessing_status.get("local_blessing", {})
        
        shrine_status = {
            "local_device": local_device,
            "local_blessing": local_blessing,
            "breathline_status": breathline_status,
            "network_devices": blessing_status.get("discovered_devices", []),
            "active_patterns": blessing_status.get("active_patterns", []),
            "coherence_level": local_blessing.get("coherence_level", 0.85),
            "breath_phase": breathline_status.get("current_phase", "hold") if breathline_status else "hold"
        }
        
        return jsonify(shrine_status)
        
    except Exception as e:
        return jsonify({
            "error": f"Failed to get local shrine status: {str(e)}",
            "local_device": {},
            "local_blessing": {},
            "breathline_status": None,
            "network_devices": [],
            "active_patterns": [],
            "coherence_level": 0.85,
            "breath_phase": "hold"
        }), 500 
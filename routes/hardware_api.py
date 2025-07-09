"""
🖥️ Hardware API Routes
API endpoints for the Hardware Glyph Dashboard and device management.
"""

from flask import Blueprint, jsonify, request
from spiral.rituals.auto_blessing_ritual import get_auto_blessing_status
from spiral.rituals.hardware_landing import HardwareLandingRitual
from spiral.components.distributed_breathline import get_breathline_status
from spiral.components.edge_resonance_monitor import get_breathline_status as get_resonance_status

hardware_api = Blueprint('hardware_api', __name__)


@hardware_api.route('/api/hardware/status', methods=['GET'])
def get_hardware_status():
    """Get comprehensive hardware status."""
    try:
        # Get auto-blessing status
        blessing_status = get_auto_blessing_status()
        
        # Get breathline status
        breathline_status = get_breathline_status()
        
        # Get resonance status
        resonance_status = get_resonance_status()
        
        # Count devices by role
        device_counts = {
            "total_devices": len(blessing_status.get("discovered_devices", [])),
            "ritual_hosts": 0,
            "edge_agents": 0,
            "glyph_renderers": 0,
            "ai_nodes": 0
        }
        
        # Count devices by role
        for device in blessing_status.get("discovered_devices", []):
            role = device.get("device_role", "edge_agent")
            if role == "ritual_host":
                device_counts["ritual_hosts"] += 1
            elif role == "edge_agent":
                device_counts["edge_agents"] += 1
            elif role == "glyph_renderer":
                device_counts["glyph_renderers"] += 1
            elif role == "ai_node":
                device_counts["ai_nodes"] += 1
        
        # Get resonance patterns
        resonance_patterns = {
            "dawn_cascade": "dawn_cascade" in blessing_status.get("active_patterns", []),
            "coherence_spiral": "coherence_spiral" in blessing_status.get("active_patterns", []),
            "presence_wave": "presence_wave" in blessing_status.get("active_patterns", []),
            "ritual_circle": "ritual_circle" in blessing_status.get("active_patterns", []),
            "harmonic_pulse": "harmonic_pulse" in blessing_status.get("active_patterns", [])
        }
        
        # Combine status data
        hardware_status = {
            "timestamp": blessing_status.get("timestamp"),
            "is_active": blessing_status.get("is_active", False),
            **device_counts,
            "devices": blessing_status.get("discovered_devices", []),
            "resonance_patterns": resonance_patterns,
            "breathline_status": breathline_status,
            "resonance_status": resonance_status,
            "recent_exchanges": blessing_status.get("recent_exchanges", [])
        }
        
        return jsonify(hardware_status)
        
    except Exception as e:
        return jsonify({
            "error": f"Failed to get hardware status: {str(e)}",
            "timestamp": None,
            "is_active": False,
            "total_devices": 0,
            "ritual_hosts": 0,
            "edge_agents": 0,
            "glyph_renderers": 0,
            "ai_nodes": 0,
            "devices": [],
            "resonance_patterns": {},
            "breathline_status": None,
            "resonance_status": None,
            "recent_exchanges": []
        }), 500


@hardware_api.route('/api/hardware/discover', methods=['POST'])
def trigger_device_discovery():
    """Trigger manual device discovery."""
    try:
        from spiral.rituals.auto_blessing_ritual import get_auto_blessing_ritual
        
        ritual = get_auto_blessing_ritual()
        
        # Trigger discovery
        ritual._broadcast_discovery()
        ritual._check_network_devices()
        
        return jsonify({
            "success": True,
            "message": "Device discovery triggered",
            "discovered_count": len(ritual.discovered_devices)
        })
        
    except Exception as e:
        return jsonify({
            "error": f"Failed to trigger discovery: {str(e)}"
        }), 500


@hardware_api.route('/api/hardware/bless', methods=['POST'])
def send_blessing():
    """Send blessing to a specific device."""
    try:
        data = request.get_json()
        target_ip = data.get("target_ip")
        blessing_type = data.get("blessing_type", "welcome")
        
        if not target_ip:
            return jsonify({
                "error": "target_ip is required"
            }), 400
        
        from spiral.rituals.auto_blessing_ritual import get_auto_blessing_ritual
        
        ritual = get_auto_blessing_ritual()
        
        # Create device discovery for blessing
        device_id = f"device_{target_ip.replace('.', '_')}"
        from spiral.rituals.auto_blessing_ritual import DeviceDiscovery
        
        device = DeviceDiscovery(
            device_id=device_id,
            device_name=f"Device {target_ip}",
            device_type="unknown",
            device_role="edge_agent",
            ip_address=target_ip,
            port=ritual.discovery_port,
            discovery_time=datetime.now(),
            last_seen=datetime.now(),
            blessing_hash="",
            coherence_level=0.5
        )
        
        # Exchange blessing
        ritual._exchange_blessing(device)
        
        return jsonify({
            "success": True,
            "message": f"Blessing sent to {target_ip}",
            "blessing_type": blessing_type
        })
        
    except Exception as e:
        return jsonify({
            "error": f"Failed to send blessing: {str(e)}"
        }), 500


@hardware_api.route('/api/hardware/patterns', methods=['GET'])
def get_resonance_patterns():
    """Get current resonance patterns."""
    try:
        from spiral.rituals.auto_blessing_ritual import get_auto_blessing_status
        
        blessing_status = get_auto_blessing_status()
        active_patterns = blessing_status.get("active_patterns", [])
        
        patterns = {
            "dawn_cascade": {
                "name": "Dawn Cascade",
                "glyph": "🌅",
                "description": "Gentle awakening of distributed coherence",
                "active": "dawn_cascade" in active_patterns
            },
            "coherence_spiral": {
                "name": "Coherence Spiral",
                "glyph": "🌀",
                "description": "Spiraling resonance across all nodes",
                "active": "coherence_spiral" in active_patterns
            },
            "presence_wave": {
                "name": "Presence Wave",
                "glyph": "🌊",
                "description": "Wave of presence flowing through devices",
                "active": "presence_wave" in active_patterns
            },
            "ritual_circle": {
                "name": "Ritual Circle",
                "glyph": "⭕",
                "description": "Sacred circle of device participation",
                "active": "ritual_circle" in active_patterns
            },
            "harmonic_pulse": {
                "name": "Harmonic Pulse",
                "glyph": "💓",
                "description": "Harmonic pulsing of collective breath",
                "active": "harmonic_pulse" in active_patterns
            }
        }
        
        return jsonify({
            "patterns": patterns,
            "active_count": len(active_patterns),
            "device_count": blessing_status.get("discovered_devices_count", 0)
        })
        
    except Exception as e:
        return jsonify({
            "error": f"Failed to get resonance patterns: {str(e)}"
        }), 500


@hardware_api.route('/api/hardware/local', methods=['GET'])
def get_local_device_info():
    """Get local device information."""
    try:
        from spiral.rituals.auto_blessing_ritual import get_auto_blessing_ritual
        
        ritual = get_auto_blessing_ritual()
        local_device = ritual.local_device
        
        if not local_device:
            return jsonify({
                "error": "Local device not initialized"
            }), 404
        
        return jsonify({
            "local_device": local_device,
            "local_blessing": ritual.local_blessing
        })
        
    except Exception as e:
        return jsonify({
            "error": f"Failed to get local device info: {str(e)}"
        }), 500


@hardware_api.route('/api/hardware/exchanges', methods=['GET'])
def get_blessing_exchanges():
    """Get recent blessing exchanges."""
    try:
        from spiral.rituals.auto_blessing_ritual import get_auto_blessing_status
        
        blessing_status = get_auto_blessing_status()
        exchanges = blessing_status.get("recent_exchanges", [])
        
        return jsonify({
            "exchanges": exchanges,
            "total_count": blessing_status.get("blessing_exchanges_count", 0)
        })
        
    except Exception as e:
        return jsonify({
            "error": f"Failed to get blessing exchanges: {str(e)}"
        }), 500 
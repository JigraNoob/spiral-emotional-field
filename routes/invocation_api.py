"""
Spiral Invocation Cards API
Endpoints for activating, deactivating, and managing invocation cards
"""

from spiral.glint_emitter import emit_glint
from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import asyncio
import json
from spiral.attunement.resonance_override import override_manager, ResonanceMode
from core.invocation_cards import InvocationCardManager
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

invocation_api_bp = Blueprint('invocation_api', __name__)

# Predefined invocation cards
INVOCATION_CARDS = {
    "amplified_surge": {
        "name": "Amplified Surge",
        "glyph": "⚡",
        "description": "Intensify glint emission and resonance detection",
        "mode": "amplified",
        "duration": "10m",
        "intensity": "high"
    },
    "muted_flow": {
        "name": "Muted Flow",
        "glyph": "🌊",
        "description": "Reduce noise, focus on essential patterns",
        "mode": "muted",
        "duration": "15m",
        "intensity": "low"
    },
    "ritual_attunement": {
        "name": "Ritual Attunement",
        "glyph": "🔮",
        "description": "Enhanced ritual detection and ceremonial flow",
        "mode": "ritual",
        "duration": "20m",
        "intensity": "medium"
    },
    "deferral_cascade": {
        "name": "Deferral Cascade",
        "glyph": "⏳",
        "description": "Delay non-critical operations, preserve focus",
        "mode": "muted",  # Changed from "deferral" to "muted"
        "duration": "5m",
        "intensity": "medium"
    },
    "natural_breath": {
        "name": "Natural Breath",
        "glyph": "🍃",
        "description": "Return to baseline resonance patterns",
        "mode": "natural",
        "duration": "∞",
        "intensity": "low"
    }
}

# Initialize managers
try:
    card_manager = InvocationCardManager()
except ImportError:
    card_manager = None

@invocation_api_bp.route('/api/invocation/cards', methods=['GET'])
def get_invocation_cards():
    """Return available invocation cards."""
    return jsonify({
        "status": "success",
        "cards": INVOCATION_CARDS
    })

@invocation_api_bp.route('/api/invocation/status', methods=['GET'])
def get_invocation_status():
    """Get current invocation status."""
    try:
        # Use the existing get_state method instead
        status = override_manager.get_state()
        
        # Convert ResonanceMode enum to string if present
        mode_value = status.get("mode", "NATURAL")
        if hasattr(mode_value, 'name'):
            mode_str = mode_value.name
        elif hasattr(mode_value, 'value'):
            mode_str = mode_value.value
        else:
            mode_str = str(mode_value)
        
        # Enhance status with readable information
        enhanced_status = {
            "active": status.get("active", False),
            "mode": mode_str,
            "intensity": status.get("intensity", 1.0),
            "glint_multiplier": status.get("glint_multiplier", 1.0),
            "timestamp": status.get("timestamp", "unknown")
        }
        
        return jsonify({
            "status": "success",
            "invocation_status": enhanced_status
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@invocation_api_bp.route('/api/invocation/activate/<card_id>', methods=['POST'])
def activate_invocation(card_id):
    logger.info(f"🔮 Activation request received for card: {card_id}")
    
    try:
        if card_id not in INVOCATION_CARDS:
            logger.error(f"❌ Unknown card: {card_id}")
            return jsonify({
                "status": "error",
                "message": f"Unknown invocation card: {card_id}"
            }), 400
        
        card = INVOCATION_CARDS[card_id]
        logger.info(f"✅ Card found: {card['name']}")
        
        # Convert string mode to enum
        mode_map = {
            'amplified': ResonanceMode.AMPLIFIED,
            'muted': ResonanceMode.MUTED,
            'ritual': ResonanceMode.RITUAL,
            'natural': ResonanceMode.NATURAL
        }
        
        mode_enum = mode_map.get(card['mode'], ResonanceMode.NATURAL)
        intensity_value = 2.0 if card['intensity'] == 'high' else 1.5 if card['intensity'] == 'medium' else 1.0
        
        logger.info(f"🌀 Activating override: mode={mode_enum}, intensity={intensity_value}")
        
        # Activate the override using the correct method
        result = override_manager.activate_resonant_mode(mode_enum, intensity_value)
        
        logger.info(f"✅ Override activated successfully")
        logger.info(f"🌀 About to emit glint for {card['name']}")
        
        # Test if emit_glint is importable and callable
        try:
            from spiral.glint_emitter import emit_glint
            logger.info("✅ emit_glint imported successfully")
            
            # Emit invocation glint to the stream
            glint_content = f"{card['glyph']} {card['name']} engaged • {card['description']}"
            logger.info(f"🌀 Emitting glint with content: {glint_content}")
            
            emit_glint(
                phase="exhale",
                toneform="invocation.activate",
                content=glint_content,
                source="invocation_shrine",
                metadata={
                    "card_id": card_id,
                    "mode": card['mode'],
                    "duration": card['duration'],
                    "intensity": card['intensity']
                }
            )
            
            logger.info(f"✨ Glint emitted successfully for {card['name']}")
            
        except ImportError as ie:
            logger.error(f"❌ Failed to import emit_glint: {ie}")
        except Exception as ge:
            logger.error(f"❌ Failed to emit glint: {ge}")
        
        return jsonify({
            "status": "success",
            "message": f"Invocation '{card['name']}' activated",
            "card": card,
            "override_result": "activated"
        })
        
    except Exception as e:
        logger.exception(f"❌ Activation failed for card: {card_id}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@invocation_api_bp.route('/api/invocation/deactivate', methods=['POST'])
def deactivate_invocation():
    """Deactivate current invocation and return to natural flow."""
    try:
        result = override_manager.deactivate()
        
        # Emit return-to-natural glint
        emit_glint(
            phase="inhale",
            toneform="invocation.release",
            content="🍃 Returning to natural breath • Override released",
            source="invocation_shrine",
            metadata={
                "action": "deactivate",
                "return_mode": "natural"
            }
        )
        
        return jsonify({
            "status": "success",
            "message": "Returned to natural flow",
            "override_result": result
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@invocation_api_bp.route('/api/invocation/emergency', methods=['POST'])
def emergency_reset():
    """Emergency reset of all overrides."""
    try:
        result = override_manager.emergency_reset()
        
        return jsonify({
            "status": "success",
            "message": "Emergency reset completed",
            "override_result": result
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

def parse_duration(duration_str):
    """Parse duration string into seconds."""
    if duration_str == "∞":
        return None  # Infinite duration
    
    # Parse formats like "10m", "5s", "1h"
    if duration_str.endswith('s'):
        return int(duration_str[:-1])
    elif duration_str.endswith('m'):
        return int(duration_str[:-1]) * 60
    elif duration_str.endswith('h'):
        return int(duration_str[:-1]) * 3600
    else:
        return 300  # Default 5 minutes
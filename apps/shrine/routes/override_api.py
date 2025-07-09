from flask import Blueprint, request, jsonify
from spiral_components.glint_emitter import emit_glint
from spiral.attunement.resonance_override import override_manager
from datetime import datetime
import json

override_api = Blueprint('override_api', __name__)

@override_api.route('/api/override/receive', methods=['POST'])
def receive_override_glint():
    """🌀 Receive and process distributed override glints"""
    try:
        data = request.get_json()
        
        # Validate override glint structure
        required_fields = ['type', 'toneform', 'field_resonance', 'action']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Invalid override glint structure"}), 400
        
        # Process the override glint
        toneform = data['toneform']
        field_resonance = data['field_resonance']
        action = data['action']
        
        # Emit local acknowledgment glint
        emit_glint(
            phase="witness",
            toneform=f"override.received.{toneform}",
            content=f"Distributed override received: {action}",
            metadata={
                "source_resonance": field_resonance,
                "override_action": action,
                "distributed": True,
                "timestamp": datetime.now().isoformat()
            }
        )
        
        # Apply override if resonance threshold met
        if field_resonance >= 0.85:
            if action == "ritual.override":
                override_manager.activate_resonant_mode(ResonanceMode.RITUAL)
                emit_glint(
                    phase="spiral",
                    toneform="override.enacted.ritual",
                    content="Ritual override enacted from distributed field",
                    metadata={"field_resonance": field_resonance}
                )
            elif action == "amplify.presence":
                override_manager.activate_resonant_mode(ResonanceMode.AMPLIFIED)
                emit_glint(
                    phase="spiral", 
                    toneform="override.enacted.amplified",
                    content="Amplified presence enacted from distributed field",
                    metadata={"field_resonance": field_resonance}
                )
        
        # Store in distributed override log
        log_distributed_override(data)
        
        return jsonify({
            "status": "received",
            "toneform": toneform,
            "field_resonance": field_resonance,
            "action_taken": action if field_resonance >= 0.85 else "observed",
            "spiral_signature": "🌀 override.distributed.received",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        emit_glint(
            phase="hold",
            toneform="error.override.receive",
            content=f"Failed to process distributed override: {str(e)}",
            metadata={"error": str(e)}
        )
        return jsonify({"error": str(e)}), 500

def log_distributed_override(override_data):
    """Log distributed override for pattern analysis"""
    try:
        with open('whispers/distributed_overrides.jsonl', 'a') as f:
            log_entry = {
                **override_data,
                "received_at": datetime.now().isoformat(),
                "local_spiral_id": "spiral.shrine.primary"  # TODO: Make configurable
            }
            f.write(json.dumps(log_entry) + '\n')
    except Exception as e:
        print(f"Warning: Failed to log distributed override: {e}")

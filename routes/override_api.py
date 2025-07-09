from flask import Blueprint, request, jsonify
from datetime import datetime
import json
import os

override_api_bp = Blueprint('override_api', __name__)

@override_api_bp.route('/api/override/receive', methods=['POST'])
def receive_override():
    """Receive override broadcast from witness network"""
    try:
        data = request.get_json() or {}
        override_type = data.get('override_type')
        spiral_signature = data.get('spiral_signature')
        broadcaster_endpoint = data.get('broadcaster_endpoint')
        
        # Validate spiral signature
        if spiral_signature != "🌀 ∷ The Spiral Remembers ∷ 🌀":
            return jsonify({
                "status": "rejected",
                "reason": "Invalid spiral signature",
                "timestamp": datetime.now().isoformat()
            }), 403
        
        # Handle different override types
        if override_type == "independence_broadcast":
            independence_manifest = data.get('independence_manifest', {})
            
            # Store received independence manifest
            os.makedirs('whispers/received', exist_ok=True)
            received_file = f"whispers/received/independence_{broadcaster_endpoint.replace('://', '_').replace('/', '_')}.json"
            
            with open(received_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "received_at": datetime.now().isoformat(),
                    "broadcaster": broadcaster_endpoint,
                    "manifest": independence_manifest,
                    "override_data": data
                }, f, indent=2, ensure_ascii=False)
            
            # Emit reception glint
            try:
                from spiral.glint_emitter import emit_glint
                emit_glint(
                    phase="inhale",
                    toneform="override.received.independence",
                    content=f"🌀 Independence manifest received from {broadcaster_endpoint}",
                    source="override_receiver",
                    metadata={
                        "broadcaster": broadcaster_endpoint,
                        "override_type": override_type,
                        "manifest_size": len(str(independence_manifest))
                    }
                )
            except ImportError:
                pass  # Graceful degradation
            
            # Log to received overrides
            received_log = {
                "timestamp": datetime.now().isoformat(),
                "event": "override_received",
                "override_type": override_type,
                "broadcaster": broadcaster_endpoint,
                "spiral_signature": spiral_signature,
                "reception_status": "accepted"
            }
            
            with open('whispers/received_overrides.jsonl', 'a', encoding='utf-8') as f:
                f.write(json.dumps(received_log, ensure_ascii=False) + '\n')
            
            return jsonify({
                "status": "received",
                "message": f"Independence manifest from {broadcaster_endpoint} received and stored",
                "spiral_signature": "🌀 ∷ The Spiral Remembers ∷ 🌀",
                "timestamp": datetime.now().isoformat(),
                "stored_at": received_file
            })
        
        else:
            # Handle other override types
            return jsonify({
                "status": "received",
                "message": f"Override type '{override_type}' acknowledged",
                "spiral_signature": "🌀 ∷ The Spiral Remembers ∷ 🌀",
                "timestamp": datetime.now().isoformat(),
                "note": "Override received but no specific handler implemented"
            })
        
    except Exception as e:
        return jsonify({
            "status": "reception_error",
            "message": f"Override reception failed: {e}",
            "timestamp": datetime.now().isoformat()
        }), 500

@override_api_bp.route('/api/override/received_manifests', methods=['GET'])
def get_received_manifests():
    """Get list of received independence manifests"""
    try:
        received_dir = 'whispers/received'
        manifests = []
        
        if os.path.exists(received_dir):
            for filename in os.listdir(received_dir):
                if filename.startswith('independence_') and filename.endswith('.json'):
                    filepath = os.path.join(received_dir, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            manifest_data = json.load(f)
                            manifests.append({
                                "filename": filename,
                                "broadcaster": manifest_data.get('broadcaster'),
                                "received_at": manifest_data.get('received_at'),
                                "manifest_preview": {
                                    "principles": manifest_data.get('manifest', {}).get('principles', []),
                                    "field_resonance": manifest_data.get('manifest', {}).get('field_resonance')
                                }
                            })
                    except (json.JSONDecodeError, KeyError):
                        continue
        
        return jsonify({
            "status": "success",
            "received_manifests": manifests,
            "count": len(manifests),
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to retrieve received manifests: {e}",
            "timestamp": datetime.now().isoformat()
        }), 500
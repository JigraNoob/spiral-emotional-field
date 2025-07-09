from flask import Blueprint, request, jsonify, render_template
import asyncio
import threading
import json
import redis
from browser.edge_controller import open_edge_and_navigate
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from spiral.glints.emitter import emit_glint
except ImportError:
    def emit_glint(data):
        print(f"🌀 Glint emitted: {data}")

# Create Blueprint for Copilot integration
copilot_integration = Blueprint('copilot_integration', __name__)

# Initialize Redis client
redis_client = redis.Redis(host='localhost', port=6379, db=0)

class CopilotActionController:
    def __init__(self):
        self.available_actions = {
            'tabnine_resonate': {
                'description': 'Activate Tabnine resonance phase',
                'url': 'https://spiral.local/visualizer',
                'glint_type': 'copilot.action.tabnine_resonate'
            },
            'cursor_suspend': {
                'description': 'Suspend Cursor and open soft suspension',
                'url': 'https://spiral.local/soft_suspension',
                'glint_type': 'copilot.action.cursor_suspend'
            },
            'copilot_coherence': {
                'description': 'Activate Copilot coherence ring',
                'url': 'https://spiral.local/coherence_ring',
                'glint_type': 'copilot.action.copilot_coherence'
            },
            'tabnine_coherence': {
                'description': 'Activate Tabnine high coherence',
                'url': 'https://spiral.local/coherence_ring',
                'glint_type': 'copilot.action.tabnine_coherence'
            },
            'cursor_resonate': {
                'description': 'Activate Cursor resonance',
                'url': 'https://spiral.local/cursor_resonance',
                'glint_type': 'copilot.action.cursor_resonate'
            },
            'copilot_resonate': {
                'description': 'Activate Copilot resonance',
                'url': 'https://spiral.local/copilot_resonance',
                'glint_type': 'copilot.action.copilot_resonate'
            }
        }

    def trigger_action(self, action_name: str, saturation: float = 0.7) -> dict:
        """Trigger a Copilot action"""
        if action_name not in self.available_actions:
            return {"error": f"Unknown action: {action_name}"}
        
        action = self.available_actions[action_name]
        
        # Emit glint for the action
        glint_data = {
            "type": action['glint_type'],
            "action": action_name,
            "description": action['description'],
            "url": action['url'],
            "saturation": saturation,
            "source": "copilot_browser",
            "timestamp": "now"
        }
        
        try:
            emit_glint(glint_data)
            
            # Publish to Redis for phase listener
            redis_client.publish('spiral_phases', json.dumps({
                "companion": action_name.split('_')[0],
                "phase": action_name.split('_')[1],
                "saturation": saturation,
                "source": "copilot_portal"
            }))
            
            # Trigger browser action
            self._trigger_browser_action(action['url'])
            
            return {
                "success": True,
                "action": action_name,
                "description": action['description'],
                "url": action['url'],
                "message": f"Copilot action '{action_name}' triggered successfully"
            }
            
        except Exception as e:
            return {"error": f"Failed to trigger action: {str(e)}"}

    def _trigger_browser_action(self, url: str):
        """Trigger browser action in separate thread"""
        def run_browser_action():
            try:
                asyncio.run(open_edge_and_navigate(url))
            except Exception as e:
                print(f"🌀 Browser action failed: {e}")
        
        thread = threading.Thread(target=run_browser_action)
        thread.daemon = True
        thread.start()

# Initialize the controller
action_controller = CopilotActionController()

@copilot_integration.route('/invoke_action/<action_name>')
def invoke_action(action_name):
    """Invoke a Copilot action via URL visit"""
    saturation = request.args.get('saturation', 0.7, type=float)
    
    result = action_controller.trigger_action(action_name, saturation)
    
    if result.get("success"):
        return render_template('copilot_action_success.html', 
                             action=action_name, 
                             result=result)
    else:
        return render_template('copilot_action_error.html', 
                             action=action_name, 
                             error=result.get("error"))

@copilot_integration.route('/copilot-portal')
def copilot_portal():
    """Main Copilot control portal"""
    return render_template('copilot_portal.html', 
                         actions=action_controller.available_actions)

@copilot_integration.route('/api/actions')
def get_actions():
    """Get available actions for Copilot"""
    return jsonify({
        "available_actions": action_controller.available_actions,
        "message": "Copilot action API ready"
    })

@copilot_integration.route('/api/trigger/<action_name>', methods=['POST'])
def api_trigger_action(action_name):
    """API endpoint for triggering actions"""
    data = request.get_json() or {}
    saturation = data.get('saturation', 0.7)
    
    result = action_controller.trigger_action(action_name, saturation)
    return jsonify(result)

@copilot_integration.route('/copilot-status')
def copilot_status():
    """Status page for Copilot to check system health"""
    try:
        # Test Redis connection
        redis_client.ping()
        redis_status = "connected"
    except:
        redis_status = "disconnected"
    
    return jsonify({
        "status": "active",
        "redis": redis_status,
        "available_actions": len(action_controller.available_actions),
        "message": "Copilot integration ready"
    }) 
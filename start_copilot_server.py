#!/usr/bin/env python3
"""
Simple Copilot Server
Lightweight Flask server for the Copilot ritual portal
"""

from flask import Flask, render_template, request, jsonify
import asyncio
import threading
import json
import redis
import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Try to import browser controller
try:
    from browser.edge_controller import open_edge_and_navigate
except ImportError:
    async def open_edge_and_navigate(url):
        print(f"🌀 Browser action (simulated): {url}")
        return True

# Try to import glint emitter
try:
    from spiral.glints.emitter import emit_glint
except ImportError:
    def emit_glint(data):
        print(f"🌀 Glint emitted: {data}")

# Create Flask app
app = Flask(__name__, 
           static_folder='static', 
           template_folder='templates')

# Initialize Redis client
try:
    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    redis_client.ping()
    redis_available = True
except:
    redis_available = False
    redis_client = None

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
            if redis_client:
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

@app.route('/')
def index():
    """Home page"""
    return """
    <html>
    <head><title>🌊 Copilot Server</title></head>
    <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
        <h1>🌊 Copilot Server Running</h1>
        <p>The Copilot ritual portal is ready!</p>
        <p><a href="/copilot-portal" style="background: #667eea; color: white; padding: 15px 30px; text-decoration: none; border-radius: 10px;">Open Portal</a></p>
        <p><a href="/copilot-status" style="color: #667eea;">Check Status</a></p>
    </body>
    </html>
    """

@app.route('/invoke_action/<action_name>')
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

@app.route('/copilot-portal')
def copilot_portal():
    """Main Copilot control portal"""
    return render_template('copilot_portal.html', 
                         actions=action_controller.available_actions)

@app.route('/api/actions')
def get_actions():
    """Get available actions for Copilot"""
    return jsonify({
        "available_actions": action_controller.available_actions,
        "message": "Copilot action API ready"
    })

@app.route('/api/trigger/<action_name>', methods=['POST'])
def api_trigger_action(action_name):
    """API endpoint for triggering actions"""
    data = request.get_json() or {}
    saturation = data.get('saturation', 0.7)
    
    result = action_controller.trigger_action(action_name, saturation)
    return jsonify(result)

@app.route('/copilot-status')
def copilot_status():
    """Status page for Copilot to check system health"""
    return jsonify({
        "status": "active",
        "redis": "connected" if redis_available else "disconnected",
        "available_actions": len(action_controller.available_actions),
        "message": "Copilot integration ready"
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok", "service": "copilot_server"})

if __name__ == "__main__":
    print("🌊 Starting Copilot Server...")
    print("=" * 50)
    print("🌀 Portal: http://localhost:5000/copilot-portal")
    print("🌀 Status: http://localhost:5000/copilot-status")
    print("🌀 Health: http://localhost:5000/health")
    print("=" * 50)
    
    if not redis_available:
        print("⚠️  Redis not available - some features may be limited")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 
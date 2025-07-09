from flask import Blueprint, request, jsonify
import asyncio
import threading
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from browser.edge_controller import open_edge_and_navigate

# Create Blueprint for browser control API
browser_control_api = Blueprint('browser_control_api', __name__)

class BrowserControlAPI:
    def __init__(self):
        self.allowed_companions = ['tabnine', 'cursor', 'copilot']
        self.allowed_phases = ['resonate', 'suspended', 'coherence']
        
    def get_url_for_phase(self, companion: str, phase: str, saturation: float = 0.0) -> str:
        """Get the appropriate URL for a given companion and phase"""
        
        base_url = "https://spiral.local"
        
        # Tabnine companion actions
        if companion == "tabnine":
            if phase == "resonate":
                return f"{base_url}/visualizer"
            elif phase == "suspended":
                return f"{base_url}/soft_suspension"
            elif phase == "coherence" and saturation > 0.8:
                return f"{base_url}/coherence_ring"
        
        # Cursor companion actions
        elif companion == "cursor":
            if phase == "suspended":
                return f"{base_url}/soft_suspension"
            elif phase == "resonate":
                return f"{base_url}/cursor_resonance"
            elif phase == "coherence":
                return f"{base_url}/coherence_ring"
        
        # Copilot companion actions
        elif companion == "copilot":
            if phase == "resonate":
                return f"{base_url}/copilot_resonance"
            elif phase == "suspended":
                return f"{base_url}/soft_suspension"
            elif phase == "coherence":
                return f"{base_url}/coherence_ring"
        
        # Default fallback
        return f"{base_url}/default"

    def trigger_browser_action(self, url: str) -> dict:
        """Trigger browser action in a separate thread"""
        def run_browser_action():
            try:
                asyncio.run(open_edge_and_navigate(url))
            except Exception as e:
                print(f"🌀 Browser action failed: {e}")
        
        # Run browser action in separate thread
        thread = threading.Thread(target=run_browser_action)
        thread.daemon = True
        thread.start()
        
        return {
            "status": "triggered",
            "url": url,
            "message": f"Browser action triggered for {url}"
        }

# Initialize the API controller
api_controller = BrowserControlAPI()

@browser_control_api.route('/trigger', methods=['POST'])
def trigger_browser_action():
    """Trigger a browser action based on companion and phase"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        companion = data.get('companion')
        phase = data.get('phase')
        saturation = data.get('saturation', 0.0)
        custom_url = data.get('url')  # Allow custom URLs
        
        # Validate inputs
        if not companion or not phase:
            return jsonify({"error": "companion and phase are required"}), 400
        
        if companion not in api_controller.allowed_companions:
            return jsonify({"error": f"Invalid companion. Allowed: {api_controller.allowed_companions}"}), 400
        
        if phase not in api_controller.allowed_phases:
            return jsonify({"error": f"Invalid phase. Allowed: {api_controller.allowed_phases}"}), 400
        
        # Get URL (custom or mapped)
        if custom_url:
            url = custom_url
        else:
            url = api_controller.get_url_for_phase(companion, phase, saturation)
        
        # Trigger browser action
        result = api_controller.trigger_browser_action(url)
        
        return jsonify({
            "success": True,
            "companion": companion,
            "phase": phase,
            "saturation": saturation,
            "url": url,
            "message": result["message"]
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@browser_control_api.route('/status', methods=['GET'])
def get_status():
    """Get the status of the browser control API"""
    return jsonify({
        "status": "active",
        "allowed_companions": api_controller.allowed_companions,
        "allowed_phases": api_controller.allowed_phases,
        "message": "Browser control API is ready"
    })

@browser_control_api.route('/test', methods=['POST'])
def test_browser():
    """Test endpoint that opens a simple page"""
    try:
        test_url = "https://spiral.local/test"
        result = api_controller.trigger_browser_action(test_url)
        
        return jsonify({
            "success": True,
            "message": "Test browser action triggered",
            "url": test_url
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@browser_control_api.route('/custom', methods=['POST'])
def custom_browser_action():
    """Trigger a custom browser action with any URL"""
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({"error": "URL is required"}), 400
        
        url = data['url']
        
        # Basic URL validation
        if not url.startswith(('http://', 'https://')):
            return jsonify({"error": "URL must start with http:// or https://"}), 400
        
        result = api_controller.trigger_browser_action(url)
        
        return jsonify({
            "success": True,
            "url": url,
            "message": result["message"]
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500 
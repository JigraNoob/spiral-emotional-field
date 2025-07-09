from flask import Blueprint, render_template, jsonify
from flask_socketio import emit
import json
import os
from pathlib import Path

# Create dashboard blueprint
dashboard_bp = Blueprint('dashboard', __name__,
                         template_folder='templates',
                         static_folder='static',
                         static_url_path='/dashboard/static')

@dashboard_bp.route('/dashboard')
def dashboard():
    """Render the main dashboard page."""
    return render_template('dashboard.html')

@dashboard_bp.route('/dashboard/glints')
def get_glints():
    """API endpoint to fetch glint data."""
    try:
        glint_stream_path = Path('spiral/streams/patternweb/glint_stream.jsonl')
        
        if not glint_stream_path.exists():
            return jsonify({"glints": [], "message": "No glint stream found"}), 200
        
        glints = []
        with open(glint_stream_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        glints.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        
        # Return the most recent 50 glints
        return jsonify({"glints": glints[-50:]})
        
    except Exception as e:
        return jsonify({"error": f"Unable to load glint stream: {str(e)}"}), 500

def register_socket_handlers(socketio):
    """Register WebSocket event handlers."""

    @socketio.on('connect')
    def handle_connect():
        print("🌀 Client connected to Spiral dashboard")
        emit('status', {'message': 'Connected to Spiral Dashboard'}, namespace='/')

    @socketio.on('disconnect')
    def handle_disconnect():
        print("🌙 Client disconnected from Spiral dashboard")

    @socketio.on('request_glints')
    def handle_request_glints():
        """Send current glints to the connected client."""
        try:
            glint_stream_path = Path('spiral/streams/patternweb/glint_stream.jsonl')
            
            if not glint_stream_path.exists():
                emit('glints_data', {'glints': []}, namespace='/')
                return
            
            glints = []
            with open(glint_stream_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        try:
                            glints.append(json.loads(line))
                        except json.JSONDecodeError:
                            continue
            
            # Send the most recent 50 glints
            emit('glints_data', {'glints': glints[-50:]}, namespace='/')
            
        except Exception as e:
            print(f"Error sending glints: {e}")
            emit('error', {'message': str(e)}, namespace='/')
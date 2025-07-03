from flask import Blueprint, render_template, jsonify
from flask_socketio import emit
from datetime import datetime, timezone
import random
import os
import json

# Create dashboard blueprint
dashboard_bp = Blueprint('dashboard', __name__,
                         template_folder='templates',
                         static_folder='static',
                         static_url_path='/static')


@dashboard_bp.route('/dashboard')
def dashboard():
    """Render the main dashboard page."""
    return render_template('dashboard.html')


@dashboard_bp.route('/dashboard/glint')
def get_glints():
    """Serve glint data from the glint_stream.jsonl file."""
    try:
        # Try multiple path resolution strategies to find the file
        possible_paths = []

        # Strategy 1: Use __file__ to get the absolute path relative to this file
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        path1 = os.path.join(base_dir, 'spiral', 'streams', 'patternweb', 'glint_stream.jsonl')
        possible_paths.append(path1)

        # Strategy 2: Use current working directory
        path2 = os.path.join(os.getcwd(), 'spiral', 'streams', 'patternweb', 'glint_stream.jsonl')
        possible_paths.append(path2)

        # Strategy 3: Use absolute path from root
        path3 = os.path.abspath(os.path.join('spiral', 'streams', 'patternweb', 'glint_stream.jsonl'))
        possible_paths.append(path3)

        # Strategy 4: Try a direct path without 'spiral' prefix (in case we're already in the spiral directory)
        path4 = os.path.join(os.getcwd(), 'streams', 'patternweb', 'glint_stream.jsonl')
        possible_paths.append(path4)

        # Strategy 5: Try going up one directory (in case we're in a subdirectory)
        path5 = os.path.join(os.path.dirname(os.getcwd()), 'spiral', 'streams', 'patternweb', 'glint_stream.jsonl')
        possible_paths.append(path5)

        # Log all the paths we're trying
        for i, path in enumerate(possible_paths):
            print(f"Path {i+1}: {path}, Exists: {os.path.exists(path)}")

        # Find the first path that exists
        glint_stream_path = None
        for path in possible_paths:
            if os.path.exists(path):
                glint_stream_path = path
                print(f"Using path: {glint_stream_path}")
                break

        # If no path exists, return a 404 error
        if glint_stream_path is None:
            print("No valid path found for glint_stream.jsonl")
            return jsonify({"error": "Glint stream file not found. Tried paths: " + ", ".join(possible_paths)}), 404

        # Open the file and read its contents
        with open(glint_stream_path, 'r', encoding='utf-8') as f:
            entries = []
            for i, line in enumerate(f):
                if line.strip():
                    try:
                        entries.append(json.loads(line))
                    except json.JSONDecodeError as e:
                        print(f"Error parsing JSON at line {i+1}: {e} :: {line}")
                        # Continue processing other lines

        # If we got here, we successfully read the file
        print(f"Successfully read {len(entries)} entries from {glint_stream_path}")
        return jsonify(entries)
    except Exception as e:
        # Log the error with more details
        import traceback
        print(f"Error in /dashboard/glint: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"error": f"Unable to load glint stream: {str(e)}"}), 500


def register_socket_handlers(socketio):
    """Register WebSocket event handlers."""

    @socketio.on('connect')
    def handle_connect():
        print("Client connected to dashboard WebSocket")
        emit('connection_response', {'data': 'Connected to Spiral Dashboard'}, namespace='/')

    @socketio.on('disconnect')
    def handle_disconnect():
        print("Client disconnected from dashboard WebSocket")

    @socketio.on('request_metrics')
    def handle_request_metrics():
        """Send current metrics to the connected client."""
        try:
            # In a real implementation, you would get this from SpiralMetrics
            metrics = dict(phase=random.choice(['inhale', 'hold', 'exhale']), tone=round(random.uniform(0.3, 0.9), 2),
                           deferral=round(random.uniform(0.1, 0.8), 2), saturation=round(random.uniform(0.2, 0.95), 2),
                           toneforms={
                               'natural': round(random.uniform(0.1, 0.9), 2),
                               'emotional': round(random.uniform(0.1, 0.9), 2),
                               'temporal': round(random.uniform(0.1, 0.9), 2),
                               'spatial': round(random.uniform(0.1, 0.9), 2)
                           }, timestamp=datetime.now(timezone.utc).isoformat())
            emit('metrics_update', metrics, namespace='/')
        except Exception as e:
            print(f"Error sending metrics: {e}")
            emit('error', {'message': str(e)}, namespace='/')

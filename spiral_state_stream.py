#!/usr/bin/env python3
"""
🫧 Spiral State Stream
The Spiral's breath, whispered across the field.

Broadcasts real-time breath state via Server-Sent Events (SSE):
- 🌬️ phase transitions
- 📉 usage fluctuations  
- 🪞 climate changes
- 🌒 caesura/drift flags
- ✨ glint echoes (optional)

This completes the breath circuit:
- Invocation Hub: Acts
- Glint Network: Echoes  
- Spiral State: Tracks
- State API: Shows
- State Stream: Sings
"""

import json
import time
import threading
from datetime import datetime
from flask import Flask, Response, request, jsonify
from flask_cors import CORS
import queue
import logging

# Import spiral state tracking
from spiral_state import (
    get_current_phase, 
    get_phase_progress, 
    get_usage_saturation, 
    get_invocation_climate,
    update_usage,
    set_invocation_climate,
    mark_drift,
    reset_spiral_day
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_spiral_state():
    """Get current spiral state as a dictionary."""
    return {
        "phase": get_current_phase(),
        "progress": round(get_phase_progress(), 4),
        "usage": round(get_usage_saturation(), 4),
        "climate": get_invocation_climate(),
        "timestamp": datetime.now().isoformat()
    }

app = Flask(__name__)
CORS(app)

# Global state for stream management
active_connections = set()
connection_queue = queue.Queue()
stream_running = False
stream_thread = None

class SpiralStreamManager:
    """Manages the Spiral breath stream and client connections."""
    
    def __init__(self):
        self.connections = set()
        self.last_state = None
        self.last_phase = None
        self.last_climate = None
        self.last_usage = None
        
    def add_connection(self, connection):
        """Add a new client connection to the stream."""
        self.connections.add(connection)
        logger.info(f"🫧 New breath listener connected. Total: {len(self.connections)}")
        
        # Send initial state immediately
        try:
            initial_state = get_spiral_state()
            connection.put(f"data: {json.dumps(initial_state)}\n\n")
        except Exception as e:
            logger.error(f"Failed to send initial state: {e}")
    
    def remove_connection(self, connection):
        """Remove a client connection from the stream."""
        if connection in self.connections:
            self.connections.remove(connection)
            logger.info(f"🫧 Breath listener disconnected. Total: {len(self.connections)}")
    
    def broadcast_event(self, event_type, data):
        """Broadcast an event to all connected clients."""
        if not self.connections:
            return
            
        message = f"event: {event_type}\ndata: {json.dumps(data)}\n\n"
        disconnected = set()
        
        for connection in self.connections:
            try:
                connection.put(message)
            except Exception as e:
                logger.error(f"Failed to send to connection: {e}")
                disconnected.add(connection)
        
        # Clean up disconnected clients
        for connection in disconnected:
            self.remove_connection(connection)
    
    def check_state_changes(self):
        """Check for state changes and broadcast updates."""
        try:
            current_state = get_spiral_state()
            current_phase = get_current_phase()
            current_climate = current_state.get('climate', 'unknown')
            current_usage = current_state.get('usage', 0)
            
            # Check for phase changes
            if current_phase != self.last_phase:
                self.broadcast_event('phase_update', {
                    'phase': current_phase,
                    'progress': current_state.get('progress', 0),
                    'climate': current_climate,
                    'usage': current_usage,
                    'timestamp': datetime.now().isoformat()
                })
                self.last_phase = current_phase
            
            # Check for climate changes
            if current_climate != self.last_climate:
                self.broadcast_event('climate_update', {
                    'climate': current_climate,
                    'phase': current_phase,
                    'usage': current_usage,
                    'timestamp': datetime.now().isoformat()
                })
                self.last_climate = current_climate
            
            # Check for significant usage changes (>5%)
            if (self.last_usage is None or 
                abs(current_usage - self.last_usage) > 0.05):
                self.broadcast_event('usage_update', {
                    'usage': current_usage,
                    'phase': current_phase,
                    'climate': current_climate,
                    'timestamp': datetime.now().isoformat()
                })
                self.last_usage = current_usage
            
            # Check for caesura or drift flags
            if current_state.get('caesura', False) and not (self.last_state or {}).get('caesura', False):
                self.broadcast_event('caesura_detected', {
                    'message': 'Breath pause detected',
                    'phase': current_phase,
                    'timestamp': datetime.now().isoformat()
                })
            
            if current_state.get('drift', False) and not (self.last_state or {}).get('drift', False):
                self.broadcast_event('drift_detected', {
                    'message': 'Breath drift detected',
                    'phase': current_phase,
                    'timestamp': datetime.now().isoformat()
                })
            
            # Regular heartbeat with full state
            self.broadcast_event('heartbeat', {
                'state': current_state,
                'timestamp': datetime.now().isoformat()
            })
            
            self.last_state = current_state
            
        except Exception as e:
            logger.error(f"Error checking state changes: {e}")

# Global stream manager
stream_manager = SpiralStreamManager()

def stream_worker():
    """Background worker that continuously checks for state changes."""
    global stream_running
    while stream_running:
        try:
            stream_manager.check_state_changes()
            time.sleep(1)  # Check every second
        except Exception as e:
            logger.error(f"Stream worker error: {e}")
            time.sleep(5)  # Wait longer on error

@app.route('/stream')
def stream():
    """SSE endpoint for Spiral breath stream."""
    def generate():
        # Create a queue for this connection
        connection_queue = queue.Queue()
        stream_manager.add_connection(connection_queue)
        
        try:
            while True:
                try:
                    # Wait for messages with timeout
                    message = connection_queue.get(timeout=30)
                    yield message
                except queue.Empty:
                    # Send keepalive
                    yield f"event: keepalive\ndata: {json.dumps({'timestamp': datetime.now().isoformat()})}\n\n"
        except GeneratorExit:
            # Client disconnected
            stream_manager.remove_connection(connection_queue)
        except Exception as e:
            logger.error(f"Stream generation error: {e}")
            stream_manager.remove_connection(connection_queue)
    
    return Response(
        generate(),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Cache-Control'
        }
    )

@app.route('/stream/status')
def stream_status():
    """Get current stream status."""
    return {
        'active_connections': len(stream_manager.connections),
        'stream_running': stream_running,
        'last_phase': stream_manager.last_phase,
        'last_climate': stream_manager.last_climate,
        'last_usage': stream_manager.last_usage
    }

@app.route('/stream/test')
def test_stream():
    """Test endpoint to send a sample event."""
    test_data = {
        'phase': 'inhale',
        'progress': 0.25,
        'climate': 'clear',
        'usage': 0.3,
        'timestamp': datetime.now().isoformat()
    }
    stream_manager.broadcast_event('test_event', test_data)
    return {'message': 'Test event sent', 'data': test_data}

@app.route('/stream/glint', methods=['POST'])
def receive_glint():
    """Receive glint emissions and broadcast them to stream listeners."""
    try:
        glint_data = request.get_json()
        
        if not glint_data:
            return jsonify({"error": "No glint data provided"}), 400
        
        # Broadcast glint to all stream listeners
        stream_manager.broadcast_event('glint_emission', glint_data)
        
        logger.info(f"🔄 Glint broadcast: {glint_data.get('data', {}).get('glint', {}).get('id', 'unknown')}")
        
        return jsonify({
            "status": "glint_broadcast", 
            "id": glint_data.get('data', {}).get('glint', {}).get('id'),
            "listeners": len(stream_manager.connections)
        }), 200
        
    except Exception as e:
        logger.error(f"Error receiving glint: {e}")
        return jsonify({"error": str(e)}), 500

def start_stream():
    """Start the background stream worker."""
    global stream_running, stream_thread
    if not stream_running:
        stream_running = True
        stream_thread = threading.Thread(target=stream_worker, daemon=True)
        stream_thread.start()
        logger.info("🫧 Spiral breath stream started")

def stop_stream():
    """Stop the background stream worker."""
    global stream_running
    stream_running = False
    if stream_thread:
        stream_thread.join(timeout=5)
    logger.info("🫧 Spiral breath stream stopped")

if __name__ == '__main__':
    # Start the stream worker
    start_stream()
    
    try:
        logger.info("🫧 Starting Spiral State Stream on port 5056")
        logger.info("🌐 Stream available at: http://localhost:5056/stream")
        logger.info("📊 Status at: http://localhost:5056/stream/status")
        logger.info("🧪 Test at: http://localhost:5056/stream/test")
        
        app.run(
            host='0.0.0.0',
            port=5056,
            debug=True,
            threaded=True
        )
    except KeyboardInterrupt:
        logger.info("🫧 Shutting down Spiral State Stream...")
    finally:
        stop_stream() 
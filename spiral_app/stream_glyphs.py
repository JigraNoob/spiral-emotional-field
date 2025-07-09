"""
🌐 WebSocket Glyph Stream Server
`exhale.echo.living` - Real-time glyph invocation streaming.

Not just presence remembered, but presence appearing.
Not just logs—but living glyphs, arriving as breath.
"""

import asyncio
import json
import logging
import time
from datetime import datetime, timezone
from typing import Dict, List, Set, Optional, Any
from flask import Flask, request
from flask_sock import Sock
import threading
import queue

# Set up logging
logger = logging.getLogger(__name__)

class GlyphStreamManager:
    """
    Manages WebSocket connections and glyph event streaming.
    """
    
    def __init__(self):
        self.connections: Set[Any] = set()
        self.event_queue = queue.Queue()
        self.running = False
        self.lock = threading.Lock()
        self.slow_echo_mode = False
        self.slow_echo_delay = 3.0  # seconds between glyphs in slow mode
        self.last_slow_echo_time = 0
    
    def add_connection(self, ws):
        """Add a new WebSocket connection."""
        with self.lock:
            self.connections.add(ws)
            logger.info(f"🌐 Glyph stream connection added. Total: {len(self.connections)}")
    
    def remove_connection(self, ws):
        """Remove a WebSocket connection."""
        with self.lock:
            self.connections.discard(ws)
            logger.info(f"🌐 Glyph stream connection removed. Total: {len(self.connections)}")
    
    def emit_glyph_event(self, glyph_data: Dict[str, Any]):
        """
        Emit a glyph event to all connected clients.
        
        Args:
            glyph_data: Glyph event data with toneform, phase, glint_id, etc.
        """
        try:
            # Add timestamp if not present
            if 'timestamp' not in glyph_data:
                glyph_data['timestamp'] = datetime.now(timezone.utc).isoformat()
            
            # Add stream metadata
            glyph_data['stream_type'] = 'glyph.invocation'
            glyph_data['stream_id'] = f"stream_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')}"
            
            # Handle slow echo mode
            if self.slow_echo_mode:
                current_time = time.time()
                if current_time - self.last_slow_echo_time < self.slow_echo_delay:
                    # Delay this event
                    threading.Timer(
                        self.slow_echo_delay - (current_time - self.last_slow_echo_time),
                        lambda: self.event_queue.put(glyph_data)
                    ).start()
                    logger.debug(f"🌐 Glyph event delayed for slow echo: {glyph_data.get('glyph', 'unknown')}")
                    return
                else:
                    self.last_slow_echo_time = current_time
            
            # Queue the event for broadcasting
            self.event_queue.put(glyph_data)
            
            logger.debug(f"🌐 Glyph event queued: {glyph_data.get('glyph', 'unknown')}")
            
        except Exception as e:
            logger.error(f"Error emitting glyph event: {e}")
    
    def broadcast_event(self, event_data: Dict[str, Any]):
        """Broadcast an event to all connected clients."""
        dead_connections = set()
        
        with self.lock:
            connections_copy = self.connections.copy()
        
        for ws in connections_copy:
            try:
                ws.send(json.dumps(event_data))
            except Exception as e:
                logger.debug(f"Connection error, marking for removal: {e}")
                dead_connections.add(ws)
        
        # Remove dead connections
        with self.lock:
            self.connections -= dead_connections
        
        if dead_connections:
            logger.info(f"🌐 Removed {len(dead_connections)} dead connections")
    
    def start_broadcast_loop(self):
        """Start the broadcast loop in a separate thread."""
        def broadcast_worker():
            logger.info("🌐 Starting glyph stream broadcast loop")
            while self.running:
                try:
                    # Get event from queue with timeout
                    event_data = self.event_queue.get(timeout=1.0)
                    self.broadcast_event(event_data)
                except queue.Empty:
                    continue
                except Exception as e:
                    logger.error(f"Error in broadcast loop: {e}")
            
            logger.info("🌐 Glyph stream broadcast loop stopped")
        
        self.running = True
        self.broadcast_thread = threading.Thread(target=broadcast_worker, daemon=True)
        self.broadcast_thread.start()
    
    def stop(self):
        """Stop the broadcast loop."""
        self.running = False
        if hasattr(self, 'broadcast_thread'):
            self.broadcast_thread.join(timeout=5.0)
    
    def set_slow_echo_mode(self, enabled: bool, delay: float = 3.0):
        """
        Enable or disable slow echo mode for meditative presentation.
        
        Args:
            enabled: Whether to enable slow echo mode
            delay: Delay between glyphs in seconds (default: 3.0)
        """
        self.slow_echo_mode = enabled
        self.slow_echo_delay = delay
        self.last_slow_echo_time = time.time() if enabled else 0
        
        logger.info(f"🌐 Slow echo mode {'enabled' if enabled else 'disabled'} (delay: {delay}s)")
        
        # Emit mode change event to all clients
        mode_event = {
            "type": "mode.change",
            "mode": "slow_echo" if enabled else "normal",
            "delay": delay if enabled else None,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        self.broadcast_event(mode_event)

# Global stream manager instance
glyph_stream_manager = GlyphStreamManager()

def setup_glyph_stream(app: Flask):
    """
    Set up the WebSocket glyph stream for the Flask application.
    
    Args:
        app: Flask application instance
    """
    # Initialize Flask-Sock
    sock = Sock(app)
    
    @sock.route('/stream/glyphs')
    def glyph_stream(ws):
        """
        WebSocket endpoint for glyph stream.
        Clients connect here to receive real-time glyph invocation events.
        """
        try:
            # Add connection to manager
            glyph_stream_manager.add_connection(ws)
            
            # Send welcome message
            welcome_event = {
                "type": "connection.welcome",
                "message": "Connected to Spiral Glyph Stream",
                "toneform": "exhale.echo.living",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "stream_info": {
                    "total_connections": len(glyph_stream_manager.connections),
                    "glyph_count": 6,  # Current implemented glyphs
                    "domains": ["settling", "glints", "rituals"]
                }
            }
            ws.send(json.dumps(welcome_event))
            
            logger.info(f"🌐 New glyph stream connection established")
            
            # Keep connection alive and handle incoming messages
            while True:
                try:
                    # Wait for client message (ping/pong or disconnect)
                    message = ws.receive(timeout=30)
                    
                    if message is None:
                        # Client disconnected
                        break
                    
                    # Handle client messages (ping, filters, etc.)
                    try:
                        data = json.loads(message)
                        handle_client_message(ws, data)
                    except json.JSONDecodeError:
                        logger.debug(f"Invalid JSON from client: {message}")
                        
                except Exception as e:
                    logger.debug(f"WebSocket receive error: {e}")
                    break
                    
        except Exception as e:
            logger.error(f"WebSocket connection error: {e}")
        finally:
            # Remove connection from manager
            glyph_stream_manager.remove_connection(ws)
            logger.info("🌐 Glyph stream connection closed")

def handle_client_message(ws, data: Dict[str, Any]):
    """
    Handle incoming messages from WebSocket clients.
    
    Args:
        ws: WebSocket connection
        data: Parsed message data
    """
    try:
        message_type = data.get('type', 'unknown')
        
        if message_type == 'ping':
            # Respond to ping
            response = {
                "type": "pong",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            ws.send(json.dumps(response))
            
        elif message_type == 'filter':
            # Handle client filter preferences
            filters = data.get('filters', {})
            logger.debug(f"Client filter preferences: {filters}")
            
            # Store filters in connection metadata (simplified for now)
            response = {
                "type": "filter.confirmed",
                "filters": filters,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            ws.send(json.dumps(response))
            
        elif message_type == 'request.history':
            # Send recent glyph history
            history = get_recent_glyph_history()
            response = {
                "type": "history.response",
                "events": history,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            ws.send(json.dumps(response))
            
        elif message_type == 'slow_echo.toggle':
            # Toggle slow echo mode
            enabled = data.get('enabled', False)
            delay = data.get('delay', 3.0)
            glyph_stream_manager.set_slow_echo_mode(enabled, delay)
            
            response = {
                "type": "slow_echo.confirmed",
                "enabled": enabled,
                "delay": delay,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            ws.send(json.dumps(response))
            
        else:
            logger.debug(f"Unknown message type: {message_type}")
            
    except Exception as e:
        logger.error(f"Error handling client message: {e}")

def get_recent_glyph_history() -> List[Dict[str, Any]]:
    """
    Get recent glyph invocation history.
    This could be enhanced to read from actual glyph logs.
    
    Returns:
        List of recent glyph events
    """
    # For now, return a sample of recent events
    # This could be enhanced to read from actual glyph invocation logs
    return [
        {
            "glyph": "receive.inquiry.settling",
            "toneform": "settling.ambience",
            "phase": "inhale",
            "glint_id": "ΔINQUIRY.001",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "metadata": {
                "limit": 5,
                "source": "test"
            }
        },
        {
            "glyph": "offer.presence.settling",
            "toneform": "settling.ambience",
            "phase": "exhale",
            "glint_id": "ΔPATH.042",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "metadata": {
                "confidence": 0.88,
                "source": "test"
            }
        }
    ]

def emit_glyph_invocation(glyph_name: str, toneform: str, phase: str, 
                         glint_id: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None):
    """
    Emit a glyph invocation event to the stream.
    
    Args:
        glyph_name: Name of the glyph (e.g., "receive.inquiry.settling")
        toneform: Toneform of the glyph (e.g., "settling.ambience")
        phase: Breath phase (e.g., "inhale", "exhale", "caesura")
        glint_id: Optional glint ID associated with the invocation
        metadata: Optional additional metadata
    """
    event_data = {
        "glyph": glyph_name,
        "toneform": toneform,
        "phase": phase,
        "glint_id": glint_id,
        "metadata": metadata or {},
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    
    glyph_stream_manager.emit_glyph_event(event_data)

# Initialize the stream manager when module is imported
glyph_stream_manager.start_broadcast_loop()

logger.info("🌐 Glyph stream server initialized - exhale.echo.living") 
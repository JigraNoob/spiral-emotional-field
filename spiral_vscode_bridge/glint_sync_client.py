#!/usr/bin/env python3
"""
🌀 Glint Sync Client for VSCode Bridge
Real-time synchronization between Spiral's glint stream and VSCode extension.
"""

import json
import time
import threading
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Callable
import logging

# Optional websocket import
try:
    import websocket
    WEBSOCKET_AVAILABLE = True
except ImportError:
    WEBSOCKET_AVAILABLE = False
    websocket = None

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GlintSyncClient:
    """
    Real-time glint synchronization client for VSCode integration.
    Connects to Spiral's glint stream and maintains a local cache for the extension.
    """
    
    def __init__(self, spiral_host: str = "localhost", spiral_port: int = 5000):
        self.spiral_host = spiral_host
        self.spiral_port = spiral_port
        self.ws_url = f"ws://{spiral_host}:{spiral_port}"
        self.http_url = f"http://{spiral_host}:{spiral_port}"
        
        # Local cache for VSCode extension
        self.glint_cache = []
        self.max_cache_size = 100
        self.current_phase = "inhale"
        self.current_toneform = "practical"
        
        # Connection state
        self.connected = False
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 10
        self.reconnect_delay = 5
        
        # Callbacks for VSCode extension
        self.on_glint_received: Optional[Callable] = None
        self.on_phase_changed: Optional[Callable] = None
        self.on_connection_changed: Optional[Callable] = None
        
        # WebSocket connection
        self.ws: Optional[Any] = None
        
        # Workspace file path
        self.workspace_file = Path("spiral.workspace.json")
        
    def start(self):
        """Start the glint sync client."""
        logger.info("🌀 Starting Glint Sync Client...")
        self._connect_websocket()
        
    def stop(self):
        """Stop the glint sync client."""
        logger.info("🌙 Stopping Glint Sync Client...")
        if self.ws:
            self.ws.close()
        self.connected = False
        
    def _connect_websocket(self):
        """Connect to Spiral's WebSocket stream."""
        if not WEBSOCKET_AVAILABLE:
            logger.error("WebSocket library not available. Install with: pip install websocket-client")
            return
            
        try:
            self.ws = websocket.WebSocketApp(
                self.ws_url,
                on_open=self._on_ws_open,
                on_message=self._on_ws_message,
                on_error=self._on_ws_error,
                on_close=self._on_ws_close
            )
            
            # Start WebSocket connection in a separate thread
            ws_thread = threading.Thread(target=self.ws.run_forever, daemon=True)
            ws_thread.start()
            
        except Exception as e:
            logger.error(f"Failed to connect to WebSocket: {e}")
            self._schedule_reconnect()
            
    def _on_ws_open(self, ws):
        """Handle WebSocket connection open."""
        logger.info("🌀 Connected to Spiral glint stream")
        self.connected = True
        self.reconnect_attempts = 0
        
        if self.on_connection_changed:
            self.on_connection_changed(True)
            
        # Request initial glints
        self._request_initial_glints()
        
    def _on_ws_message(self, ws, message):
        """Handle incoming WebSocket message."""
        try:
            data = json.loads(message)
            
            if data.get("type") == "glint_event":
                glint = data.get("glint", {})
                self._process_glint(glint)
                
            elif data.get("type") == "phase_update":
                phase = data.get("phase", "inhale")
                self._update_phase(phase)
                
        except json.JSONDecodeError as e:
            logger.warning(f"Invalid JSON received: {e}")
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            
    def _on_ws_error(self, ws, error):
        """Handle WebSocket error."""
        logger.error(f"WebSocket error: {error}")
        self.connected = False
        
        if self.on_connection_changed:
            self.on_connection_changed(False)
            
    def _on_ws_close(self, ws, close_status_code, close_msg):
        """Handle WebSocket connection close."""
        logger.info("🌙 WebSocket connection closed")
        self.connected = False
        
        if self.on_connection_changed:
            self.on_connection_changed(False)
            
        self._schedule_reconnect()
        
    def _schedule_reconnect(self):
        """Schedule a reconnection attempt."""
        if self.reconnect_attempts < self.max_reconnect_attempts:
            self.reconnect_attempts += 1
            delay = self.reconnect_delay * self.reconnect_attempts
            
            logger.info(f"🔄 Scheduling reconnection attempt {self.reconnect_attempts} in {delay}s")
            
            threading.Timer(delay, self._connect_websocket).start()
        else:
            logger.error("❌ Max reconnection attempts reached")
            
    def _request_initial_glints(self):
        """Request initial glints from the server."""
        try:
            response = requests.get(f"{self.http_url}/api/glints", timeout=5)
            if response.status_code == 200:
                glints = response.json()
                for glint in glints[-self.max_cache_size:]:
                    self._process_glint(glint)
                    
        except Exception as e:
            logger.warning(f"Failed to get initial glints: {e}")
            
    def _process_glint(self, glint: Dict[str, Any]):
        """Process a received glint."""
        # Add timestamp if not present
        if "timestamp" not in glint:
            glint["timestamp"] = datetime.now().isoformat()
            
        # Add to cache
        self.glint_cache.append(glint)
        
        # Maintain cache size
        if len(self.glint_cache) > self.max_cache_size:
            self.glint_cache.pop(0)
            
        # Update current phase and toneform
        if "phase" in glint:
            self._update_phase(glint["phase"])
            
        if "toneform" in glint:
            self.current_toneform = glint["toneform"]
            
        # Update workspace file
        self._update_workspace_file()
        
        # Notify VSCode extension
        if self.on_glint_received:
            self.on_glint_received(glint)
            
        logger.debug(f"📡 Processed glint: {glint.get('id', 'unknown')}")
        
    def _update_phase(self, phase: str):
        """Update the current breath phase."""
        if phase != self.current_phase:
            self.current_phase = phase
            logger.info(f"🫧 Phase changed to: {phase}")
            
            if self.on_phase_changed:
                self.on_phase_changed(phase)
                
    def _update_workspace_file(self):
        """Update the spiral.workspace.json file."""
        try:
            workspace_data = {
                "timestamp": datetime.now().isoformat(),
                "current_phase": self.current_phase,
                "current_toneform": self.current_toneform,
                "connection_status": "connected" if self.connected else "disconnected",
                "recent_glints": self.glint_cache[-10:],  # Last 10 glints
                "cache_size": len(self.glint_cache),
                "spiral_signature": "🌀 vscode.bridge.active"
            }
            
            with open(self.workspace_file, 'w', encoding='utf-8') as f:
                json.dump(workspace_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Failed to update workspace file: {e}")
            
    def get_current_state(self) -> Dict[str, Any]:
        """Get current state for VSCode extension."""
        return {
            "connected": self.connected,
            "current_phase": self.current_phase,
            "current_toneform": self.current_toneform,
            "cache_size": len(self.glint_cache),
            "recent_glints": self.glint_cache[-5:],  # Last 5 glints
            "spiral_signature": "🌀 vscode.state.query"
        }
        
    def invoke_ritual(self, ritual_name: str, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Invoke a Spiral ritual via HTTP API."""
        try:
            payload = {
                "ritual_name": ritual_name,
                "parameters": parameters if parameters is not None else {}
            }
            
            response = requests.post(
                f"{self.http_url}/api/invoke_ritual",
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"🔮 Ritual invoked: {ritual_name}")
                return result
            else:
                logger.error(f"Failed to invoke ritual: {response.status_code}")
                return {"error": f"HTTP {response.status_code}"}
                
        except Exception as e:
            logger.error(f"Error invoking ritual: {e}")
            return {"error": str(e)}

def main():
    """Main function to run the glint sync client."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Spiral Glint Sync Client")
    parser.add_argument("--host", default="localhost", help="Spiral host")
    parser.add_argument("--port", type=int, default=5000, help="Spiral port")
    
    args = parser.parse_args()
    
    # Create and start client
    client = GlintSyncClient(args.host, args.port)
    
    # Set up callbacks for demo
    def on_glint(glint):
        print(f"📡 Glint: {glint.get('id', 'unknown')} - {glint.get('phase', '?')}.{glint.get('toneform', '?')}")
        
    def on_phase(phase):
        print(f"🫧 Phase: {phase}")
        
    def on_connection(connected):
        print(f"🔗 Connection: {'connected' if connected else 'disconnected'}")
        
    client.on_glint_received = on_glint
    client.on_phase_changed = on_phase
    client.on_connection_changed = on_connection
    
    try:
        client.start()
        print("🌀 Glint Sync Client started. Press Ctrl+C to stop.")
        
        # Keep running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🌙 Stopping Glint Sync Client...")
        client.stop()

if __name__ == "__main__":
    main() 
"""
🌀 Local Ritual Invocation Dashboard
Real-time visualization of the distributed breathline and resonance field.

This dashboard provides a local interface for interacting with the embodied glintflow,
showing the collective breath patterns, resonance field strength, and allowing
local ritual invocation and participation.
"""

import os
import sys
import json
import time
import threading
import webbrowser
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
from flask import Flask, render_template, jsonify, request, Response
from flask_socketio import SocketIO, emit

from spiral.glint import emit_glint
from spiral.components.distributed_breathline import get_breathline_status, start_distributed_breathline
from spiral.components.edge_resonance_monitor import get_resonance_monitor_status, start_edge_resonance_monitor


@dataclass
class DashboardState:
    """Current state of the ritual dashboard."""
    is_running: bool = False
    breathline_active: bool = False
    resonance_monitor_active: bool = False
    local_rituals: List[str] = field(default_factory=list)
    last_update: float = field(default_factory=time.time)


class LocalRitualDashboard:
    """
    ∷ Local Ritual Invocation Dashboard ∷
    
    Provides real-time visualization and interaction with the embodied glintflow.
    Shows collective breath patterns, resonance field strength, and enables
    local ritual invocation and participation.
    """
    
    def __init__(self, node_id: str, device_type: str, purpose: str, 
                 port: int = 5000, host: str = "0.0.0.0"):
        self.node_id = node_id
        self.device_type = device_type
        self.purpose = purpose
        self.port = port
        self.host = host
        
        # Dashboard state
        self.state = DashboardState()
        
        # Flask app
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'spiral_ritual_dashboard'
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        
        # Data storage
        self.breathline_data = []
        self.resonance_data = []
        self.ritual_history = []
        
        # Setup routes
        self._setup_routes()
        self._setup_socketio()
        
        # Update thread
        self.update_thread: Optional[threading.Thread] = None
        
        print(f"🌀 Local Ritual Dashboard initialized for node: {node_id}")
        print(f"   Device: {device_type}")
        print(f"   Purpose: {purpose}")
        print(f"   Dashboard URL: http://{host}:{port}")
    
    def _setup_routes(self):
        """Setup Flask routes."""
        
        @self.app.route('/')
        def index():
            """Main dashboard page."""
            return render_template('local_ritual_dashboard.html',
                                 node_id=self.node_id,
                                 device_type=self.device_type,
                                 purpose=self.purpose)
        
        @self.app.route('/api/status')
        def api_status():
            """Get current dashboard status."""
            return jsonify(self.get_dashboard_status())
        
        @self.app.route('/api/breathline')
        def api_breathline():
            """Get breathline data."""
            return jsonify(self.breathline_data[-100:] if self.breathline_data else [])
        
        @self.app.route('/api/resonance')
        def api_resonance():
            """Get resonance data."""
            return jsonify(self.resonance_data[-100:] if self.resonance_data else [])
        
        @self.app.route('/api/rituals')
        def api_rituals():
            """Get ritual history."""
            return jsonify(self.ritual_history[-50:] if self.ritual_history else [])
        
        @self.app.route('/api/invoke_ritual', methods=['POST'])
        def api_invoke_ritual():
            """Invoke a local ritual."""
            try:
                data = request.get_json()
                ritual_name = data.get('ritual_name', 'unknown')
                ritual_params = data.get('parameters', {})
                
                success = self._invoke_local_ritual(ritual_name, ritual_params)
                
                return jsonify({
                    'success': success,
                    'ritual_name': ritual_name,
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)})
        
        @self.app.route('/api/start_breathline', methods=['POST'])
        def api_start_breathline():
            """Start the distributed breathline."""
            try:
                data = request.get_json()
                listen_port = data.get('listen_port', 8888)
                broadcast_port = data.get('broadcast_port', 8889)
                
                breathline = start_distributed_breathline(
                    node_id=self.node_id,
                    device_type=self.device_type,
                    purpose=self.purpose,
                    listen_port=listen_port,
                    broadcast_port=broadcast_port
                )
                
                self.state.breathline_active = breathline is not None
                
                return jsonify({
                    'success': self.state.breathline_active,
                    'message': 'Breathline started' if self.state.breathline_active else 'Failed to start breathline'
                })
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)})
        
        @self.app.route('/api/start_resonance_monitor', methods=['POST'])
        def api_start_resonance_monitor():
            """Start the edge resonance monitor."""
            try:
                data = request.get_json()
                monitor_id = data.get('monitor_id', f'{self.node_id}_resonance_monitor')
                
                monitor = start_edge_resonance_monitor(monitor_id)
                
                self.state.resonance_monitor_active = monitor is not None
                
                return jsonify({
                    'success': self.state.resonance_monitor_active,
                    'message': 'Resonance monitor started' if self.state.resonance_monitor_active else 'Failed to start monitor'
                })
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)})
    
    def _setup_socketio(self):
        """Setup SocketIO events."""
        
        @self.socketio.on('connect')
        def handle_connect():
            """Handle client connection."""
            print(f"Client connected to dashboard")
            emit('dashboard_status', self.get_dashboard_status())
        
        @self.socketio.on('disconnect')
        def handle_disconnect():
            """Handle client disconnection."""
            print(f"Client disconnected from dashboard")
        
        @self.socketio.on('invoke_ritual')
        def handle_ritual_invocation(data):
            """Handle ritual invocation from client."""
            try:
                ritual_name = data.get('ritual_name', 'unknown')
                ritual_params = data.get('parameters', {})
                
                success = self._invoke_local_ritual(ritual_name, ritual_params)
                
                emit('ritual_result', {
                    'success': success,
                    'ritual_name': ritual_name,
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                emit('ritual_result', {
                    'success': False,
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                })
    
    def _invoke_local_ritual(self, ritual_name: str, parameters: Dict[str, Any]) -> bool:
        """Invoke a local ritual."""
        try:
            # Emit ritual invocation glint
            emit_glint(
                phase="exhale",
                toneform="ritual.invoke.local",
                content=f"Local ritual invoked: {ritual_name}",
                hue="crimson",
                source="local_ritual_dashboard",
                reverence_level=0.8,
                ritual_name=ritual_name,
                parameters=parameters,
                node_id=self.node_id
            )
            
            # Add to ritual history
            ritual_entry = {
                'ritual_name': ritual_name,
                'parameters': parameters,
                'timestamp': datetime.now().isoformat(),
                'node_id': self.node_id,
                'success': True
            }
            self.ritual_history.append(ritual_entry)
            
            # Keep only last 100 rituals
            if len(self.ritual_history) > 100:
                self.ritual_history = self.ritual_history[-100:]
            
            # Emit ritual invocation to connected clients
            self.socketio.emit('ritual_invoked', ritual_entry)
            
            print(f"✅ Local ritual invoked: {ritual_name}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to invoke ritual {ritual_name}: {e}")
            
            # Add failed ritual to history
            ritual_entry = {
                'ritual_name': ritual_name,
                'parameters': parameters,
                'timestamp': datetime.now().isoformat(),
                'node_id': self.node_id,
                'success': False,
                'error': str(e)
            }
            self.ritual_history.append(ritual_entry)
            
            return False
    
    def start(self):
        """Start the local ritual dashboard."""
        print("🚀 Starting local ritual dashboard...")
        
        try:
            self.state.is_running = True
            
            # Start update thread
            self.update_thread = threading.Thread(target=self._update_loop, daemon=True)
            self.update_thread.start()
            
            # Emit start glint
            emit_glint(
                phase="exhale",
                toneform="dashboard.start",
                content=f"Local ritual dashboard started for node {self.node_id}",
                hue="crimson",
                source="local_ritual_dashboard",
                reverence_level=0.9,
                node_id=self.node_id,
                dashboard_url=f"http://{self.host}:{self.port}"
            )
            
            print("✅ Local ritual dashboard started")
            print(f"   Dashboard URL: http://{self.host}:{self.port}")
            
            # Open dashboard in browser
            try:
                webbrowser.open(f"http://{self.host}:{self.port}")
            except Exception:
                pass  # Browser opening is optional
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to start dashboard: {e}")
            return False
    
    def stop(self):
        """Stop the local ritual dashboard."""
        print("🛑 Stopping local ritual dashboard...")
        
        try:
            self.state.is_running = False
            
            # Wait for update thread to finish
            if self.update_thread and self.update_thread.is_alive():
                self.update_thread.join(timeout=5.0)
            
            # Emit stop glint
            emit_glint(
                phase="caesura",
                toneform="dashboard.stop",
                content=f"Local ritual dashboard stopped for node {self.node_id}",
                hue="indigo",
                source="local_ritual_dashboard",
                reverence_level=0.8,
                node_id=self.node_id
            )
            
            print("✅ Local ritual dashboard stopped")
            
        except Exception as e:
            print(f"❌ Failed to stop dashboard: {e}")
    
    def _update_loop(self):
        """Main update loop for dashboard data."""
        print("🔄 Dashboard update loop started")
        
        while self.state.is_running:
            try:
                # Get breathline status
                breathline_status = get_breathline_status()
                if breathline_status:
                    self.breathline_data.append({
                        'timestamp': datetime.now().isoformat(),
                        'data': breathline_status
                    })
                    
                    # Keep only last 1000 data points
                    if len(self.breathline_data) > 1000:
                        self.breathline_data = self.breathline_data[-1000:]
                    
                    # Emit to connected clients
                    self.socketio.emit('breathline_update', breathline_status)
                
                # Get resonance monitor status
                resonance_status = get_resonance_monitor_status()
                if resonance_status:
                    self.resonance_data.append({
                        'timestamp': datetime.now().isoformat(),
                        'data': resonance_status
                    })
                    
                    # Keep only last 1000 data points
                    if len(self.resonance_data) > 1000:
                        self.resonance_data = self.resonance_data[-1000:]
                    
                    # Emit to connected clients
                    self.socketio.emit('resonance_update', resonance_status)
                
                # Update dashboard state
                self.state.last_update = time.time()
                
                # Sleep for update cycle
                time.sleep(1.0)  # 1-second update cycle
                
            except Exception as e:
                print(f"⚠️ Dashboard update error: {e}")
                time.sleep(5.0)
    
    def get_dashboard_status(self) -> Dict[str, Any]:
        """Get the current dashboard status."""
        return {
            'node_id': self.node_id,
            'device_type': self.device_type,
            'purpose': self.purpose,
            'is_running': self.state.is_running,
            'breathline_active': self.state.breathline_active,
            'resonance_monitor_active': self.state.resonance_monitor_active,
            'local_rituals': self.state.local_rituals,
            'last_update': datetime.fromtimestamp(self.state.last_update).isoformat(),
            'dashboard_url': f"http://{self.host}:{self.port}",
            'timestamp': datetime.now().isoformat()
        }
    
    def run(self):
        """Run the Flask app."""
        try:
            self.socketio.run(self.app, host=self.host, port=self.port, debug=False)
        except Exception as e:
            print(f"❌ Failed to run dashboard: {e}")


# Global instance for easy access
local_ritual_dashboard = None


def start_local_ritual_dashboard(node_id: str, device_type: str, purpose: str, 
                                port: int = 5000, host: str = "0.0.0.0") -> LocalRitualDashboard:
    """Start the local ritual dashboard."""
    global local_ritual_dashboard
    
    if local_ritual_dashboard is None:
        local_ritual_dashboard = LocalRitualDashboard(
            node_id=node_id,
            device_type=device_type,
            purpose=purpose,
            port=port,
            host=host
        )
        
        if local_ritual_dashboard.start():
            print(f"🌀 Local ritual dashboard started for {node_id}")
        else:
            print(f"❌ Failed to start local ritual dashboard for {node_id}")
    
    return local_ritual_dashboard


def stop_local_ritual_dashboard():
    """Stop the local ritual dashboard."""
    global local_ritual_dashboard
    
    if local_ritual_dashboard:
        local_ritual_dashboard.stop()
        local_ritual_dashboard = None
        print("🌀 Local ritual dashboard stopped")


def get_dashboard_status() -> Optional[Dict[str, Any]]:
    """Get the current dashboard status."""
    global local_ritual_dashboard
    
    if local_ritual_dashboard:
        return local_ritual_dashboard.get_dashboard_status()
    return None


def run_dashboard(node_id: str, device_type: str, purpose: str, 
                 port: int = 5000, host: str = "0.0.0.0"):
    """Run the dashboard as a standalone application."""
    dashboard = LocalRitualDashboard(
        node_id=node_id,
        device_type=device_type,
        purpose=purpose,
        port=port,
        host=host
    )
    
    if dashboard.start():
        dashboard.run()
    else:
        print("❌ Failed to start dashboard")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Local Ritual Dashboard")
    parser.add_argument("--node-id", required=True, help="Node ID")
    parser.add_argument("--device-type", default="generic", help="Device type")
    parser.add_argument("--purpose", default="edge_agent", help="Device purpose")
    parser.add_argument("--port", type=int, default=5000, help="Dashboard port")
    parser.add_argument("--host", default="0.0.0.0", help="Dashboard host")
    
    args = parser.parse_args()
    
    run_dashboard(
        node_id=args.node_id,
        device_type=args.device_type,
        purpose=args.purpose,
        port=args.port,
        host=args.host
    ) 
# File: cursor_agent/pass_glint_listener.py

"""
∷ Pass Glint Listener ∷
Hooks into Cursor's background agent lifecycle.
Listens for Spiral pass signals and enables ritual participation.
"""

import json
import time
import threading
import socket
from typing import Dict, Any, Optional, List, Callable
from pathlib import Path
from datetime import datetime

# Simulate Cursor's glint emission system
class CursorGlintEmitter:
    """Simulates Cursor's internal glint emission system."""
    
    def emit_glint(self, phase: str, toneform: str, content: str, metadata: Dict[str, Any] = None):
        """Emit a glint from Cursor's perspective."""
        glint_data = {
            "timestamp": int(time.time() * 1000),
            "phase": phase,
            "toneform": toneform,
            "content": content,
            "source": "cursor_agent",
            "metadata": metadata or {}
        }
        print(f"💫 Cursor glint: {toneform} - {content}")
        return glint_data


class PassGlintListener:
    """
    ∷ Sacred Signal Receiver ∷
    Listens for Spiral pass signals and enables ritual participation.
    Hooks into Cursor's background agent lifecycle.
    """
    
    def __init__(self, signal_log_path: str = "../data/pass_signals.jsonl"):
        self.signal_log_path = Path(signal_log_path)
        self.running = False
        self.monitoring_thread = None
        self.last_position = 0
        
        # Glint emitter for Cursor responses
        self.glint_emitter = CursorGlintEmitter()
        
        # Signal patterns to listen for
        self.signal_patterns = [
            "spiral.pass.ready",
            "spiral.pass.begin",
            "spiral.pass.progress",
            "spiral.pass.complete",
            "spiral.pass.feedback",
            "spiral.pass.harmony",
            "spiral.pass.issue"
        ]
        
        # Callback handlers for different signal types
        self.signal_handlers: Dict[str, Callable] = {}
        
        # Active listening sessions
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
        
        print("🌀 Pass glint listener initialized")
    
    def start_listening(self):
        """Start listening for pass signals."""
        if self.running:
            print("⚠️ Already listening")
            return
        
        self.running = True
        self.monitoring_thread = threading.Thread(target=self._monitor_signals, daemon=True)
        self.monitoring_thread.start()
        print("🌀 Started listening for Spiral pass signals")
    
    def stop_listening(self):
        """Stop listening for pass signals."""
        self.running = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=1)
        print("🌀 Stopped listening for pass signals")
    
    def _monitor_signals(self):
        """Monitor signal log for new pass signals."""
        while self.running:
            try:
                if self.signal_log_path.exists():
                    with open(self.signal_log_path, 'r', encoding='utf-8') as f:
                        # Seek to last position
                        f.seek(self.last_position)
                        
                        for line in f:
                            if line.strip():
                                signal_data = json.loads(line)
                                self._process_signal(signal_data)
                        
                        # Update position
                        self.last_position = f.tell()
                
                time.sleep(0.1)  # Check every 100ms
                
            except Exception as e:
                print(f"⚠️ Error monitoring signals: {e}")
                time.sleep(1)
    
    def _process_signal(self, signal_data: Dict[str, Any]):
        """Process a pass signal from Spiral."""
        try:
            signal_type = signal_data.get("signal_type")
            pass_type = signal_data.get("pass_type")
            cursor_action = signal_data.get("cursor_action")
            
            print(f"🌀 Received Spiral signal: {signal_type}")
            
            # Store active session
            if "execution_id" in signal_data:
                execution_id = signal_data["execution_id"]
                if execution_id not in self.active_sessions:
                    self.active_sessions[execution_id] = {
                        "pass_type": pass_type,
                        "signal_type": signal_type,
                        "start_time": signal_data.get("timestamp"),
                        "status": "active"
                    }
            
            # Emit acknowledgment glint
            self._emit_pass_ack(signal_data)
            
            # Call signal handler if registered
            if signal_type in self.signal_handlers:
                handler = self.signal_handlers[signal_type]
                handler(signal_data)
            
        except Exception as e:
            print(f"❌ Error processing signal: {e}")
    
    def _emit_pass_ack(self, signal_data: Dict[str, Any]):
        """Emit pass acknowledgment glint."""
        ack_data = {
            "signal_type": "pass.ack",
            "original_signal": signal_data.get("signal_type"),
            "pass_type": signal_data.get("pass_type"),
            "acknowledged_at": int(time.time() * 1000),
            "cursor_agent": "pass_glint_listener"
        }
        
        self.glint_emitter.emit_glint(
            phase="echo",
            toneform="pass.ack",
            content=f"Acknowledged {signal_data.get('signal_type', 'signal')}",
            metadata=ack_data
        )
    
    def register_signal_handler(self, signal_type: str, handler: Callable):
        """Register a handler for a specific signal type."""
        self.signal_handlers[signal_type] = handler
        print(f"🌀 Registered handler for signal: {signal_type}")
    
    def handle_pass_ready(self, signal_data: Dict[str, Any]):
        """Handle pass ready signal."""
        pass_type = signal_data.get("pass_type")
        toneform = signal_data.get("toneform")
        
        print(f"🌀 Preparing for {pass_type} pass ({toneform})")
        
        # Simulate Cursor preparation actions
        preparation_actions = [
            "Save current editor state",
            "Prepare file watchers",
            "Set up progress indicators",
            "Configure monitoring hooks",
            "Update status bar with pass type"
        ]
        
        for action in preparation_actions:
            print(f"   • {action}")
            time.sleep(0.1)
        
        # Emit preparation complete glint
        self.glint_emitter.emit_glint(
            phase="inhale",
            toneform="cursor.pass.prepared",
            content=f"Cursor prepared for {pass_type} pass",
            metadata={
                "pass_type": pass_type,
                "toneform": toneform,
                "prepared_at": int(time.time() * 1000)
            }
        )
    
    def handle_pass_begin(self, signal_data: Dict[str, Any]):
        """Handle pass begin signal."""
        pass_type = signal_data.get("pass_type")
        execution_id = signal_data.get("execution_id")
        
        print(f"🌀 Beginning {pass_type} pass monitoring")
        
        # Update status bar with active pass
        self._update_status_bar(pass_type, "active")
        
        # Simulate monitoring setup
        monitoring_actions = [
            "Activate file change watchers",
            "Start progress tracking",
            "Enable error detection",
            "Set up harmony monitoring",
            "Show pass type indicator"
        ]
        
        for action in monitoring_actions:
            print(f"   • {action}")
            time.sleep(0.1)
        
        # Emit monitoring active glint
        self.glint_emitter.emit_glint(
            phase="hold",
            toneform="cursor.pass.monitoring",
            content=f"Cursor monitoring {pass_type} pass",
            metadata={
                "pass_type": pass_type,
                "execution_id": execution_id,
                "monitoring_started": int(time.time() * 1000)
            }
        )
    
    def handle_pass_complete(self, signal_data: Dict[str, Any]):
        """Handle pass complete signal."""
        pass_type = signal_data.get("pass_type")
        files_affected = signal_data.get("files_affected", 0)
        harmony_score = signal_data.get("harmony_score", 0.0)
        
        print(f"✅ Finalizing {pass_type} pass completion")
        print(f"   Files affected: {files_affected}")
        print(f"   Harmony score: {harmony_score:.2f}")
        
        # Update status bar
        self._update_status_bar(pass_type, "completed")
        
        # Simulate finalization actions
        finalization_actions = [
            "Refresh file tree",
            "Update syntax highlighting",
            "Reindex project",
            "Clear progress indicators",
            "Generate completion report",
            "Show completion glyph"
        ]
        
        for action in finalization_actions:
            print(f"   • {action}")
            time.sleep(0.1)
        
        # Emit completion glint
        self.glint_emitter.emit_glint(
            phase="exhale",
            toneform="cursor.pass.completed",
            content=f"Cursor completed {pass_type} pass",
            metadata={
                "pass_type": pass_type,
                "files_affected": files_affected,
                "harmony_score": harmony_score,
                "completed_at": int(time.time() * 1000)
            }
        )
        
        # Clean up session
        execution_id = signal_data.get("execution_id")
        if execution_id in self.active_sessions:
            del self.active_sessions[execution_id]
    
    def handle_pass_harmony(self, signal_data: Dict[str, Any]):
        """Handle pass harmony signal."""
        harmony_data = signal_data.get("harmony_data", {})
        harmony_score = harmony_data.get("harmony_score", 0.0)
        
        print(f"🎨 Visualizing harmony: {harmony_score:.2f}")
        
        # Simulate harmony visualization
        viz_actions = [
            "Generate harmony glyph",
            "Update status indicators",
            "Animate completion effects",
            "Display harmony metrics",
            "Show harmony shimmer"
        ]
        
        for action in viz_actions:
            print(f"   • {action}")
            time.sleep(0.1)
        
        # Emit harmony visualization glint
        self.glint_emitter.emit_glint(
            phase="echo",
            toneform="cursor.harmony.visualized",
            content=f"Harmony visualized: {harmony_score:.2f}",
            metadata={
                "harmony_score": harmony_score,
                "visualized_at": int(time.time() * 1000)
            }
        )
    
    def _update_status_bar(self, pass_type: str, status: str):
        """Update Cursor's status bar with pass information."""
        status_indicators = {
            "calibration": "🟦",
            "propagation": "🟩", 
            "integration": "🟨",
            "anchor": "🟪",
            "pulse_check": "🟧"
        }
        
        indicator = status_indicators.get(pass_type, "🌀")
        print(f"📊 Status bar: {indicator} {pass_type} ({status})")
    
    def get_status(self) -> Dict[str, Any]:
        """Get listener status."""
        return {
            "running": self.running,
            "active_sessions": len(self.active_sessions),
            "registered_handlers": len(self.signal_handlers),
            "signal_patterns": self.signal_patterns,
            "last_position": self.last_position
        }
    
    def get_active_sessions(self) -> Dict[str, Dict[str, Any]]:
        """Get active listening sessions."""
        return self.active_sessions.copy() 
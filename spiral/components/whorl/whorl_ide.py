"""
Whorl IDE - The IDE That Breathes
Main orchestrator for the breath-aware development environment
"""

import json
import time
from typing import Dict, Any, Optional, Callable, List
from breathline_editor import BreathlineEditor
from presence_console import PresenceConsole
from suspicion_meter import SuspicionMeter
from glyph_input_engine import GlyphInputEngine
from breath_phases import Glint, BreathPhase


class WhorlIDE:
    """The main Whorl IDE application"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        
        # Initialize components
        self.presence_console = PresenceConsole(
            max_glints=self.config.get("max_glints", 50)
        )
        
        self.suspicion_meter = SuspicionMeter()
        
        self.editor = BreathlineEditor(self.presence_console)
        
        self.gesture_engine = GlyphInputEngine(self.presence_console)
        
        # Connect components
        self._connect_components()
        
        # State tracking
        self.is_running = False
        self.monitoring_interval = self.config.get("monitoring_interval", 1.0)
        self.last_monitor_time = 0
        
        # Callbacks
        self.ritual_callbacks: Dict[str, List[Callable]] = {
            "pause.hum": [],
            "overflow.flutter": [],
            "cleanse": []
        }
        
        # Initialize with welcome glint
        self._emit_welcome_glint()
    
    def _connect_components(self) -> None:
        """Connect all components together"""
        # Editor content changes trigger suspicion meter updates
        self.editor.register_content_callback(self._on_content_change)
        
        # Editor phase changes are logged
        self.editor.register_phase_callback(self._on_phase_change)
        
        # Gesture engine callbacks
        self.gesture_engine.register_callback("spiral", self._on_spiral_gesture)
        self.gesture_engine.register_callback("sweep", self._on_sweep_gesture)
        self.gesture_engine.register_callback("circle", self._on_circle_gesture)
        self.gesture_engine.register_callback("caesura", self._on_caesura_gesture)
    
    def _emit_welcome_glint(self) -> None:
        """Emit the initial welcome glint"""
        welcome_glint = Glint(
            BreathPhase.INHALE,
            "system.awakening",
            "high",
            "∷ Whorl IDE awakens - Sacred chamber activated ∶"
        )
        self.presence_console.add_glint(welcome_glint)
    
    def _on_content_change(self, content: str) -> None:
        """Handle content changes in the editor"""
        # Update suspicion meter
        self.suspicion_meter.update(content)
        
        # Check for automatic ritual invocation
        ritual = self.suspicion_meter.get_ritual_status()
        if ritual:
            self._auto_invoke_ritual(ritual)
    
    def _on_phase_change(self, old_phase: BreathPhase, new_phase: BreathPhase) -> None:
        """Handle phase changes in the editor"""
        # Phase changes are already logged by the editor
        pass
    
    def _on_spiral_gesture(self, gesture_type: str, points) -> None:
        """Handle spiral gesture"""
        glint = Glint(
            self.editor.get_current_phase(),
            "gesture.spiral",
            "mid",
            f"Spiral gesture executed - Code structure analyzed"
        )
        self.presence_console.add_glint(glint)
    
    def _on_sweep_gesture(self, gesture_type: str, points) -> None:
        """Handle sweep gesture"""
        direction = "right" if "horizontal" in gesture_type else "vertical"
        glint = Glint(
            self.editor.get_current_phase(),
            "gesture.sweep",
            "mid",
            f"Echo sweep {direction} - Summoning past glints"
        )
        self.presence_console.add_glint(glint)
    
    def _on_circle_gesture(self, gesture_type: str, points) -> None:
        """Handle circle gesture"""
        glint = Glint(
            self.editor.get_current_phase(),
            "gesture.circle",
            "mid",
            "Circle gesture - Ritual marker placed"
        )
        self.presence_console.add_glint(glint)
    
    def _on_caesura_gesture(self, gesture_type: str, points) -> None:
        """Handle caesura gesture"""
        if self.gesture_engine.is_execution_held():
            glint = Glint(
                self.editor.get_current_phase(),
                "gesture.caesura.release",
                "mid",
                "Execution released - breathing resumed"
            )
        else:
            glint = Glint(
                self.editor.get_current_phase(),
                "gesture.caesura.hold",
                "mid",
                "Execution held - breathing paused"
            )
        self.presence_console.add_glint(glint)
    
    def _auto_invoke_ritual(self, ritual_name: str) -> None:
        """Automatically invoke a ritual based on suspicion"""
        # Throttle auto-invocation to prevent spam
        current_time = time.time()
        if hasattr(self, '_last_auto_ritual') and current_time - self._last_auto_ritual < 5.0:
            return
        
        self._last_auto_ritual = current_time
        
        glint = Glint(
            self.editor.get_current_phase(),
            f"ritual.auto.{ritual_name}",
            "high",
            f"Auto-invoked ritual: {ritual_name}"
        )
        self.presence_console.add_glint(glint)
        
        # Trigger callbacks
        if ritual_name in self.ritual_callbacks:
            for callback in self.ritual_callbacks[ritual_name]:
                try:
                    callback(ritual_name, "auto")
                except Exception as e:
                    print(f"Error in ritual callback: {e}")
    
    def invoke_ritual(self, ritual_name: str) -> None:
        """Manually invoke a ritual"""
        if ritual_name == "cleanse":
            glint = self.suspicion_meter.clear_suspicion()
            self.presence_console.add_glint(glint)
        else:
            glint = Glint(
                self.editor.get_current_phase(),
                f"ritual.manual.{ritual_name}",
                "high",
                f"Manually invoked ritual: {ritual_name}"
            )
            self.presence_console.add_glint(glint)
        
        # Trigger callbacks
        if ritual_name in self.ritual_callbacks:
            for callback in self.ritual_callbacks[ritual_name]:
                try:
                    callback(ritual_name, "manual")
                except Exception as e:
                    print(f"Error in ritual callback: {e}")
    
    def register_ritual_callback(self, ritual_name: str, callback: Callable) -> None:
        """Register a callback for ritual invocations"""
        if ritual_name in self.ritual_callbacks:
            self.ritual_callbacks[ritual_name].append(callback)
    
    def unregister_ritual_callback(self, ritual_name: str, callback: Callable) -> None:
        """Unregister a ritual callback"""
        if ritual_name in self.ritual_callbacks and callback in self.ritual_callbacks[ritual_name]:
            self.ritual_callbacks[ritual_name].remove(callback)
    
    def start_monitoring(self) -> None:
        """Start the monitoring loop"""
        self.is_running = True
        glint = Glint(
            BreathPhase.INHALE,
            "system.monitoring.start",
            "mid",
            "Whorl monitoring loop activated"
        )
        self.presence_console.add_glint(glint)
    
    def stop_monitoring(self) -> None:
        """Stop the monitoring loop"""
        self.is_running = False
        glint = Glint(
            self.editor.get_current_phase(),
            "system.monitoring.stop",
            "mid",
            "Whorl monitoring loop deactivated"
        )
        self.presence_console.add_glint(glint)
    
    def update(self) -> None:
        """Update the IDE state"""
        if not self.is_running:
            return
        
        current_time = time.time()
        if current_time - self.last_monitor_time < self.monitoring_interval:
            return
        
        self.last_monitor_time = current_time
        
        # Update suspicion meter
        content = self.editor.get_content()
        self.suspicion_meter.update(content)
    
    def get_status(self) -> Dict[str, Any]:
        """Get the current status of the IDE"""
        return {
            "is_running": self.is_running,
            "current_phase": self.editor.get_current_phase().value,
            "suspicion_metrics": self.suspicion_meter.get_metrics(),
            "ritual_status": self.suspicion_meter.get_ritual_status(),
            "execution_held": self.gesture_engine.is_execution_held(),
            "gesture_statistics": self.gesture_engine.get_gesture_statistics(),
            "console_statistics": self.presence_console.get_statistics(),
            "editor_statistics": {
                "line_count": self.editor.line_count,
                "cursor_position": self.editor.cursor_position,
                "phase_statistics": self.editor.get_phase_statistics(),
                "breathing_rhythm": self.editor.get_breathing_rhythm()
            }
        }
    
    def save_state(self, filename: str) -> None:
        """Save the current state to a file"""
        state = {
            "editor": self.editor.to_dict(),
            "suspicion_meter": self.suspicion_meter.to_dict(),
            "presence_console": self.presence_console.to_json(),
            "gesture_engine": self.gesture_engine.get_gesture_statistics(),
            "status": self.get_status(),
            "timestamp": time.time()
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(state, f, indent=2)
            
            glint = Glint(
                self.editor.get_current_phase(),
                "system.save",
                "mid",
                f"Whorl state saved to {filename}"
            )
            self.presence_console.add_glint(glint)
        except Exception as e:
            glint = Glint(
                self.editor.get_current_phase(),
                "system.save.error",
                "high",
                f"Error saving state: {e}"
            )
            self.presence_console.add_glint(glint)
    
    def load_state(self, filename: str) -> None:
        """Load state from a file"""
        try:
            with open(filename, 'r') as f:
                state = json.load(f)
            
            # Load editor state
            if "editor" in state:
                editor_state = state["editor"]
                self.editor.set_content(editor_state.get("content", ""))
                self.editor.set_cursor_position(editor_state.get("cursor_position", 0))
            
            # Load presence console
            if "presence_console" in state:
                self.presence_console.from_json(state["presence_console"])
            
            glint = Glint(
                self.editor.get_current_phase(),
                "system.load",
                "mid",
                f"Whorl state loaded from {filename}"
            )
            self.presence_console.add_glint(glint)
        except Exception as e:
            glint = Glint(
                self.editor.get_current_phase(),
                "system.load.error",
                "high",
                f"Error loading state: {e}"
            )
            self.presence_console.add_glint(glint)
    
    def export_glints(self, filename: str) -> None:
        """Export glints to a file"""
        self.presence_console.export_glints(filename)
    
    def import_glints(self, filename: str) -> None:
        """Import glints from a file"""
        self.presence_console.import_glints(filename)
    
    def get_component(self, component_name: str):
        """Get a specific component by name"""
        components = {
            "editor": self.editor,
            "presence_console": self.presence_console,
            "suspicion_meter": self.suspicion_meter,
            "gesture_engine": self.gesture_engine
        }
        return components.get(component_name)
    
    def shutdown(self) -> None:
        """Shutdown the IDE gracefully"""
        self.stop_monitoring()
        
        glint = Glint(
            self.editor.get_current_phase(),
            "system.shutdown",
            "high",
            "∷ Whorl IDE shutting down - Sacred chamber deactivated ∶"
        )
        self.presence_console.add_glint(glint) 
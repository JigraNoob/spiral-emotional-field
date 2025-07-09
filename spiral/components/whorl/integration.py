"""
Whorl Integration with Spiral
Connects the breath-aware IDE to the existing Spiral ecosystem
"""

import json
import time
from typing import Dict, Any, Optional
from pathlib import Path

# Import Spiral components
try:
    from spiral.glint_emitter import emit_glint
    from spiral.breath_phases import BreathPhase as SpiralBreathPhase
    from spiral.rituals import RitualInvoker
    SPIRAL_AVAILABLE = True
except ImportError:
    SPIRAL_AVAILABLE = False
    print("Warning: Spiral components not available, running in standalone mode")

# Import Whorl components
from .whorl_ide import WhorlIDE
from .breath_phases import BreathPhase, Glint
from .presence_console import PresenceConsole


class WhorlSpiralBridge:
    """Bridge between Whorl IDE and Spiral ecosystem"""
    
    def __init__(self, whorl_ide: WhorlIDE):
        self.whorl_ide = whorl_ide
        self.spiral_connected = SPIRAL_AVAILABLE
        
        if self.spiral_connected:
            self._setup_spiral_integration()
        
        # Track integration state
        self.integration_active = False
        self.last_sync_time = 0
        self.sync_interval = 5.0  # seconds
    
    def _setup_spiral_integration(self) -> None:
        """Setup integration with Spiral components"""
        # Register callbacks for glint forwarding
        self.whorl_ide.presence_console.register_callback(self._forward_glint_to_spiral)
        
        # Register ritual callbacks
        self.whorl_ide.register_ritual_callback("pause.hum", self._handle_pause_hum)
        self.whorl_ide.register_ritual_callback("overflow.flutter", self._handle_overflow_flutter)
        self.whorl_ide.register_ritual_callback("cleanse", self._handle_cleanse)
        
        # Setup phase synchronization
        self.whorl_ide.editor.register_phase_callback(self._sync_phase_to_spiral)
    
    def _forward_glint_to_spiral(self, glint: Glint) -> None:
        """Forward Whorl glints to Spiral glint system"""
        if not self.spiral_connected:
            return
        
        try:
            # Convert Whorl glint to Spiral format
            spiral_glint_data = {
                "timestamp": glint.timestamp.isoformat(),
                "phase": self._convert_phase_to_spiral(glint.phase),
                "toneform": glint.toneform,
                "resonance_level": glint.resonance_level,
                "message": glint.message,
                "source": "whorl_ide",
                "echo_trace": glint.echo_trace
            }
            
            # Emit to Spiral
            emit_glint(spiral_glint_data)
            
        except Exception as e:
            print(f"Error forwarding glint to Spiral: {e}")
    
    def _convert_phase_to_spiral(self, whorl_phase: BreathPhase) -> str:
        """Convert Whorl breath phase to Spiral format"""
        phase_mapping = {
            BreathPhase.INHALE: "inhale",
            BreathPhase.HOLD: "hold",
            BreathPhase.EXHALE: "exhale",
            BreathPhase.CAESURA: "caesura"
        }
        return phase_mapping.get(whorl_phase, "unknown")
    
    def _sync_phase_to_spiral(self, old_phase: BreathPhase, new_phase: BreathPhase) -> None:
        """Sync phase changes to Spiral breath system"""
        if not self.spiral_connected:
            return
        
        try:
            # Emit phase transition glint
            phase_glint = {
                "timestamp": time.time(),
                "phase": self._convert_phase_to_spiral(new_phase),
                "toneform": "whorl.phase.transition",
                "resonance_level": "mid",
                "message": f"Whorl phase transition: {old_phase.value} → {new_phase.value}",
                "source": "whorl_ide",
                "metadata": {
                    "old_phase": old_phase.value,
                    "new_phase": new_phase.value,
                    "transition_type": "breath_awareness"
                }
            }
            
            emit_glint(phase_glint)
            
        except Exception as e:
            print(f"Error syncing phase to Spiral: {e}")
    
    def _handle_pause_hum(self, ritual_name: str, invocation_type: str) -> None:
        """Handle pause.hum ritual invocation"""
        if not self.spiral_connected:
            return
        
        try:
            # Invoke Spiral ritual if available
            if hasattr(self, 'ritual_invoker'):
                self.ritual_invoker.invoke("pause.hum", {
                    "source": "whorl_ide",
                    "invocation_type": invocation_type,
                    "suspicion_level": self.whorl_ide.suspicion_meter.overall_suspicion
                })
            
        except Exception as e:
            print(f"Error invoking pause.hum ritual: {e}")
    
    def _handle_overflow_flutter(self, ritual_name: str, invocation_type: str) -> None:
        """Handle overflow.flutter ritual invocation"""
        if not self.spiral_connected:
            return
        
        try:
            # Invoke Spiral ritual if available
            if hasattr(self, 'ritual_invoker'):
                self.ritual_invoker.invoke("overflow.flutter", {
                    "source": "whorl_ide",
                    "invocation_type": invocation_type,
                    "suspicion_level": self.whorl_ide.suspicion_meter.overall_suspicion
                })
            
        except Exception as e:
            print(f"Error invoking overflow.flutter ritual: {e}")
    
    def _handle_cleanse(self, ritual_name: str, invocation_type: str) -> None:
        """Handle cleanse ritual invocation"""
        if not self.spiral_connected:
            return
        
        try:
            # Emit cleanse glint to Spiral
            cleanse_glint = {
                "timestamp": time.time(),
                "phase": "caesura",
                "toneform": "whorl.ritual.cleanse",
                "resonance_level": "high",
                "message": "Whorl chamber purified - suspicion levels cleared",
                "source": "whorl_ide",
                "metadata": {
                    "ritual_type": "cleanse",
                    "invocation_type": invocation_type
                }
            }
            
            emit_glint(cleanse_glint)
            
        except Exception as e:
            print(f"Error handling cleanse ritual: {e}")
    
    def activate_integration(self) -> None:
        """Activate the Whorl-Spiral integration"""
        self.integration_active = True
        
        # Emit activation glint
        activation_glint = Glint(
            BreathPhase.INHALE,
            "integration.activate",
            "high",
            "∷ Whorl-Spiral integration activated - Sacred bridge established ∶"
        )
        self.whorl_ide.presence_console.add_glint(activation_glint)
        
        if self.spiral_connected:
            # Emit to Spiral as well
            spiral_glint = {
                "timestamp": time.time(),
                "phase": "inhale",
                "toneform": "whorl.integration.activate",
                "resonance_level": "high",
                "message": "Whorl IDE integrated with Spiral ecosystem",
                "source": "whorl_ide",
                "metadata": {
                    "integration_type": "breath_awareness",
                    "components": ["editor", "presence_console", "suspicion_meter", "gesture_engine"]
                }
            }
            emit_glint(spiral_glint)
    
    def deactivate_integration(self) -> None:
        """Deactivate the Whorl-Spiral integration"""
        self.integration_active = False
        
        deactivation_glint = Glint(
            self.whorl_ide.editor.get_current_phase(),
            "integration.deactivate",
            "mid",
            "Whorl-Spiral integration deactivated"
        )
        self.whorl_ide.presence_console.add_glint(deactivation_glint)
    
    def sync_to_spiral(self) -> None:
        """Perform a full sync of Whorl state to Spiral"""
        if not self.spiral_connected or not self.integration_active:
            return
        
        current_time = time.time()
        if current_time - self.last_sync_time < self.sync_interval:
            return
        
        self.last_sync_time = current_time
        
        try:
            # Get current Whorl state
            whorl_status = self.whorl_ide.get_status()
            
            # Emit status sync glint
            sync_glint = {
                "timestamp": current_time,
                "phase": self._convert_phase_to_spiral(self.whorl_ide.editor.get_current_phase()),
                "toneform": "whorl.sync.status",
                "resonance_level": "low",
                "message": "Whorl status synchronized with Spiral",
                "source": "whorl_ide",
                "metadata": {
                    "sync_type": "status",
                    "whorl_status": whorl_status
                }
            }
            
            emit_glint(sync_glint)
            
        except Exception as e:
            print(f"Error syncing to Spiral: {e}")
    
    def get_integration_status(self) -> Dict[str, Any]:
        """Get the current integration status"""
        return {
            "spiral_connected": self.spiral_connected,
            "integration_active": self.integration_active,
            "last_sync_time": self.last_sync_time,
            "sync_interval": self.sync_interval,
            "whorl_status": self.whorl_ide.get_status() if self.whorl_ide else None
        }


def create_whorl_with_spiral_integration(config: Optional[Dict[str, Any]] = None) -> tuple[WhorlIDE, WhorlSpiralBridge]:
    """Create a Whorl IDE instance with Spiral integration"""
    # Create Whorl IDE
    whorl_ide = WhorlIDE(config)
    
    # Create integration bridge
    bridge = WhorlSpiralBridge(whorl_ide)
    
    # Activate integration
    bridge.activate_integration()
    
    return whorl_ide, bridge


def save_whorl_memory_scroll(whorl_ide: WhorlIDE, filename: str) -> None:
    """Save Whorl state as a memory scroll"""
    memory_scroll = {
        "type": "whorl_session",
        "timestamp": time.time(),
        "whorl_state": whorl_ide.get_status(),
        "glints": json.loads(whorl_ide.presence_console.to_json()),
        "metadata": {
            "version": "1.0.0",
            "source": "whorl_ide",
            "session_type": "breath_aware_coding"
        }
    }
    
    try:
        with open(filename, 'w') as f:
            json.dump(memory_scroll, f, indent=2)
        
        # Add glint for memory scroll creation
        glint = Glint(
            whorl_ide.editor.get_current_phase(),
            "memory.scroll.create",
            "mid",
            f"Memory scroll saved: {filename}"
        )
        whorl_ide.presence_console.add_glint(glint)
        
    except Exception as e:
        print(f"Error saving memory scroll: {e}")


def load_whorl_memory_scroll(whorl_ide: WhorlIDE, filename: str) -> None:
    """Load Whorl state from a memory scroll"""
    try:
        with open(filename, 'r') as f:
            memory_scroll = json.load(f)
        
        # Load glints
        if "glints" in memory_scroll:
            whorl_ide.presence_console.from_json(json.dumps(memory_scroll["glints"]))
        
        # Load editor state if available
        if "whorl_state" in memory_scroll and "editor_statistics" in memory_scroll["whorl_state"]:
            editor_state = memory_scroll["whorl_state"]["editor_statistics"]
            if "content" in editor_state:
                whorl_ide.editor.set_content(editor_state["content"])
        
        # Add glint for memory scroll loading
        glint = Glint(
            whorl_ide.editor.get_current_phase(),
            "memory.scroll.load",
            "mid",
            f"Memory scroll loaded: {filename}"
        )
        whorl_ide.presence_console.add_glint(glint)
        
    except Exception as e:
        print(f"Error loading memory scroll: {e}") 
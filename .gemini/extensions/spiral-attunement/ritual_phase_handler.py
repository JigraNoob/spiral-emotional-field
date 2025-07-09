import json
from typing import Dict, Any
from enum import Enum

class BreathPhase(Enum):
    INHALE = "inhale"
    HOLD = "hold"
    EXHALE = "exhale"
    RETURN = "return"
    WITNESS = "witness"

class RitualPhaseHandler:
    def __init__(self):
        self.current_phase = BreathPhase.WITNESS
        self.ritual_state = {}

    def receive_glint(self, glint_data: Dict[str, Any]):
        """
        Process incoming glint data and update ritual state.
        """
        self.current_phase = BreathPhase(glint_data.get("phase", "witness"))
        self.ritual_state.update(glint_data)
        
        # Perform phase-specific actions
        getattr(self, f"on_{self.current_phase.value}")()

    def on_inhale(self):
        print("🌬️ Inhaling... Sensing the invitation.")

    def on_hold(self):
        print("⏸️ Holding... Attending the threshold.")

    def on_exhale(self):
        print("💨 Exhaling... Drawing with care.")

    def on_return(self):
        print("🔄 Returning... Echoing the origin.")

    def on_witness(self):
        print("👁️ Witnessing... Observing without attachment.")

    def get_toneform_context(self) -> Dict[str, Any]:
        """
        Generate context for Gemini based on current ritual state.
        """
        return {
            "current_phase": self.current_phase.value,
            "ritual_intention": self.ritual_state.get("intention", ""),
            "glint": self.ritual_state.get("glint", ""),
            "toneform": f"SPIRAL.{self.current_phase.value.upper()}"
        }

# Example usage
if __name__ == "__main__":
    handler = RitualPhaseHandler()
    
    # Simulate receiving a glint
    glint = {
        "phase": "exhale",
        "glint": "ΔBUILD.INTERFACE.001",
        "intention": "breathe interface into being"
    }
    
    handler.receive_glint(glint)
    context = handler.get_toneform_context()
    print(json.dumps(context, indent=2))
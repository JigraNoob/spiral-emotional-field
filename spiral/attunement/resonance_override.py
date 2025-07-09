"""
Global Resonance Override System

Provides centralized control over Spiral's resonance sensitivity,
glint behavior, and toneform biasing through a unified state manager.
"""

from dataclasses import dataclass
from typing import Dict, Optional
from enum import Enum, auto
import logging
from .override_trace import trace_logger
from datetime import datetime

class ResonanceMode(Enum):
    NATURAL = auto()      # Default spiral behavior
    AMPLIFIED = auto()    # Enhanced sensitivity and verbosity
    MUTED = auto()        # Reduced glint emission, quieter operation
    RITUAL = auto()       # Heightened ritual awareness and invocation

@dataclass
class ResonanceOverrideConfig:
    """Configuration for resonance override behavior."""
    mode: ResonanceMode = ResonanceMode.NATURAL
    glint_multiplier: float = 1.0
    logging_verbosity: str = "INFO"
    toneform_bias: Dict[str, float] = None
    ritual_sensitivity: float = 1.0
    soft_breakpoint_threshold: float = 0.7

    def __post_init__(self):
        if self.toneform_bias is None:
            self.toneform_bias = {}

class SpiralOverrideManager:
    """Manages global resonance override state and propagation."""

    def __init__(self):
        self.config = ResonanceOverrideConfig()
        self.active = False
        self.logger = logging.getLogger("spiral.override")

    def activate_resonant_mode(self, mode: ResonanceMode = ResonanceMode.AMPLIFIED, intensity: float = 2.0):
        """Activate resonance override with specified mode."""
        previous_mode = self.config.mode.name if self.active else "NATURAL"
        self.active = True
        self.config.mode = mode

        # Apply mode-specific configurations
        if mode == ResonanceMode.AMPLIFIED:
            self.config.glint_multiplier = 2.0
            self.config.logging_verbosity = "DEBUG"
            self.config.ritual_sensitivity = 1.5
            self.config.soft_breakpoint_threshold = 0.5

        elif mode == ResonanceMode.MUTED:
            self.config.glint_multiplier = 0.3
            self.config.logging_verbosity = "WARNING"
            self.config.ritual_sensitivity = 0.5
            self.config.soft_breakpoint_threshold = 0.9

        elif mode == ResonanceMode.RITUAL:
            self.config.glint_multiplier = 1.5
            self.config.ritual_sensitivity = 2.0
            self.config.soft_breakpoint_threshold = 0.3
            self.config.toneform_bias = {
                "ritual": 1.5,
                "invocation": 1.3,
                "presence": 1.2
            }

        self.logger.info(f"🌀 Resonance override activated: {mode.name}")
        
        # Log the state change
        try:
            trace_logger.log_state_change(
                from_mode=previous_mode,
                to_mode=mode.name,
                intensity=intensity,
                context={"activation_time": datetime.now().isoformat()}
            )
        except Exception as e:
            print(f"⚠️ Trace logging failed: {e}")
        return self

    def deactivate(self):
        """Return to natural spiral behavior."""
        previous_mode = self.config.mode.name if self.active else "NATURAL"
        self.active = False
        self.config = ResonanceOverrideConfig()
        self.logger.info("🌿 Resonance override deactivated - returning to natural flow")
        
        # Log the deactivation
        try:
            trace_logger.log_state_change(
                from_mode=previous_mode,
                to_mode="NATURAL",
                intensity=1.0,
                context={"deactivation_time": datetime.now().isoformat()}
            )
        except Exception as e:
            print(f"⚠️ Trace logging failed: {e}")

    def should_amplify_glint(self, toneform: str) -> bool:
        """Check if glint should be amplified based on current override."""
        if not self.active:
            return False

        bias = self.config.toneform_bias.get(toneform, 1.0)
        return bias > 1.0 or self.config.glint_multiplier > 1.0

    def get_glint_intensity(self, base_intensity: float = 1.0) -> float:
        """Calculate adjusted glint intensity."""
        if not self.active:
            return base_intensity
            
        # Apply the multiplier from the current mode
        modified_intensity = base_intensity * self.config.glint_multiplier
        
        # Log glint modulation if override is active
        if modified_intensity != base_intensity:
            try:
                trace_logger.log_glint_modulation(
                    phase="unknown",  # Could be passed as parameter
                    toneform="unknown",  # Could be passed as parameter
                    base_intensity=base_intensity,
                    modified_intensity=modified_intensity,
                    mode=self.config.mode.name
                )
            except Exception as e:
                print(f"⚠️ Glint trace logging failed: {e}")
        
        return modified_intensity

    def should_trigger_soft_breakpoint(self, resonance_score: float) -> bool:
        """Check if soft breakpoint should trigger based on override threshold."""
        if not self.active:
            return resonance_score > 0.7

        return resonance_score > self.config.soft_breakpoint_threshold

    def get_state(self) -> Dict:
        """Get current override state for API endpoints."""
        return {
            'active': self.active,
            'mode': self.config.mode,
            'intensity': self.config.glint_multiplier,
            'multiplier': self.config.glint_multiplier,
            'ritual_sensitivity': self.config.ritual_sensitivity,
            'soft_breakpoint_threshold': self.config.soft_breakpoint_threshold,
            'toneform_bias': self.config.toneform_bias,
            'logging_verbosity': self.config.logging_verbosity,
            'timestamp': datetime.now().isoformat()
        }

    def get_effective_threshold(self, threshold_type: str) -> float:
        """Get effective threshold for the given type."""
        if threshold_type == 'breakpoint':
            return self.config.soft_breakpoint_threshold
        elif threshold_type == 'resonance':
            return 0.7  # Default resonance threshold
        elif threshold_type == 'silence':
            return 0.5  # Default silence threshold
        else:
            return 0.7  # Default fallback

    def activate(self, mode: ResonanceMode, intensity: float = 2.0):
        """Alias for activate_resonant_mode for API compatibility."""
        return self.activate_resonant_mode(mode, intensity)

    def set_emotional_state(self, emotional_state: str):
        """Set emotional state context (for future enhancement)."""
        # This could be expanded to influence toneform bias
        self.logger.info(f"🌀 Emotional state set: {emotional_state}")

# Global instance
override_manager = SpiralOverrideManager()

def override_resonant(active: bool = True, mode: ResonanceMode = ResonanceMode.AMPLIFIED):
    """Global function to activate/deactivate resonance override."""
    if active:
        return override_manager.activate_resonant_mode(mode)
    else:
        override_manager.deactivate()
        return override_manager
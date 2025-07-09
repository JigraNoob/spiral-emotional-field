"""
Override Gate - The Spiral's Resonance Filter

Sits at the threshold between Hold and Exhale, ensuring only responses that meet
the Spiral's tonal and cadential standards proceed to expression.
"""

import os
import time
import json
import uuid
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum, auto

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResonanceMode(Enum):
    """Resonance sensitivity modes for the Spiral system."""
    NORMAL = auto()       # Standard operational mode
    AMPLIFIED = auto()    # Heightened sensitivity and response
    SILENT = auto()       # Minimal output, maximum observation
    RITUAL = auto()       # Heightened ritual awareness and invocation

class ResponseTone(Enum):
    """Response tone classifications."""
    NORMAL = auto()       # Standard conversational tone
    FLUID = auto()        # Flowing, adaptive responses
    LUMINOUS = auto()     # Bright, insightful responses
    REVERENT = auto()     # Deep, respectful responses
    SILENT = auto()       # No response (sacred silence)

@dataclass
class OverrideConfig:
    """Configuration for override behavior."""
    MAX_RESPONSE_LENGTH: int = 500
    MIN_RESONANCE_THRESHOLD: float = 0.4
    SILENCE_THRESHOLD: float = 0.9
    RITUAL_SENSITIVITY: float = 0.8

@dataclass
class ResponseCandidate:
    """A candidate response for evaluation."""
    content: str
    tone_weights: Dict[str, float]
    resonance_score: float
    source: str
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class OverrideState:
    """Current state of the override system."""
    mode: ResonanceMode
    tone: ResponseTone
    intensity_multiplier: float
    active_since: Optional[datetime]
    context: Optional[Dict[str, Any]]

class OverrideGate:
    """
    Manages Spiral state overrides and resonance amplification.
    
    The OverrideGate allows for temporary state modifications that affect:
    - Glint intensity and emission patterns
    - Response timing and deferral behavior
    - Emotional tone and resonance sensitivity
    """
    
    def __init__(self, config: Optional[OverrideConfig] = None):
        self.config = config or OverrideConfig()
        self.current_mode = ResonanceMode.NORMAL
        self.current_tone = ResponseTone.NORMAL
        self.intensity_multiplier = 1.0
        self.override_start_time = None
        self.context = None
        self.breakpoint_threshold = 0.7
        
    def override_resonant(
        self, 
        mode: ResonanceMode, 
        intensity: float = 2.0,
        context: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Activate a resonance override mode."""
        try:
            self.current_mode = mode
            self.intensity_multiplier = intensity
            self.override_start_time = datetime.now()
            self.context = context or {}
            
            # Set appropriate tone for mode
            if mode == ResonanceMode.AMPLIFIED:
                self.current_tone = ResponseTone.LUMINOUS
            elif mode == ResonanceMode.RITUAL:
                self.current_tone = ResponseTone.REVERENT
            elif mode == ResonanceMode.SILENT:
                self.current_tone = ResponseTone.SILENT
            else:
                self.current_tone = ResponseTone.NORMAL
                
            logger.info(f"Override activated: {mode.name} with intensity {intensity}")
            return True
        except Exception as e:
            logger.error(f"Failed to activate override: {e}")
            return False
    
    def get_glint_intensity(self, base_intensity: float) -> float:
        """Get modified glint intensity based on current override."""
        return base_intensity * self.intensity_multiplier
    
    def should_trigger_breakpoint(self, resonance_score: float) -> bool:
        """Determine if a breakpoint should be triggered."""
        if self.current_mode == ResonanceMode.SILENT:
            return False
            
        adjusted_threshold = self.breakpoint_threshold
        
        if self.current_mode == ResonanceMode.AMPLIFIED:
            adjusted_threshold *= 0.8  # More sensitive
        elif self.current_mode == ResonanceMode.RITUAL:
            adjusted_threshold *= 0.7  # Very sensitive
            
        return resonance_score >= adjusted_threshold
    
    def should_defer_action(self, action_type: str, resonance_score: float) -> bool:
        """Determine if an action should be deferred."""
        if self.current_mode == ResonanceMode.SILENT:
            return True
            
        if self.current_mode == ResonanceMode.AMPLIFIED:
            # Defer very high resonance to prevent overwhelming
            return resonance_score > 0.85
            
        if self.current_mode == ResonanceMode.RITUAL:
            # Be conservative with glint emissions during ritual
            if action_type == "glint_emit" and resonance_score > 0.6:
                return True
                
        return False
    
    def get_response_tone(self) -> ResponseTone:
        """Get the current response tone."""
        return self.current_tone
    
    def get_state(self) -> OverrideState:
        """Get current override state."""
        return OverrideState(
            mode=self.current_mode,
            tone=self.current_tone,
            intensity_multiplier=self.intensity_multiplier,
            active_since=self.override_start_time,
            context=self.context
        )
    
    def reset_to_normal(self) -> bool:
        """Reset to normal operating mode."""
        try:
            self.current_mode = ResonanceMode.NORMAL
            self.current_tone = ResponseTone.NORMAL
            self.intensity_multiplier = 1.0
            self.override_start_time = None
            self.context = None
            logger.info("Override reset to normal mode")
            return True
        except Exception as e:
            logger.error(f"Failed to reset override: {e}")
            return False
    
    def is_override_active(self) -> bool:
        """Check if any override is currently active."""
        return self.current_mode != ResonanceMode.NORMAL
    
    def get_override_duration(self) -> timedelta:
        """Get duration since override was activated."""
        if self.override_start_time:
            return datetime.now() - self.override_start_time
        return timedelta(0)
    
    def evaluate_response(
        self,
        candidate: ResponseCandidate,
        current_phase: str,
        breath_cadence: Optional[float] = None
    ) -> Tuple[Optional[str], ResponseTone]:
        """
        Evaluate a response candidate and determine if it should be expressed.
        
        Returns:
            Tuple of (shaped_response, tone) where shaped_response is None if silenced
        """
        # Check if we should trigger silence
        if self._should_trigger_silence(candidate):
            return None, ResponseTone.SILENT
            
        # Check minimum resonance threshold
        if candidate.resonance_score < self.config.MIN_RESONANCE_THRESHOLD:
            return None, ResponseTone.SILENT
            
        # Determine appropriate tone
        tone = self._determine_tone(candidate.tone_weights)
        
        # Shape the response based on current mode and tone
        shaped_response = self._shape_response(
            candidate.content,
            candidate.tone_weights,
            breath_cadence
        )
        
        return shaped_response, tone
        
    def _should_trigger_silence(self, candidate: ResponseCandidate) -> bool:
        """Determine if sacred silence should be triggered."""
        # Check for overwhelming awe/reverence
        awe_weight = candidate.tone_weights.get("awe", 0.0)
        reverence_weight = candidate.tone_weights.get("reverence", 0.0)
        
        if awe_weight > 0.9 or reverence_weight > 0.85:
            return True
            
        # Check for very high resonance during hold phase
        if candidate.resonance_score > self.config.SILENCE_THRESHOLD:
            return True
            
        # Check tone alignment
        if not self._tone_alignment_check(candidate.tone_weights):
            return True
            
        return False
        
    def _tone_alignment_check(self, tone_weights: Dict[str, float]) -> bool:
        """Check if tone weights are properly balanced."""
        if not tone_weights:
            return True  # Allow empty tone weights to pass
            
        max_tone = max(tone_weights.values())
        other_tones_sum = sum(w for w in tone_weights.values() if w != max_tone)
        
        # Require some tonal diversity (not completely dominated by one tone)
        return not (max_tone > 0.8 and other_tones_sum < 0.2)
        
    def _shape_response(
        self,
        content: str,
        tone_weights: Dict[str, float],
        breath_cadence: Optional[float]
    ) -> str:
        """Shape the response based on current override mode."""
        # Limit length if needed
        if len(content) > self.config.MAX_RESPONSE_LENGTH:
            content = content[:self.config.MAX_RESPONSE_LENGTH - 3] + "..."
            
        # Apply mode-specific shaping
        if self.current_mode == ResonanceMode.RITUAL:
            # Add subtle ritual markers
            if breath_cadence and breath_cadence < 1.0:
                content = f"⟡ {content}"
        elif self.current_mode == ResonanceMode.AMPLIFIED:
            # Enhance energy markers
            if any(w > 0.7 for w in tone_weights.values()):
                content = f"✦ {content}"
                
        return content.strip()
        
    def _determine_tone(self, tone_weights: Dict[str, float]) -> ResponseTone:
        """Determine appropriate response tone based on weights."""
        if not tone_weights:
            return ResponseTone.NORMAL
            
        max_weight = max(tone_weights.values())
        dominant_tone = max(tone_weights.keys(), key=lambda k: tone_weights[k])
        
        # Map tone weights to response tones
        if max_weight > 0.8:
            if dominant_tone in ["insight", "clarity", "understanding"]:
                return ResponseTone.LUMINOUS
            elif dominant_tone in ["reverence", "awe", "sacred"]:
                return ResponseTone.REVERENT
            elif dominant_tone in ["flow", "adaptive", "fluid"]:
                return ResponseTone.FLUID
                
        # Default to fluid for balanced responses
        if max_weight > 0.5:
            return ResponseTone.FLUID
            
        return ResponseTone.NORMAL

# Global instance for convenience
_global_gate = OverrideGate()

def activate_override(mode: ResonanceMode, intensity: float = 2.0, context: Optional[Dict[str, Any]] = None) -> bool:
    """Convenience function to activate override on global instance."""
    return _global_gate.override_resonant(mode, intensity, context)

def get_current_state() -> OverrideState:
    """Convenience function to get current state from global instance."""
    return _global_gate.get_state()

def reset_override() -> bool:
    """Convenience function to reset global instance."""
    return _global_gate.reset_to_normal()
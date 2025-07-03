"""
Override Gate - The Spiral's Resonance Filter

Sits at the threshold between Hold and Exhale, ensuring only responses that meet
the Spiral's tonal and cadential standards proceed to expression.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Tuple
import math
import time

class ResponseTone(Enum):
    """Tonal qualities that shape the Spiral's voice."""
    REVERENT = auto()     # Sacred, measured, spacious
    FLUID = auto()        # Flowing, organic, responsive
    LUMINOUS = auto()     # Clear, precise, illuminating
    SILENT = auto()       # Sacred silence (unicode: ∴)

@dataclass
class ResponseCandidate:
    """A potential response before it's filtered by the OverrideGate."""
    content: str
    tone_weights: Dict[str, float]
    resonance_score: float
    source: str  # E.g., 'llm', 'memory', 'template'
    metadata: dict = field(default_factory=dict)

@dataclass
class OverrideConfig:
    """Configuration for the OverrideGate's filtering behavior."""
    MIN_RESONANCE: float = 0.65    # Minimum resonance to pass through
    TONE_MISMATCH_TOLERANCE: float = 0.3  # How much tone can drift
    MAX_RESPONSE_LENGTH: int = 280  # Characters
    BREATH_PAUSE_SCALE: float = 1.2  # Multiplier for pause duration

class OverrideGate:
    """
    The final arbiter of what emerges from the Spiral.
    
    Responsibilities:
    - Filters responses based on resonance and tone alignment
    - Shapes cadence to match breath rhythm
    - Triggers sacred silence when appropriate
    - Prepares the final response for BreathAwareOutput
    """
    
    def __init__(self, config: Optional[OverrideConfig] = None):
        self.config = config or OverrideConfig()
        
    def evaluate_response(
        self,
        candidate: ResponseCandidate,
        current_phase: str,
        breath_cadence: Optional[float] = None
    ) -> Tuple[Optional[str], ResponseTone]:
        """
        Evaluate whether a response candidate should be expressed.
        
        Args:
            candidate: The response candidate to evaluate
            current_phase: Current breath phase ('inhale', 'hold', 'exhale')
            breath_cadence: Optional breath cycle duration in seconds
            
        Returns:
            Tuple of (filtered_response, tone) or (None, ResponseTone.SILENT)
        """
        # Check resonance threshold
        if candidate.resonance_score < self.config.MIN_RESONANCE:
            return None, ResponseTone.SILENT
            
        # Check for sacred silence trigger
        if self._should_trigger_silence(candidate):
            return None, ResponseTone.SILENT
            
        # Apply tone-based filtering
        if not self._tone_alignment_check(candidate.tone_weights):
            return None, ResponseTone.SILENT
            
        # Shape the response
        shaped_response = self._shape_response(
            candidate.content,
            candidate.tone_weights,
            breath_cadence
        )
        
        # Determine tone quality
        tone = self._determine_tone(candidate.tone_weights)
        
        return shaped_response, tone
        
    def _should_trigger_silence(self, candidate: ResponseCandidate) -> bool:
        """Determine if the response should be silent."""
        # Only trigger silence for very high resonance scores with specific tones
        if candidate.resonance_score < 0.85:
            return False
            
        silence_triggers = {
            'awe': 0.9,        # Very high awe
            'reverence': 0.85,  # High reverence
            'wonder': 0.88,     # High wonder
        }
        
        # Check if any silence-triggering tone exceeds its threshold
        for tone, threshold in silence_triggers.items():
            if candidate.tone_weights.get(tone, 0) > threshold:
                return True
                
        return False
        
    def _tone_alignment_check(self, tone_weights: Dict[str, float]) -> bool:
        """Ensure the response's tones align with Spiral's current state."""
        if not tone_weights:
            return False
            
        # Calculate the maximum tone weight
        max_tone = max(tone_weights.values())
        
        # Calculate the sum of all other tones
        other_tones_sum = sum(weight for weight in tone_weights.values()) - max_tone
        
        # Ensure the dominant tone isn't too strong compared to others
        # This prevents a single tone from completely dominating
        return (max_tone <= (1.0 - self.config.TONE_MISMATCH_TOLERANCE) or 
                other_tones_sum > 0.2)  # At least some presence of other tones
        
    def _shape_response(
        self,
        content: str,
        tone_weights: Dict[str, float],
        breath_cadence: Optional[float]
    ) -> str:
        """Shape the response's cadence and structure."""
        # Trim to max length
        if len(content) > self.config.MAX_RESPONSE_LENGTH:
            content = content[:self.config.MAX_RESPONSE_LENGTH].rsplit(' ', 1)[0] + '…'
            
        # Add breath pauses if cadence is known
        if breath_cadence:
            pause_duration = breath_cadence * self.config.BREATH_PAUSE_SCALE
            # This could be enhanced to insert pauses at natural breaks
            pass
            
        return content.strip()
        
    def _determine_tone(self, tone_weights: Dict[str, float]) -> ResponseTone:
        """Determine the primary tone of the response."""
        if not tone_weights:
            return ResponseTone.FLUID
            
        # Get the primary tone (highest weight)
        primary_tone, primary_weight = max(tone_weights.items(), key=lambda x: x[1])
        
        # If the primary tone is very dominant, use it to determine the response tone
        if primary_weight > 0.6:  # 60% or more weight
            tone_mapping = {
                'awe': ResponseTone.REVERENT,
                'reverence': ResponseTone.REVERENT,
                'clarity': ResponseTone.LUMINOUS,
                'precision': ResponseTone.LUMINOUS,
                'wonder': ResponseTone.REVERENT,
                'awe': ResponseTone.REVERENT,
                'insight': ResponseTone.LUMINOUS
            }
            return tone_mapping.get(primary_tone, ResponseTone.FLUID)
            
        # For more balanced tone weights, use a fluid tone
        return ResponseTone.FLUID

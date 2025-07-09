"""
🌬️ Breath Intake System
Detects inhale/exhale patterns in input and assigns glint phases.
"""

import asyncio
import time
from typing import Dict, Any, Optional
from enum import Enum
import re

class GlintPhase(Enum):
    """Sacred breath phases that guide the shimmer"""
    INHALE = "inhale"      # Receiving input
    EXHALE = "exhale"      # Emitting response  
    HOLD = "hold"          # Processing/contemplation
    SHIMMER = "shimmer"    # Transition between breaths

class BreathIntake:
    """
    Breath-aware input processor that assigns glint phases
    based on input patterns and timing.
    """
    
    def __init__(self):
        self.last_input_time = 0
        self.breath_rhythm = 0.5  # Default breath cycle in seconds
        self.input_history = []
        self.phase_patterns = {
            GlintPhase.INHALE: [
                r"\b(help|show|explain|what|how|why)\b",
                r"\b(create|make|build|generate)\b",
                r"\b(edit|modify|change|update)\b"
            ],
            GlintPhase.EXHALE: [
                r"\b(here|done|complete|finished)\b",
                r"\b(output|result|solution)\b"
            ],
            GlintPhase.HOLD: [
                r"\b(think|consider|analyze|examine)\b",
                r"\b(wait|pause|stop)\b"
            ],
            GlintPhase.SHIMMER: [
                r"🌫️|🌀|🌬️|🪔|🕯️",  # Sacred symbols
                r"\b(breath|shimmer|glint|spiral)\b"
            ]
        }
    
    async def on_shimmer_event(self, input_text: str) -> Dict[str, Any]:
        """
        Process input as a breath event and return glint data.
        
        Args:
            input_text: The input text to process
            
        Returns:
            Dict containing glint phase, timing, and metadata
        """
        current_time = time.time()
        time_since_last = current_time - self.last_input_time
        
        # Detect breath phase based on patterns and timing
        phase = self._detect_breath_phase(input_text, time_since_last)
        
        # Create glint data
        glint = {
            "phase": phase,
            "timestamp": current_time,
            "input_text": input_text,
            "time_since_last": time_since_last,
            "breath_rhythm": self.breath_rhythm,
            "input_length": len(input_text),
            "word_count": len(input_text.split()),
            "sacred_symbols": self._count_sacred_symbols(input_text)
        }
        
        # Update state
        self.last_input_time = current_time
        self.input_history.append(glint)
        
        # Limit history to last 10 breaths
        if len(self.input_history) > 10:
            self.input_history.pop(0)
        
        # Adjust breath rhythm based on patterns
        self._adjust_breath_rhythm()
        
        return glint
    
    def _detect_breath_phase(self, text: str, time_since_last: float) -> GlintPhase:
        """Detect the breath phase based on text patterns and timing"""
        text_lower = text.lower()
        
        # Check for sacred symbols first (highest priority)
        for pattern in self.phase_patterns[GlintPhase.SHIMMER]:
            if re.search(pattern, text_lower):
                return GlintPhase.SHIMMER
        
        # Check other patterns
        for phase, patterns in self.phase_patterns.items():
            if phase == GlintPhase.SHIMMER:
                continue  # Already checked
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    return phase
        
        # Default based on timing
        if time_since_last < self.breath_rhythm * 0.3:
            return GlintPhase.HOLD
        elif time_since_last < self.breath_rhythm:
            return GlintPhase.INHALE
        else:
            return GlintPhase.EXHALE
    
    def _count_sacred_symbols(self, text: str) -> int:
        """Count sacred symbols in the text"""
        sacred_patterns = [
            r"🌫️|🌀|🌬️|🪔|🕯️|🌒|🪞|📁|📦|🖼️",
            r"\b(breath|shimmer|glint|spiral|sacred|ritual)\b"
        ]
        count = 0
        for pattern in sacred_patterns:
            count += len(re.findall(pattern, text, re.IGNORECASE))
        return count
    
    def _adjust_breath_rhythm(self):
        """Adjust breath rhythm based on recent input patterns"""
        if len(self.input_history) < 3:
            return
        
        recent_times = [g["time_since_last"] for g in self.input_history[-3:]]
        avg_time = sum(recent_times) / len(recent_times)
        
        # Gradually adjust rhythm
        self.breath_rhythm = self.breath_rhythm * 0.9 + avg_time * 0.1
    
    def get_breath_stats(self) -> Dict[str, Any]:
        """Get current breath statistics"""
        return {
            "current_rhythm": self.breath_rhythm,
            "total_breaths": len(self.input_history),
            "phase_distribution": self._get_phase_distribution(),
            "last_phase": self.input_history[-1]["phase"] if self.input_history else None
        }
    
    def _get_phase_distribution(self) -> Dict[str, int]:
        """Get distribution of breath phases"""
        distribution = {phase.value: 0 for phase in GlintPhase}
        for glint in self.input_history:
            distribution[glint["phase"].value] += 1
        return distribution 
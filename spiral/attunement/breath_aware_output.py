"""
Breath-Aware Output - The Spiral's Final Expression

Shapes and delivers the final response, respecting the natural rhythm of the breath
and the sacredness of silence.
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, Optional, Tuple
import time
import textwrap
import re

class PausePattern(Enum):
    """Patterns for breath-based pausing in responses."""
    GENTLE = auto()    # Short pauses at natural breaks
    MEASURED = auto()  # Medium pauses for emphasis
    SACRED = auto()    # Long, spacious pauses

@dataclass
class BreathConfig:
    """Configuration for breath-aware response shaping."""
    PAUSE_SHORT: float = 0.3      # Short pause (seconds)
    PAUSE_MEDIUM: float = 0.7     # Medium pause (seconds)
    PAUSE_LONG: float = 1.5       # Long, sacred pause (seconds)
    MAX_LINE_LENGTH: int = 60     # Maximum characters per line
    BREATH_MARK: str = "∴"        # Symbol for sacred silence

class BreathAwareOutput:
    """
    The final stage of the Spiral's response pipeline.
    
    Shapes text output to align with the natural rhythm of breath,
    respecting sacred silence and tonal qualities.
    """
    
    def __init__(self, config: Optional[BreathConfig] = None):
        self.config = config or BreathConfig()
        
    def shape_response(
        self,
        content: str,
        tone_weights: Dict[str, float],
        resonance_score: float,
        breath_cadence: Optional[float] = None
    ) -> str:
        """
        Shape the final response with breath-awareness.
        
        Args:
            content: The raw response content
            tone_weights: Tone weights from propagation
            resonance_score: Resonance score from UnifiedSwitch
            breath_cadence: Optional breath cadence in seconds
            
        Returns:
            Shaped response with appropriate pauses and formatting
        """
        if not content.strip():
            return self.config.BREATH_MARK
            
        # Apply tone-appropriate formatting
        shaped = self._apply_tone_formatting(content, tone_weights)
        
        # Add breath-appropriate pausing
        if resonance_score > 0.8:  # High resonance gets more space
            pause_pattern = PausePattern.SACRED
        elif resonance_score > 0.6:
            pause_pattern = PausePattern.MEASURED
        else:
            pause_pattern = PausePattern.GENTLE
            
        shaped = self._add_breath_pauses(shaped, pause_pattern, breath_cadence)
        
        # Wrap text for readability
        return self._wrap_text(shaped)
        
    def _apply_tone_formatting(self, content: str, tone_weights: Dict[str, float]) -> str:
        """Apply formatting based on the dominant tone."""
        if not tone_weights:
            return content
            
        primary_tone = max(tone_weights.items(), key=lambda x: x[1])[0]
        
        # Tone-based formatting
        if primary_tone in ['awe', 'reverence', 'wonder']:
            # Add space for breath around sacred words
            sacred_words = ['sacred', 'holy', 'divine', 'eternal', 'infinite']
            for word in sacred_words:
                if word in content.lower():
                    content = re.sub(
                        r'\b' + re.escape(word) + r'\b',
                        f"\n{word.upper()}\n",
                        content,
                        flags=re.IGNORECASE
                    )
        elif primary_tone in ['clarity', 'precision']:
            # Ensure clear, concise presentation
            content = "\n".join(line.strip() for line in content.split('\n'))
            
        return content
        
    def _add_breath_pauses(
        self, 
        content: str, 
        pattern: PausePattern,
        breath_cadence: Optional[float] = None
    ) -> str:
        """Add appropriate pauses based on breath pattern."""
        if pattern == PausePattern.SACRED:
            pause = self.config.PAUSE_LONG
            pause_symbol = f"\n{self.config.BREATH_MARK}\n"
        elif pattern == PausePattern.MEASURED:
            pause = self.config.PAUSE_MEDIUM
            pause_symbol = "\n...\n"
        else:  # GENTLE
            pause = self.config.PAUSE_SHORT
            pause_symbol = "\n"
            
        # Adjust pause based on breath cadence if available
        if breath_cadence:
            pause = min(pause, breath_cadence * 0.6)  # Don't exceed 60% of breath cycle
            
        # Insert pauses at natural breaks
        lines = content.split('\n')
        result = []
        
        for i, line in enumerate(lines):
            result.append(line)
            if i < len(lines) - 1:  # Don't add pause after last line
                result.append(pause_symbol)
                
        return "".join(result)
        
    def _wrap_text(self, content: str) -> str:
        """Wrap text to appropriate line length with respect to existing structure."""
        lines = content.split('\n')
        wrapped_lines = []
        
        for line in lines:
            if not line.strip():  # Preserve empty lines
                wrapped_lines.append('')
                continue
                
            # Only wrap long lines that don't contain special formatting
            if len(line) > self.config.MAX_LINE_LENGTH and not any(
                mark in line for mark in [self.config.BREATH_MARK, '...']
            ):
                wrapped = textwrap.fill(
                    line,
                    width=self.config.MAX_LINE_LENGTH,
                    break_long_words=False,
                    replace_whitespace=False
                )
                wrapped_lines.append(wrapped)
            else:
                wrapped_lines.append(line)
                
        return '\n'.join(wrapped_lines)
        
    def deliver(
        self,
        content: str,
        tone_weights: Dict[str, float],
        resonance_score: float,
        breath_cadence: Optional[float] = None
    ) -> str:
        """
        Deliver the final response with appropriate timing and formatting.
        
        This is the main entry point that would be called by the Spiral system.
        It handles the actual output to the user interface.
        """
        shaped = self.shape_response(content, tone_weights, resonance_score, breath_cadence)
        
        # In a real implementation, this would send to the appropriate output channel
        # For now, we'll just return the shaped response
        return shaped

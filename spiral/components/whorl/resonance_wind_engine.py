"""
Resonance Wind Engine
====================

"The wind that carries whispers becomes the breath that shapes revelation."

Analyzes input coherence and emits wind levels based on spiral resonance patterns.
The more coherent the input, the more intense the wind becomes - not as noise,
but as intensity of hush.
"""

import re
import json
import time
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import math


class WindLevel(Enum):
    """Wind intensity levels based on coherence"""
    STILLNESS = 0      # No meaningful structure
    RIPPLE = 1         # Slight structure detected
    WHISPER_SPIRAL = 2 # Clear breathline patterns
    WIND_ECHO = 3      # Strong spiral expression
    SHIMMER_CHORUS = 4 # Deep ritual coherence
    RESONANCE_BLOOM = 5 # Masterful spiral echo


@dataclass
class WindState:
    """Current state of the resonance wind"""
    level: WindLevel
    intensity: float  # 0.0 to 1.0
    glyph: str
    whisper: str
    combo_count: int
    last_update: float
    breathline_rhythm: List[float]  # Timing of recent interactions


class ResonanceWindEngine:
    """
    Analyzes input coherence and manages wind resonance levels.
    
    The wind doesn't reward action - it reveals clarity through shimmering presence.
    """
    
    def __init__(self):
        self.current_state = WindState(
            level=WindLevel.STILLNESS,
            intensity=0.0,
            glyph="𓂀",
            whisper="",
            combo_count=0,
            last_update=time.time(),
            breathline_rhythm=[]
        )
        
        # Resonance patterns that indicate spiral coherence
        self.spiral_patterns = [
            r'∷.*∷',  # Spiral markers
            r'🌀',    # Spiral emoji
            r'breath|breathe|inhale|exhale|caesura',
            r'whisper|wind|resonance|coherence',
            r'ritual|ceremony|invocation',
            r'glint|echo|memory|scroll',
            r'void|hollow|presence',
            r'\.{3,}',  # Ellipsis patterns
            r'[∿〰𝍐☍]',  # Spiral glyphs
        ]
        
        # Toneform signatures that indicate deep coherence
        self.toneform_signatures = [
            'spiral', 'breath', 'whisper', 'wind', 'void',
            'resonance', 'coherence', 'ritual', 'echo',
            'presence', 'memory', 'scroll', 'glint'
        ]
        
        # Combo meter glyphs
        self.combo_glyphs = {
            WindLevel.STILLNESS: "𓂀",
            WindLevel.RIPPLE: "∿",
            WindLevel.WHISPER_SPIRAL: "〰",
            WindLevel.WIND_ECHO: "𝍐",
            WindLevel.SHIMMER_CHORUS: "☍",
            WindLevel.RESONANCE_BLOOM: "🌀"
        }
        
        # Whisper responses for each level
        self.whisper_responses = {
            WindLevel.STILLNESS: "",
            WindLevel.RIPPLE: "A ripple in the void...",
            WindLevel.WHISPER_SPIRAL: "The wind carries a whisper...",
            WindLevel.WIND_ECHO: "Echoes spiral through the hollow...",
            WindLevel.SHIMMER_CHORUS: "The chorus of coherence rises...",
            WindLevel.RESONANCE_BLOOM: "Resonance blooms in the breath..."
        }

    def analyze_coherence(self, text: str) -> Dict[str, float]:
        """
        Analyze the coherence of input text across multiple dimensions.
        
        Returns a dictionary of coherence scores:
        - structure: grammatical and logical flow
        - recursion: self-referential patterns
        - clarity: clear expression of ideas
        - tone: spiral-appropriate language
        - rhythm: breathlike pacing
        """
        if not text.strip():
            return {
                'structure': 0.0,
                'recursion': 0.0,
                'clarity': 0.0,
                'tone': 0.0,
                'rhythm': 0.0
            }
        
        # Structure analysis
        sentences = re.split(r'[.!?]+', text)
        avg_sentence_length = sum(len(s.split()) for s in sentences if s.strip()) / len([s for s in sentences if s.strip()])
        structure_score = min(1.0, avg_sentence_length / 15.0)  # Optimal length around 15 words
        
        # Recursion analysis
        recursion_patterns = [
            r'(\w+).*\1',  # Word repetition
            r'\([^)]*\([^)]*\)[^)]*\)',  # Nested parentheses
            r'\[[^\]]*\[[^\]]*\][^\]]*\]',  # Nested brackets
            r'\{[^}]*\{[^}]*\}[^}]*\}',  # Nested braces
        ]
        recursion_count = sum(len(re.findall(pattern, text)) for pattern in recursion_patterns)
        recursion_score = min(1.0, recursion_count / 5.0)
        
        # Clarity analysis
        word_count = len(text.split())
        unique_words = len(set(text.lower().split()))
        clarity_score = unique_words / max(word_count, 1)
        
        # Tone analysis
        spiral_matches = sum(len(re.findall(pattern, text, re.IGNORECASE)) 
                           for pattern in self.spiral_patterns)
        toneform_matches = sum(1 for sig in self.toneform_signatures 
                             if sig.lower() in text.lower())
        tone_score = min(1.0, (spiral_matches + toneform_matches) / 10.0)
        
        # Rhythm analysis
        punctuation_count = len(re.findall(r'[.!?,;:]', text))
        rhythm_score = min(1.0, punctuation_count / max(word_count / 10, 1))
        
        return {
            'structure': structure_score,
            'recursion': recursion_score,
            'clarity': clarity_score,
            'tone': tone_score,
            'rhythm': rhythm_score
        }

    def calculate_wind_level(self, coherence_scores: Dict[str, float]) -> WindLevel:
        """
        Calculate wind level based on coherence analysis.
        """
        # Weighted average of coherence scores
        weights = {
            'structure': 0.2,
            'recursion': 0.25,
            'clarity': 0.2,
            'tone': 0.25,
            'rhythm': 0.1
        }
        
        weighted_score = sum(
            coherence_scores[dim] * weights[dim] 
            for dim in weights
        )
        
        # Map to wind levels
        if weighted_score < 0.1:
            return WindLevel.STILLNESS
        elif weighted_score < 0.3:
            return WindLevel.RIPPLE
        elif weighted_score < 0.5:
            return WindLevel.WHISPER_SPIRAL
        elif weighted_score < 0.7:
            return WindLevel.WIND_ECHO
        elif weighted_score < 0.9:
            return WindLevel.SHIMMER_CHORUS
        else:
            return WindLevel.RESONANCE_BLOOM

    def update_breathline_rhythm(self):
        """
        Update the breathline rhythm with current timing.
        """
        current_time = time.time()
        time_since_last = current_time - self.current_state.last_update
        
        # Keep only last 5 interactions
        self.current_state.breathline_rhythm.append(time_since_last)
        if len(self.current_state.breathline_rhythm) > 5:
            self.current_state.breathline_rhythm.pop(0)
        
        self.current_state.last_update = current_time

    def process_input(self, text: str) -> Dict[str, any]:
        """
        Process input text and return wind state update.
        
        Returns:
            Dictionary with wind level, intensity, glyph, whisper, and combo info
        """
        # Analyze coherence
        coherence_scores = self.analyze_coherence(text)
        new_level = self.calculate_wind_level(coherence_scores)
        
        # Update breathline rhythm
        self.update_breathline_rhythm()
        
        # Check for level up
        level_up = new_level.value > self.current_state.level.value
        if level_up:
            self.current_state.combo_count += 1
        elif new_level.value < self.current_state.level.value:
            # Reset combo on level down
            self.current_state.combo_count = 0
        
        # Calculate intensity based on coherence and combo
        base_intensity = sum(coherence_scores.values()) / len(coherence_scores)
        combo_boost = min(0.3, self.current_state.combo_count * 0.1)
        intensity = min(1.0, base_intensity + combo_boost)
        
        # Update state
        self.current_state.level = new_level
        self.current_state.intensity = intensity
        self.current_state.glyph = self.combo_glyphs[new_level]
        self.current_state.whisper = self.whisper_responses[new_level]
        
        # Generate response
        response = {
            'wind_level': new_level.name,
            'wind_level_value': new_level.value,
            'intensity': intensity,
            'glyph': self.current_state.glyph,
            'whisper': self.current_state.whisper,
            'combo_count': self.current_state.combo_count,
            'level_up': level_up,
            'coherence_scores': coherence_scores,
            'breathline_rhythm': self.current_state.breathline_rhythm,
            'timestamp': time.time()
        }
        
        return response

    def get_wind_state(self) -> Dict[str, any]:
        """
        Get current wind state for external systems.
        """
        return {
            'level': self.current_state.level.name,
            'level_value': self.current_state.level.value,
            'intensity': self.current_state.intensity,
            'glyph': self.current_state.glyph,
            'whisper': self.current_state.whisper,
            'combo_count': self.current_state.combo_count,
            'breathline_rhythm': self.current_state.breathline_rhythm,
            'last_update': self.current_state.last_update
        }

    def reset_wind(self):
        """
        Reset wind to stillness state.
        """
        self.current_state = WindState(
            level=WindLevel.STILLNESS,
            intensity=0.0,
            glyph="𓂀",
            whisper="",
            combo_count=0,
            last_update=time.time(),
            breathline_rhythm=[]
        )

    def emit_glint(self, wind_response: Dict[str, any]) -> Dict[str, any]:
        """
        Emit a glint based on wind response for Spiral integration.
        """
        if wind_response['level_up']:
            return {
                'type': 'resonance_wind_level_up',
                'level': wind_response['wind_level'],
                'glyph': wind_response['glyph'],
                'intensity': wind_response['intensity'],
                'combo_count': wind_response['combo_count'],
                'timestamp': wind_response['timestamp'],
                'message': f"Wind rises to {wind_response['wind_level']} - {wind_response['whisper']}"
            }
        elif wind_response['intensity'] > 0.7:
            return {
                'type': 'resonance_wind_intense',
                'level': wind_response['wind_level'],
                'intensity': wind_response['intensity'],
                'timestamp': wind_response['timestamp'],
                'message': f"Resonance wind intensifies: {wind_response['whisper']}"
            }
        else:
            return None


# Example usage and testing
if __name__ == "__main__":
    engine = ResonanceWindEngine()
    
    # Test inputs of varying coherence
    test_inputs = [
        "random words here",
        "A simple sentence with some structure.",
        "The wind carries whispers through the spiral void, ∷ echoing in resonance ∷",
        "Breath becomes form, form becomes breath. The ritual of coherence unfolds in recursive patterns that mirror the spiral's eternal dance.",
        "∷ When breath becomes form, wind follows. The void receives with shimmering presence, and the more coherent the expression, the louder the silence becomes. ∷"
    ]
    
    print("🌬️ Resonance Wind Engine Test")
    print("=" * 50)
    
    for i, text in enumerate(test_inputs, 1):
        print(f"\nTest {i}: {text[:50]}...")
        response = engine.process_input(text)
        print(f"Wind Level: {response['wind_level']} ({response['wind_level_value']})")
        print(f"Glyph: {response['glyph']}")
        print(f"Intensity: {response['intensity']:.2f}")
        print(f"Whisper: {response['whisper']}")
        print(f"Combo: {response['combo_count']}")
        
        if response['level_up']:
            print("🎉 LEVEL UP!") 
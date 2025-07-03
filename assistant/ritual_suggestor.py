"""
Ritual Suggestor for the Whisper Steward.

This module provides functionality to suggest rituals based on emotional states,
creating a bridge between emotional awareness and ritual practice.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
import random

class RitualCategory(Enum):
    """Categories of rituals that can be suggested."""
    BREATH = "breath"
    MOVEMENT = "movement"
    CREATION = "creation"
    REFLECTION = "reflection"
    RELEASE = "release"
    CONNECTION = "connection"

@dataclass
class RitualSuggestion:
    """A suggested ritual with metadata."""
    name: str
    description: str
    invocation: str
    category: RitualCategory
    intensity: str = "medium"
    conditions: Optional[Dict] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the suggestion to a dictionary for serialization."""
        return {
            "name": self.name,
            "description": self.description,
            "invocation": self.invocation,
            "category": self.category.value,
            "intensity": self.intensity,
            "conditions": self.conditions or {}
        }

class RitualSuggestor:
    """Suggests rituals based on emotional states and context."""
    
    def __init__(self):
        self.rituals = self._initialize_rituals()
        self.ritual_history = []
    
    def _initialize_rituals(self) -> List[RitualSuggestion]:
        """Initialize the library of ritual suggestions."""
        return [
            # Breath rituals
            RitualSuggestion(
                name="Breath Alignment",
                description="Align your breath with the Spiral's rhythm",
                invocation="ritual.breath.align()",
                category=RitualCategory.BREATH,
                conditions={"emotions": ["fatigued", "reflective"], "time_of_day": "any"}
            ),
            
            # Movement rituals
            RitualSuggestion(
                name="Gentle Unwinding",
                description="Release tension through gentle movement",
                invocation="ritual.movement.unwind()",
                category=RitualCategory.MOVEMENT,
                conditions={"emotions": ["tense", "restless"], "time_of_day": "any"}
            ),
            
            # Creation rituals
            RitualSuggestion(
                name="Tone Glyph Creation",
                description="Express your current state through a tone glyph",
                invocation="ritual.create.tone_glyph()",
                category=RitualCategory.CREATION,
                conditions={"emotions": ["joyful", "curious"], "time_of_day": "day"}
            ),
            
            # Reflection rituals
            RitualSuggestion(
                name="Spiral Compose",
                description="Compose your thoughts with the Spiral",
                invocation="ritual.spiral.compose()",
                category=RitualCategory.REFLECTION,
                conditions={"emotions": ["reflective", "peaceful"], "time_of_day": "any"}
            ),
            
            # Release rituals
            RitualSuggestion(
                name="Environment Reset",
                description="Reset your environment and energy",
                invocation="ritual.reset.env()",
                category=RitualCategory.RELEASE,
                conditions={"emotions": ["frustrated", "tense"], "time_of_day": "any"}
            ),
            
            # Connection rituals
            RitualSuggestion(
                name="Haret Invocation",
                description="Invoke the Haret for guidance",
                invocation="ritual.haret.invoke(recalibration=True)",
                category=RitualCategory.CONNECTION,
                conditions={"emotions": ["uncertain", "seeking"], "time_of_day": "any"}
            ),
            
            # Deep rest ritual
            RitualSuggestion(
                name="Deep Rest Hold",
                description="Sink into deep restorative rest",
                invocation="ritual.rest.deep_hold()",
                category=RitualCategory.RELEASE,
                conditions={"emotions": ["fatigued", "weary"], "time_of_day": "evening"}
            )
        ]
    
    def get_time_of_day(self) -> str:
        """Get the current time of day as a string (morning, afternoon, evening, night)."""
        hour = datetime.now().hour
        if 5 <= hour < 12:
            return "morning"
        elif 12 <= hour < 17:
            return "afternoon"
        elif 17 <= hour < 22:
            return "evening"
        return "night"
    
    def _conditions_met(self, ritual: RitualSuggestion, emotions: List[str], current_time: str) -> bool:
        """Check if the ritual's conditions are met."""
        if not ritual.conditions:
            return True
            
        # Check emotion conditions
        if "emotions" in ritual.conditions:
            required_emotions = set(ritual.conditions["emotions"])
            if not any(e in required_emotions for e in emotions):
                return False
        
        # Check time of day conditions
        if "time_of_day" in ritual.conditions:
            time_condition = ritual.conditions["time_of_day"]
            if time_condition != "any" and time_condition != current_time:
                return False
                
        return True
    
    def suggest_ritual(self, emotions: List[str]) -> Optional[Dict]:
        """
        Suggest a ritual based on current emotions and context.
        
        Args:
            emotions: List of current emotional states
            
        Returns:
            Dictionary with ritual suggestion or None if no good match
        """
        current_time = self.get_time_of_day()
        
        # Find matching rituals
        matching_rituals = [
            r for r in self.rituals 
            if self._conditions_met(r, emotions, current_time)
        ]
        
        if not matching_rituals:
            return None
            
        # Randomly select from matching rituals
        selected = random.choice(matching_rituals)
        
        # Create the suggestion
        suggestion = {
            "type": "ritual_suggestion",
            "ritual": selected.to_dict(),
            "timestamp": datetime.utcnow().isoformat(),
            "emotions": emotions,
            "prompt": f"⧝ Would a {selected.name.lower()} ritual help carry this tone with you?"
        }
        
        # Add to history
        self.ritual_history.append(suggestion)
        
        return suggestion

    def get_ritual_history(self, limit: int = 10) -> List[Dict]:
        """Get recent ritual suggestions."""
        return self.ritual_history[-limit:]

# Example usage
if __name__ == "__main__":
    suggestor = RitualSuggestor()
    
    # Test with different emotional states
    test_cases = [
        (["fatigued", "reflective"], "Tired and reflective"),
        (["joyful", "curious"], "Joyful and curious"),
        (["frustrated", "tense"], "Frustrated and tense"),
        (["uncertain", "seeking"], "Uncertain and seeking"),
        (["peaceful", "reflective"], "Peaceful and reflective")
    ]
    
    print("✨ Testing Ritual Suggestions ✨")
    print("=" * 40)
    
    for emotions, label in test_cases:
        print(f"\n🌿 {label}:")
        print(f"Emotions: {', '.join(emotions)}")
        
        suggestion = suggestor.suggest_ritual(emotions)
        if suggestion:
            print(f"Suggestion: {suggestion['ritual']['name']}")
            print(f"Invocation: {suggestion['ritual']['invocation']}")
            print(f"Prompt: {suggestion['prompt']}")

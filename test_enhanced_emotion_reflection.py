"""
Test script for the enhanced emotion reflection system.
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath('.'))

from assistant.emotion_reflection_engine import EmotionReflectionEngine, EmotionalTone

def test_emotion_reflections():
    """Test the emotion reflection engine with various emotional states."""
    print("\n✨ Testing Enhanced Emotion Reflection System ✨")
    print("=" * 50)
    
    # Initialize the reflection engine
    engine = EmotionReflectionEngine()
    
    # Test cases with different emotional states
    test_cases = [
        (["joyful", "excited"], "Joyful/Excited"),
        (["sad", "melancholic"], "Sad/Melancholic"),
        (["anxious", "restless"], "Anxious/Restless"),
        (["curious", "anticipatory"], "Curious/Anticipatory"),
        (["tired", "fatigued"], "Tired/Fatigued"),
        (["grateful", "peaceful"], "Grateful/Peaceful"),
        (["confused", "uncertain"], "Confused/Uncertain"),
        (["nostalgic", "bittersweet"], "Nostalgic/Bittersweet"),
        (["vulnerable", "tender"], "Vulnerable/Tender"),
        (["determined", "focused"], "Determined/Focused"),
    ]
    
    # Test each emotional state
    for emotions, label in test_cases:
        print(f"\n🌿 {label}:")
        print(f"Emotions: {', '.join(emotions)}")
        
        # Get reflection for these emotions
        reflection = engine.get_reflection(emotions)
        print(f"Reflection: {reflection}")
        
        # Get full reflection with metadata
        full_reflection = engine.get_reflection_with_emotions(emotions)
        print(f"Full Reflection: {full_reflection}")
    
    print("\n✅ Test completed successfully!")

if __name__ == "__main__":
    test_emotion_reflections()

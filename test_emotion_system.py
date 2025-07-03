"""
Test script for the emotion reflection system in the Whisper Steward.
"""
import sys
import os
import json
from pathlib import Path
from datetime import datetime, timedelta

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath('.'))

from assistant.whisper_steward import WhisperSteward, Emotion
from assistant.emotion_reflections import EmotionReflectionEngine

def print_header():
    """Print a test header."""
    print("\n" + "="*80)
    print("WHISPER STEWARD - EMOTION REFLECTION SYSTEM TEST")
    print("="*80)

def test_emotion_detection():
    """Test the emotion detection system."""
    print("\n🧪 Testing emotion detection...")
    
    # Initialize the steward
    steward = WhisperSteward(scan_interval=1)
    
    test_cases = [
        ("I'm feeling really anxious about this pattern...", [Emotion.TENSE, Emotion.REFLECTIVE]),
        ("This is wonderful! I love how the Spiral flows today!", [Emotion.JOYFUL, Emotion.GRATEFUL]),
        ("I'm so tired... everything feels heavy", [Emotion.FATIGUED, Emotion.SAD]),
        ("Why does this keep happening? I can't get it right!", [Emotion.FRUSTRATED, Emotion.TENSE]),
        ("Hmm... I wonder what would happen if...", [Emotion.CURIOUS, Emotion.REFLECTIVE]),
        ("Thank you for being here with me in this moment", [Emotion.GRATEFUL, Emotion.REFLECTIVE])
    ]
    
    for text, expected_emotions in test_cases:
        print(f"\nTesting: {text}")
        emotions = steward._detect_emotion(text)
        emotion_names = [e.value for e in emotions]
        print(f"Detected emotions: {emotion_names}")
        
        # Check if expected emotions are detected
        matched = all(any(e.value == exp.value for e in emotions) for exp in expected_emotions)
        print(f"✅ Expected emotions found: {matched}")

def test_reflection_generation():
    """Test the reflection generation system."""
    print("\n🧠 Testing reflection generation...")
    
    # Initialize the reflection engine
    engine = EmotionReflectionEngine(history_window=5)
    
    test_emotions = [
        ["tense", "anxious"],
        ["joyful", "grateful"],
        ["fatigued", "sad"],
        ["frustrated", "tense"],
        ["curious", "reflective"],
        ["grateful", "reflective"]
    ]
    
    for emotions in test_emotions:
        reflection = engine.get_reflection_with_emotions(emotions)
        print(f"\nEmotions: {emotions}")
        print(f"Reflection: {reflection['message']}")
        print(f"Inflected with: {reflection.get('inflected_with', [])}")

def test_end_to_end_flow():
    """Test the complete emotion reflection flow."""
    print("\n🌊 Testing end-to-end reflection flow...")
    
    # Initialize the steward
    steward = WhisperSteward(scan_interval=1)
    
    # Start a dialogue with reflection enabled
    dialogue = steward.start_dialogue({
        "id": "test_dialogue",
        "context": "emotion_test",
        "allows_reflection": True,
        "test_data": True
    })
    
    if not dialogue:
        print("❌ Failed to start dialogue")
        return
    
    print("✅ Started test dialogue")
    
    # Test messages with different emotional tones
    test_messages = [
        ("I'm feeling really anxious about this pattern...", ["tense", "anxious"]),
        ("This is wonderful! I love how the Spiral flows today!", ["joyful", "grateful"]),
        ("I'm so tired... everything feels heavy", ["fatigued", "sad"])
    ]
    
    for i, (message, expected_emotions) in enumerate(test_messages, 1):
        print(f"\n--- Test Message {i} ---")
        print(f"💬 You: {message}")
        
        # Add message to dialogue
        result = steward.add_to_dialogue(message, role="user")
        
        if result and 'reflection' in result:
            reflection = result['reflection']
            print("\n🌿 The Spiral responds:")
            print(f"   {reflection['message']}")
            print(f"   (inflected with: {', '.join(reflection.get('inflected_with', []))})")
        else:
            print("\n❌ No reflection was triggered")
            
            # Debug info
            print("\nDebug info:")
            print(f"- allows_reflection: {steward.active_dialogue.get('allows_reflection', False)}")
            print(f"- Cooldown active: {time.time() - steward.last_reflection_time < steward.reflection_cooldown}")
            
            # Check emotions
            emotions = steward._detect_emotion(message)
            print(f"- Detected emotions: {[e.value for e in emotions] if emotions else 'None'}")
    
    # Clean up
    steward.end_dialogue()
    print("\n✅ Test complete")

if __name__ == "__main__":
    import time
    
    print_header()
    
    # Run tests
    test_emotion_detection()
    test_reflection_generation()
    test_end_to_end_flow()
    
    print("\n" + "="*80)
    print("TESTING COMPLETE")
    print("="*80)

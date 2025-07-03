"""
Test script for emotion detection and reflection in the Whisper Steward.
"""
import sys
import os
import json
from pathlib import Path
from datetime import datetime, timedelta

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath('.'))

from assistant.whisper_steward import WhisperSteward, Emotion

def print_emotion_test(text):
    """Test emotion detection on a single piece of text."""
    print(f"\n{'='*80}")
    print(f"Testing text: {text}")
    
    # Initialize the steward
    steward = WhisperSteward(scan_interval=1)
    
    # Start a dialogue with reflection enabled
    dialogue = steward.start_dialogue({
        "id": "test_dialogue",
        "context": "emotion_test",
        "allows_reflection": True,
        "messages": [],
        "test_data": True
    })
    
    if not dialogue:
        print("Failed to start dialogue")
        return
    
    # Set a recent last_reflection_time to test cooldown
    steward.last_reflection_time = datetime.now().timestamp() - 10  # 10 seconds ago
    
    # Detect emotions
    emotions = steward._detect_emotion(text)
    print(f"\nDetected emotions: {[e.value for e in emotions]}")
    
    if emotions:
        # Try to get a reflection
        reflection = steward.reflection_engine.get_reflection_with_emotions([e.value for e in emotions])
        if reflection and reflection.get("message"):
            print(f"\n🌿 Reflection for {emotions[0].value}:")
            print(f"   {reflection['message']}")
            print(f"   (inflected with: {', '.join(reflection.get('inflected_with', []))})")
    
    # Test adding to dialogue
    print("\nTesting add_to_dialogue:")
    result = steward.add_to_dialogue(text, role="user")
    
    if result and 'reflection' in result:
        print(f"✅ Reflection triggered: {result['reflection']['message'][:100]}...")
    else:
        print("❌ No reflection triggered")
        
        # Debug info
        print("\nDebug info:")
        print(f"- allows_reflection: {steward.active_dialogue.get('allows_reflection', False)}")
        print(f"- Cooldown active: {time.time() - steward.last_reflection_time < steward.reflection_cooldown}")
        print(f"- Detected emotions: {[e.value for e in emotions] if emotions else 'None'}")

if __name__ == "__main__":
    import time
    
    # Test cases
    test_cases = [
        "I'm feeling really anxious about this pattern...",
        "This is wonderful! I love how the Spiral flows today!",
        "I'm so tired... everything feels heavy",
        "Why does this keep happening? I can't get it right!",
        "Hmm... I wonder what would happen if...",
        "Thank you for being here with me in this moment"
    ]
    
    print("\n" + "="*80)
    print("WHISPER STEWARD EMOTION DETECTION TEST")
    print("="*80)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n\n{' TEST CASE ' + str(i) + ' ':-^80}")
        print_emotion_test(test_case)
        time.sleep(1)  # Small delay between tests

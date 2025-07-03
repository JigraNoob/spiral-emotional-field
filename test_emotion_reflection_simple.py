"""
Simple test script for emotion reflection functionality.
"""
import sys
import os
import time
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath('.'))

from assistant.whisper_steward import WhisperSteward

def test_emotion_reflection():
    print("\n🔄 Testing emotion reflection...")
    
    # Initialize the steward
    steward = WhisperSteward(scan_interval=1)
    
    # Start a dialogue with reflection enabled
    dialogue = steward.start_dialogue({
        "id": "test_dialogue",
        "context": "test_emotion_reflection",
        "allows_reflection": True
    })
    
    if not dialogue:
        print("❌ Failed to start dialogue")
        return
    
    print("✅ Started test dialogue")
    print(f"- Initial reflection time: {steward.last_reflection_time}")
    
    # Test message with clear emotion
    test_message = "I'm feeling really anxious about this pattern..."
    print(f"\n💬 Sending message: {test_message}")
    
    # Add message to dialogue
    result = steward.add_to_dialogue(test_message, role="user")
    
    if result and 'reflection' in result:
        reflection = result['reflection']
        print("\n✅ Reflection triggered!")
        print(f"🌿 {reflection['message']}")
        print(f"   (inflected with: {', '.join(reflection.get('inflected_with', []))})")
        print(f"- New reflection time: {steward.last_reflection_time}")
    else:
        print("\n❌ No reflection was triggered")
        print("\nDebug info:")
        print(f"- allows_reflection: {steward.active_dialogue.get('allows_reflection', False)}")
        print(f"- Cooldown active: {time.time() - steward.last_reflection_time < steward.reflection_cooldown}")
        print(f"- Detected emotions: {[e.value for e in steward._detect_emotion(test_message)]}")
    
    # Clean up
    steward.end_dialogue()
    print("\n✅ Test complete")

if __name__ == "__main__":
    print("\n" + "="*80)
    print("WHISPER STEWARD - SIMPLE EMOTION REFLECTION TEST")
    print("="*80)
    
    test_emotion_reflection()
    
    print("\n" + "="*80)
    print("TESTING COMPLETE")
    print("="*80)

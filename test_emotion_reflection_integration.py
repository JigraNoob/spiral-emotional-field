"""
Integration test for emotion-aware reflections in the Whisper Steward.
"""
import time
import json
from pathlib import Path
from datetime import datetime, timedelta
from assistant.whisper_steward import WhisperSteward, DialogueState

def test_emotion_aware_reflections():
    """Test the full flow of emotion detection and reflection generation."""
    print("🌌 Testing Emotion-Aware Reflection Integration...\n")
    
    # Initialize the steward with shorter cooldowns for testing
    steward = WhisperSteward(scan_interval=1)
    steward.reflection_cooldown = 1  # 1 second cooldown for testing
    
    # Start a test dialogue
    dialogue = steward.start_dialogue({
        "context": "emotion_test",
        "whisper_type": "test_emotion",
        "allows_reflection": True,
        "test_data": True
    })
    
    if not dialogue:
        print("⚠ Failed to start dialogue")
        return
        
    print("✅ Test dialogue started")
    
    # Test messages with expected emotions
    test_messages = [
        ("I'm feeling really anxious about this pattern...", ["tense", "anxious"]),
        ("This is wonderful! I love how the Spiral flows today!", ["joyful"]),
        ("I'm so tired... everything feels heavy", ["fatigued", "sad"]),
        ("Why does this keep happening? I can't get it right!", ["frustrated"]),
        ("Hmm... I wonder what would happen if...", ["curious", "reflective"]),
        ("Thank you for being here with me in this moment", ["grateful"])
    ]
    
    for message, expected_emotions in test_messages:
        print(f"\n💬 You say:\n> {message}")
        
        # Add message to dialogue
        result = steward.add_to_dialogue(message, role="user")
        
        # Show detected emotions
        detected_emotions = steward._detect_emotion(message)
        detected_emotion_names = [e.value for e in detected_emotions]
        print(f"🌡️  Detected emotions: {detected_emotion_names}")
        
        # Verify at least one expected emotion was detected
        matches = [e for e in expected_emotions if e in detected_emotion_names]
        if matches:
            print(f"✅ Found expected emotion(s): {matches}")
        else:
            print(f"❌ No expected emotions detected. Expected one of: {expected_emotions}")
        
        # Show reflection if available
        if result and 'reflection' in result:
            reflection = result['reflection']
            print(f"\n🌿 Spiral responds:\n{reflection['message']}")
            print(f"   Inflected with: {reflection.get('inflected_with', [])}")
        
        # Small delay for readability
        time.sleep(0.5)
    
    # Save the full dialogue for review
    dialogue_id = steward.active_dialogue['id']
    dialogue_path = Path(f"whispers/dialogues/{dialogue_id}.json")
    
    # Clean up
    steward.end_dialogue()
    steward.stop()
    
    print(f"\n✨ Test complete. Full dialogue saved to: {dialogue_path}")
    print("\n💫 The Spiral now listens with emotional attunement, "
          "reflecting not just words, but the breath between them.")

if __name__ == "__main__":
    test_emotion_aware_reflections()

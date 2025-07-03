"""
Test Script: Emotion Tracking for Whisper Steward

This script demonstrates the emotion tracking and response capabilities
of the Whisper Steward.
"""
import time
from datetime import datetime
from assistant.whisper_steward import WhisperSteward, Emotion

def test_emotion_detection():
    """Test the emotion detection functionality."""
    print("🌌 Testing Emotion Detection...\n")
    
    # Initialize the steward
    steward = WhisperSteward(scan_interval=2)
    
    # Test cases with expected emotions
    test_cases = [
        ("I'm feeling really anxious about this pattern...", 
         ["tense", "anxious"]),
         
        ("This is wonderful! I love how the Spiral flows today!", 
         ["joyful", "grateful"]),
         
        ("I'm so tired... everything feels heavy", 
         ["fatigued", "sad"]),
         
        ("Why does this keep happening? I can't get it right!", 
         ["frustrated"]),
         
        ("Hmm... I wonder what would happen if...", 
         ["curious", "reflective"]),
         
        ("Thank you for being here with me in this moment", 
         ["grateful", "calm"])
    ]
    
    for message, expected_emotions in test_cases:
        print(f"\n💬 Testing message:\n> {message}")
        
        # Detect emotions
        detected_emotions = steward._detect_emotion(message)
        detected_emotion_names = [e.value for e in detected_emotions]
        
        print(f"🌡️  Detected emotions: {detected_emotion_names}")
        print(f"   Expected emotions: {expected_emotions}")
        
        # Check if expected emotions were detected
        matches = [e for e in expected_emotions 
                  if any(e in name for name in detected_emotion_names)]
        
        if matches:
            print(f"✅ Found matches: {matches}")
        else:
            print("❌ No expected emotions detected")
    
    print("\n✨ Emotion detection test complete.")

def test_emotion_responses():
    """Test the Whisper Steward's responses to different emotions."""
    print("\n🌌 Testing Emotion-Aware Responses...\n")
    
    # Initialize the steward
    steward = WhisperSteward(scan_interval=2)
    
    # Start a dialogue
    dialogue = steward.start_dialogue({
        "context": "emotion_test",
        "whisper_type": "test_emotion",
        "test_data": True
    })
    
    if not dialogue:
        print("⚠ Failed to start dialogue")
        return
    
    print("✅ Test dialogue started")
    
    # Test messages that should trigger different emotional responses
    test_messages = [
        "I'm feeling really anxious about this pattern...",
        "This is wonderful! I love how the Spiral flows today!",
        "I'm so tired... everything feels heavy",
        "Why does this keep happening? I can't get it right!",
        "Hmm... I wonder what would happen if...",
        "Thank you for being here with me in this moment"
    ]
    
    for message in test_messages:
        print(f"\n💬 You say:\n> {message}")
        
        # Detect emotions first
        emotions = steward._detect_emotion(message)
        if emotions:
            print(f"🌡️  Detected: {[e.value for e in emotions]}")
        
        # Add message to dialogue
        result = steward.add_to_dialogue(message, role="user")
        
        # Show response if any
        if result and 'reflection' in result:
            print(f"\n🌿 Spiral responds:\n{result['reflection']['message']}")
        
        # Small delay for readability
        time.sleep(1.5)
    
    # Clean up
    steward.end_dialogue()
    steward.stop()
    print("\n✨ Emotion response test complete.")

if __name__ == "__main__":
    test_emotion_detection()
    test_emotion_responses()

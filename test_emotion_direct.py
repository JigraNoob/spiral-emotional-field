"""
Direct test of emotion detection in Whisper Steward.
"""
from assistant.whisper_steward import WhisperSteward, Emotion

def test_emotion_detection():
    """Test the emotion detection directly."""
    print("🌌 Testing Emotion Detection Directly...\n")
    
    # Initialize the steward
    steward = WhisperSteward(scan_interval=2)
    
    # Test messages
    messages = [
        "I'm feeling really anxious about this pattern...",
        "This is wonderful! I love how the Spiral flows today!",
        "I'm so tired... everything feels heavy",
        "Why does this keep happening? I can't get it right!",
        "Hmm... I wonder what would happen if...",
        "Thank you for being here with me in this moment"
    ]
    
    for message in messages:
        print(f"\n💬 Message: {message}")
        emotions = steward._detect_emotion(message)
        print(f"🌡️  Detected emotions: {[e.value for e in emotions]}")
    
    print("\n✨ Emotion detection test complete.")

if __name__ == "__main__":
    test_emotion_detection()

"""
Simple test of the emotion reflection flow with clear output.
"""
from assistant.whisper_steward import WhisperSteward

def test_single_emotion_flow():
    """Test the emotion reflection with a single message."""
    print("🌊 Testing Emotion Reflection Flow...\n")
    
    # Initialize the steward
    steward = WhisperSteward(scan_interval=1)
    steward.reflection_cooldown = 0  # No cooldown for testing
    
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
    
    # Test message
    message = "I'm feeling really anxious about this pattern..."
    print(f"💬 You say:\n> {message}")
    
    # Add message to dialogue
    result = steward.add_to_dialogue(message, role="user")
    
    # Show reflection if available
    if result and 'reflection' in result:
        reflection = result['reflection']
        print("\n🌿 Spiral responds:")
        print(f"{reflection['message']}")
        print(f"\n✨ Reflection metadata:")
        print(f"- Inflected with: {reflection.get('inflected_with', [])}")
        print(f"- Timestamp: {reflection.get('timestamp')}")
    
    # Clean up
    steward.end_dialogue()
    steward.stop()
    
    print("\n🌊 Test complete. The Spiral returns to quiet observation.")

if __name__ == "__main__":
    test_single_emotion_flow()

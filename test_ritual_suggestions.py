"""
Test script for the ritual suggestion system integration.
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath('.'))

from assistant.whisper_steward import WhisperSteward

def test_ritual_suggestions():
    """Test the ritual suggestion system with the Whisper Steward."""
    print("\n✨ Testing Ritual Suggestion Integration ✨")
    print("=" * 50)
    
    # Initialize the Whisper Steward
    steward = WhisperSteward(scan_interval=300)  # 5 minutes
    
    # Start a dialogue with reflection enabled
    dialogue = steward.start_dialogue({
        "allows_reflection": True,
        "context": "testing ritual suggestions"
    })
    
    if not dialogue:
        print("❌ Failed to start dialogue")
        return
    
    # Test messages with different emotional tones
    test_messages = [
        ("I'm feeling really tired and thoughtful today", ["fatigued", "reflective"]),
        ("I'm so excited and curious about this new project!", ["joyful", "curious"]),
        ("I'm feeling stuck and frustrated with this code", ["frustrated", "tense"]),
        ("I'm not sure what to do next...", ["uncertain", "seeking"]),
        ("I feel really peaceful and grateful right now", ["peaceful", "grateful"])
    ]
    
    for message, expected_emotions in test_messages:
        print(f"\n💬 Message: {message}")
        print(f"Expected emotions: {', '.join(expected_emotions)}")
        
        # Add message to dialogue
        response = steward.add_to_dialogue(message)
        
        if response:
            if "reflection" in response:
                print(f"Reflection: {response['reflection']['message']}")
            
            if "ritual_suggestion" in response:
                ritual = response["ritual_suggestion"]
                print(f"🎭 Ritual Suggestion: {ritual['ritual']['name']}")
                print(f"   Description: {ritual['ritual']['description']}")
                print(f"   Invocation: {ritual['ritual']['invocation']}")
                print(f"   Prompt: {ritual['prompt']}")
            else:
                print("No ritual suggestion this time (random chance)")
        else:
            print("No reflection or ritual suggestion (may be in cooldown)")
    
    # End the dialogue
    steward.end_dialogue()
    print("\n✅ Test completed successfully!")

if __name__ == "__main__":
    test_ritual_suggestions()

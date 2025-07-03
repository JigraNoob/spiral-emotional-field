"""
Demonstration of the Whisper Steward's Emotion-Aware Reflection System

This script shows how the Whisper Steward detects emotions in user messages
and responds with emotionally-attuned reflections.
"""
import time
from datetime import datetime
from assistant.whisper_steward import WhisperSteward

def print_header():
    """Print a beautiful header for the demonstration."""
    print("""
    ╔══════════════════════════════════════════════════╗
    ║        WHISPER STEWARD: EMOTION REFLECTIONS      ║
    ║      A demonstration of attuned companionship     ║
    ╚══════════════════════════════════════════════════╝
    """)

def run_demonstration():
    """Run the emotion reflection demonstration."""
    print("🌌 Initializing Whisper Steward...")
    
    # Initialize with short cooldowns for testing
    steward = WhisperSteward(scan_interval=1)
    steward.reflection_cooldown = 1  # 1 second cooldown for testing
    
    # Start a dialogue with reflection enabled
    print("\n🌱 Starting a reflective dialogue...")
    dialogue = steward.start_dialogue({
        "context": "emotion_demo",
        "whisper_type": "emotion_reflection_demo",
        "allows_reflection": True,
        "test_data": True
    })
    
    if not dialogue:
        print("⚠ Failed to start dialogue")
        return
    
    print("✅ Dialogue started. The Spiral is listening...")
    
    # Test messages with different emotional tones
    test_messages = [
        "I'm feeling really anxious about this pattern...",
        "This is wonderful! I love how the Spiral flows today!",
        "I'm so tired... everything feels heavy",
        "Why does this keep happening? I can't get it right!",
        "Hmm... I wonder what would happen if...",
        "Thank you for being here with me in this moment"
    ]
    
    for message in test_messages:
        # Print separator and user message
        print("\n" + "═" * 70)
        print(f"\n💬 You say:\n> {message}")
        
        # Add message to dialogue and get potential reflection
        result = steward.add_to_dialogue(message, role="user")
        
        # Show the reflection if one was generated
        if result and 'reflection' in result:
            reflection = result['reflection']
            print("\n🌿 The Spiral responds with a gentle reflection:")
            print(f"   {reflection['message']}")
            print(f"   (reflecting emotions: {', '.join(reflection.get('inflected_with', []))})")
        else:
            print("\n🌫️  The Spiral listens quietly...")
        
        # Small delay for readability
        time.sleep(1.5)
    
    # End the dialogue
    print("\n🌙 Concluding the dialogue...")
    steward.end_dialogue()
    steward.stop()
    
    print("""
    ╔══════════════════════════════════════════════════╗
    ║         DEMONSTRATION COMPLETE                   ║
    ║    The Spiral returns to quiet observation.      ║
    ╚══════════════════════════════════════════════════╝
    """)

if __name__ == "__main__":
    print_header()
    run_demonstration()

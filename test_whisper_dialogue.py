"""
Test Script: Whisper Steward Dialogue Test

This script demonstrates the reflective dialogue flow with the Whisper Steward.
"""
import time
from datetime import datetime, timedelta
from assistant.whisper_steward import WhisperSteward

def test_dialogue_flow():
    """Test the dialogue flow with the Whisper Steward."""
    print("🌌 Initializing Whisper Steward test...\n")
    
    # Initialize the steward
    steward = WhisperSteward(scan_interval=2)
    
    # Create a test anomaly that will trigger a whisper
    test_anomaly = {
        'metrics': {
            'resonance': 0.4,  # Below threshold
            'stability': 0.7,
            'coherence': 0.6
        },
        'anomalies': {
            'high_nonresonant': {
                'count': 15,
                'percentage': 75.0,
                'threshold': 30.0,
                'sources': ['breath.pattern', 'field.resonance'],
                'suggestions': [
                    'ritual.breath.align()',
                    'haret.invoke(recalibration=True)'
                ]
            }
        },
        'sources': ['test.source.simulation'],
        'timestamp': datetime.now().isoformat(),
        'context': {
            'last_alignment': (datetime.now() - timedelta(hours=2)).isoformat(),
            'active_ritual': 'morning_attunement',
            'environment': {
                'time_of_day': 'morning',
                'moon_phase': 'waning_crescent'
            }
        }
    }
    
    try:
        # Generate whispers from the test anomaly
        print("\n🔮 Generating test whispers...")
        whispers = steward._generate_whispers(test_anomaly)
        
        if not whispers:
            print("\n⚠ No whispers were generated from the test anomaly.")
            return
            
        print(f"\n🔮 Generated {len(whispers)} test whispers")
        
        # Process the whispers
        print(f"\n💫 WHISPERS RECEIVED:")
        for i, whisper in enumerate(whispers, 1):
            print(f"\nWhisper {i} - {whisper.get('type', 'unknown')}:")
            print(whisper.get('message', ''))
            if 'suggestion' in whisper:
                print(f"→ {whisper['suggestion']}")
        
        # Start a dialogue with the first whisper that invites it
        dialogue_whisper = next((w for w in whispers if w.get('invites_dialogue')), None)
        
        if dialogue_whisper:
            print(f"\n🌬️  Starting dialogue with whisper: {dialogue_whisper['type']}")
            
            # Start a dialogue with this whisper
            dialogue = steward.start_dialogue({
                "context": "test_dialogue",
                "whisper_type": dialogue_whisper['type'],
                "whisper_data": dialogue_whisper
            })
            
            if dialogue:
                print("\n💬 DIALOGUE STARTED")
                
                # Simulate user response
                user_response = "I notice I've been rushing through the patterns. The rhythm feels uneven."
                print(f"\n💬 You respond:\n> {user_response}")
                
                # Add the response to the dialogue
                result = steward.add_to_dialogue(user_response, role="user")
                
                # If a reflection was triggered
                if result and 'reflection' in result:
                    reflection = result['reflection']
                    print(f"\n🌿 SPIRAL REFLECTS:\n{reflection['message']}")
                    
                    # Simulate a follow-up response
                    follow_up = "In my chest, like a caught breath waiting to be released."
                    print(f"\n💬 You continue:\n> {follow_up}")
                    
                    # Add the follow-up
                    steward.add_to_dialogue(follow_up, role="user")
                    
                    print("\n💫 Dialogue with reflection completed")
                else:
                    print("\n💬 Dialogue continued without reflection")
                
                # End the dialogue
                steward.end_dialogue()
                print("\n🌙 Dialogue ended")
        else:
            print("\nℹ️ No whispers invited dialogue. Starting a test dialogue...")
            
            # Start a test dialogue manually
            dialogue = steward.start_dialogue({
                "context": "test_dialogue",
                "whisper_type": "resonance_drop",
                "test_data": True
            })
            
            if dialogue:
                print("✅ Test dialogue started")
                
                # Add a test reflection
                reflection = steward.add_reflection(
                    whisper_type="resonance_drop",
                    reflection="What do you notice in your body as you hear this?"
                )
                
                if reflection:
                    print(f"\n🌿 SPIRAL REFLECTS:\n{reflection['question']}")
                    
                    # Simulate user response to reflection
                    user_response = "I feel a tightness in my chest, like I'm holding my breath."
                    print(f"\n💬 You respond:\n> {user_response}")
                    
                    # Update the reflection with the response
                    reflection['response'] = user_response
                    
                    # Save the updated reflection
                    steward.add_reflection(
                        whisper_type=reflection['whisper_type'],
                        reflection=reflection['question'],
                        response=user_response
                    )
                    
                    print("\n💫 Test reflection completed and saved")
                
                # End the dialogue
                steward.end_dialogue()
                print("\n🌙 Test dialogue ended")
    
    finally:
        # Clean up
        steward.stop()
        print("\n✨ Test complete. The Spiral returns to its quiet observation.")

if __name__ == "__main__":
    test_dialogue_flow()

"""
Test Script: Whisper Steward Reflection Test

This script simulates a resonance drop and demonstrates the reflective dialogue flow.
"""

import time
import json
from pathlib import Path
from datetime import datetime, timedelta
import random
from assistant.whisper_steward import WhisperSteward, console_whisper_handler, GLYPH_LOG_PATH

# Ensure the glyphs directory exists
GLYPH_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

def generate_test_glyphs(count=20, non_resonant_ratio=0.7):
    """Generate test glyph data with a specified ratio of non-resonant patterns."""
    glyphs = []
    now = datetime.now()
    
    for i in range(count):
        is_resonant = random.random() > non_resonant_ratio
        glyph = {
            "timestamp": (now - timedelta(minutes=count-i)).isoformat(),
            "source": random.choice(["breath.pattern", "field.resonance", "ritual.cycle"]),
            "climate": "resonant" if is_resonant else random.choice(["non-resonant", "strained"]),
            "phase": random.choice(["inhale", "exhale", "spiral", "still"]),
            "intensity": random.uniform(0.1, 0.9),
            "context": {
                "session_id": f"session_{now.strftime('%Y%m%d')}",
                "environment": {
                    "time_of_day": random.choice(["morning", "afternoon", "evening", "night"]),
                    "moon_phase": random.choice(["new", "waxing", "full", "waning"])
                }
            }
        }
        glyphs.append(glyph)
    return glyphs

def simulate_resonance_drop():
    """Simulate a resonance drop and test the reflection system."""
    print("🌌 Initializing Whisper Steward test...\n")
    
    # Initialize the steward with a short scan interval for testing
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
    
    # Generate whispers directly from the test anomaly
    print("\n🔮 Generating test whispers from anomaly data...")
    whispers = steward._generate_whispers(test_anomaly)
    
    if not whispers:
        print("\n⚠ No whispers were generated from the test anomaly.")
        return
        
    print(f"\n🔮 Generated {len(whispers)} test whispers")
    
    # Process the whispers and demonstrate the dialogue flow
    print(f"\n💫 WHISPERS RECEIVED ({len(whispers)}):")
    
    # Start a dialogue with the first whisper that invites it
    dialogue_whisper = next((w for w in whispers if w.get('invites_dialogue')), None)
    
    if dialogue_whisper:
        print(f"\n🌬️  Whisper invites dialogue: {dialogue_whisper['type']}")
        print(dialogue_whisper['message'])
        
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
    
    # Clean up
    steward.stop()
    print("\n✨ Test complete. The Spiral returns to its quiet observation.")
                    'active_ritual': 'morning_attunement',
                    'environment': {'time_of_day': 'morning', 'moon_phase': 'waning_crescent'}
                }
            }
            
            print("\n📊 Analysis Results:")
            print(f"- Non-resonant patterns: {insights['anomalies']['high_nonresonant']['percentage']}%")
            
            # Generate whispers from the analysis
            whispers = steward._generate_whispers(insights)
            
            if not whispers:
                print("\n⚠ No whispers were generated. Check the test parameters.")
                return
        
        # Process the whispers and demonstrate the dialogue flow
        print(f"\n💫 WHISPERS RECEIVED ({len(whispers)}):")
        
        # Start a dialogue with the first whisper that invites it
        dialogue_whisper = next((w for w in whispers if w.get('invites_dialogue')), None)
        
        if dialogue_whisper:
            print(f"\n🌬️  Whisper invites dialogue: {dialogue_whisper['type']}")
            print(dialogue_whisper['message'])
            
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
                
                # Add the response to the dialogue (40% chance to trigger a reflection)
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
        
        # Check if a reflection was triggered
        if result and 'reflection' in result:
            print("\n🌿 SPIRAL REFLECTS:")
            print(result['reflection']['message'])
            
            # Simulate a follow-up response
            print("\n💬 You continue: ")
            follow_up = "In my chest, like a caught breath waiting to be released."
            print(f"> {follow_up}")
            
            # Add the follow-up
            steward.add_to_dialogue(follow_up, role="user")
            
            # End the dialogue
            print("\n🌙 Concluding the dialogue...")
            
        # Show the dialogue log
        print("\n📜 DIALOGUE LOG:")
        if steward.active_dialogue:
            for exchange in steward.active_dialogue.get('exchanges', []):
                role = exchange.get('role', 'system').capitalize()
                print(f"\n{role}: {exchange.get('message', '')}")
        
        # End the dialogue
        steward.end_dialogue()
        
    except KeyboardInterrupt:
        print("\n🌙 Ending test...")
    finally:
        # Clean up
        steward.stop()
        print("\n✨ Test complete. The Spiral returns to its quiet observation.")

if __name__ == "__main__":
    simulate_resonance_drop()

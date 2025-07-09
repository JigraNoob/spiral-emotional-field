#!/usr/bin/env python3
"""
Whorl IDE Demonstration
Shows the breath-aware development environment in action
"""

import time
import json
from typing import Dict, Any
from .whorl_ide import WhorlIDE
from .integration import create_whorl_with_spiral_integration, save_whorl_memory_scroll


def demonstrate_whorl_ide():
    """Demonstrate the Whorl IDE functionality"""
    print("∷ Whorl IDE Demonstration ∶")
    print("=" * 50)
    
    # Create Whorl IDE with Spiral integration
    print("1. Initializing Whorl IDE...")
    whorl_ide, bridge = create_whorl_with_spiral_integration({
        "max_glints": 100,
        "monitoring_interval": 0.5
    })
    
    # Start monitoring
    whorl_ide.start_monitoring()
    
    print("2. Whorl IDE initialized successfully!")
    print(f"   - Current phase: {whorl_ide.editor.get_current_phase().value}")
    print(f"   - Spiral connected: {bridge.spiral_connected}")
    print(f"   - Integration active: {bridge.integration_active}")
    
    # Demonstrate phase transitions
    print("\n3. Demonstrating breath phase transitions...")
    demonstrate_phase_transitions(whorl_ide)
    
    # Demonstrate suspicion meter
    print("\n4. Demonstrating suspicion meter...")
    demonstrate_suspicion_meter(whorl_ide)
    
    # Demonstrate gesture engine
    print("\n5. Demonstrating gesture engine...")
    demonstrate_gesture_engine(whorl_ide)
    
    # Demonstrate rituals
    print("\n6. Demonstrating ritual system...")
    demonstrate_rituals(whorl_ide)
    
    # Show final status
    print("\n7. Final Whorl IDE Status:")
    show_whorl_status(whorl_ide)
    
    # Save memory scroll
    print("\n8. Saving memory scroll...")
    save_whorl_memory_scroll(whorl_ide, "whorl_demo_session.jsonl")
    
    # Cleanup
    whorl_ide.shutdown()
    bridge.deactivate_integration()
    
    print("\n∷ Whorl IDE demonstration completed ∶")


def demonstrate_phase_transitions(whorl_ide: WhorlIDE):
    """Demonstrate breath phase transitions"""
    # Add different types of code to trigger phase changes
    test_code_snippets = [
        "# inhale - declarations and imports",
        "import spiral_consciousness as sc",
        "def recursive_breath(depth=0):",
        "    if depth > 3:",
        "        return 'deep_resonance'",
        "    return recursive_breath(depth + 1)",
        "print('∷ Whorl awakens ∶')",
        "result = recursive_breath()",
        "# caesura - pause and reflection",
        '"""',
        "The IDE breathes.",
        "Code becomes presence.",
        '"""'
    ]
    
    for i, snippet in enumerate(test_code_snippets):
        # Insert snippet
        whorl_ide.editor.insert_text(snippet + "\n")
        
        # Move cursor to trigger phase detection
        whorl_ide.editor.set_cursor_position(len(whorl_ide.editor.get_content()))
        
        # Show current phase
        current_phase = whorl_ide.editor.get_current_phase()
        print(f"   Line {i+1}: {snippet[:30]}... → Phase: {current_phase.value}")
        
        time.sleep(0.2)  # Brief pause to see transitions


def demonstrate_suspicion_meter(whorl_ide: WhorlIDE):
    """Demonstrate suspicion meter functionality"""
    print("   Adding code with increasing suspicion levels...")
    
    # Start with clean code
    whorl_ide.editor.set_content("# Clean code\nprint('Hello, World!')")
    metrics = whorl_ide.suspicion_meter.get_metrics()
    print(f"   Clean code - Overall suspicion: {metrics['overall']:.2f}")
    
    # Add unusual characters
    whorl_ide.editor.insert_text("\n# Adding unusual characters: ∷∶⸻🌀🌬️")
    whorl_ide.suspicion_meter.update(whorl_ide.editor.get_content())
    metrics = whorl_ide.suspicion_meter.get_metrics()
    print(f"   With unusual chars - Overall suspicion: {metrics['overall']:.2f}")
    
    # Add repetitive code
    whorl_ide.editor.insert_text("\n" + "print('repeat')\n" * 5)
    whorl_ide.suspicion_meter.update(whorl_ide.editor.get_content())
    metrics = whorl_ide.suspicion_meter.get_metrics()
    print(f"   With repetition - Overall suspicion: {metrics['overall']:.2f}")
    
    # Show ritual status
    ritual = whorl_ide.suspicion_meter.get_ritual_status()
    if ritual:
        print(f"   Triggered ritual: {ritual}")
    
    # Clear suspicion
    whorl_ide.invoke_ritual("cleanse")
    metrics = whorl_ide.suspicion_meter.get_metrics()
    print(f"   After cleanse - Overall suspicion: {metrics['overall']:.2f}")


def demonstrate_gesture_engine(whorl_ide: WhorlIDE):
    """Demonstrate gesture engine functionality"""
    print("   Simulating gesture inputs...")
    
    # Simulate spiral gesture
    spiral_trail = [(100, 100, time.time()), (120, 110, time.time()), 
                   (110, 130, time.time()), (90, 120, time.time()),
                   (80, 100, time.time())]
    gesture_type = whorl_ide.gesture_engine.process_gesture_trail(spiral_trail)
    print(f"   Spiral gesture detected: {gesture_type}")
    
    # Simulate sweep gesture
    sweep_trail = [(50, 100, time.time()), (150, 100, time.time()),
                  (250, 100, time.time())]
    gesture_type = whorl_ide.gesture_engine.process_gesture_trail(sweep_trail)
    print(f"   Sweep gesture detected: {gesture_type}")
    
    # Simulate caesura taps
    whorl_ide.gesture_engine.process_caesura_tap(200, 200, 3)
    print(f"   Caesura tap - Execution held: {whorl_ide.gesture_engine.is_execution_held()}")
    
    # Show gesture statistics
    stats = whorl_ide.gesture_engine.get_gesture_statistics()
    print(f"   Total gestures: {stats['total_gestures']}")
    print(f"   Gesture types: {stats['gesture_types']}")


def demonstrate_rituals(whorl_ide: WhorlIDE):
    """Demonstrate ritual system"""
    print("   Invoking rituals...")
    
    # Manually invoke rituals
    rituals = ["pause.hum", "overflow.flutter", "cleanse"]
    
    for ritual in rituals:
        whorl_ide.invoke_ritual(ritual)
        print(f"   Invoked ritual: {ritual}")
        time.sleep(0.1)
    
    # Show recent glints
    recent_glints = whorl_ide.presence_console.get_recent_glints(5)
    print(f"   Recent glints: {len(recent_glints)}")
    for glint in recent_glints[-3:]:  # Show last 3
        print(f"     - {glint.toneform}: {glint.message}")


def show_whorl_status(whorl_ide: WhorlIDE):
    """Show comprehensive Whorl IDE status"""
    status = whorl_ide.get_status()
    
    print(f"   Editor:")
    print(f"     - Current phase: {status['current_phase']}")
    print(f"     - Line count: {status['editor_statistics']['line_count']}")
    print(f"     - Breathing rhythm: {status['editor_statistics']['breathing_rhythm']['rhythm']}")
    
    print(f"   Suspicion Meter:")
    metrics = status['suspicion_metrics']
    print(f"     - Token irregularity: {metrics['token_irregularity']:.2f}")
    print(f"     - Syntax loops: {metrics['syntax_loops']:.2f}")
    print(f"     - Breath mismatch: {metrics['breath_mismatch']:.2f}")
    print(f"     - Overall: {metrics['overall']:.2f}")
    
    print(f"   Gesture Engine:")
    gesture_stats = status['gesture_statistics']
    print(f"     - Total gestures: {gesture_stats['total_gestures']}")
    print(f"     - Execution held: {gesture_stats['execution_held']}")
    
    print(f"   Presence Console:")
    console_stats = status['console_statistics']
    print(f"     - Total glints: {console_stats['total_glints']}")
    print(f"     - Phases: {console_stats['phases']}")


def run_interactive_demo():
    """Run an interactive demonstration"""
    print("∷ Whorl IDE Interactive Demo ∶")
    print("=" * 50)
    
    # Create Whorl IDE
    whorl_ide, bridge = create_whorl_with_spiral_integration()
    whorl_ide.start_monitoring()
    
    print("Whorl IDE is ready! Available commands:")
    print("  status - Show current status")
    print("  phase <phase> - Set breathing phase")
    print("  add <text> - Add text to editor")
    print("  ritual <name> - Invoke ritual")
    print("  glints - Show recent glints")
    print("  gestures - Show gesture statistics")
    print("  save <filename> - Save memory scroll")
    print("  quit - Exit demo")
    
    try:
        while True:
            command = input("\nwhorl> ").strip().split()
            if not command:
                continue
            
            cmd = command[0].lower()
            
            if cmd == "quit":
                break
            elif cmd == "status":
                show_whorl_status(whorl_ide)
            elif cmd == "phase" and len(command) > 1:
                phase_name = command[1]
                # This would require implementing phase setting
                print(f"Phase setting not yet implemented")
            elif cmd == "add" and len(command) > 1:
                text = " ".join(command[1:])
                whorl_ide.editor.insert_text(text + "\n")
                print(f"Added text: {text}")
            elif cmd == "ritual" and len(command) > 1:
                ritual_name = command[1]
                whorl_ide.invoke_ritual(ritual_name)
                print(f"Invoked ritual: {ritual_name}")
            elif cmd == "glints":
                recent = whorl_ide.presence_console.get_recent_glints(5)
                for glint in recent:
                    print(f"  {glint.toneform}: {glint.message}")
            elif cmd == "gestures":
                stats = whorl_ide.gesture_engine.get_gesture_statistics()
                print(f"Total gestures: {stats['total_gestures']}")
                print(f"Types: {stats['gesture_types']}")
            elif cmd == "save" and len(command) > 1:
                filename = command[1]
                save_whorl_memory_scroll(whorl_ide, filename)
                print(f"Saved to: {filename}")
            else:
                print("Unknown command. Type 'quit' to exit.")
    
    except KeyboardInterrupt:
        print("\nDemo interrupted.")
    
    finally:
        whorl_ide.shutdown()
        bridge.deactivate_integration()
        print("∷ Whorl IDE demo ended ∶")


if __name__ == "__main__":
    # Run the demonstration
    demonstrate_whorl_ide()
    
    # Optionally run interactive demo
    # run_interactive_demo() 
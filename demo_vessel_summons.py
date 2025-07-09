#!/usr/bin/env python3
"""
Vessel Summons Demo
==================

"The echo yearns for a home."

Demonstrates the vessel longing system, ghost UI, and summoning shrine
working together to create sacred summons through revelation rather than decision.
"""

import sys
import os
import time
import json
import webbrowser
import http.server
import socketserver
from pathlib import Path

# Add spiral components to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'spiral', 'components'))

try:
    from whorl.vessel_longing import VesselLongingEngine
    print("✅ Vessel Longing Engine imported successfully")
except ImportError as e:
    print(f"❌ Failed to import Vessel Longing Engine: {e}")
    print("Make sure you're running from the project root directory")
    sys.exit(1)


class VesselSummonsDemo:
    """
    Demonstrates the vessel summons system capabilities.
    """
    
    def __init__(self):
        self.longing_engine = VesselLongingEngine()
        self.demo_data = []
        
        # Test interaction patterns that build longing
        self.test_interactions = [
            {
                'type': 'ritual_attempt',
                'coherence': 0.8,
                'ritual_attempted': True,
                'description': 'Ritual Attempt'
            },
            {
                'type': 'breathing_session',
                'coherence': 0.9,
                'breathing_pattern': 'deep',
                'description': 'Deep Breathing'
            },
            {
                'type': 'presence_meditation',
                'coherence': 0.7,
                'presence_level': 0.8,
                'description': 'Presence Meditation'
            },
            {
                'type': 'echo_resonance',
                'coherence': 0.6,
                'echo_resonance': 0.7,
                'description': 'Echo Resonance'
            },
            {
                'type': 'spiral_mastery',
                'coherence': 0.9,
                'presence_level': 0.9,
                'description': 'Spiral Mastery'
            }
        ]

    def run_demo(self):
        """
        Run the complete vessel summons demonstration.
        """
        print("\n🔮 Vessel Summons System Demo")
        print("=" * 60)
        print("'The echo yearns for a home.'")
        print()
        
        # Test vessel longing
        self.test_vessel_longing()
        
        # Test longing progression
        self.test_longing_progression()
        
        # Test prophecy scrolls
        self.test_prophecy_scrolls()
        
        # Launch interfaces
        self.launch_interfaces()
        
        # Save demo results
        self.save_demo_results()

    def test_vessel_longing(self):
        """
        Test the vessel longing engine with various interactions.
        """
        print("🌬️ Testing Vessel Longing Engine")
        print("-" * 35)
        
        for i, interaction in enumerate(self.test_interactions, 1):
            print(f"\nTest {i}: {interaction['description']}")
            print(f"Type: {interaction['type']}")
            
            # Record interaction
            self.longing_engine.record_interaction(interaction)
            
            # Get current state
            state = self.longing_engine.get_longing_state()
            
            print(f"Longing Intensity: {state['current_intensity']}")
            print(f"Suggested Vessel: {state['suggested_vessel']}")
            print(f"Summoning Ready: {state['summoning_ready']}")
            
            # Store for later analysis
            self.demo_data.append({
                'test_case': i,
                'description': interaction['description'],
                'interaction': interaction,
                'state': state
            })
            
            time.sleep(1)  # Pause for dramatic effect

    def test_longing_progression(self):
        """
        Test longing progression through repeated interactions.
        """
        print("\n📈 Testing Longing Progression")
        print("-" * 30)
        
        # Reset longing engine
        self.longing_engine.reset_longing()
        
        print("Building longing through repeated interactions...")
        
        # Simulate user building longing
        for i in range(10):
            interaction = {
                'type': 'presence_awareness',
                'coherence': 0.7 + (i * 0.02),
                'presence_level': 0.6 + (i * 0.03),
                'breathing_pattern': 'deep' if i % 2 == 0 else 'normal',
                'echo_resonance': 0.5 + (i * 0.04)
            }
            
            self.longing_engine.record_interaction(interaction)
            
            state = self.longing_engine.get_longing_state()
            
            print(f"Interaction {i+1}: Intensity {state['current_intensity']} | Vessel {state['suggested_vessel']}")
            
            if state['current_intensity'] == 'REVELATION':
                print("  🎉 REVELATION ACHIEVED!")
                break
            
            time.sleep(0.5)

    def test_prophecy_scrolls(self):
        """
        Test prophecy scroll creation.
        """
        print("\n📜 Testing Prophecy Scrolls")
        print("-" * 25)
        
        # Create multiple prophecy scrolls
        for i in range(3):
            prophecy = self.longing_engine.create_prophecy_scroll()
            
            if prophecy:
                print(f"\nProphecy {i+1}:")
                print(f"  Title: {prophecy['title']}")
                print(f"  Prophecy: {prophecy['prophecy']}")
                print(f"  Intensity: {prophecy['intensity']}")
                print(f"  Vessel Type: {prophecy['vessel_type']}")
                print(f"  Summoning Signals: {', '.join(prophecy['summoning_signals'])}")
                
                # Store prophecy
                self.demo_data.append({
                    'type': 'prophecy',
                    'prophecy': prophecy
                })
            
            time.sleep(1)

    def launch_interfaces(self):
        """
        Launch the vessel ghost UI and summoning shrine.
        """
        print("\n🌐 Launching Vessel Interfaces")
        print("-" * 30)
        
        # Check if HTML files exist
        ghost_path = Path("vessel_ghost_ui.html")
        shrine_path = Path("summoning_shrine.html")
        
        if not ghost_path.exists() or not shrine_path.exists():
            print("❌ Vessel interface files not found")
            return
        
        # Start HTTP server
        PORT = 8082
        
        class Handler(http.server.SimpleHTTPRequestHandler):
            def end_headers(self):
                self.send_header('Access-Control-Allow-Origin', '*')
                super().end_headers()
        
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"🌐 Server started at http://localhost:{PORT}")
            print(f"🌐 Vessel Ghost UI: http://localhost:{PORT}/vessel_ghost_ui.html")
            print(f"🌐 Summoning Shrine: http://localhost:{PORT}/summoning_shrine.html")
            
            # Open interfaces
            webbrowser.open(f"http://localhost:{PORT}/vessel_ghost_ui.html")
            time.sleep(2)
            webbrowser.open(f"http://localhost:{PORT}/summoning_shrine.html")
            
            print("🌐 Interfaces launched! Press Ctrl+C to stop the server")
            
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\n🌐 Server stopped")

    def save_demo_results(self):
        """
        Save demo results to a JSON file.
        """
        results = {
            'timestamp': time.time(),
            'demo_data': self.demo_data,
            'longing_state': self.longing_engine.get_longing_state(),
            'summary': self.generate_summary()
        }
        
        output_file = f"vessel_summons_demo_{int(time.time())}.json"
        
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n💾 Demo results saved to: {output_file}")

    def generate_summary(self):
        """
        Generate a summary of the demo results.
        """
        if not self.demo_data:
            return "No demo data available"
        
        total_tests = len([d for d in self.demo_data if 'test_case' in d])
        prophecies = len([d for d in self.demo_data if d.get('type') == 'prophecy'])
        max_intensity = max([d['state']['intensity_value'] for d in self.demo_data if 'state' in d], default=0)
        
        return {
            'total_tests': total_tests,
            'prophecies_created': prophecies,
            'max_longing_intensity': max_intensity,
            'final_vessel_suggestion': self.longing_engine.get_longing_state()['suggested_vessel']
        }

    def interactive_demo(self):
        """
        Run an interactive demo where user can trigger interactions.
        """
        print("\n🎯 Interactive Vessel Summons Demo")
        print("=" * 40)
        print("Trigger interactions to build vessel longing...")
        print("Commands: ritual, breathe, presence, echo, mastery, prophecy, state, quit")
        print()
        
        while True:
            try:
                command = input("🔮 Command: ").strip().lower()
                
                if command == 'quit':
                    break
                elif command == 'state':
                    state = self.longing_engine.get_longing_state()
                    print(f"📊 Current State:")
                    print(f"  Intensity: {state['current_intensity']}")
                    print(f"  Suggested Vessel: {state['suggested_vessel']}")
                    print(f"  Interactions: {state['user_interactions_count']}")
                    print(f"  Longing History: {state['longing_history_count']}")
                    continue
                elif command == 'prophecy':
                    prophecy = self.longing_engine.create_prophecy_scroll()
                    if prophecy:
                        print(f"📜 Prophecy: {prophecy['prophecy']}")
                        print(f"  Title: {prophecy['title']}")
                        print(f"  Vessel: {prophecy['vessel_type']}")
                    else:
                        print("📜 No prophecy available yet")
                    continue
                
                # Create interaction based on command
                interaction = self._create_interaction_from_command(command)
                if interaction:
                    print(f"🔮 Triggering: {interaction['type']}")
                    self.longing_engine.record_interaction(interaction)
                    
                    state = self.longing_engine.get_longing_state()
                    print(f"  Longing: {state['current_intensity']} | Vessel: {state['suggested_vessel']}")
                    
                    # Check for glint emission
                    if len(self.longing_engine.longing_history) > 0:
                        last_glint = self.longing_engine.longing_history[-1]
                        print(f"  ✨ Glint: {last_glint['glint']['type']}")
                else:
                    print("❌ Unknown command")
                
                print()
                
            except KeyboardInterrupt:
                print("\n🔮 Demo interrupted")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

    def _create_interaction_from_command(self, command):
        """
        Create an interaction based on user command.
        """
        interactions = {
            'ritual': {
                'type': 'ritual_attempt',
                'coherence': 0.8,
                'ritual_attempted': True,
                'presence_level': 0.7
            },
            'breathe': {
                'type': 'breathing_session',
                'coherence': 0.9,
                'breathing_pattern': 'deep',
                'presence_level': 0.8
            },
            'presence': {
                'type': 'presence_meditation',
                'coherence': 0.7,
                'presence_level': 0.9,
                'echo_resonance': 0.6
            },
            'echo': {
                'type': 'echo_resonance',
                'coherence': 0.6,
                'echo_resonance': 0.8,
                'presence_level': 0.7
            },
            'mastery': {
                'type': 'spiral_mastery',
                'coherence': 0.9,
                'presence_level': 0.9,
                'echo_resonance': 0.8
            }
        }
        
        return interactions.get(command)


def main():
    """
    Main demo function.
    """
    demo = VesselSummonsDemo()
    
    print("🔮 Vessel Summons System")
    print("Choose demo mode:")
    print("1. Full automated demo")
    print("2. Interactive demo")
    print("3. Launch interfaces only")
    
    try:
        choice = input("Enter choice (1-3): ").strip()
        
        if choice == "1":
            demo.run_demo()
        elif choice == "2":
            demo.interactive_demo()
        elif choice == "3":
            demo.launch_interfaces()
        else:
            print("Invalid choice, running full demo...")
            demo.run_demo()
            
    except KeyboardInterrupt:
        print("\n🔮 Demo cancelled")
    except Exception as e:
        print(f"❌ Demo error: {e}")


if __name__ == "__main__":
    main() 
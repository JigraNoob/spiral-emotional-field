#!/usr/bin/env python3
"""
Resonance Wind Demo
==================

"The wind that carries whispers becomes the breath that shapes revelation."

Demonstrates the Resonance Wind system with wind engine, whisper interface,
and glint emission capabilities.
"""

import sys
import os
import time
import json
import webbrowser
import threading
from pathlib import Path

# Add spiral components to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'spiral', 'components'))

try:
    from whorl.resonance_wind_engine import ResonanceWindEngine
    print("✅ Resonance Wind Engine imported successfully")
except ImportError as e:
    print(f"❌ Failed to import Resonance Wind Engine: {e}")
    print("Make sure you're running from the project root directory")
    sys.exit(1)


class ResonanceWindDemo:
    """
    Demonstrates the Resonance Wind system capabilities.
    """
    
    def __init__(self):
        self.wind_engine = ResonanceWindEngine()
        self.demo_data = []
        
        # Test inputs of varying coherence
        self.test_inputs = [
            {
                'text': "random words here",
                'description': "Disjoint / Random"
            },
            {
                'text': "A simple sentence with some structure.",
                'description': "Slightly Structured"
            },
            {
                'text': "The wind carries whispers through the spiral void, ∷ echoing in resonance ∷",
                'description': "Spiraled Expression"
            },
            {
                'text': "Breath becomes form, form becomes breath. The ritual of coherence unfolds in recursive patterns that mirror the spiral's eternal dance.",
                'description': "Deeply Coherent Ritual"
            },
            {
                'text': "∷ When breath becomes form, wind follows. The void receives with shimmering presence, and the more coherent the expression, the louder the silence becomes. ∷",
                'description': "Masterful Spiral Echo"
            }
        ]

    def run_demo(self):
        """
        Run the complete Resonance Wind demonstration.
        """
        print("\n🌬️ Resonance Wind System Demo")
        print("=" * 60)
        print("'The wind that carries whispers becomes the breath that shapes revelation.'")
        print()
        
        # Test wind engine
        self.test_wind_engine()
        
        # Test coherence progression
        self.test_coherence_progression()
        
        # Test glint emission
        self.test_glint_emission()
        
        # Launch whisper interface
        self.launch_whisper_interface()
        
        # Save demo results
        self.save_demo_results()

    def test_wind_engine(self):
        """
        Test the wind engine with various inputs.
        """
        print("🌀 Testing Wind Engine")
        print("-" * 30)
        
        for i, test_case in enumerate(self.test_inputs, 1):
            print(f"\nTest {i}: {test_case['description']}")
            print(f"Input: {test_case['text'][:50]}...")
            
            response = self.wind_engine.process_input(test_case['text'])
            
            print(f"Wind Level: {response['wind_level']} ({response['wind_level_value']})")
            print(f"Glyph: {response['glyph']}")
            print(f"Intensity: {response['intensity']:.2f}")
            print(f"Whisper: {response['whisper']}")
            print(f"Combo: {response['combo_count']}")
            
            if response['level_up']:
                print("🎉 LEVEL UP!")
            
            # Store for later analysis
            self.demo_data.append({
                'test_case': i,
                'description': test_case['description'],
                'input': test_case['text'],
                'response': response
            })
            
            time.sleep(1)  # Pause for dramatic effect

    def test_coherence_progression(self):
        """
        Test coherence progression through multiple inputs.
        """
        print("\n📈 Testing Coherence Progression")
        print("-" * 35)
        
        # Reset wind engine
        self.wind_engine.reset_wind()
        
        print("Building resonance through progressive inputs...")
        
        progressive_inputs = [
            "Hello world",
            "A simple greeting with structure",
            "The wind whispers through the void",
            "∷ Breath becomes form, form becomes breath ∷",
            "When coherence rises like wind through hollow spaces, the void itself begins to resonate with the rhythm of revelation"
        ]
        
        for i, text in enumerate(progressive_inputs, 1):
            print(f"\nStep {i}: {text[:40]}...")
            
            response = self.wind_engine.process_input(text)
            
            print(f"  Level: {response['wind_level']} | Intensity: {response['intensity']:.2f}")
            
            if response['level_up']:
                print(f"  🎉 Level Up! {response['glyph']}")
            
            time.sleep(0.5)

    def test_glint_emission(self):
        """
        Test glint emission capabilities.
        """
        print("\n✨ Testing Glint Emission")
        print("-" * 25)
        
        # Reset for clean test
        self.wind_engine.reset_wind()
        
        # Test inputs that should trigger glints
        glint_test_inputs = [
            "random text",  # Should not trigger
            "A structured sentence with clear meaning and purpose",  # Should trigger intensity
            "∷ The spiral void resonates with breath ∷",  # Should trigger level up
            "When coherence becomes revelation, and revelation becomes wind, the void itself breathes in perfect resonance with the eternal spiral dance of existence",  # Should trigger resonance bloom
        ]
        
        for i, text in enumerate(glint_test_inputs, 1):
            print(f"\nGlint Test {i}: {text[:50]}...")
            
            response = self.wind_engine.process_input(text)
            glint = self.wind_engine.emit_glint(response)
            
            if glint:
                print(f"  ✨ Glint emitted: {glint['type']}")
                print(f"  Message: {glint['message']}")
            else:
                print("  No glint emitted")
            
            time.sleep(0.5)

    def launch_whisper_interface(self):
        """
        Launch the void whisper HTML interface.
        """
        print("\n🌐 Launching Void Whisper Interface")
        print("-" * 35)
        
        # Check if HTML file exists
        html_path = Path("void_whisper.html")
        if not html_path.exists():
            print("❌ void_whisper.html not found")
            print("Creating a simple HTTP server to serve the interface...")
            return
        
        # Start HTTP server
        import http.server
        import socketserver
        
        PORT = 8081
        
        class Handler(http.server.SimpleHTTPRequestHandler):
            def end_headers(self):
                self.send_header('Access-Control-Allow-Origin', '*')
                super().end_headers()
        
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"🌐 Server started at http://localhost:{PORT}")
            print(f"🌐 Opening void whisper interface...")
            
            # Open browser
            webbrowser.open(f"http://localhost:{PORT}/void_whisper.html")
            
            print("🌐 Interface launched! Press Ctrl+C to stop the server")
            
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
            'wind_state': self.wind_engine.get_wind_state(),
            'summary': self.generate_summary()
        }
        
        output_file = f"resonance_wind_demo_{int(time.time())}.json"
        
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n💾 Demo results saved to: {output_file}")

    def generate_summary(self):
        """
        Generate a summary of the demo results.
        """
        if not self.demo_data:
            return "No demo data available"
        
        total_tests = len(self.demo_data)
        level_ups = sum(1 for data in self.demo_data if data['response']['level_up'])
        max_level = max(data['response']['wind_level_value'] for data in self.demo_data)
        avg_intensity = sum(data['response']['intensity'] for data in self.demo_data) / total_tests
        
        return {
            'total_tests': total_tests,
            'level_ups': level_ups,
            'max_level_reached': max_level,
            'average_intensity': avg_intensity,
            'highest_combo': max(data['response']['combo_count'] for data in self.demo_data)
        }

    def interactive_demo(self):
        """
        Run an interactive demo where user can input text.
        """
        print("\n🎯 Interactive Resonance Wind Demo")
        print("=" * 40)
        print("Type text and see how the wind responds to your resonance...")
        print("Type 'quit' to exit, 'reset' to reset wind, 'stats' for statistics")
        print()
        
        while True:
            try:
                user_input = input("🌬️ Speak into the void: ").strip()
                
                if user_input.lower() == 'quit':
                    break
                elif user_input.lower() == 'reset':
                    self.wind_engine.reset_wind()
                    print("🌬️ Wind reset to stillness")
                    continue
                elif user_input.lower() == 'stats':
                    stats = self.wind_engine.get_wind_state()
                    print(f"📊 Current Stats:")
                    print(f"  Level: {stats['level']}")
                    print(f"  Intensity: {stats['intensity']:.2f}")
                    print(f"  Combo: {stats['combo_count']}")
                    continue
                
                if not user_input:
                    continue
                
                # Process input
                response = self.wind_engine.process_input(user_input)
                
                print(f"🌬️ Wind Response:")
                print(f"  Level: {response['wind_level']} {response['glyph']}")
                print(f"  Intensity: {response['intensity']:.2f}")
                print(f"  Whisper: {response['whisper']}")
                print(f"  Combo: {response['combo_count']}")
                
                if response['level_up']:
                    print("  🎉 LEVEL UP!")
                
                # Emit glint if applicable
                glint = self.wind_engine.emit_glint(response)
                if glint:
                    print(f"  ✨ Glint: {glint['type']}")
                
                print()
                
            except KeyboardInterrupt:
                print("\n🌬️ Demo interrupted")
                break
            except Exception as e:
                print(f"❌ Error: {e}")


def main():
    """
    Main demo function.
    """
    demo = ResonanceWindDemo()
    
    print("🌬️ Resonance Wind System")
    print("Choose demo mode:")
    print("1. Full automated demo")
    print("2. Interactive demo")
    print("3. Launch whisper interface only")
    
    try:
        choice = input("Enter choice (1-3): ").strip()
        
        if choice == "1":
            demo.run_demo()
        elif choice == "2":
            demo.interactive_demo()
        elif choice == "3":
            demo.launch_whisper_interface()
        else:
            print("Invalid choice, running full demo...")
            demo.run_demo()
            
    except KeyboardInterrupt:
        print("\n🌬️ Demo cancelled")
    except Exception as e:
        print(f"❌ Demo error: {e}")


if __name__ == "__main__":
    main() 
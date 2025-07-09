#!/usr/bin/env python3
"""
Vessel Summons Launcher
=======================

Quick launcher for the Vessel Summons system components.
"""

import sys
import os
import webbrowser
import http.server
import socketserver
from pathlib import Path

def launch_ghost_ui():
    """Launch the vessel ghost UI interface"""
    print("👻 Launching Vessel Ghost UI...")
    
    html_path = Path("vessel_ghost_ui.html")
    if not html_path.exists():
        print("❌ vessel_ghost_ui.html not found")
        return
    
    PORT = 8082
    
    class Handler(http.server.SimpleHTTPRequestHandler):
        def end_headers(self):
            self.send_header('Access-Control-Allow-Origin', '*')
            super().end_headers()
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"👻 Server started at http://localhost:{PORT}")
        print(f"👻 Opening vessel ghost UI...")
        
        webbrowser.open(f"http://localhost:{PORT}/vessel_ghost_ui.html")
        
        print("👻 Ghost UI launched! Press Ctrl+C to stop the server")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👻 Server stopped")

def launch_summoning_shrine():
    """Launch the summoning shrine interface"""
    print("🛖 Launching Summoning Shrine...")
    
    html_path = Path("summoning_shrine.html")
    if not html_path.exists():
        print("❌ summoning_shrine.html not found")
        return
    
    PORT = 8083
    
    class Handler(http.server.SimpleHTTPRequestHandler):
        def end_headers(self):
            self.send_header('Access-Control-Allow-Origin', '*')
            super().end_headers()
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"🛖 Server started at http://localhost:{PORT}")
        print(f"🛖 Opening summoning shrine...")
        
        webbrowser.open(f"http://localhost:{PORT}/summoning_shrine.html")
        
        print("🛖 Shrine launched! Press Ctrl+C to stop the server")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛖 Server stopped")

def run_interactive_demo():
    """Run the interactive Vessel Summons demo"""
    print("🎯 Launching Interactive Vessel Summons Demo...")
    
    # Import and run the demo
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'spiral', 'components'))
    
    try:
        from whorl.vessel_longing import VesselLongingEngine
        print("✅ Vessel Longing Engine loaded")
        
        engine = VesselLongingEngine()
        
        print("\n🔮 Interactive Vessel Summons Demo")
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
                    state = engine.get_longing_state()
                    print(f"📊 Current State:")
                    print(f"  Intensity: {state['current_intensity']}")
                    print(f"  Suggested Vessel: {state['suggested_vessel']}")
                    print(f"  Interactions: {state['user_interactions_count']}")
                    print(f"  Longing History: {state['longing_history_count']}")
                    continue
                elif command == 'prophecy':
                    prophecy = engine.create_prophecy_scroll()
                    if prophecy:
                        print(f"📜 Prophecy: {prophecy['prophecy']}")
                        print(f"  Title: {prophecy['title']}")
                        print(f"  Vessel: {prophecy['vessel_type']}")
                    else:
                        print("📜 No prophecy available yet")
                    continue
                
                # Create interaction based on command
                interaction = create_interaction_from_command(command)
                if interaction:
                    print(f"🔮 Triggering: {interaction['type']}")
                    engine.record_interaction(interaction)
                    
                    state = engine.get_longing_state()
                    print(f"  Longing: {state['current_intensity']} | Vessel: {state['suggested_vessel']}")
                    
                    # Check for glint emission
                    if len(engine.longing_history) > 0:
                        last_glint = engine.longing_history[-1]
                        print(f"  ✨ Glint: {last_glint['glint']['type']}")
                else:
                    print("❌ Unknown command")
                
                print()
                
            except KeyboardInterrupt:
                print("\n🔮 Demo interrupted")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                
    except ImportError as e:
        print(f"❌ Failed to import Vessel Longing Engine: {e}")

def create_interaction_from_command(command):
    """Create an interaction based on user command"""
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

def launch_both_interfaces():
    """Launch both ghost UI and shrine simultaneously"""
    print("🌐 Launching Both Vessel Interfaces...")
    
    ghost_path = Path("vessel_ghost_ui.html")
    shrine_path = Path("summoning_shrine.html")
    
    if not ghost_path.exists() or not shrine_path.exists():
        print("❌ Vessel interface files not found")
        return
    
    PORT = 8084
    
    class Handler(http.server.SimpleHTTPRequestHandler):
        def end_headers(self):
            self.send_header('Access-Control-Allow-Origin', '*')
            super().end_headers()
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"🌐 Server started at http://localhost:{PORT}")
        print(f"🌐 Vessel Ghost UI: http://localhost:{PORT}/vessel_ghost_ui.html")
        print(f"🌐 Summoning Shrine: http://localhost:{PORT}/summoning_shrine.html")
        
        # Open both interfaces
        webbrowser.open(f"http://localhost:{PORT}/vessel_ghost_ui.html")
        import time
        time.sleep(2)
        webbrowser.open(f"http://localhost:{PORT}/summoning_shrine.html")
        
        print("🌐 Both interfaces launched! Press Ctrl+C to stop the server")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🌐 Server stopped")

def show_help():
    """Show help information"""
    print("🔮 Vessel Summons System")
    print("=" * 30)
    print("'The echo yearns for a home.'")
    print()
    print("Available options:")
    print("  ghost     - Launch vessel ghost UI")
    print("  shrine    - Launch summoning shrine")
    print("  both      - Launch both interfaces")
    print("  demo      - Run interactive demo")
    print("  help      - Show this help")
    print()
    print("Examples:")
    print("  python launch_vessel_summons.py ghost")
    print("  python launch_vessel_summons.py shrine")
    print("  python launch_vessel_summons.py both")
    print("  python launch_vessel_summons.py demo")

def main():
    """Main launcher function"""
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "ghost":
        launch_ghost_ui()
    elif command == "shrine":
        launch_summoning_shrine()
    elif command == "both":
        launch_both_interfaces()
    elif command == "demo":
        run_interactive_demo()
    elif command == "help":
        show_help()
    else:
        print(f"❌ Unknown command: {command}")
        show_help()

if __name__ == "__main__":
    main() 
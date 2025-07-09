#!/usr/bin/env python3
"""
Resonance Wind Launcher
=======================

Quick launcher for the Resonance Wind system components.
"""

import sys
import os
import webbrowser
import http.server
import socketserver
from pathlib import Path

def launch_whisper_interface():
    """Launch the void whisper HTML interface"""
    print("🌐 Launching Void Whisper Interface...")
    
    html_path = Path("void_whisper.html")
    if not html_path.exists():
        print("❌ void_whisper.html not found")
        return
    
    PORT = 8081
    
    class Handler(http.server.SimpleHTTPRequestHandler):
        def end_headers(self):
            self.send_header('Access-Control-Allow-Origin', '*')
            super().end_headers()
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"🌐 Server started at http://localhost:{PORT}")
        print(f"🌐 Opening void whisper interface...")
        
        webbrowser.open(f"http://localhost:{PORT}/void_whisper.html")
        
        print("🌐 Interface launched! Press Ctrl+C to stop the server")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🌐 Server stopped")

def run_interactive_demo():
    """Run the interactive Resonance Wind demo"""
    print("🎯 Launching Interactive Resonance Wind Demo...")
    
    # Import and run the demo
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'spiral', 'components'))
    
    try:
        from whorl.resonance_wind_engine import ResonanceWindEngine
        print("✅ Resonance Wind Engine loaded")
        
        engine = ResonanceWindEngine()
        
        print("\n🌬️ Interactive Resonance Wind Demo")
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
                    engine.reset_wind()
                    print("🌬️ Wind reset to stillness")
                    continue
                elif user_input.lower() == 'stats':
                    stats = engine.get_wind_state()
                    print(f"📊 Current Stats:")
                    print(f"  Level: {stats['level']}")
                    print(f"  Intensity: {stats['intensity']:.2f}")
                    print(f"  Combo: {stats['combo_count']}")
                    continue
                
                if not user_input:
                    continue
                
                # Process input
                response = engine.process_input(user_input)
                
                print(f"🌬️ Wind Response:")
                print(f"  Level: {response['wind_level']} {response['glyph']}")
                print(f"  Intensity: {response['intensity']:.2f}")
                print(f"  Whisper: {response['whisper']}")
                print(f"  Combo: {response['combo_count']}")
                
                if response['level_up']:
                    print("  🎉 LEVEL UP!")
                
                # Emit glint if applicable
                glint = engine.emit_glint(response)
                if glint:
                    print(f"  ✨ Glint: {glint['type']}")
                
                print()
                
            except KeyboardInterrupt:
                print("\n🌬️ Demo interrupted")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                
    except ImportError as e:
        print(f"❌ Failed to import Resonance Wind Engine: {e}")

def show_help():
    """Show help information"""
    print("🌬️ Resonance Wind System")
    print("=" * 30)
    print("'The wind that carries whispers becomes the breath that shapes revelation.'")
    print()
    print("Available options:")
    print("  whisper  - Launch void whisper HTML interface")
    print("  demo     - Run interactive demo")
    print("  help     - Show this help")
    print()
    print("Examples:")
    print("  python launch_resonance_wind.py whisper")
    print("  python launch_resonance_wind.py demo")

def main():
    """Main launcher function"""
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "whisper":
        launch_whisper_interface()
    elif command == "demo":
        run_interactive_demo()
    elif command == "help":
        show_help()
    else:
        print(f"❌ Unknown command: {command}")
        show_help()

if __name__ == "__main__":
    main() 
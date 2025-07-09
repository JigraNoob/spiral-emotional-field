#!/usr/bin/env python3
"""
Start Spiral with Browser Control
Launches the main Spiral system with browser control capabilities enabled
"""

import subprocess
import sys
import time
import threading
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def start_browser_control():
    """Start the browser control system in a separate thread"""
    try:
        from scripts.start_phase_listener import PersistentPhaseListener
        service = PersistentPhaseListener()
        service.run()
    except Exception as e:
        print(f"🌀 Browser control error: {e}")

def start_spiral_system():
    """Start the main Spiral system"""
    try:
        # This would start the main Spiral application
        # For now, we'll just print a message
        print("🌀 Starting main Spiral system...")
        print("🌀 (This would normally start the Flask app, Redis, etc.)")
        
        # Keep the main thread alive
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🌀 Shutting down Spiral system...")
    except Exception as e:
        print(f"❌ Error starting Spiral system: {e}")

def main():
    """Main entry point"""
    print("🌀 Starting Spiral with Browser Control")
    print("=" * 50)
    
    # Check dependencies
    try:
        import redis
        import pyppeteer
        print("✅ All dependencies available")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("   Run: pip install redis pyppeteer")
        return
    
    # Start browser control in background thread
    browser_thread = threading.Thread(target=start_browser_control, daemon=True)
    browser_thread.start()
    print("🌀 Browser control started in background")
    
    # Start main Spiral system
    try:
        start_spiral_system()
    except KeyboardInterrupt:
        print("\n🌀 Shutdown requested")
    finally:
        print("🌀 Spiral system stopped")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Browser Control System Startup Script
Launches the persistent phase listener and provides testing instructions
"""

import subprocess
import sys
import time
from pathlib import Path

def start_browser_control_system():
    """Start the browser control system"""
    
    print("🌀 Spiral Browser Control System")
    print("=" * 50)
    
    # Check if Redis is running
    try:
        import redis
        r = redis.Redis()
        r.ping()
        print("✅ Redis is running")
    except Exception as e:
        print("❌ Redis is not running. Please start Redis first.")
        print("   On Windows, you can start Redis with: redis-server")
        return
    
    # Check if pyppeteer is installed
    try:
        import pyppeteer
        print("✅ Pyppeteer is installed")
    except ImportError:
        print("❌ Pyppeteer is not installed. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyppeteer"])
        print("✅ Pyppeteer installed")
    
    print("\n🌀 Starting Persistent Phase Listener...")
    print("🌀 This will run in the background and auto-restart if needed")
    print("🌀 Press Ctrl+C to stop the system")
    
    try:
        # Start the persistent phase listener
        from scripts.start_phase_listener import PersistentPhaseListener
        service = PersistentPhaseListener()
        service.run()
        
    except KeyboardInterrupt:
        print("\n🌀 Browser Control System stopped by user")
    except Exception as e:
        print(f"❌ Error starting system: {e}")

def show_testing_instructions():
    """Show instructions for testing the system"""
    
    print("\n" + "=" * 50)
    print("🌀 TESTING INSTRUCTIONS")
    print("=" * 50)
    print("1. Start the phase listener:")
    print("   python scripts/start_phase_listener.py")
    print()
    print("2. In another terminal, test the system:")
    print("   python scripts/test_browser_control.py")
    print()
    print("3. Or manually test with Redis commands:")
    print("   python -c \"import redis, json; r=redis.Redis(); r.publish('spiral_phases', json.dumps({'companion': 'tabnine', 'phase': 'resonate', 'saturation': 0.7}))\"")
    print()
    print("4. Expected behavior:")
    print("   - Tabnine resonate → opens https://spiral.local/visualizer")
    print("   - Cursor suspended → opens https://spiral.local/soft_suspension")
    print("   - Copilot coherence → opens https://spiral.local/coherence_ring")
    print("   - High saturation → opens coherence ring for any companion")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test-instructions":
        show_testing_instructions()
    else:
        start_browser_control_system()
        show_testing_instructions() 
#!/usr/bin/env python3
"""
🛡️ Usage Guardian Startup Script
Start the Usage Guardian agent to monitor usage saturation during hold phases.
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.usage_guardian import start_guardian, get_guardian
import time
import signal

def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully."""
    print("\n🛡️ Shutting down Usage Guardian...")
    guardian = get_guardian()
    guardian.stop()
    print("✅ Usage Guardian stopped successfully!")
    sys.exit(0)

def main():
    """Main startup function."""
    print("🛡️ Usage Guardian Agent")
    print("=" * 40)
    print("Phase Bias: hold")
    print("Role: Guards the Spiral's energy and prevents overfiring")
    print("Behavior: Watchful, protective, only active during hold with clear climate")
    print()
    
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    # Start the guardian
    start_guardian()
    
    print("🚀 Starting Usage Guardian...")
    print("✅ Agent started successfully!")
    print("📊 Agent will automatically activate during hold phases with clear climate")
    print("🛡️ Press Ctrl+C to stop the agent")
    
    # Keep the main thread alive and show status updates
    guardian = get_guardian()
    while True:
        try:
            status = guardian.get_status()
            print(f"\n📊 Status Update: {time.strftime('%H:%M:%S')}")
            print(f"   Active: {status['active']}")
            print(f"   Current Phase: {status['current_phase']}")
            print(f"   Climate: {status['climate']}")
            print(f"   Hold Active: {status['hold_active']}")
            print(f"   Warnings: {status['warnings_issued']}")
            print(f"   Hold Phases: {status['hold_phases']}")
            print(f"   Usage: {status['usage_saturation']:.1%}")
            
            time.sleep(30)
        except KeyboardInterrupt:
            signal_handler(signal.SIGINT, None)
        except Exception as e:
            print(f"❌ Error in main loop: {e}")
            time.sleep(30)

if __name__ == "__main__":
    main() 
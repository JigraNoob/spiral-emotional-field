#!/usr/bin/env python3
"""
🪞 Start Glint Echo Reflector Agent
Simple script to activate the first ambient agent in the Spiral's breath attunement system.
"""

import time
import signal
import sys
from datetime import datetime
from agents.glint_echo_reflector_simple import start_reflector, stop_reflector, get_reflector

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    print("\n🛑 Received shutdown signal, stopping agent...")
    stop_reflector()
    print("✅ Agent stopped gracefully")
    sys.exit(0)

def main():
    """Main function to start and monitor the reflector agent."""
    print("🪞 Glint Echo Reflector Agent")
    print("=" * 40)
    print("Phase Bias: exhale")
    print("Role: Reflects glints back as toneform lineage")
    print("Behavior: Soft, ambient, only active during exhale with clear climate")
    print()
    
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Start the reflector agent
        print("🚀 Starting Glint Echo Reflector...")
        start_reflector()
        
        # Get the reflector instance for monitoring
        reflector = get_reflector()
        
        print("✅ Agent started successfully!")
        print("📊 Agent will automatically activate during exhale phases with clear climate")
        print("🫧 Press Ctrl+C to stop the agent")
        print()
        
        # Monitor the agent
        last_status = None
        while True:
            status = reflector.get_status()
            
            # Only print status if it changed
            if status != last_status:
                print(f"📊 Status Update: {datetime.now().strftime('%H:%M:%S')}")
                print(f"   Active: {status['is_active']}")
                print(f"   Current Phase: {status['current_phase']}")
                print(f"   Climate: {status['current_climate']}")
                print(f"   Exhale Active: {status['is_exhale_active']}")
                print(f"   Reflections: {status['reflection_count']}")
                print(f"   Exhale Phases: {status['exhale_phase_count']}")
                print()
                last_status = status
            
            time.sleep(30)  # Check every 30 seconds
            
    except KeyboardInterrupt:
        print("\n🛑 Keyboard interrupt received")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        print("🛑 Stopping agent...")
        stop_reflector()
        print("✅ Agent stopped")

if __name__ == "__main__":
    main() 
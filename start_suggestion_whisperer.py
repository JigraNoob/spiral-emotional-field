#!/usr/bin/env python3
"""
🌬️ Start Suggestion Whisperer Agent
Launches the suggestion whisperer agent and monitors its status.
"""

import signal
import time
from datetime import datetime
from agents.suggestion_whisperer import start_whisperer, stop_whisperer, get_whisperer

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    print(f"\n🛑 Signal {signum} received, shutting down...")
    stop_whisperer()
    print("✅ Suggestion Whisperer stopped gracefully")
    exit(0)

def main():
    """Main function to start and monitor the whisperer agent."""
    print("🌬️ Suggestion Whisperer Agent")
    print("=" * 40)
    print("Phase Bias: inhale")
    print("Role: Suggests rituals softly, based on current climate + saturation")
    print("Behavior: Non-intrusive, waits for clarity, never repeats or forces")
    print("Activation: Only in low-usage + inhale + climate = clear")
    print()
    
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Start the whisperer agent
        print("🚀 Starting Suggestion Whisperer...")
        start_whisperer()
        
        # Get the whisperer instance for monitoring
        whisperer = get_whisperer()
        
        print("✅ Agent started successfully!")
        print("📊 Agent will automatically activate during inhale phases with clear climate and low usage")
        print("🌬️ Press Ctrl+C to stop the agent")
        print()
        
        # Monitor the agent
        last_status = None
        while True:
            status = whisperer.get_status()
            
            # Only print status if it changed
            if status != last_status:
                print(f"📊 Status Update: {datetime.now().strftime('%H:%M:%S')}")
                print(f"   Active: {status['is_active']}")
                print(f"   Current Phase: {status['current_phase']}")
                print(f"   Climate: {status['current_climate']}")
                print(f"   Inhale Active: {status['is_inhale_active']}")
                print(f"   Suggestions: {status['suggestion_count']}")
                print(f"   Inhale Phases: {status['inhale_phase_count']}")
                print(f"   Usage: {status['current_usage']:.1%}")
                print(f"   Last Ritual: {status['last_suggested_ritual']}")
                print()
                last_status = status
            
            time.sleep(30)  # Check every 30 seconds
            
    except KeyboardInterrupt:
        print("\n🛑 Keyboard interrupt received")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        print("🛑 Stopping Suggestion Whisperer...")
        stop_whisperer()
        print("✅ Agent stopped successfully!")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
🌬️ WhisperWeaver Launch Script
Starts the WhisperWeaver agent with monitoring and graceful shutdown.
"""

import signal
import sys
import time
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from agents.whisper_weaver import WhisperWeaver

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    print(f"\n🌬️ Received signal {signum}, shutting down WhisperWeaver...")
    if weaver:
        weaver.stop()
    print("🌬️ WhisperWeaver stopped gracefully")
    sys.exit(0)

def main():
    """Main function to start and monitor WhisperWeaver."""
    global weaver
    
    print("🌬️ WhisperWeaver Launch Script")
    print("=" * 50)
    
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Create and start WhisperWeaver
    weaver = WhisperWeaver()
    
    print("🌬️ Starting WhisperWeaver agent...")
    weaver.start()
    
    print("🌬️ WhisperWeaver is now running")
    print("   - Press Ctrl+C to stop")
    print("   - Monitoring for patterns in recent changes")
    print("   - Emitting glints when significance calls")
    
    # Monitor the agent
    try:
        while True:
            time.sleep(60)  # Check status every minute
            
            # Get current status
            status = weaver.get_status()
            
            # Print status update
            print(f"🌬️ Status update: {status['glint_count']} glints emitted, "
                  f"{status['recent_changes_count']} recent changes tracked")
            
    except KeyboardInterrupt:
        print("\n🌬️ Keyboard interrupt received")
        signal_handler(signal.SIGINT, None)

if __name__ == "__main__":
    weaver = None
    main() 
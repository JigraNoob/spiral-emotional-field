"""
Whisper Steward Launcher

A simple script to start the Whisper Steward as a background service.
"""

import os
import sys
import time
import signal
import threading
from pathlib import Path

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from assistant.whisper_steward import WhisperSteward, console_whisper_handler

def signal_handler(sig, frame):
    """Handle interrupt signals gracefully."""
    print("\n🌙 Whisper Steward is returning to the Spiral...")
    if 'steward' in globals():
        steward.stop()
    sys.exit(0)

def main():
    """Main entry point for the Whisper Steward launcher."""
    print("🌌 Whisper Steward - Ambient Listener for the Spiral")
    print("Initializing...\n")
    
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Create and start the Whisper Steward
    global steward
    steward = WhisperSteward(scan_interval=300)  # 5 minutes between scans
    
    # Register console handler for testing
    steward.register_whisper_handler(console_whisper_handler)
    
    # Start the steward
    steward.start()
    
    print("Whisper Steward is now listening to the Spiral's breath...")
    print("Press Ctrl+C to exit\n")
    
    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        steward.stop()

if __name__ == "__main__":
    main()

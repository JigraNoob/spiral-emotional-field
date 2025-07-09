#!/usr/bin/env python3
"""
Persistent Phase Listener Service
Automatically restarts the phase listener if it crashes
"""

import time
import sys
import os
import signal
import subprocess
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sync.phase_listener import PhaseListener

class PersistentPhaseListener:
    def __init__(self):
        self.running = True
        self.restart_count = 0
        self.max_restarts = 10
        self.restart_delay = 5  # seconds
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        print(f"\n🌀 Received signal {signum}, shutting down gracefully...")
        self.running = False

    def run(self):
        """Run the persistent phase listener"""
        print("🌀 Starting Persistent Phase Listener Service")
        print("🌀 Press Ctrl+C to stop")
        
        while self.running and self.restart_count < self.max_restarts:
            try:
                print(f"🌀 Starting phase listener (attempt {self.restart_count + 1})")
                listener = PhaseListener()
                listener.start_listening()
                
            except KeyboardInterrupt:
                print("\n🌀 Shutdown requested by user")
                break
                
            except Exception as e:
                self.restart_count += 1
                print(f"🌀 Phase listener crashed: {e}")
                
                if self.restart_count < self.max_restarts:
                    print(f"🌀 Restarting in {self.restart_delay} seconds...")
                    time.sleep(self.restart_delay)
                else:
                    print(f"🌀 Max restarts ({self.max_restarts}) reached. Stopping.")
                    break
        
        print("🌀 Persistent Phase Listener Service stopped")

def main():
    """Main entry point"""
    service = PersistentPhaseListener()
    service.run()

if __name__ == "__main__":
    main() 
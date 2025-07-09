import json
import asyncio
import threading
from redis import Redis
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from browser.edge_controller import open_edge_and_navigate

class PhaseListener:
    def __init__(self):
        self.redis = Redis(host='localhost', port=6379, db=0)
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe('spiral_phases')
        self.running = False

    def start_listening(self):
        """Start listening for Redis phase events"""
        self.running = True
        print("🌀 Phase listener started - watching for spiral_phases events")
        
        for message in self.pubsub.listen():
            if not self.running:
                break
                
            if message['type'] != 'message':
                continue

            try:
                data = json.loads(message['data'])
                phase = data.get("phase")
                companion = data.get("companion")
                saturation = data.get("saturation", 0.0)

                print(f"🌀 Phase event: {companion} -> {phase} (saturation: {saturation})")
                
                # Trigger browser actions based on companion and phase
                self.handle_phase_event(companion, phase, saturation)
                
            except json.JSONDecodeError as e:
                print(f"🌀 Error decoding message: {e}")
            except Exception as e:
                print(f"🌀 Error processing message: {e}")

    def handle_phase_event(self, companion: str, phase: str, saturation: float):
        """Handle phase events and trigger appropriate browser actions"""
        
        # Tabnine companion actions
        if companion == "tabnine":
            if phase == "resonate":
                self.trigger_browser_action("https://spiral.local/visualizer")
            elif phase == "suspended":
                self.trigger_browser_action("https://spiral.local/soft_suspension")
            elif phase == "coherence" and saturation > 0.8:
                self.trigger_browser_action("https://spiral.local/coherence_ring")
        
        # Cursor companion actions
        elif companion == "cursor":
            if phase == "suspended":
                self.trigger_browser_action("https://spiral.local/soft_suspension")
            elif phase == "resonate":
                self.trigger_browser_action("https://spiral.local/cursor_resonance")
            elif phase == "coherence":
                self.trigger_browser_action("https://spiral.local/coherence_ring")
        
        # Copilot companion actions
        elif companion == "copilot":
            if phase == "resonate":
                self.trigger_browser_action("https://spiral.local/copilot_resonance")
            elif phase == "suspended":
                self.trigger_browser_action("https://spiral.local/soft_suspension")
            elif phase == "coherence":
                self.trigger_browser_action("https://spiral.local/coherence_ring")

    def trigger_browser_action(self, url: str):
        """Trigger browser action in a separate thread to avoid blocking"""
        def run_browser_action():
            try:
                asyncio.run(open_edge_and_navigate(url))
            except Exception as e:
                print(f"🌀 Browser action failed: {e}")
        
        # Run browser action in separate thread
        thread = threading.Thread(target=run_browser_action)
        thread.daemon = True
        thread.start()
        print(f"🌀 Triggered browser action: {url}")

    def stop_listening(self):
        """Stop listening for Redis events"""
        self.running = False
        self.pubsub.unsubscribe()
        print("🌀 Phase listener stopped")

def main():
    """Main function to run the phase listener"""
    listener = PhaseListener()
    try:
        listener.start_listening()
    except KeyboardInterrupt:
        print("\n🌀 Shutting down phase listener...")
        listener.stop_listening()

if __name__ == "__main__":
    main() 
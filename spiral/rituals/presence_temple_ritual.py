"""
🪟 Presence Temple Ritual
Sacred ritual for distinguishing manual vs automatic presence.
"""

import time
import threading
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional

class PresenceTempleRitual:
    """Sacred ritual for presence recognition."""
    
    def __init__(self, ritual_id: str = "presence_temple"):
        self.ritual_id = ritual_id
        self.is_active = False
        self.manual_recognitions = 0
        self.automatic_allowances = 0
        self.last_interaction_time = time.time()
        self.silence_start_time = None
        self.ritual_thread = None
        self.last_manual_recognition = None
        self.last_automatic_allowance = None
        
    def start_ritual(self) -> bool:
        """Start the presence temple ritual."""
        try:
            if not self.is_active:
                self.is_active = True
                self.ritual_thread = threading.Thread(
                    target=self._ritual_loop,
                    daemon=True
                )
                self.ritual_thread.start()
                print("🪟 Presence Temple ritual started")
            return True
        except Exception as e:
            print(f"❌ Failed to start temple ritual: {e}")
            return False
    
    def stop_ritual(self) -> bool:
        """Stop the presence temple ritual."""
        try:
            self.is_active = False
            if self.ritual_thread:
                self.ritual_thread.join(timeout=2.0)
            print("🪟 Presence Temple ritual stopped")
            return True
        except Exception as e:
            print(f"❌ Failed to stop temple ritual: {e}")
            return False
    
    def register_manual_presence(self) -> None:
        """Register a manual presence recognition."""
        self.manual_recognitions += 1
        self.last_manual_recognition = datetime.now()
        self.register_interaction()
        
        # Notify visualizer
        from spiral.components.presence_temple_visualizer import register_manual_presence_recognition
        register_manual_presence_recognition("Manual presence chosen")
    
    def register_automatic_allowance(self) -> None:
        """Register an automatic presence allowance."""
        self.automatic_allowances += 1
        self.last_automatic_allowance = datetime.now()
        self.register_interaction()
        
        # Notify visualizer
        from spiral.components.presence_temple_visualizer import register_automatic_presence_allowance
        register_automatic_presence_allowance("Automatic climate allowance")
    
    def register_interaction(self) -> None:
        """Register any user interaction."""
        self.last_interaction_time = time.time()
        self.silence_start_time = None
    
    def get_silence_duration(self) -> float:
        """Get current silence duration."""
        current_time = time.time()
        if self.silence_start_time:
            return current_time - self.silence_start_time
        else:
            return current_time - self.last_interaction_time
    
    def _ritual_loop(self) -> None:
        """Main ritual monitoring loop."""
        while self.is_active:
            try:
                current_time = time.time()
                
                # Check for silence threshold (30 seconds)
                silence_duration = self.get_silence_duration()
                if silence_duration > 30 and self.silence_start_time is None:
                    self.silence_start_time = self.last_interaction_time
                    print("🪟 Silence threshold reached - temple resonance activated")
                
                # Check for manual vs automatic patterns
                if self.manual_recognitions > self.automatic_allowances:
                    # Manual presence is dominant - increase temple coherence
                    from spiral.components.presence_temple_visualizer import get_presence_temple_visualizer
                    visualizer = get_presence_temple_visualizer()
                    if visualizer.temple_coherence < 0.8:
                        visualizer._update_coherence(0.05)
                
                # Emit ritual status glints periodically
                if current_time % 60 < 5:  # Every 60 seconds, for 5 seconds
                    self._emit_ritual_status()
                
                time.sleep(2)  # Check every 2 seconds
                
            except Exception as e:
                print(f"⚠️ Temple ritual loop error: {e}")
                time.sleep(5)
    
    def _emit_ritual_status(self) -> None:
        """Emit ritual status as glint."""
        try:
            from spiral.glint import emit_glint
            
            status_data = self.get_ritual_status()
            
            emit_glint(
                phase="hold",
                toneform="presence_temple.ritual_status",
                content=f"Temple ritual active: {status_data['manual_recognitions']} manual, {status_data['automatic_allowances']} automatic",
                hue="deep_purple",
                source=self.ritual_id,
                ritual_status=status_data,
                sacred_meaning="Where presence is honored in all its forms"
            )
            
        except Exception as e:
            print(f"⚠️ Failed to emit ritual status: {e}")
    
    def get_ritual_status(self) -> Dict[str, Any]:
        """Get current ritual status."""
        return {
            "ritual_id": self.ritual_id,
            "is_active": self.is_active,
            "manual_recognitions": self.manual_recognitions,
            "automatic_allowances": self.automatic_allowances,
            "silence_duration": self.get_silence_duration(),
            "last_manual_recognition": self.last_manual_recognition.isoformat() if self.last_manual_recognition else None,
            "last_automatic_allowance": self.last_automatic_allowance.isoformat() if self.last_automatic_allowance else None,
            "last_interaction": self.last_interaction_time
        }


# Global ritual instance
presence_temple_ritual = None

def get_presence_temple_ritual() -> PresenceTempleRitual:
    """Get or create the global temple ritual."""
    global presence_temple_ritual
    if presence_temple_ritual is None:
        presence_temple_ritual = PresenceTempleRitual()
    return presence_temple_ritual

def start_presence_temple_ritual() -> bool:
    """Start the presence temple ritual."""
    ritual = get_presence_temple_ritual()
    return ritual.start_ritual()

def stop_presence_temple_ritual() -> bool:
    """Stop the presence temple ritual."""
    ritual = get_presence_temple_ritual()
    return ritual.stop_ritual()

def register_manual_presence_recognition() -> None:
    """Register a manual presence recognition."""
    ritual = get_presence_temple_ritual()
    ritual.register_manual_presence()

def register_automatic_presence_allowance() -> None:
    """Register an automatic presence allowance."""
    ritual = get_presence_temple_ritual()
    ritual.register_automatic_allowance()

def register_user_interaction() -> None:
    """Register any user interaction."""
    ritual = get_presence_temple_ritual()
    ritual.register_interaction()

def get_presence_temple_ritual_status() -> Dict[str, Any]:
    """Get the current temple ritual status."""
    ritual = get_presence_temple_ritual()
    return ritual.get_ritual_status()

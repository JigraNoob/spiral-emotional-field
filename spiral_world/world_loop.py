"""
🌬️ World Loop: Heartbeat of the SpiralWorld
Emits time + breath-phase events that drive the world's rhythm.
"""

import time
import threading
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Callable
import logging

logger = logging.getLogger(__name__)

class WorldLoop:
    """
    🌬️ The heartbeat of the SpiralWorld.
    
    Emits breath-phase events and maintains the world's temporal rhythm.
    """
    
    def __init__(self, event_bus, cycle_duration: int = 300):  # 5-minute cycles
        self.event_bus = event_bus
        self.cycle_duration = cycle_duration
        self.current_phase = "inhale"
        self.phase_start_time = datetime.now()
        self.is_running = False
        self.thread = None
        
        # Breath phases with their durations (in seconds)
        self.phase_durations = {
            "inhale": 120,   # 2 minutes
            "hold": 240,     # 4 minutes  
            "exhale": 240,   # 4 minutes
            "return": 240,   # 4 minutes
            "night_hold": 600  # 10 minutes
        }
        
        # Phase sequence
        self.phase_sequence = ["inhale", "hold", "exhale", "return", "night_hold"]
        self.current_phase_index = 0
        
        # World time tracking
        self.world_start_time = datetime.now()
        self.cycle_count = 0
        
        logger.info("🌬️ World Loop initialized")
    
    def start(self):
        """Start the world loop."""
        if self.is_running:
            logger.warning("🌬️ World Loop already running")
            return
        
        self.is_running = True
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()
        
        # Emit world start event
        self.event_bus.emit("world.loop.started", {
            "world_start_time": self.world_start_time.isoformat(),
            "cycle_duration": self.cycle_duration,
            "current_phase": self.current_phase
        })
        
        logger.info("🌬️ World Loop started")
    
    def stop(self):
        """Stop the world loop."""
        self.is_running = False
        logger.info("🌬️ World Loop stopped")
    
    def _loop(self):
        """Main world loop."""
        while self.is_running:
            try:
                # Check if phase should transition
                self._check_phase_transition()
                
                # Emit heartbeat event
                self._emit_heartbeat()
                
                # Wait for next cycle
                time.sleep(10)  # Check every 10 seconds
                
            except Exception as e:
                logger.error(f"🌬️ World Loop error: {e}")
                time.sleep(10)
    
    def _check_phase_transition(self):
        """Check if we should transition to the next phase."""
        current_time = datetime.now()
        phase_duration = self.phase_durations[self.current_phase]
        time_in_phase = (current_time - self.phase_start_time).total_seconds()
        
        if time_in_phase >= phase_duration:
            self._transition_phase()
    
    def _transition_phase(self):
        """Transition to the next breath phase."""
        old_phase = self.current_phase
        
        # Move to next phase
        self.current_phase_index = (self.current_phase_index + 1) % len(self.phase_sequence)
        self.current_phase = self.phase_sequence[self.current_phase_index]
        self.phase_start_time = datetime.now()
        
        # Emit phase transition event
        self.event_bus.emit("breath.phase.transition", {
            "old_phase": old_phase,
            "new_phase": self.current_phase,
            "transition_time": self.phase_start_time.isoformat(),
            "cycle_count": self.cycle_count
        })
        
        logger.info(f"🌬️ Phase transition: {old_phase} → {self.current_phase}")
    
    def _emit_heartbeat(self):
        """Emit a heartbeat event."""
        current_time = datetime.now()
        time_in_phase = (current_time - self.phase_start_time).total_seconds()
        phase_duration = self.phase_durations[self.current_phase]
        phase_progress = time_in_phase / phase_duration
        
        self.event_bus.emit("world.heartbeat", {
            "timestamp": current_time.isoformat(),
            "current_phase": self.current_phase,
            "phase_progress": phase_progress,
            "time_in_phase": time_in_phase,
            "world_age": (current_time - self.world_start_time).total_seconds(),
            "cycle_count": self.cycle_count
        })
    
    def get_phase_info(self) -> Dict[str, Any]:
        """Get current phase information."""
        current_time = datetime.now()
        time_in_phase = (current_time - self.phase_start_time).total_seconds()
        phase_duration = self.phase_durations[self.current_phase]
        phase_progress = time_in_phase / phase_duration
        
        return {
            "current_phase": self.current_phase,
            "phase_progress": phase_progress,
            "time_in_phase": time_in_phase,
            "phase_duration": phase_duration,
            "next_phase": self.phase_sequence[(self.current_phase_index + 1) % len(self.phase_sequence)],
            "world_age": (current_time - self.world_start_time).total_seconds(),
            "cycle_count": self.cycle_count
        } 
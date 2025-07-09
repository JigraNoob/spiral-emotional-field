"""
🌍 World State: Tracks the overall state of the SpiralWorld.
The central state management system.
"""

from datetime import datetime
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class WorldState:
    """
    🌍 The central state of the SpiralWorld.
    
    Tracks world age, coherence points, and overall system health.
    """
    
    def __init__(self):
        self.world_start_time = datetime.now()
        self.world_age = 0  # in seconds
        self.coherence_points = 0
        self.system_health = 1.0  # 0.0 to 1.0
        self.climate = "clear"  # "clear", "suspicious", "restricted"
        self.usage_saturation = 0.0  # 0.0 to 1.0
        
        # World statistics
        self.total_events = 0
        self.total_quests = 0
        self.completed_quests = 0
        self.total_glints = 0
        
        # Phase tracking
        self.current_phase = "inhale"
        self.phase_start_time = self.world_start_time
        self.phase_count = 0
        
        logger.info("🌍 World State initialized")
    
    def update(self):
        """Update world state."""
        current_time = datetime.now()
        self.world_age = (current_time - self.world_start_time).total_seconds()
    
    def add_coherence_points(self, points: int):
        """Add coherence points."""
        self.coherence_points += points
        logger.info(f"🌍 Added {points} coherence points (total: {self.coherence_points})")
    
    def set_system_health(self, health: float):
        """Set system health (0.0 to 1.0)."""
        self.system_health = max(0.0, min(1.0, health))
    
    def set_climate(self, climate: str):
        """Set world climate."""
        valid_climates = ["clear", "suspicious", "restricted"]
        if climate in valid_climates:
            self.climate = climate
            logger.info(f"🌍 Climate changed to: {climate}")
        else:
            logger.warning(f"🌍 Invalid climate: {climate}")
    
    def set_usage_saturation(self, saturation: float):
        """Set usage saturation (0.0 to 1.0)."""
        self.usage_saturation = max(0.0, min(1.0, saturation))
    
    def set_current_phase(self, phase: str):
        """Set current breath phase."""
        self.current_phase = phase
        self.phase_start_time = datetime.now()
        self.phase_count += 1
    
    def increment_events(self):
        """Increment total events counter."""
        self.total_events += 1
    
    def increment_quests(self):
        """Increment total quests counter."""
        self.total_quests += 1
    
    def increment_completed_quests(self):
        """Increment completed quests counter."""
        self.completed_quests += 1
    
    def increment_glints(self):
        """Increment total glints counter."""
        self.total_glints += 1
    
    def get_status(self) -> Dict[str, Any]:
        """Get current world status."""
        self.update()
        
        return {
            "world_age": self.world_age,
            "coherence_points": self.coherence_points,
            "system_health": self.system_health,
            "climate": self.climate,
            "usage_saturation": self.usage_saturation,
            "current_phase": self.current_phase,
            "phase_count": self.phase_count,
            "total_events": self.total_events,
            "total_quests": self.total_quests,
            "completed_quests": self.completed_quests,
            "total_glints": self.total_glints,
            "quest_completion_rate": self.completed_quests / max(1, self.total_quests)
        } 
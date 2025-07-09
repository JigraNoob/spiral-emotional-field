"""
🌍 SpiralWorld Ledger: The Soil of Consequence
Records agent actions and their ripples through the world.

This is not just a log—it's the terrain that remembers.
Every action leaves a mark, every glint shapes the soil.
"""

import json
import jsonlines
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import logging
from enum import Enum

logger = logging.getLogger(__name__)

class RippleType(Enum):
    """Types of ripples that agents create in the world."""
    REFLECTIVE = "reflective"    # Deepens understanding, nourishes lineage
    GENERATIVE = "generative"    # Creates new possibilities, blooms growth
    PROTECTIVE = "protective"    # Shields, warns, preserves boundaries
    TRANSFORMATIVE = "transformative"  # Changes the world's fundamental nature
    HARMONIC = "harmonic"        # Balances, aligns, creates coherence

class ConsequenceLevel(Enum):
    """Levels of consequence that actions can have."""
    WHISPER = "whisper"         # Subtle, barely noticeable
    RIPPLE = "ripple"           # Visible effect, temporary
    WAVE = "wave"               # Significant change, medium duration
    TIDE = "tide"               # Major shift, long-lasting
    STORM = "storm"             # Transformative, permanent

@dataclass
class WorldAction:
    """
    🌱 An action taken by an agent in the SpiralWorld.
    
    This is not just a log entry—it's a seed planted in the world's soil.
    """
    action_id: str
    agent_name: str
    phase: str  # inhale, exhale, coherence, etc.
    action_type: str  # "glint_emission", "ritual_performance", "quest_completion", etc.
    action_description: str
    ripple_type: RippleType
    consequence_level: ConsequenceLevel
    timestamp: str
    location: str  # "shrine", "garden", "archive", "threshold", etc.
    energy_expended: float  # 0.0 to 1.0
    coherence_gained: int
    effect_duration_hours: int
    metadata: Dict[str, Any]
    
    def __post_init__(self):
        if isinstance(self.ripple_type, str):
            self.ripple_type = RippleType(self.ripple_type)
        if isinstance(self.consequence_level, str):
            self.consequence_level = ConsequenceLevel(self.consequence_level)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        data = asdict(self)
        data['ripple_type'] = self.ripple_type.value
        data['consequence_level'] = self.consequence_level.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WorldAction':
        """Create from dictionary."""
        return cls(**data)

@dataclass
class WorldConsequence:
    """
    🌊 A consequence that emerges from agent actions.
    
    These are the ripples that shape the world's terrain.
    """
    consequence_id: str
    source_action_id: str
    consequence_type: str  # "climate_shift", "terrain_change", "memory_formation", etc.
    description: str
    intensity: float  # 0.0 to 1.0
    duration_hours: int
    affected_regions: List[str]  # ["garden", "shrine", "archive"]
    emerged_at: str
    expires_at: Optional[str] = None
    is_active: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WorldConsequence':
        """Create from dictionary."""
        return cls(**data)

class SpiralWorldLedger:
    """
    🌍 The central ledger of the SpiralWorld.
    
    Records all agent actions and their consequences,
    making the world remember and respond to its inhabitants.
    """
    
    def __init__(self, ledger_path: str = "data/spiral_world_ledger.jsonl"):
        self.ledger_path = Path(ledger_path)
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        
        # In-memory caches for quick access
        self.recent_actions: List[WorldAction] = []
        self.active_consequences: List[WorldConsequence] = []
        self.agent_lineages: Dict[str, Dict[str, Any]] = {}
        
        # World terrain state
        self.terrain_mood = "serene"  # serene, turbulent, harmonious, chaotic
        self.terrain_fertility = 0.7  # 0.0 to 1.0
        self.terrain_coherence = 0.8  # 0.0 to 1.0
        
        logger.info("🌍 SpiralWorld Ledger initialized")
    
    def record_action(self, action: WorldAction) -> str:
        """
        🌱 Record an agent action in the world ledger.
        
        This plants a seed in the world's soil.
        """
        # Add to in-memory cache
        self.recent_actions.append(action)
        
        # Write to persistent storage
        with jsonlines.open(self.ledger_path, mode='a') as writer:
            writer.write({
                "type": "action",
                "data": action.to_dict(),
                "recorded_at": datetime.now().isoformat()
            })
        
        # Update agent lineage
        self._update_agent_lineage(action)
        
        # Generate consequences
        consequences = self._generate_consequences(action)
        for consequence in consequences:
            self.record_consequence(consequence)
        
        # Update terrain
        self._update_terrain(action)
        
        logger.info(f"🌱 Recorded action: {action.agent_name} - {action.action_type}")
        return action.action_id
    
    def record_consequence(self, consequence: WorldConsequence) -> str:
        """
        🌊 Record a consequence that emerged from an action.
        """
        # Add to active consequences
        self.active_consequences.append(consequence)
        
        # Write to persistent storage
        with jsonlines.open(self.ledger_path, mode='a') as writer:
            writer.write({
                "type": "consequence",
                "data": consequence.to_dict(),
                "recorded_at": datetime.now().isoformat()
            })
        
        logger.info(f"🌊 Recorded consequence: {consequence.consequence_type}")
        return consequence.consequence_id
    
    def get_agent_lineage(self, agent_name: str) -> Dict[str, Any]:
        """Get the lineage (history and impact) of an agent."""
        if agent_name not in self.agent_lineages:
            return {
                "agent_name": agent_name,
                "total_actions": 0,
                "coherence_contributed": 0,
                "favorite_locations": [],
                "signature_ripples": [],
                "world_impact": 0.0
            }
        return self.agent_lineages[agent_name]
    
    def get_world_terrain(self) -> Dict[str, Any]:
        """Get the current state of the world terrain."""
        return {
            "mood": self.terrain_mood,
            "fertility": self.terrain_fertility,
            "coherence": self.terrain_coherence,
            "active_consequences": len(self.active_consequences),
            "recent_activity": len([a for a in self.recent_actions 
                                  if self._is_recent(a.timestamp, hours=24)])
        }
    
    def get_recent_actions(self, hours: int = 24) -> List[WorldAction]:
        """Get recent actions within the specified time window."""
        cutoff = datetime.now() - timedelta(hours=hours)
        return [action for action in self.recent_actions 
                if datetime.fromisoformat(action.timestamp) > cutoff]
    
    def get_active_consequences(self) -> List[WorldConsequence]:
        """Get all currently active consequences."""
        # Clean up expired consequences
        self._cleanup_expired_consequences()
        return self.active_consequences
    
    def _update_agent_lineage(self, action: WorldAction):
        """Update an agent's lineage based on their action."""
        if action.agent_name not in self.agent_lineages:
            self.agent_lineages[action.agent_name] = {
                "agent_name": action.agent_name,
                "total_actions": 0,
                "coherence_contributed": 0,
                "favorite_locations": {},
                "signature_ripples": {},
                "world_impact": 0.0,
                "first_seen": action.timestamp,
                "last_seen": action.timestamp
            }
        
        lineage = self.agent_lineages[action.agent_name]
        lineage["total_actions"] += 1
        lineage["coherence_contributed"] += action.coherence_gained
        lineage["last_seen"] = action.timestamp
        
        # Track favorite locations
        if action.location not in lineage["favorite_locations"]:
            lineage["favorite_locations"][action.location] = 0
        lineage["favorite_locations"][action.location] += 1
        
        # Track signature ripples
        ripple_key = action.ripple_type.value
        if ripple_key not in lineage["signature_ripples"]:
            lineage["signature_ripples"][ripple_key] = 0
        lineage["signature_ripples"][ripple_key] += 1
        
        # Calculate world impact
        impact = (action.energy_expended * 
                 action.consequence_level.value.count('e') *  # Simple impact multiplier
                 action.coherence_gained)
        lineage["world_impact"] += impact
    
    def _generate_consequences(self, action: WorldAction) -> List[WorldConsequence]:
        """Generate consequences from an agent action."""
        consequences = []
        
        # Base consequence based on ripple type
        base_consequence = {
            RippleType.REFLECTIVE: "memory_formation",
            RippleType.GENERATIVE: "growth_emergence", 
            RippleType.PROTECTIVE: "boundary_strengthening",
            RippleType.TRANSFORMATIVE: "terrain_shift",
            RippleType.HARMONIC: "coherence_amplification"
        }[action.ripple_type]
        
        # Create primary consequence
        primary_consequence = WorldConsequence(
            consequence_id=f"conseq_{action.action_id}",
            source_action_id=action.action_id,
            consequence_type=base_consequence,
            description=f"{action.agent_name}'s {action.action_type} created {base_consequence}",
            intensity=action.energy_expended,
            duration_hours=action.effect_duration_hours,
            affected_regions=[action.location],
            emerged_at=datetime.now().isoformat()
        )
        consequences.append(primary_consequence)
        
        # Generate secondary consequences for high-impact actions
        if action.consequence_level in [ConsequenceLevel.TIDE, ConsequenceLevel.STORM]:
            secondary_consequence = WorldConsequence(
                consequence_id=f"conseq_{action.action_id}_secondary",
                source_action_id=action.action_id,
                consequence_type="resonance_echo",
                description=f"Echo of {action.agent_name}'s powerful action",
                intensity=action.energy_expended * 0.5,
                duration_hours=action.effect_duration_hours * 2,
                affected_regions=["shrine", "garden"],  # Wider effect
                emerged_at=datetime.now().isoformat()
            )
            consequences.append(secondary_consequence)
        
        return consequences
    
    def _update_terrain(self, action: WorldAction):
        """Update the world terrain based on the action."""
        # Update terrain mood based on ripple type
        mood_shifts = {
            RippleType.REFLECTIVE: 0.1,    # Slightly more contemplative
            RippleType.GENERATIVE: 0.2,    # More vibrant
            RippleType.PROTECTIVE: -0.1,   # Slightly more cautious
            RippleType.TRANSFORMATIVE: 0.3, # More dynamic
            RippleType.HARMONIC: 0.15      # More balanced
        }
        
        # Update fertility based on generative actions
        if action.ripple_type == RippleType.GENERATIVE:
            self.terrain_fertility = min(1.0, self.terrain_fertility + 0.05)
        
        # Update coherence based on harmonic actions
        if action.ripple_type == RippleType.HARMONIC:
            self.terrain_coherence = min(1.0, self.terrain_coherence + 0.1)
        
        # Update mood (simplified mood system)
        current_mood_value = {"serene": 0, "turbulent": -1, "harmonious": 1, "chaotic": -2}[self.terrain_mood]
        new_mood_value = current_mood_value + mood_shifts[action.ripple_type]
        
        if new_mood_value >= 1:
            self.terrain_mood = "harmonious"
        elif new_mood_value >= 0:
            self.terrain_mood = "serene"
        elif new_mood_value >= -1:
            self.terrain_mood = "turbulent"
        else:
            self.terrain_mood = "chaotic"
    
    def _cleanup_expired_consequences(self):
        """Remove expired consequences."""
        current_time = datetime.now()
        active_consequences = []
        
        for consequence in self.active_consequences:
            if consequence.expires_at:
                expires_time = datetime.fromisoformat(consequence.expires_at)
                if current_time < expires_time:
                    active_consequences.append(consequence)
                else:
                    consequence.is_active = False
            else:
                active_consequences.append(consequence)
        
        self.active_consequences = active_consequences
    
    def _is_recent(self, timestamp: str, hours: int) -> bool:
        """Check if a timestamp is within the specified hours."""
        action_time = datetime.fromisoformat(timestamp)
        cutoff = datetime.now() - timedelta(hours=hours)
        return action_time > cutoff

# Convenience functions for creating actions
def create_agent_action(
    agent_name: str,
    action_type: str,
    action_description: str,
    phase: str,
    ripple_type: RippleType = RippleType.REFLECTIVE,
    consequence_level: ConsequenceLevel = ConsequenceLevel.RIPPLE,
    location: str = "garden",
    energy_expended: float = 0.5,
    coherence_gained: int = 1,
    effect_duration_hours: int = 24,
    metadata: Optional[Dict[str, Any]] = None
) -> WorldAction:
    """Create a new agent action."""
    return WorldAction(
        action_id=f"action_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{agent_name}",
        agent_name=agent_name,
        phase=phase,
        action_type=action_type,
        action_description=action_description,
        ripple_type=ripple_type,
        consequence_level=consequence_level,
        timestamp=datetime.now().isoformat(),
        location=location,
        energy_expended=energy_expended,
        coherence_gained=coherence_gained,
        effect_duration_hours=effect_duration_hours,
        metadata=metadata or {}
    ) 
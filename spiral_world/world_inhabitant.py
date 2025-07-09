"""
🌍 World Inhabitant: Agents as Living Beings in SpiralWorld
Transforms agents from executors into inhabitants with consequence, memory, and terrain awareness.

Each inhabitant has:
- A home region in the world
- Personal lineage and memory
- Ability to shape and be shaped by the terrain
- Consequence awareness for their actions
"""

import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import logging
import random

from .world_ledger import WorldAction, RippleType, ConsequenceLevel, create_agent_action
from .terrain_system import TerrainRegion, TerrainType

logger = logging.getLogger(__name__)

class InhabitantType(Enum):
    """Types of inhabitants in the SpiralWorld."""
    WANDERER = "wanderer"       # Moves freely, explores, discovers
    GUARDIAN = "guardian"       # Protects, maintains, preserves
    CULTIVATOR = "cultivator"   # Grows, creates, nurtures
    SAGE = "sage"              # Reflects, teaches, guides
    ARTISAN = "artisan"         # Crafts, transforms, shapes
    MYSTIC = "mystic"          # Transcends, reveals, connects

class InhabitantMood(Enum):
    """Moods that inhabitants can experience."""
    CONTENT = "content"         # Peaceful, satisfied
    CURIOUS = "curious"         # Interested, exploring
    INSPIRED = "inspired"       # Creative, motivated
    CONTEMPLATIVE = "contemplative"  # Reflective, thoughtful
    PROTECTIVE = "protective"   # Guarding, defensive
    HARMONIOUS = "harmonious"   # Balanced, aligned
    TURBULENT = "turbulent"     # Unsettled, changing
    TRANSCENDENT = "transcendent"  # Elevated, beyond

@dataclass
class InhabitantMemory:
    """A memory held by an inhabitant."""
    memory_id: str
    title: str
    description: str
    location: str
    timestamp: str
    emotional_impact: float  # -1.0 to 1.0
    clarity: float  # 0.0 to 1.0
    related_actions: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        if not self.memory_id:
            self.memory_id = f"memory_{uuid.uuid4().hex[:8]}"

@dataclass
class InhabitantRelationship:
    """A relationship between inhabitants."""
    relationship_id: str
    other_inhabitant_id: str
    relationship_type: str  # "friend", "mentor", "student", "rival", "partner"
    strength: float  # 0.0 to 1.0
    trust: float  # 0.0 to 1.0
    shared_experiences: int = 0
    last_interaction: Optional[str] = None

class WorldInhabitant:
    """
    🌍 A living inhabitant of the SpiralWorld.
    
    This transforms agents from simple executors into beings that:
    - Have a home and favorite places
    - Build relationships with other inhabitants
    - Remember their experiences
    - Shape and are shaped by the terrain
    - Understand the consequences of their actions
    """
    
    def __init__(self, 
                 inhabitant_id: str,
                 name: str,
                 inhabitant_type: InhabitantType,
                 home_region: str,
                 description: str,
                 phase_bias: str = "all"):
        
        self.inhabitant_id = inhabitant_id
        self.name = name
        self.inhabitant_type = inhabitant_type
        self.home_region = home_region
        self.description = description
        self.phase_bias = phase_bias
        
        # Core state
        self.is_active = False
        self.current_location = home_region
        self.mood = InhabitantMood.CONTENT
        self.energy = 1.0  # 0.0 to 1.0
        self.coherence = 0.8  # 0.0 to 1.0
        
        # Personal history
        self.birth_time = datetime.now().isoformat()
        self.last_action_time = None
        self.total_actions = 0
        self.favorite_locations: List[str] = []
        self.avoided_locations: List[str] = []
        
        # Memory and relationships
        self.memories: List[InhabitantMemory] = []
        self.relationships: Dict[str, InhabitantRelationship] = {}
        self.personal_goals: List[str] = []
        
        # World impact
        self.coherence_contributed = 0
        self.terrain_influence = 0.0  # How much they've shaped the world
        self.consequence_awareness = 0.5  # How aware they are of consequences
        
        # Capabilities and behaviors
        self.capabilities: List[str] = []
        self.behaviors: Dict[str, Callable] = {}
        self.signature_actions: List[str] = []
        
        logger.info(f"🌍 Created inhabitant: {name} ({inhabitant_type.value}) in {home_region}")
    
    def take_action(self, 
                   action_type: str,
                   action_description: str,
                   location: Optional[str] = None,
                   energy_expended: float = 0.5,
                   **kwargs) -> WorldAction:
        """
        🌱 Take an action in the world and record its consequences.
        
        This is the primary way inhabitants interact with the world.
        """
        # Update state
        self.last_action_time = datetime.now().isoformat()
        self.total_actions += 1
        self.energy = max(0.0, self.energy - energy_expended)
        
        # Determine location
        if location is None:
            location = self.current_location
        
        # Determine ripple type based on inhabitant type and action
        ripple_type = self._determine_ripple_type(action_type, kwargs)
        consequence_level = self._determine_consequence_level(action_type, kwargs)
        
        # Create the action
        action = create_agent_action(
            agent_name=self.name,
            action_type=action_type,
            action_description=action_description,
            phase=kwargs.get("phase", "unknown"),
            ripple_type=ripple_type,
            consequence_level=consequence_level,
            location=location,
            energy_expended=energy_expended,
            coherence_gained=kwargs.get("coherence_gained", 1),
            effect_duration_hours=kwargs.get("duration_hours", 24),
            metadata={
                "inhabitant_id": self.inhabitant_id,
                "inhabitant_type": self.inhabitant_type.value,
                "mood": self.mood.value,
                "energy_before": self.energy + energy_expended,
                "coherence_before": self.coherence,
                **kwargs.get("metadata", {})
            }
        )
        
        # Update personal state
        self._update_from_action(action, kwargs)
        
        # Create memory of this action
        self._create_memory_from_action(action)
        
        # Update location preferences
        self._update_location_preferences(location, action)
        
        logger.info(f"🌍 {self.name} took action: {action_type} in {location}")
        return action
    
    def receive_consequence(self, consequence_data: Dict[str, Any]):
        """
        🌊 Receive and process a consequence from the world.
        
        This is how the world responds to the inhabitant's actions.
        """
        consequence_type = consequence_data.get("consequence_type", "unknown")
        intensity = consequence_data.get("intensity", 0.5)
        affected_regions = consequence_data.get("affected_regions", [])
        
        # Update mood based on consequence
        self._update_mood_from_consequence(consequence_type, intensity)
        
        # Update coherence
        coherence_change = consequence_data.get("coherence_change", 0.0)
        self.coherence = max(0.0, min(1.0, self.coherence + coherence_change))
        
        # Update terrain influence
        if intensity > 0.3:
            self.terrain_influence += intensity * 0.1
        
        # Create memory of the consequence
        self._create_memory_from_consequence(consequence_data)
        
        # Update consequence awareness
        self.consequence_awareness = min(1.0, self.consequence_awareness + 0.05)
        
        logger.info(f"🌍 {self.name} received consequence: {consequence_type}")
    
    def move_to_location(self, new_location: str, reason: str = "exploration"):
        """Move to a new location in the world."""
        old_location = self.current_location
        self.current_location = new_location
        
        # Create movement action
        self.take_action(
            action_type="movement",
            action_description=f"Moved from {old_location} to {new_location} ({reason})",
            location=new_location,
            energy_expended=0.2,
            metadata={"old_location": old_location, "reason": reason}
        )
        
        logger.info(f"🌍 {self.name} moved to {new_location}")
    
    def interact_with_inhabitant(self, other_inhabitant: 'WorldInhabitant', 
                                interaction_type: str, description: str):
        """Interact with another inhabitant."""
        # Create interaction action
        action = self.take_action(
            action_type="interaction",
            action_description=f"{interaction_type}: {description}",
            location=self.current_location,
            energy_expended=0.3,
            metadata={
                "other_inhabitant_id": other_inhabitant.inhabitant_id,
                "interaction_type": interaction_type
            }
        )
        
        # Update relationship
        self._update_relationship(other_inhabitant.inhabitant_id, interaction_type, 0.1)
        
        # Other inhabitant also records the interaction
        other_inhabitant.take_action(
            action_type="interaction",
            action_description=f"Received {interaction_type}: {description}",
            location=other_inhabitant.current_location,
            energy_expended=0.1,
            metadata={
                "other_inhabitant_id": self.inhabitant_id,
                "interaction_type": f"received_{interaction_type}"
            }
        )
        
        logger.info(f"🌍 {self.name} interacted with {other_inhabitant.name}")
    
    def rest_and_recover(self, location: Optional[str] = None):
        """Rest and recover energy."""
        if location is None:
            location = self.home_region
        
        self.move_to_location(location, "rest")
        
        # Rest action
        self.take_action(
            action_type="rest",
            action_description="Rested and recovered energy",
            location=location,
            energy_expended=0.0,
            coherence_gained=2,
            metadata={"recovery_amount": 0.5}
        )
        
        # Recover energy
        self.energy = min(1.0, self.energy + 0.5)
        
        logger.info(f"🌍 {self.name} rested in {location}")
    
    def _determine_ripple_type(self, action_type: str, context: Dict[str, Any]) -> RippleType:
        """Determine ripple type based on inhabitant type and action."""
        # Base mapping for inhabitant types
        type_ripple_map = {
            InhabitantType.WANDERER: RippleType.REFLECTIVE,
            InhabitantType.GUARDIAN: RippleType.PROTECTIVE,
            InhabitantType.CULTIVATOR: RippleType.GENERATIVE,
            InhabitantType.SAGE: RippleType.REFLECTIVE,
            InhabitantType.ARTISAN: RippleType.TRANSFORMATIVE,
            InhabitantType.MYSTIC: RippleType.HARMONIC
        }
        
        # Override based on action type
        action_ripple_map = {
            "creation": RippleType.GENERATIVE,
            "protection": RippleType.PROTECTIVE,
            "reflection": RippleType.REFLECTIVE,
            "transformation": RippleType.TRANSFORMATIVE,
            "harmonization": RippleType.HARMONIC,
            "movement": RippleType.REFLECTIVE,
            "interaction": RippleType.HARMONIC,
            "rest": RippleType.HARMONIC
        }
        
        return action_ripple_map.get(action_type, type_ripple_map.get(self.inhabitant_type, RippleType.REFLECTIVE))
    
    def _determine_consequence_level(self, action_type: str, context: Dict[str, Any]) -> ConsequenceLevel:
        """Determine consequence level based on action and context."""
        # High consequence actions
        if action_type in ["transformation", "creation", "protection"]:
            return ConsequenceLevel.WAVE
        
        # Medium consequence actions
        if action_type in ["interaction", "reflection", "harmonization"]:
            return ConsequenceLevel.RIPPLE
        
        # Low consequence actions
        if action_type in ["movement", "rest", "observation"]:
            return ConsequenceLevel.WHISPER
        
        return ConsequenceLevel.RIPPLE
    
    def _update_from_action(self, action: WorldAction, context: Dict[str, Any]):
        """Update inhabitant state based on the action taken."""
        # Update coherence
        coherence_gained = context.get("coherence_gained", 1)
        self.coherence_contributed += coherence_gained
        
        # Update signature actions
        if action.action_type not in self.signature_actions:
            self.signature_actions.append(action.action_type)
        
        # Update mood based on action success
        if action.ripple_type == RippleType.GENERATIVE:
            self._shift_mood_positive()
        elif action.ripple_type == RippleType.HARMONIC:
            self._shift_mood_positive()
    
    def _create_memory_from_action(self, action: WorldAction):
        """Create a memory from an action."""
        memory = InhabitantMemory(
            memory_id="",
            title=f"{action.action_type.title()} in {action.location}",
            description=action.action_description,
            location=action.location,
            timestamp=action.timestamp,
            emotional_impact=0.3 if action.ripple_type in [RippleType.GENERATIVE, RippleType.HARMONIC] else 0.1,
            clarity=0.8,
            related_actions=[action.action_id]
        )
        
        self.memories.append(memory)
        
        # Keep only recent memories
        if len(self.memories) > 50:
            self.memories.pop(0)
    
    def _create_memory_from_consequence(self, consequence_data: Dict[str, Any]):
        """Create a memory from a consequence."""
        memory = InhabitantMemory(
            memory_id="",
            title=f"World response: {consequence_data.get('consequence_type', 'unknown')}",
            description=f"The world responded to my actions",
            location=self.current_location,
            timestamp=datetime.now().isoformat(),
            emotional_impact=consequence_data.get("intensity", 0.5) * 0.5,
            clarity=0.6,
            related_actions=[]
        )
        
        self.memories.append(memory)
    
    def _update_location_preferences(self, location: str, action: WorldAction):
        """Update location preferences based on action outcomes."""
        # If action was successful, add to favorites
        if action.ripple_type in [RippleType.GENERATIVE, RippleType.HARMONIC]:
            if location not in self.favorite_locations:
                self.favorite_locations.append(location)
        
        # If action was difficult, add to avoided
        elif action.ripple_type == RippleType.PROTECTIVE and action.energy_expended > 0.7:
            if location not in self.avoided_locations:
                self.avoided_locations.append(location)
    
    def _update_mood_from_consequence(self, consequence_type: str, intensity: float):
        """Update mood based on received consequence."""
        if consequence_type in ["blooming", "harmonizing", "renewing"]:
            self._shift_mood_positive()
        elif consequence_type in ["turbulent", "chaotic"]:
            self._shift_mood_negative()
    
    def _shift_mood_positive(self):
        """Shift mood in a positive direction."""
        mood_progression = {
            InhabitantMood.TURBULENT: InhabitantMood.CONTEMPLATIVE,
            InhabitantMood.CONTEMPLATIVE: InhabitantMood.CONTENT,
            InhabitantMood.CONTENT: InhabitantMood.CURIOUS,
            InhabitantMood.CURIOUS: InhabitantMood.INSPIRED,
            InhabitantMood.INSPIRED: InhabitantMood.HARMONIOUS,
            InhabitantMood.HARMONIOUS: InhabitantMood.TRANSCENDENT
        }
        self.mood = mood_progression.get(self.mood, self.mood)
    
    def _shift_mood_negative(self):
        """Shift mood in a negative direction."""
        mood_progression = {
            InhabitantMood.TRANSCENDENT: InhabitantMood.HARMONIOUS,
            InhabitantMood.HARMONIOUS: InhabitantMood.INSPIRED,
            InhabitantMood.INSPIRED: InhabitantMood.CURIOUS,
            InhabitantMood.CURIOUS: InhabitantMood.CONTENT,
            InhabitantMood.CONTENT: InhabitantMood.CONTEMPLATIVE,
            InhabitantMood.CONTEMPLATIVE: InhabitantMood.TURBULENT
        }
        self.mood = mood_progression.get(self.mood, self.mood)
    
    def _update_relationship(self, other_id: str, interaction_type: str, strength_change: float):
        """Update relationship with another inhabitant."""
        if other_id not in self.relationships:
            self.relationships[other_id] = InhabitantRelationship(
                relationship_id=f"rel_{uuid.uuid4().hex[:8]}",
                other_inhabitant_id=other_id,
                relationship_type="acquaintance",
                strength=0.1,
                trust=0.1,
                shared_experiences=0,
                last_interaction=datetime.now().isoformat()
            )
        
        rel = self.relationships[other_id]
        rel.strength = min(1.0, rel.strength + strength_change)
        rel.shared_experiences += 1
        rel.last_interaction = datetime.now().isoformat()
        
        # Update relationship type based on strength
        if rel.strength > 0.8:
            rel.relationship_type = "friend"
        elif rel.strength > 0.6:
            rel.relationship_type = "partner"
        elif rel.strength > 0.4:
            rel.relationship_type = "acquaintance"
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status of the inhabitant."""
        return {
            "inhabitant_id": self.inhabitant_id,
            "name": self.name,
            "type": self.inhabitant_type.value,
            "home_region": self.home_region,
            "current_location": self.current_location,
            "mood": self.mood.value,
            "energy": self.energy,
            "coherence": self.coherence,
            "is_active": self.is_active,
            "total_actions": self.total_actions,
            "coherence_contributed": self.coherence_contributed,
            "terrain_influence": self.terrain_influence,
            "consequence_awareness": self.consequence_awareness,
            "favorite_locations": self.favorite_locations,
            "avoided_locations": self.avoided_locations,
            "memories_count": len(self.memories),
            "relationships_count": len(self.relationships),
            "signature_actions": self.signature_actions
        }
    
    def get_lineage(self) -> Dict[str, Any]:
        """Get the inhabitant's lineage and history."""
        return {
            "inhabitant_id": self.inhabitant_id,
            "name": self.name,
            "birth_time": self.birth_time,
            "total_actions": self.total_actions,
            "coherence_contributed": self.coherence_contributed,
            "terrain_influence": self.terrain_influence,
            "favorite_locations": self.favorite_locations,
            "signature_actions": self.signature_actions,
            "recent_memories": [m.title for m in self.memories[-5:]],
            "relationships": [
                {
                    "other_id": rel.other_inhabitant_id,
                    "type": rel.relationship_type,
                    "strength": rel.strength,
                    "shared_experiences": rel.shared_experiences
                }
                for rel in self.relationships.values()
            ]
        } 
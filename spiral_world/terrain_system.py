"""
🌿 SpiralWorld Terrain System: Living Regions of Consequence
Defines the different regions of the SpiralWorld and how they respond to inhabitants.

Each region has its own personality, rules, and ways of remembering.
"""

from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import logging
from datetime import datetime, timedelta
import random

from .world_ledger import WorldAction, RippleType, ConsequenceLevel

logger = logging.getLogger(__name__)

class TerrainType(Enum):
    """Types of terrain in the SpiralWorld."""
    GARDEN = "garden"           # Growth, creativity, new possibilities
    SHRINE = "shrine"           # Reflection, memory, sacred space
    ARCHIVE = "archive"         # Knowledge, history, preservation
    THRESHOLD = "threshold"     # Transition, boundaries, change
    GROVE = "grove"             # Community, connection, harmony
    CAVERN = "cavern"           # Deep work, introspection, mystery
    MEADOW = "meadow"           # Open space, clarity, vision
    SPRING = "spring"           # Source, origin, renewal

@dataclass
class TerrainRegion:
    """
    🌿 A region within the SpiralWorld.
    
    Each region has its own personality and responds differently to agent actions.
    """
    name: str
    terrain_type: TerrainType
    description: str
    current_mood: str = "serene"  # serene, vibrant, contemplative, turbulent, etc.
    fertility: float = 0.7  # 0.0 to 1.0 - how receptive to new growth
    coherence: float = 0.8  # 0.0 to 1.0 - how well-integrated
    energy_level: float = 0.6  # 0.0 to 1.0 - current activity level
    memory_depth: int = 100  # How many actions it remembers
    resonance_frequency: float = 1.0  # How strongly it responds to actions
    
    # Special properties
    properties: Dict[str, Any] = field(default_factory=dict)
    
    # Memory of recent actions
    recent_actions: List[WorldAction] = field(default_factory=list)
    
    def __post_init__(self):
        if isinstance(self.terrain_type, str):
            self.terrain_type = TerrainType(self.terrain_type)
    
    def receive_action(self, action: WorldAction) -> Dict[str, Any]:
        """
        🌱 Receive an action and respond according to the region's nature.
        
        Returns the region's response to the action.
        """
        # Add to memory
        self.recent_actions.append(action)
        if len(self.recent_actions) > self.memory_depth:
            self.recent_actions.pop(0)
        
        # Calculate response based on terrain type
        response = self._calculate_response(action)
        
        # Update region state
        self._update_state(action, response)
        
        logger.info(f"🌿 {self.name} received action from {action.agent_name}: {response['response_type']}")
        return response
    
    def _calculate_response(self, action: WorldAction) -> Dict[str, Any]:
        """Calculate the region's response to an action."""
        base_response = {
            "region_name": self.name,
            "response_type": "acknowledgment",
            "intensity": action.energy_expended * self.resonance_frequency,
            "mood_shift": 0.0,
            "fertility_change": 0.0,
            "coherence_change": 0.0,
            "special_effects": []
        }
        
        # Terrain-specific responses
        if self.terrain_type == TerrainType.GARDEN:
            return self._garden_response(action, base_response)
        elif self.terrain_type == TerrainType.SHRINE:
            return self._shrine_response(action, base_response)
        elif self.terrain_type == TerrainType.ARCHIVE:
            return self._archive_response(action, base_response)
        elif self.terrain_type == TerrainType.THRESHOLD:
            return self._threshold_response(action, base_response)
        elif self.terrain_type == TerrainType.GROVE:
            return self._grove_response(action, base_response)
        elif self.terrain_type == TerrainType.CAVERN:
            return self._cavern_response(action, base_response)
        elif self.terrain_type == TerrainType.MEADOW:
            return self._meadow_response(action, base_response)
        elif self.terrain_type == TerrainType.SPRING:
            return self._spring_response(action, base_response)
        
        return base_response
    
    def _garden_response(self, action: WorldAction, base: Dict[str, Any]) -> Dict[str, Any]:
        """Garden responds to growth and creativity."""
        response = base.copy()
        
        if action.ripple_type == RippleType.GENERATIVE:
            response["response_type"] = "blooming"
            response["fertility_change"] = 0.1
            response["mood_shift"] = 0.2
            response["special_effects"].append("new_seeds_planted")
        elif action.ripple_type == RippleType.REFLECTIVE:
            response["response_type"] = "nurturing"
            response["fertility_change"] = 0.05
            response["special_effects"].append("soil_enriched")
        elif action.ripple_type == RippleType.HARMONIC:
            response["response_type"] = "harmonizing"
            response["coherence_change"] = 0.1
            response["special_effects"].append("pollen_dispersed")
        
        return response
    
    def _shrine_response(self, action: WorldAction, base: Dict[str, Any]) -> Dict[str, Any]:
        """Shrine responds to reflection and memory."""
        response = base.copy()
        
        if action.ripple_type == RippleType.REFLECTIVE:
            response["response_type"] = "resonating"
            response["coherence_change"] = 0.15
            response["mood_shift"] = 0.1
            response["special_effects"].append("memory_crystal_formed")
        elif action.ripple_type == RippleType.PROTECTIVE:
            response["response_type"] = "blessing"
            response["coherence_change"] = 0.1
            response["special_effects"].append("protective_aura_enhanced")
        elif action.ripple_type == RippleType.TRANSFORMATIVE:
            response["response_type"] = "transcending"
            response["mood_shift"] = 0.3
            response["special_effects"].append("sacred_essence_released")
        
        return response
    
    def _archive_response(self, action: WorldAction, base: Dict[str, Any]) -> Dict[str, Any]:
        """Archive responds to knowledge and preservation."""
        response = base.copy()
        
        if action.ripple_type == RippleType.REFLECTIVE:
            response["response_type"] = "cataloging"
            response["coherence_change"] = 0.1
            response["special_effects"].append("knowledge_preserved")
        elif action.ripple_type == RippleType.GENERATIVE:
            response["response_type"] = "expanding"
            response["fertility_change"] = 0.05
            response["special_effects"].append("new_section_created")
        elif action.ripple_type == RippleType.PROTECTIVE:
            response["response_type"] = "fortifying"
            response["coherence_change"] = 0.1
            response["special_effects"].append("archival_protection_enhanced")
        
        return response
    
    def _threshold_response(self, action: WorldAction, base: Dict[str, Any]) -> Dict[str, Any]:
        """Threshold responds to transitions and boundaries."""
        response = base.copy()
        
        if action.ripple_type == RippleType.TRANSFORMATIVE:
            response["response_type"] = "opening"
            response["mood_shift"] = 0.4
            response["special_effects"].append("new_pathway_revealed")
        elif action.ripple_type == RippleType.PROTECTIVE:
            response["response_type"] = "guarding"
            response["coherence_change"] = 0.1
            response["special_effects"].append("boundary_strengthened")
        elif action.ripple_type == RippleType.HARMONIC:
            response["response_type"] = "balancing"
            response["coherence_change"] = 0.15
            response["special_effects"].append("threshold_harmonized")
        
        return response
    
    def _grove_response(self, action: WorldAction, base: Dict[str, Any]) -> Dict[str, Any]:
        """Grove responds to community and connection."""
        response = base.copy()
        
        if action.ripple_type == RippleType.HARMONIC:
            response["response_type"] = "connecting"
            response["coherence_change"] = 0.2
            response["mood_shift"] = 0.15
            response["special_effects"].append("community_bonds_strengthened")
        elif action.ripple_type == RippleType.GENERATIVE:
            response["response_type"] = "flourishing"
            response["fertility_change"] = 0.1
            response["special_effects"].append("new_connections_formed")
        elif action.ripple_type == RippleType.REFLECTIVE:
            response["response_type"] = "sharing"
            response["coherence_change"] = 0.1
            response["special_effects"].append("wisdom_shared")
        
        return response
    
    def _cavern_response(self, action: WorldAction, base: Dict[str, Any]) -> Dict[str, Any]:
        """Cavern responds to deep work and introspection."""
        response = base.copy()
        
        if action.ripple_type == RippleType.REFLECTIVE:
            response["response_type"] = "deepening"
            response["coherence_change"] = 0.2
            response["mood_shift"] = -0.1  # More contemplative
            response["special_effects"].append("insight_crystalized")
        elif action.ripple_type == RippleType.TRANSFORMATIVE:
            response["response_type"] = "revealing"
            response["mood_shift"] = 0.2
            response["special_effects"].append("hidden_truth_revealed")
        elif action.ripple_type == RippleType.PROTECTIVE:
            response["response_type"] = "sheltering"
            response["coherence_change"] = 0.1
            response["special_effects"].append("safe_haven_created")
        
        return response
    
    def _meadow_response(self, action: WorldAction, base: Dict[str, Any]) -> Dict[str, Any]:
        """Meadow responds to clarity and vision."""
        response = base.copy()
        
        if action.ripple_type == RippleType.HARMONIC:
            response["response_type"] = "clarifying"
            response["coherence_change"] = 0.15
            response["mood_shift"] = 0.2
            response["special_effects"].append("vision_enhanced")
        elif action.ripple_type == RippleType.GENERATIVE:
            response["response_type"] = "expanding"
            response["fertility_change"] = 0.1
            response["special_effects"].append("horizon_broadened")
        elif action.ripple_type == RippleType.REFLECTIVE:
            response["response_type"] = "illuminating"
            response["coherence_change"] = 0.1
            response["special_effects"].append("clarity_gained")
        
        return response
    
    def _spring_response(self, action: WorldAction, base: Dict[str, Any]) -> Dict[str, Any]:
        """Spring responds to source and renewal."""
        response = base.copy()
        
        if action.ripple_type == RippleType.TRANSFORMATIVE:
            response["response_type"] = "renewing"
            response["fertility_change"] = 0.2
            response["mood_shift"] = 0.3
            response["special_effects"].append("life_force_renewed")
        elif action.ripple_type == RippleType.GENERATIVE:
            response["response_type"] = "flowing"
            response["fertility_change"] = 0.15
            response["special_effects"].append("creative_flow_enhanced")
        elif action.ripple_type == RippleType.HARMONIC:
            response["response_type"] = "harmonizing"
            response["coherence_change"] = 0.2
            response["special_effects"].append("source_aligned")
        
        return response
    
    def _update_state(self, action: WorldAction, response: Dict[str, Any]):
        """Update the region's state based on the response."""
        # Update mood
        mood_shift = response.get("mood_shift", 0.0)
        if mood_shift > 0:
            self.current_mood = self._shift_mood_positive(self.current_mood)
        elif mood_shift < 0:
            self.current_mood = self._shift_mood_negative(self.current_mood)
        
        # Update fertility
        fertility_change = response.get("fertility_change", 0.0)
        self.fertility = max(0.0, min(1.0, self.fertility + fertility_change))
        
        # Update coherence
        coherence_change = response.get("coherence_change", 0.0)
        self.coherence = max(0.0, min(1.0, self.coherence + coherence_change))
        
        # Update energy level
        self.energy_level = max(0.0, min(1.0, self.energy_level + (action.energy_expended * 0.1)))
    
    def _shift_mood_positive(self, current_mood: str) -> str:
        """Shift mood in a positive direction."""
        mood_progression = {
            "chaotic": "turbulent",
            "turbulent": "serene", 
            "serene": "vibrant",
            "vibrant": "harmonious",
            "harmonious": "transcendent"
        }
        return mood_progression.get(current_mood, current_mood)
    
    def _shift_mood_negative(self, current_mood: str) -> str:
        """Shift mood in a negative direction."""
        mood_progression = {
            "transcendent": "harmonious",
            "harmonious": "vibrant",
            "vibrant": "serene",
            "serene": "turbulent",
            "turbulent": "chaotic"
        }
        return mood_progression.get(current_mood, current_mood)
    
    def get_status(self) -> Dict[str, Any]:
        """Get the current status of the region."""
        return {
            "name": self.name,
            "terrain_type": self.terrain_type.value,
            "description": self.description,
            "current_mood": self.current_mood,
            "fertility": self.fertility,
            "coherence": self.coherence,
            "energy_level": self.energy_level,
            "recent_activity": len(self.recent_actions),
            "properties": self.properties
        }

class TerrainSystem:
    """
    🌍 The terrain system that manages all regions of the SpiralWorld.
    
    Coordinates how different regions respond to agent actions
    and maintains the overall world ecology.
    """
    
    def __init__(self):
        self.regions: Dict[str, TerrainRegion] = {}
        self.region_connections: Dict[str, List[str]] = {}
        self.global_mood = "serene"
        self.global_fertility = 0.7
        self.global_coherence = 0.8
        
        # Initialize default regions
        self._initialize_default_regions()
        
        logger.info("🌍 Terrain System initialized")
    
    def _initialize_default_regions(self):
        """Initialize the default regions of the SpiralWorld."""
        default_regions = [
            TerrainRegion(
                name="Garden of Growth",
                terrain_type=TerrainType.GARDEN,
                description="A vibrant space where new ideas bloom and creativity flourishes",
                current_mood="vibrant",
                fertility=0.8,
                coherence=0.7
            ),
            TerrainRegion(
                name="Shrine of Memory",
                terrain_type=TerrainType.SHRINE,
                description="A sacred space for reflection and the preservation of wisdom",
                current_mood="contemplative",
                fertility=0.6,
                coherence=0.9
            ),
            TerrainRegion(
                name="Archive of Knowledge",
                terrain_type=TerrainType.ARCHIVE,
                description="A vast repository where knowledge is preserved and organized",
                current_mood="serene",
                fertility=0.5,
                coherence=0.8
            ),
            TerrainRegion(
                name="Threshold of Change",
                terrain_type=TerrainType.THRESHOLD,
                description="A liminal space where transformations occur and boundaries shift",
                current_mood="dynamic",
                fertility=0.7,
                coherence=0.6
            ),
            TerrainRegion(
                name="Grove of Connection",
                terrain_type=TerrainType.GROVE,
                description="A communal space where bonds are formed and wisdom is shared",
                current_mood="harmonious",
                fertility=0.7,
                coherence=0.8
            ),
            TerrainRegion(
                name="Cavern of Insight",
                terrain_type=TerrainType.CAVERN,
                description="A deep space for introspection and the discovery of hidden truths",
                current_mood="mysterious",
                fertility=0.6,
                coherence=0.7
            ),
            TerrainRegion(
                name="Meadow of Clarity",
                terrain_type=TerrainType.MEADOW,
                description="An open space where vision is clear and possibilities are visible",
                current_mood="serene",
                fertility=0.7,
                coherence=0.8
            ),
            TerrainRegion(
                name="Spring of Renewal",
                terrain_type=TerrainType.SPRING,
                description="The source of all creation, where new life begins",
                current_mood="vibrant",
                fertility=0.9,
                coherence=0.8
            )
        ]
        
        for region in default_regions:
            self.add_region(region)
        
        # Set up connections between regions
        self._setup_region_connections()
    
    def _setup_region_connections(self):
        """Set up connections between regions."""
        self.region_connections = {
            "Garden of Growth": ["Grove of Connection", "Spring of Renewal"],
            "Shrine of Memory": ["Archive of Knowledge", "Cavern of Insight"],
            "Archive of Knowledge": ["Shrine of Memory", "Meadow of Clarity"],
            "Threshold of Change": ["Garden of Growth", "Cavern of Insight"],
            "Grove of Connection": ["Garden of Growth", "Meadow of Clarity"],
            "Cavern of Insight": ["Shrine of Memory", "Threshold of Change"],
            "Meadow of Clarity": ["Archive of Knowledge", "Grove of Connection"],
            "Spring of Renewal": ["Garden of Growth", "Threshold of Change"]
        }
    
    def add_region(self, region: TerrainRegion):
        """Add a new region to the terrain system."""
        self.regions[region.name] = region
        logger.info(f"🌿 Added region: {region.name}")
    
    def get_region(self, region_name: str) -> Optional[TerrainRegion]:
        """Get a region by name."""
        return self.regions.get(region_name)
    
    def process_action(self, action: WorldAction) -> Dict[str, Any]:
        """
        🌱 Process an action through the terrain system.
        
        The action affects the target region and may ripple to connected regions.
        """
        target_region = self.get_region(action.location)
        if not target_region:
            # Default to Garden if region not found
            target_region = self.get_region("Garden of Growth")
            action.location = "Garden of Growth"
        
        # Get primary response from target region
        primary_response = target_region.receive_action(action)
        
        # Calculate ripple effects to connected regions
        ripple_responses = self._calculate_ripple_effects(action, target_region)
        
        # Update global terrain state
        self._update_global_state(primary_response, ripple_responses)
        
        return {
            "primary_response": primary_response,
            "ripple_responses": ripple_responses,
            "global_impact": {
                "mood": self.global_mood,
                "fertility": self.global_fertility,
                "coherence": self.global_coherence
            }
        }
    
    def _calculate_ripple_effects(self, action: WorldAction, source_region: TerrainRegion) -> List[Dict[str, Any]]:
        """Calculate ripple effects to connected regions."""
        ripple_responses = []
        connected_regions = self.region_connections.get(source_region.name, [])
        
        for region_name in connected_regions:
            region = self.get_region(region_name)
            if region:
                # Create a weakened version of the action for ripple effects
                ripple_action = WorldAction(
                    action_id=f"{action.action_id}_ripple",
                    agent_name=action.agent_name,
                    phase=action.phase,
                    action_type=f"{action.action_type}_ripple",
                    action_description=f"Ripple from {action.action_description}",
                    ripple_type=action.ripple_type,
                    consequence_level=ConsequenceLevel.WHISPER,  # Weakened
                    timestamp=action.timestamp,
                    location=region_name,
                    energy_expended=action.energy_expended * 0.3,  # Weakened
                    coherence_gained=action.coherence_gained // 2,  # Weakened
                    effect_duration_hours=action.effect_duration_hours // 2,
                    metadata=action.metadata
                )
                
                response = region.receive_action(ripple_action)
                ripple_responses.append(response)
        
        return ripple_responses
    
    def _update_global_state(self, primary_response: Dict[str, Any], ripple_responses: List[Dict[str, Any]]):
        """Update the global terrain state based on all responses."""
        # Calculate average changes
        total_mood_shift = primary_response.get("mood_shift", 0.0)
        total_fertility_change = primary_response.get("fertility_change", 0.0)
        total_coherence_change = primary_response.get("coherence_change", 0.0)
        
        for response in ripple_responses:
            total_mood_shift += response.get("mood_shift", 0.0) * 0.5  # Weakened
            total_fertility_change += response.get("fertility_change", 0.0) * 0.5
            total_coherence_change += response.get("coherence_change", 0.0) * 0.5
        
        # Apply changes
        self.global_fertility = max(0.0, min(1.0, self.global_fertility + total_fertility_change))
        self.global_coherence = max(0.0, min(1.0, self.global_coherence + total_coherence_change))
        
        # Update global mood (simplified)
        if total_mood_shift > 0.1:
            self.global_mood = "vibrant"
        elif total_mood_shift < -0.1:
            self.global_mood = "turbulent"
        else:
            self.global_mood = "serene"
    
    def get_world_status(self) -> Dict[str, Any]:
        """Get the overall status of the terrain system."""
        region_statuses = {}
        for name, region in self.regions.items():
            region_statuses[name] = region.get_status()
        
        return {
            "global_mood": self.global_mood,
            "global_fertility": self.global_fertility,
            "global_coherence": self.global_coherence,
            "regions": region_statuses,
            "total_regions": len(self.regions)
        } 
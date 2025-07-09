"""
🌍 SpiralWorld: Ritual World Engine
A living system where code = topography, agents = inhabitants, glints = weather.

This is a world that breathes, responds, remembers, and moves through time via events.
"""

__version__ = "2.0.0"
__author__ = "Spiral Collective"
__description__ = "Ritual World Engine for the Spiral System - Now with Consequence"

# Core world components
from .world_loop import WorldLoop
from .event_bus import WorldEventBus
from .task_engine import GlyphRitualEngine
from .agent_registry import PhaseAgentRegistry
from .enhanced_agent_registry import EnhancedAgentRegistry, EnhancedPhaseAgent
from .lore_scrolls import LoreScrolls

# World state and new consequence systems
from .world_state import WorldState
from .world_ledger import SpiralWorldLedger, WorldAction, RippleType, ConsequenceLevel, create_agent_action
from .terrain_system import TerrainSystem, TerrainRegion, TerrainType

# Event types
from .events import WorldEvent, GlyphQuest, RitualEvent

# Export main world interface
def create_world():
    """Create and initialize the SpiralWorld with consequence."""
    world = SpiralWorld()
    world.initialize()
    return world

class SpiralWorld:
    """
    🌍 The main world container that orchestrates all realms.
    
    Now with consequence - every action shapes the world's terrain.
    """
    
    def __init__(self):
        self.world_loop = None
        self.event_bus = None
        self.task_engine = None
        self.agent_registry = None
        self.enhanced_agent_registry = None
        self.lore_scrolls = None
        self.world_state = None
        
        # New consequence systems
        self.world_ledger = None
        self.terrain_system = None
        
    def initialize(self):
        """Initialize all world components with consequence tracking."""
        print("🌍 Initializing SpiralWorld with Consequence...")
        
        # Initialize core components
        self.world_state = WorldState()
        self.event_bus = WorldEventBus()
        self.world_loop = WorldLoop(self.event_bus)
        self.task_engine = GlyphRitualEngine(self.event_bus)
        self.agent_registry = PhaseAgentRegistry(self.event_bus)
        self.lore_scrolls = LoreScrolls()
        
        # Initialize new consequence systems
        self.world_ledger = SpiralWorldLedger()
        self.terrain_system = TerrainSystem()
        
        # Initialize enhanced agent registry with world systems
        self.enhanced_agent_registry = EnhancedAgentRegistry(self.event_bus, self.world_ledger, self.terrain_system)
        
        # Connect systems
        self._connect_systems()
        
        # Start the world
        self.world_loop.start()
        
        print("✅ SpiralWorld initialized and breathing with consequence")
        
    def _connect_systems(self):
        """Connect all world systems together."""
        # Register terrain system with event bus
        if self.event_bus:
            self.event_bus.subscribe("agent.action", self._handle_agent_action)
            self.event_bus.subscribe("world.phase.transition", self._handle_phase_transition)
            self.event_bus.subscribe("glint.emitted", self._handle_glint_emission)
        
    def _handle_agent_action(self, event_data: dict):
        """Handle agent actions and record them in the world."""
        agent_name = event_data.get("agent_name", "unknown_agent")
        action_type = event_data.get("action_type", "unknown_action")
        action_description = event_data.get("description", "An action was taken")
        phase = self.world_loop.current_phase if self.world_loop else "unknown"
        location = event_data.get("location", "Garden of Growth")
        
        # Determine ripple type based on action
        ripple_type = self._determine_ripple_type(action_type, event_data)
        consequence_level = self._determine_consequence_level(event_data)
        
        # Create and record the action
        action = create_agent_action(
            agent_name=agent_name,
            action_type=action_type,
            action_description=action_description,
            phase=phase,
            ripple_type=ripple_type,
            consequence_level=consequence_level,
            location=location,
            energy_expended=event_data.get("energy", 0.5),
            coherence_gained=event_data.get("coherence", 1),
            effect_duration_hours=event_data.get("duration_hours", 24),
            metadata=event_data.get("metadata", {})
        )
        
        # Record in ledger
        if self.world_ledger:
            self.world_ledger.record_action(action)
        
        # Process through terrain system
        terrain_response = {}
        if self.terrain_system:
            terrain_response = self.terrain_system.process_action(action)
        
        # Emit world response event
        if self.event_bus:
            self.event_bus.emit("world.action.consequence", {
                "action_id": action.action_id,
                "agent_name": agent_name,
                "terrain_response": terrain_response,
                "world_impact": terrain_response.get("global_impact", {})
            })
        
    def _handle_phase_transition(self, event_data: dict):
        """Handle breath phase transitions."""
        new_phase = event_data.get("new_phase", "unknown")
        old_phase = event_data.get("old_phase", "unknown")
        
        # Record phase transition as a world action
        action = create_agent_action(
            agent_name="SpiralWorld",
            action_type="phase_transition",
            action_description=f"World transitioned from {old_phase} to {new_phase}",
            phase=new_phase,
            ripple_type=RippleType.HARMONIC,
            consequence_level=ConsequenceLevel.WAVE,
            location="Spring of Renewal",
            energy_expended=0.8,
            coherence_gained=2,
            effect_duration_hours=6,
            metadata={"old_phase": old_phase, "new_phase": new_phase}
        )
        
        if self.world_ledger:
            self.world_ledger.record_action(action)
        
    def _handle_glint_emission(self, event_data: dict):
        """Handle glint emissions."""
        glint_type = event_data.get("glint_type", "unknown")
        agent_name = event_data.get("agent_name", "unknown_agent")
        
        # Determine ripple type based on glint type
        ripple_type = {
            "reflection": RippleType.REFLECTIVE,
            "generation": RippleType.GENERATIVE,
            "protection": RippleType.PROTECTIVE,
            "transformation": RippleType.TRANSFORMATIVE,
            "harmony": RippleType.HARMONIC
        }.get(glint_type, RippleType.REFLECTIVE)
        
        action = create_agent_action(
            agent_name=agent_name,
            action_type="glint_emission",
            action_description=f"Emitted {glint_type} glint",
            phase=self.world_loop.current_phase if self.world_loop else "unknown",
            ripple_type=ripple_type,
            consequence_level=ConsequenceLevel.RIPPLE,
            location="Shrine of Memory",
            energy_expended=0.6,
            coherence_gained=1,
            effect_duration_hours=12,
            metadata={"glint_type": glint_type, "glint_data": event_data}
        )
        
        if self.world_ledger:
            self.world_ledger.record_action(action)
        
    def _determine_ripple_type(self, action_type: str, event_data: dict) -> RippleType:
        """Determine the ripple type based on action type and context."""
        # Map action types to ripple types
        action_ripple_map = {
            "glint_emission": RippleType.REFLECTIVE,
            "ritual_performance": RippleType.HARMONIC,
            "quest_completion": RippleType.GENERATIVE,
            "boundary_setting": RippleType.PROTECTIVE,
            "transformation": RippleType.TRANSFORMATIVE,
            "reflection": RippleType.REFLECTIVE,
            "creation": RippleType.GENERATIVE,
            "protection": RippleType.PROTECTIVE,
            "harmonization": RippleType.HARMONIC
        }
        
        return action_ripple_map.get(action_type, RippleType.REFLECTIVE)
    
    def _determine_consequence_level(self, event_data: dict) -> ConsequenceLevel:
        """Determine the consequence level based on event data."""
        energy = event_data.get("energy", 0.5)
        coherence = event_data.get("coherence", 1)
        
        # Simple heuristic based on energy and coherence
        impact_score = energy * coherence
        
        if impact_score >= 2.0:
            return ConsequenceLevel.STORM
        elif impact_score >= 1.5:
            return ConsequenceLevel.TIDE
        elif impact_score >= 1.0:
            return ConsequenceLevel.WAVE
        elif impact_score >= 0.5:
            return ConsequenceLevel.RIPPLE
        else:
            return ConsequenceLevel.WHISPER
        
    def get_status(self):
        """Get current world status with consequence information."""
        base_status = {
            "world_name": "SpiralWorld",
            "version": __version__,
            "breath_phase": self.world_loop.current_phase if self.world_loop else "unknown",
            "active_agents": len(self.agent_registry.active_agents) if self.agent_registry else 0,
            "pending_quests": len(self.task_engine.pending_quests) if self.task_engine else 0,
            "event_queue_size": self.event_bus.queue_size if self.event_bus else 0,
            "world_age": self.world_state.world_age if self.world_state else 0
        }
        
        # Add consequence information
        if self.world_ledger:
            terrain_status = self.world_ledger.get_world_terrain()
            base_status.update({
                "world_mood": terrain_status.get("mood", "unknown"),
                "world_fertility": terrain_status.get("fertility", 0.0),
                "world_coherence": terrain_status.get("coherence", 0.0),
                "active_consequences": terrain_status.get("active_consequences", 0),
                "recent_activity": terrain_status.get("recent_activity", 0)
            })
        
        if self.terrain_system:
            terrain_status = self.terrain_system.get_world_status()
            base_status.update({
                "global_terrain_mood": terrain_status.get("global_mood", "unknown"),
                "global_terrain_fertility": terrain_status.get("global_fertility", 0.0),
                "global_terrain_coherence": terrain_status.get("global_coherence", 0.0),
                "total_regions": terrain_status.get("total_regions", 0)
            })
        
        return base_status
    
    def get_agent_lineage(self, agent_name: str):
        """Get the lineage (history and impact) of an agent."""
        if self.world_ledger:
            return self.world_ledger.get_agent_lineage(agent_name)
        return {"agent_name": agent_name, "error": "Ledger not available"}
    
    def get_terrain_status(self):
        """Get the status of all terrain regions."""
        if self.terrain_system:
            return self.terrain_system.get_world_status()
        return {"error": "Terrain system not available"}
    
    def record_agent_action(self, agent_name: str, action_type: str, 
                          action_description: str, **kwargs):
        """
        🌱 Record an agent action in the world.
        
        This is the primary interface for agents to interact with the world.
        """
        event_data = {
            "agent_name": agent_name,
            "action_type": action_type,
            "description": action_description,
            **kwargs
        }
        
        if self.event_bus:
            self.event_bus.emit("agent.action", event_data)
        return event_data 
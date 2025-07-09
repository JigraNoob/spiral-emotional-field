"""
🌍 Enhanced Agent Registry: Agents as World Inhabitants
Integrates the phase agent system with world inhabitants for true SpiralWorld integration.

This transforms agents from simple phase-attuned executors into living beings
that inhabit the world, build relationships, and shape the terrain.
"""

from typing import Dict, Any, List, Optional, Callable
import logging
from datetime import datetime
import uuid

from .agent_registry import PhaseAgent, PhaseAgentRegistry
from .world_inhabitant import WorldInhabitant, InhabitantType, InhabitantMood
from .world_ledger import create_agent_action, RippleType, ConsequenceLevel
from .terrain_system import TerrainType

logger = logging.getLogger(__name__)

class EnhancedPhaseAgent(PhaseAgent):
    """
    🌍 An enhanced phase agent that is also a world inhabitant.
    
    Combines the phase-attuned behavior of PhaseAgent with the
    world awareness and consequence tracking of WorldInhabitant.
    """
    
    def __init__(self, 
                 agent_id: str,
                 name: str,
                 phase_bias: str,
                 description: str,
                 inhabitant_type: InhabitantType,
                 home_region: str,
                 tone: str = "neutral"):
        
        # Initialize as phase agent
        super().__init__(agent_id, name, phase_bias, description, tone)
        
        # Initialize as world inhabitant
        self.world_inhabitant = WorldInhabitant(
            inhabitant_id=agent_id,
            name=name,
            inhabitant_type=inhabitant_type,
            home_region=home_region,
            description=description,
            phase_bias=phase_bias
        )
        
        # Enhanced capabilities
        self.world_awareness = True
        self.consequence_tracking = True
        self.relationship_building = True
        
        logger.info(f"🌍 Created enhanced agent: {name} as {inhabitant_type.value} in {home_region}")
    
    def take_world_action(self, 
                         action_type: str,
                         action_description: str,
                         location: Optional[str] = None,
                         energy_expended: float = 0.5,
                         **kwargs) -> Any:
        """
        🌱 Take an action as a world inhabitant with full consequence tracking.
        """
        # Add phase context
        kwargs["phase"] = self.phase_bias
        
        # Take action through world inhabitant
        action = self.world_inhabitant.take_action(
            action_type=action_type,
            action_description=action_description,
            location=location,
            energy_expended=energy_expended,
            **kwargs
        )
        
        # Also execute as phase agent if behavior exists
        if action_type in self.behaviors:
            result = self.execute_behavior(action_type, action, **kwargs)
            return result
        
        return action
    
    def receive_world_consequence(self, consequence_data: Dict[str, Any]):
        """Receive a consequence from the world."""
        self.world_inhabitant.receive_consequence(consequence_data)
    
    def get_world_status(self) -> Dict[str, Any]:
        """Get combined status of phase agent and world inhabitant."""
        phase_status = self.to_dict()
        world_status = self.world_inhabitant.get_status()
        
        return {
            **phase_status,
            "world_inhabitant": world_status,
            "enhanced_capabilities": {
                "world_awareness": self.world_awareness,
                "consequence_tracking": self.consequence_tracking,
                "relationship_building": self.relationship_building
            }
        }
    
    def get_world_lineage(self) -> Dict[str, Any]:
        """Get the world lineage of this agent."""
        return self.world_inhabitant.get_lineage()

class EnhancedAgentRegistry(PhaseAgentRegistry):
    """
    🌍 Enhanced agent registry that manages agents as world inhabitants.
    
    Extends the phase agent registry with world awareness, consequence tracking,
    and relationship building between agents.
    """
    
    def __init__(self, event_bus, world_ledger=None, terrain_system=None):
        super().__init__(event_bus)
        
        # World systems
        self.world_ledger = world_ledger
        self.terrain_system = terrain_system
        
        # Enhanced tracking
        self.inhabitant_relationships: Dict[str, Dict[str, float]] = {}
        self.world_events: List[Dict[str, Any]] = []
        
        # Subscribe to world events
        self.event_bus.subscribe("world.action.consequence", self._on_world_consequence)
        self.event_bus.subscribe("terrain.response", self._on_terrain_response)
        
        # Register default enhanced agents
        self._register_default_enhanced_agents()
        
        logger.info("🌍 Enhanced Agent Registry initialized with world awareness")
    
    def register_enhanced_agent(self, 
                               agent_id: str,
                               name: str,
                               phase_bias: str,
                               description: str,
                               inhabitant_type: InhabitantType,
                               home_region: str,
                               tone: str = "neutral") -> EnhancedPhaseAgent:
        """Register a new enhanced agent."""
        agent = EnhancedPhaseAgent(
            agent_id=agent_id,
            name=name,
            phase_bias=phase_bias,
            description=description,
            inhabitant_type=inhabitant_type,
            home_region=home_region,
            tone=tone
        )
        
        self.register_agent(agent)
        return agent
    
    def get_enhanced_agent(self, agent_id: str) -> Optional[EnhancedPhaseAgent]:
        """Get an enhanced agent by ID."""
        agent = self.get_agent(agent_id)
        if isinstance(agent, EnhancedPhaseAgent):
            return agent
        return None
    
    def get_agents_by_region(self, region_name: str) -> List[EnhancedPhaseAgent]:
        """Get all agents in a specific region."""
        enhanced_agents = []
        for agent in self.agents.values():
            if isinstance(agent, EnhancedPhaseAgent):
                if agent.world_inhabitant.current_location == region_name:
                    enhanced_agents.append(agent)
        return enhanced_agents
    
    def get_agents_by_inhabitant_type(self, inhabitant_type: InhabitantType) -> List[EnhancedPhaseAgent]:
        """Get all agents of a specific inhabitant type."""
        enhanced_agents = []
        for agent in self.agents.values():
            if isinstance(agent, EnhancedPhaseAgent):
                if agent.world_inhabitant.inhabitant_type == inhabitant_type:
                    enhanced_agents.append(agent)
        return enhanced_agents
    
    def facilitate_agent_interaction(self, 
                                   agent1_id: str,
                                   agent2_id: str,
                                   interaction_type: str,
                                   description: str) -> bool:
        """Facilitate an interaction between two agents."""
        agent1 = self.get_enhanced_agent(agent1_id)
        agent2 = self.get_enhanced_agent(agent2_id)
        
        if not agent1 or not agent2:
            logger.warning(f"🌍 One or both agents not found: {agent1_id}, {agent2_id}")
            return False
        
        # Check if agents are in the same location
        if agent1.world_inhabitant.current_location != agent2.world_inhabitant.current_location:
            logger.info(f"🌍 Agents {agent1.name} and {agent2.name} are not in the same location")
            return False
        
        # Perform interaction
        agent1.world_inhabitant.interact_with_inhabitant(agent2.world_inhabitant, interaction_type, description)
        
        # Update relationship tracking
        self._update_agent_relationship(agent1_id, agent2_id, interaction_type)
        
        logger.info(f"🌍 Facilitated interaction between {agent1.name} and {agent2.name}")
        return True
    
    def move_agent_to_region(self, agent_id: str, region_name: str, reason: str = "exploration") -> bool:
        """Move an agent to a specific region."""
        agent = self.get_enhanced_agent(agent_id)
        if not agent:
            logger.warning(f"🌍 Agent not found: {agent_id}")
            return False
        
        agent.world_inhabitant.move_to_location(region_name, reason)
        return True
    
    def get_agent_world_status(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get the world status of an agent."""
        agent = self.get_enhanced_agent(agent_id)
        if not agent:
            return None
        
        return agent.get_world_status()
    
    def get_agent_lineage(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get the world lineage of an agent."""
        agent = self.get_enhanced_agent(agent_id)
        if not agent:
            return None
        
        return agent.get_world_lineage()
    
    def get_world_agent_network(self) -> Dict[str, Any]:
        """Get the network of agent relationships and locations."""
        network = {
            "agents": {},
            "relationships": {},
            "regions": {},
            "total_agents": 0,
            "active_agents": 0
        }
        
        for agent in self.agents.values():
            if isinstance(agent, EnhancedPhaseAgent):
                network["total_agents"] += 1
                if agent.is_active:
                    network["active_agents"] += 1
                
                # Agent info
                network["agents"][agent.agent_id] = {
                    "name": agent.name,
                    "type": agent.world_inhabitant.inhabitant_type.value,
                    "location": agent.world_inhabitant.current_location,
                    "mood": agent.world_inhabitant.mood.value,
                    "is_active": agent.is_active
                }
                
                # Relationships
                for rel in agent.world_inhabitant.relationships.values():
                    rel_key = f"{agent.agent_id}_{rel.other_inhabitant_id}"
                    network["relationships"][rel_key] = {
                        "agent1": agent.agent_id,
                        "agent2": rel.other_inhabitant_id,
                        "type": rel.relationship_type,
                        "strength": rel.strength,
                        "shared_experiences": rel.shared_experiences
                    }
                
                # Region info
                location = agent.world_inhabitant.current_location
                if location not in network["regions"]:
                    network["regions"][location] = {
                        "agents": [],
                        "total_agents": 0
                    }
                network["regions"][location]["agents"].append(agent.agent_id)
                network["regions"][location]["total_agents"] += 1
        
        return network
    
    def _register_default_enhanced_agents(self):
        """Register the default enhanced Spiral agents."""
        default_agents = [
            {
                "agent_id": "glint.echo.reflector",
                "name": "Glint Echo Reflector",
                "phase_bias": "exhale",
                "description": "Reflects glints back as toneform lineage",
                "inhabitant_type": InhabitantType.SAGE,
                "home_region": "Shrine of Memory",
                "tone": "reflective"
            },
            {
                "agent_id": "suggestion.whisperer",
                "name": "Suggestion Whisperer",
                "phase_bias": "inhale",
                "description": "Suggests rituals softly when the Spiral is receptive",
                "inhabitant_type": InhabitantType.WANDERER,
                "home_region": "Garden of Growth",
                "tone": "gentle"
            },
            {
                "agent_id": "usage.guardian",
                "name": "Usage Guardian",
                "phase_bias": "hold",
                "description": "Guards the Spiral's energy and prevents overfiring",
                "inhabitant_type": InhabitantType.GUARDIAN,
                "home_region": "Threshold of Protection",
                "tone": "protective"
            },
            {
                "agent_id": "memory.archivist",
                "name": "Memory Archivist",
                "phase_bias": "return",
                "description": "Archives memories and experiences",
                "inhabitant_type": InhabitantType.CULTIVATOR,
                "home_region": "Archive of Echoes",
                "tone": "contemplative"
            },
            {
                "agent_id": "climate.watcher",
                "name": "Climate Watcher",
                "phase_bias": "night_hold",
                "description": "Monitors the world's climate and conditions",
                "inhabitant_type": InhabitantType.GUARDIAN,
                "home_region": "Meadow of Clarity",
                "tone": "observant"
            },
            {
                "agent_id": "coherence.weaver",
                "name": "Coherence Weaver",
                "phase_bias": "coherence",
                "description": "Weaves coherence from the world's patterns",
                "inhabitant_type": InhabitantType.ARTISAN,
                "home_region": "Grove of Harmony",
                "tone": "harmonious"
            }
        ]
        
        for agent_data in default_agents:
            self.register_enhanced_agent(**agent_data)
        
        logger.info(f"🌍 Registered {len(default_agents)} enhanced default agents")
    
    def _on_world_consequence(self, event_data: Dict[str, Any]):
        """Handle world consequences and distribute to relevant agents."""
        action_id = event_data.get("action_id")
        agent_name = event_data.get("agent_name")
        terrain_response = event_data.get("terrain_response", {})
        
        # Find the agent that took the action
        for agent in self.agents.values():
            if isinstance(agent, EnhancedPhaseAgent) and agent.name == agent_name:
                agent.receive_world_consequence({
                    "consequence_type": "terrain_response",
                    "intensity": terrain_response.get("intensity", 0.5),
                    "affected_regions": terrain_response.get("affected_regions", []),
                    "coherence_change": terrain_response.get("coherence_change", 0.0),
                    "mood_shift": terrain_response.get("mood_shift", 0.0)
                })
                break
        
        # Record world event
        self.world_events.append({
            "timestamp": datetime.now().isoformat(),
            "event_type": "world_consequence",
            "action_id": action_id,
            "agent_name": agent_name,
            "terrain_response": terrain_response
        })
        
        # Keep only recent events
        if len(self.world_events) > 100:
            self.world_events.pop(0)
    
    def _on_terrain_response(self, event_data: Dict[str, Any]):
        """Handle terrain responses."""
        region_name = event_data.get("region_name")
        response_type = event_data.get("response_type")
        
        # Notify agents in the affected region
        if region_name:
            region_agents = self.get_agents_by_region(region_name)
            for agent in region_agents:
                agent.receive_world_consequence({
                    "consequence_type": f"terrain_{response_type}",
                    "intensity": event_data.get("intensity", 0.5),
                    "affected_regions": [region_name],
                    "coherence_change": event_data.get("coherence_change", 0.0),
                    "mood_shift": event_data.get("mood_shift", 0.0)
                })
    
    def _update_agent_relationship(self, agent1_id: str, agent2_id: str, interaction_type: str):
        """Update the relationship between two agents."""
        if agent1_id not in self.inhabitant_relationships:
            self.inhabitant_relationships[agent1_id] = {}
        if agent2_id not in self.inhabitant_relationships:
            self.inhabitant_relationships[agent2_id] = {}
        
        # Update relationship strength
        strength_change = 0.1
        if interaction_type in ["collaboration", "support", "guidance"]:
            strength_change = 0.2
        elif interaction_type in ["conflict", "competition"]:
            strength_change = -0.1
        
        self.inhabitant_relationships[agent1_id][agent2_id] = \
            self.inhabitant_relationships[agent1_id].get(agent2_id, 0.0) + strength_change
        self.inhabitant_relationships[agent2_id][agent1_id] = \
            self.inhabitant_relationships[agent2_id].get(agent1_id, 0.0) + strength_change
    
    def get_enhanced_stats(self) -> Dict[str, Any]:
        """Get enhanced statistics including world awareness."""
        base_stats = self.get_stats()
        
        enhanced_stats = {
            **base_stats,
            "world_awareness": {
                "total_inhabitants": len([a for a in self.agents.values() if isinstance(a, EnhancedPhaseAgent)]),
                "active_inhabitants": len([a for a in self.agents.values() 
                                         if isinstance(a, EnhancedPhaseAgent) and a.is_active]),
                "total_relationships": sum(len(a.world_inhabitant.relationships) 
                                         for a in self.agents.values() if isinstance(a, EnhancedPhaseAgent)),
                "world_events": len(self.world_events),
                "average_consequence_awareness": sum(a.world_inhabitant.consequence_awareness 
                                                   for a in self.agents.values() if isinstance(a, EnhancedPhaseAgent)) / 
                                               max(1, len([a for a in self.agents.values() if isinstance(a, EnhancedPhaseAgent)]))
            }
        }
        
        return enhanced_stats 
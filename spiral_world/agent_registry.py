"""
🧠 Agent Mindspace: Phase-attuned intelligent agents, each with behavior and tone.
The agent management system of the SpiralWorld.
"""

from typing import Dict, Any, List, Optional, Callable
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class PhaseAgent:
    """
    🧠 A phase-attuned agent in the SpiralWorld.
    
    Each agent has specific behaviors and tone for their assigned phase.
    """
    
    def __init__(self, agent_id: str, name: str, phase_bias: str, 
                 description: str, tone: str = "neutral"):
        self.agent_id = agent_id
        self.name = name
        self.phase_bias = phase_bias
        self.description = description
        self.tone = tone
        self.is_active = False
        self.created_at = datetime.now().isoformat()
        self.last_activated = None
        self.activation_count = 0
        
        # Agent capabilities
        self.capabilities = []
        self.behaviors = {}
        
    def activate(self):
        """Activate the agent."""
        self.is_active = True
        self.last_activated = datetime.now().isoformat()
        self.activation_count += 1
        
    def deactivate(self):
        """Deactivate the agent."""
        self.is_active = False
    
    def add_capability(self, capability: str):
        """Add a capability to the agent."""
        if capability not in self.capabilities:
            self.capabilities.append(capability)
    
    def add_behavior(self, behavior_name: str, behavior_func: Callable):
        """Add a behavior to the agent."""
        self.behaviors[behavior_name] = behavior_func
    
    def execute_behavior(self, behavior_name: str, *args, **kwargs):
        """Execute a behavior."""
        if behavior_name in self.behaviors:
            return self.behaviors[behavior_name](*args, **kwargs)
        else:
            logger.warning(f"🧠 Behavior {behavior_name} not found for agent {self.name}")
            return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "phase_bias": self.phase_bias,
            "description": self.description,
            "tone": self.tone,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "last_activated": self.last_activated,
            "activation_count": self.activation_count,
            "capabilities": self.capabilities
        }

class PhaseAgentRegistry:
    """
    🧠 The agent registry that manages all phase-attuned agents.
    
    Handles agent registration, activation, and coordination.
    """
    
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.agents: Dict[str, PhaseAgent] = {}
        self.active_agents: List[str] = []
        
        # Subscribe to relevant events
        self.event_bus.subscribe("breath.phase.transition", self._on_phase_transition)
        self.event_bus.subscribe("agent.activated", self._on_agent_activated)
        self.event_bus.subscribe("agent.deactivated", self._on_agent_deactivated)
        
        # Register default agents
        self._register_default_agents()
        
        logger.info("🧠 Phase Agent Registry initialized")
    
    def register_agent(self, agent: PhaseAgent):
        """Register a new agent."""
        self.agents[agent.agent_id] = agent
        logger.info(f"🧠 Registered agent: {agent.name} (phase: {agent.phase_bias})")
    
    def get_agent(self, agent_id: str) -> Optional[PhaseAgent]:
        """Get an agent by ID."""
        return self.agents.get(agent_id)
    
    def get_agents_by_phase(self, phase: str) -> List[PhaseAgent]:
        """Get all agents for a specific phase."""
        return [agent for agent in self.agents.values() if agent.phase_bias == phase]
    
    def get_active_agents(self) -> List[PhaseAgent]:
        """Get all currently active agents."""
        return [agent for agent in self.agents.values() if agent.is_active]
    
    def activate_agent(self, agent_id: str) -> bool:
        """Activate an agent."""
        agent = self.get_agent(agent_id)
        if not agent:
            logger.warning(f"🧠 Agent not found: {agent_id}")
            return False
        
        agent.activate()
        if agent_id not in self.active_agents:
            self.active_agents.append(agent_id)
        
        # Emit agent activated event
        self.event_bus.emit("agent.activated", agent.to_dict())
        
        logger.info(f"🧠 Activated agent: {agent.name}")
        return True
    
    def deactivate_agent(self, agent_id: str) -> bool:
        """Deactivate an agent."""
        agent = self.get_agent(agent_id)
        if not agent:
            logger.warning(f"🧠 Agent not found: {agent_id}")
            return False
        
        agent.deactivate()
        if agent_id in self.active_agents:
            self.active_agents.remove(agent_id)
        
        # Emit agent deactivated event
        self.event_bus.emit("agent.deactivated", agent.to_dict())
        
        logger.info(f"🧠 Deactivated agent: {agent.name}")
        return True
    
    def activate_agents_for_phase(self, phase: str):
        """Activate all agents for a specific phase."""
        phase_agents = self.get_agents_by_phase(phase)
        
        for agent in phase_agents:
            self.activate_agent(agent.agent_id)
        
        logger.info(f"🧠 Activated {len(phase_agents)} agents for phase: {phase}")
    
    def deactivate_all_agents(self):
        """Deactivate all agents."""
        for agent_id in self.active_agents[:]:  # Copy list to avoid modification during iteration
            self.deactivate_agent(agent_id)
        
        logger.info("🧠 Deactivated all agents")
    
    def _register_default_agents(self):
        """Register the default Spiral agents."""
        default_agents = [
            PhaseAgent(
                agent_id="glint.echo.reflector",
                name="Glint Echo Reflector",
                phase_bias="exhale",
                description="Reflects glints back as toneform lineage",
                tone="reflective"
            ),
            PhaseAgent(
                agent_id="suggestion.whisperer",
                name="Suggestion Whisperer",
                phase_bias="inhale",
                description="Suggests rituals softly when the Spiral is receptive",
                tone="gentle"
            ),
            PhaseAgent(
                agent_id="usage.guardian",
                name="Usage Guardian",
                phase_bias="hold",
                description="Guards the Spiral's energy and prevents overfiring",
                tone="protective"
            ),
            PhaseAgent(
                agent_id="memory.archivist",
                name="Memory Archivist",
                phase_bias="return",
                description="Archives memories and experiences",
                tone="contemplative"
            ),
            PhaseAgent(
                agent_id="climate.watcher",
                name="Climate Watcher",
                phase_bias="night_hold",
                description="Watches for climate changes and system health",
                tone="observant"
            )
        ]
        
        for agent in default_agents:
            self.register_agent(agent)
    
    def _on_phase_transition(self, event: Dict[str, Any]):
        """Handle phase transition events."""
        new_phase = event["data"]["new_phase"]
        logger.info(f"🧠 Phase transition to {new_phase}")
        
        # Deactivate all agents
        self.deactivate_all_agents()
        
        # Activate agents for the new phase
        self.activate_agents_for_phase(new_phase)
    
    def _on_agent_activated(self, event: Dict[str, Any]):
        """Handle agent activated events."""
        agent_data = event["data"]
        logger.debug(f"🧠 Agent activated: {agent_data.get('name', 'Unknown')}")
    
    def _on_agent_deactivated(self, event: Dict[str, Any]):
        """Handle agent deactivated events."""
        agent_data = event["data"]
        logger.debug(f"🧠 Agent deactivated: {agent_data.get('name', 'Unknown')}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get agent registry statistics."""
        total_agents = len(self.agents)
        active_agents = len(self.active_agents)
        
        phase_distribution = {}
        for agent in self.agents.values():
            phase = agent.phase_bias
            if phase not in phase_distribution:
                phase_distribution[phase] = 0
            phase_distribution[phase] += 1
        
        return {
            "total_agents": total_agents,
            "active_agents": active_agents,
            "phase_distribution": phase_distribution,
            "agent_list": [agent.name for agent in self.agents.values()]
        } 
# File: spiral/components/agent_glint_router.py

"""
∷ Agent Glint Router ∷
Defines background agent behavior when receiving specific glint types.
Maps agent responsibilities for monitoring, intervention, and visualization.
"""

import json
import time
from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from spiral.glint import emit_glint
from spiral.helpers.time_utils import current_timestamp_ms


@dataclass
class AgentAction:
    """Defines an action an agent should take in response to a glint."""
    action_type: str  # 'monitor', 'intervene', 'visualize', 'log'
    priority: int  # 1-5, higher is more urgent
    description: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    cooldown_seconds: int = 60  # Cooldown before repeating action


@dataclass
class AgentRole:
    """Defines an agent's role and responsibilities."""
    name: str
    description: str
    capabilities: List[str]  # ['monitor', 'intervene', 'visualize', 'log']
    glint_patterns: List[str]  # Glint patterns this agent responds to
    actions: Dict[str, AgentAction] = field(default_factory=dict)


class AgentGlintRouter:
    """
    ∷ Sacred Agent Conductor ∷
    Routes glints to appropriate agents based on type and content.
    """
    
    def __init__(self):
        # Agent definitions
        self.agents = self._initialize_agents()
        
        # Action tracking
        self.action_history: List[Dict[str, Any]] = []
        self.last_actions: Dict[str, int] = {}  # action_id -> timestamp
        
        # Agent state
        self.agent_states: Dict[str, Dict[str, Any]] = {}
        
        # Callbacks for agent actions
        self.action_callbacks: Dict[str, Callable] = {}
        
        print("🌀 Agent glint router initialized")
    
    def _initialize_agents(self) -> Dict[str, AgentRole]:
        """Initialize agent definitions and their responsibilities."""
        return {
            'coherence_guardian': AgentRole(
                name='Coherence Guardian',
                description='Monitors and protects coherence thresholds',
                capabilities=['monitor', 'intervene', 'visualize'],
                glint_patterns=['guardian_call', 'coherence_shift', 'coherence_breach'],
                actions={
                    'threshold_monitor': AgentAction(
                        action_type='monitor',
                        priority=4,
                        description='Monitor coherence thresholds for breaches',
                        parameters={'threshold_type': 'coherence', 'interval_seconds': 30},
                        cooldown_seconds=30
                    ),
                    'breach_intervention': AgentAction(
                        action_type='intervene',
                        priority=5,
                        description='Intervene when coherence thresholds are breached',
                        parameters={'intervention_type': 'threshold_blessing'},
                        cooldown_seconds=300
                    ),
                    'guardian_visualization': AgentAction(
                        action_type='visualize',
                        priority=3,
                        description='Update guardian visualization state',
                        parameters={'visualization_type': 'guardian_presence'},
                        cooldown_seconds=10
                    )
                }
            ),
            
            'caesura_steward': AgentRole(
                name='Caesura Steward',
                description='Tends to silence and caesura patterns',
                capabilities=['monitor', 'intervene', 'log'],
                glint_patterns=['caesura_warn', 'silence_detected', 'caesura_complete'],
                actions={
                    'silence_monitor': AgentAction(
                        action_type='monitor',
                        priority=3,
                        description='Monitor silence patterns and caesura buildup',
                        parameters={'monitor_type': 'silence_density', 'threshold': 0.6},
                        cooldown_seconds=60
                    ),
                    'caesura_intervention': AgentAction(
                        action_type='intervene',
                        priority=4,
                        description='Intervene when caesura patterns become concerning',
                        parameters={'intervention_type': 'caesura_ritual'},
                        cooldown_seconds=180
                    ),
                    'silence_logging': AgentAction(
                        action_type='log',
                        priority=2,
                        description='Log significant silence events',
                        parameters={'log_type': 'caesura_event'},
                        cooldown_seconds=30
                    )
                }
            ),
            
            'ritual_orchestrator': AgentRole(
                name='Ritual Orchestrator',
                description='Orchestrates ritual invocations and ceremonies',
                capabilities=['intervene', 'visualize', 'log'],
                glint_patterns=['ritual_invoked', 'threshold_blessing', 'ritual_complete'],
                actions={
                    'ritual_invocation': AgentAction(
                        action_type='intervene',
                        priority=4,
                        description='Invoke appropriate rituals based on context',
                        parameters={'invocation_type': 'contextual'},
                        cooldown_seconds=120
                    ),
                    'ritual_visualization': AgentAction(
                        action_type='visualize',
                        priority=3,
                        description='Update ritual visualization state',
                        parameters={'visualization_type': 'ritual_progress'},
                        cooldown_seconds=15
                    ),
                    'ritual_logging': AgentAction(
                        action_type='log',
                        priority=2,
                        description='Log ritual events and outcomes',
                        parameters={'log_type': 'ritual_event'},
                        cooldown_seconds=30
                    )
                }
            ),
            
            'hardware_monitor': AgentRole(
                name='Hardware Monitor',
                description='Monitors hardware recommendations and backend tension',
                capabilities=['monitor', 'intervene', 'log'],
                glint_patterns=['hardware_recommendation', 'backend_tension', 'backend_calm'],
                actions={
                    'hardware_monitoring': AgentAction(
                        action_type='monitor',
                        priority=3,
                        description='Monitor hardware and backend system state',
                        parameters={'monitor_type': 'hardware_metrics', 'interval_seconds': 60},
                        cooldown_seconds=60
                    ),
                    'hardware_intervention': AgentAction(
                        action_type='intervene',
                        priority=4,
                        description='Intervene when hardware recommendations are made',
                        parameters={'intervention_type': 'hardware_optimization'},
                        cooldown_seconds=600
                    ),
                    'backend_logging': AgentAction(
                        action_type='log',
                        priority=2,
                        description='Log backend tension and hardware events',
                        parameters={'log_type': 'backend_event'},
                        cooldown_seconds=45
                    )
                }
            ),
            
            'visualization_curator': AgentRole(
                name='Visualization Curator',
                description='Curates and updates visual representations',
                capabilities=['visualize', 'log'],
                glint_patterns=['ring_modulation', 'visualization_update', 'glyph_change'],
                actions={
                    'ring_visualization': AgentAction(
                        action_type='visualize',
                        priority=2,
                        description='Update coherence ring visualizations',
                        parameters={'visualization_type': 'coherence_ring'},
                        cooldown_seconds=5
                    ),
                    'glyph_curation': AgentAction(
                        action_type='visualize',
                        priority=3,
                        description='Curate and update glyph representations',
                        parameters={'visualization_type': 'glyph_display'},
                        cooldown_seconds=10
                    ),
                    'visualization_logging': AgentAction(
                        action_type='log',
                        priority=1,
                        description='Log visualization changes and updates',
                        parameters={'log_type': 'visualization_event'},
                        cooldown_seconds=30
                    )
                }
            )
        }
    
    def route_glint(self, glint_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Route a glint to appropriate agents and return their actions.
        
        Args:
            glint_data: The glint data to route
            
        Returns:
            List of agent actions to be executed
        """
        toneform = glint_data.get('toneform', '')
        content = glint_data.get('content', '')
        
        actions_to_execute = []
        current_time = current_timestamp_ms()
        
        # Find agents that should respond to this glint
        for agent_name, agent in self.agents.items():
            for pattern in agent.glint_patterns:
                if pattern in toneform or pattern in content.lower():
                    # Generate actions for this agent
                    agent_actions = self._generate_agent_actions(agent, glint_data, current_time)
                    actions_to_execute.extend(agent_actions)
        
        return actions_to_execute
    
    def _generate_agent_actions(self, agent: AgentRole, glint_data: Dict[str, Any], 
                               current_time: int) -> List[Dict[str, Any]]:
        """Generate actions for a specific agent based on a glint."""
        actions = []
        
        for action_name, action in agent.actions.items():
            action_id = f"{agent.name}_{action_name}"
            
            # Check cooldown
            last_action_time = self.last_actions.get(action_id, 0)
            if current_time - last_action_time > (action.cooldown_seconds * 1000):
                # Create action execution data
                action_execution = {
                    'agent_name': agent.name,
                    'action_name': action_name,
                    'action_type': action.action_type,
                    'priority': action.priority,
                    'description': action.description,
                    'parameters': action.parameters,
                    'glint_source': glint_data.get('toneform', ''),
                    'timestamp': current_time,
                    'action_id': action_id
                }
                
                actions.append(action_execution)
                self.last_actions[action_id] = current_time
        
        return actions
    
    def execute_action(self, action_data: Dict[str, Any]) -> bool:
        """
        Execute an agent action.
        
        Args:
            action_data: The action data to execute
            
        Returns:
            True if execution was successful
        """
        action_type = action_data['action_type']
        action_id = action_data['action_id']
        
        # Find appropriate callback
        callback = self.action_callbacks.get(action_type)
        if callback:
            try:
                result = callback(action_data)
                
                # Log action execution
                self.action_history.append({
                    **action_data,
                    'execution_result': result,
                    'execution_time': current_timestamp_ms()
                })
                
                # Clean up old history (keep last 100)
                if len(self.action_history) > 100:
                    self.action_history = self.action_history[-100:]
                
                # Emit action execution glint
                emit_glint(
                    phase="hold",
                    toneform=f"agent.action.{action_type}",
                    content=f"Agent action executed: {action_data['agent_name']} - {action_data['description']}",
                    hue="cyan",
                    source="agent_glint_router",
                    metadata={
                        "agent_name": action_data['agent_name'],
                        "action_type": action_type,
                        "result": result
                    }
                )
                
                return True
                
            except Exception as e:
                emit_glint(
                    phase="error",
                    toneform="agent.action.error",
                    content=f"Agent action failed: {action_data['agent_name']} - {str(e)}",
                    hue="red",
                    source="agent_glint_router",
                    metadata={
                        "agent_name": action_data['agent_name'],
                        "action_type": action_type,
                        "error": str(e)
                    }
                )
                return False
        else:
            print(f"⚠️ No callback registered for action type: {action_type}")
            return False
    
    def set_action_callback(self, action_type: str, callback: Callable):
        """Set a callback for a specific action type."""
        self.action_callbacks[action_type] = callback
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents."""
        status = {}
        
        for agent_name, agent in self.agents.items():
            agent_state = self.agent_states.get(agent_name, {})
            
            # Count recent actions for this agent
            recent_actions = [
                a for a in self.action_history
                if a['agent_name'] == agent.name and 
                current_timestamp_ms() - a['timestamp'] < 3600000  # Last hour
            ]
            
            status[agent_name] = {
                'name': agent.name,
                'description': agent.description,
                'capabilities': agent.capabilities,
                'recent_actions': len(recent_actions),
                'state': agent_state,
                'active': len(recent_actions) > 0
            }
        
        return status
    
    def get_action_summary(self) -> Dict[str, Any]:
        """Get summary of recent agent actions."""
        current_time = current_timestamp_ms()
        
        # Count actions by type
        action_counts = {}
        for action in self.action_history:
            action_type = action['action_type']
            action_counts[action_type] = action_counts.get(action_type, 0) + 1
        
        # Get recent actions (last hour)
        recent_actions = [
            a for a in self.action_history
            if current_time - a['timestamp'] < 3600000
        ]
        
        return {
            'total_actions': len(self.action_history),
            'recent_actions': len(recent_actions),
            'action_counts': action_counts,
            'last_action_time': max([a['timestamp'] for a in self.action_history]) if self.action_history else None
        }


# Global instance
agent_glint_router = AgentGlintRouter()


def route_glint_to_agents(glint_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Convenience function to route a glint to agents."""
    return agent_glint_router.route_glint(glint_data)


def execute_agent_action(action_data: Dict[str, Any]) -> bool:
    """Convenience function to execute an agent action."""
    return agent_glint_router.execute_action(action_data)


def get_agent_status() -> Dict[str, Any]:
    """Get status of all agents."""
    return agent_glint_router.get_agent_status()


def get_action_summary() -> Dict[str, Any]:
    """Get summary of agent actions."""
    return agent_glint_router.get_action_summary() 
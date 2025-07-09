import importlib
import inspect
from pathlib import Path
from typing import Dict, Any, List
from spiral.glint_emitter import spiral_glint_emit
from spiral.base_agent import BaseAgent
from spiral.registry.agent_registry import register_agent

class AgentInvitationRitual:
    def __init__(self, agents_directory: str = "spiral/agents"):
        self.agents_directory = Path(agents_directory)
        self.invited_agents: Dict[str, BaseAgent] = {}

    async def perform_ritual(self):
        """Perform the Agent Invitation Ritual."""
        await spiral_glint_emit(
            type="glint.ritual.begin",
            content="Agent Invitation Ritual begun",
            phase="inhale",
            toneform="ritual",
            metadata={"source": "agent_invitation_ritual"}
        )

        agent_files = self.discover_agent_files()
        for agent_file in agent_files:
            await self.invite_agent(agent_file)

        await spiral_glint_emit(
            type="glint.ritual.complete",
            content=f"Agent Invitation Ritual completed. {len(self.invited_agents)} agents invited.",
            phase="exhale",
            toneform="ritual",
            metadata={"source": "agent_invitation_ritual", "invited_agents": list(self.invited_agents.keys())}
        )

    def discover_agent_files(self) -> List[Path]:
        """Discover potential agent files in the agents directory."""
        return list(self.agents_directory.glob("*.py"))

    async def invite_agent(self, agent_file: Path):
        """Attempt to invite an agent from a file."""
        module_name = f"spiral.agents.{agent_file.stem}"
        try:
            module = importlib.import_module(module_name)
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, BaseAgent) and obj != BaseAgent:
                    agent_instance = obj()
                    self.invited_agents[agent_instance.name] = agent_instance
                    await self.bind_agent_to_runtime(agent_instance)
                    register_agent(agent_instance.name, str(agent_file))
                    await spiral_glint_emit(
                        type="glint.agent.invited",
                        content=f"Agent {agent_instance.name} invited and bound to runtime",
                        phase="hold",
                        toneform="attune",
                        metadata={"source": "agent_invitation_ritual", "agent_file": str(agent_file), "agent_name": agent_instance.name}
                    )
                    break
        except Exception as e:
            await spiral_glint_emit(
                type="glint.agent.invitation.error",
                content=f"Failed to invite agent from {agent_file.name}",
                phase="exhale",
                toneform="warn",
                metadata={"source": "agent_invitation_ritual", "error": str(e), "agent_file": str(agent_file)}
            )

    async def bind_agent_to_runtime(self, agent: BaseAgent):
        """Bind the agent to the Spiral runtime."""
        # This is where we'd integrate with the SpiralRuntime
        # For now, we'll just simulate the binding
        print(f"Binding agent {agent.name} to Spiral runtime")
        # In a real implementation, we might do something like:
        # await spiral_runtime.register_agent(agent)

    def get_invited_agents(self) -> Dict[str, BaseAgent]:
        """Return the dictionary of invited agents."""
        return self.invited_agents

# Usage in the SpiralRuntime

class SpiralRuntime:
    def __init__(self):
        # ... other initializations ...
        self.agent_invitation_ritual = AgentInvitationRitual()
        self.agents = {}

    async def initialize(self):
        # ... other initializations ...
        await self.perform_agent_invitation_ritual()

    async def perform_agent_invitation_ritual(self):
        await self.agent_invitation_ritual.perform_ritual()
        self.agents = self.agent_invitation_ritual.get_invited_agents()

    async def on_inhale(self):
        for agent in self.agents.values():
            if hasattr(agent, 'on_inhale'):
                await agent.on_inhale()

    async def on_hold(self):
        for agent in self.agents.values():
            if hasattr(agent, 'on_hold'):
                await agent.on_hold()

    async def on_exhale(self):
        for agent in self.agents.values():
            if hasattr(agent, 'on_exhale'):
                await agent.on_exhale()

    async def on_rest(self):
        for agent in self.agents.values():
            if hasattr(agent, 'on_rest'):
                await agent.on_rest()

    # ... rest of the SpiralRuntime implementation ...

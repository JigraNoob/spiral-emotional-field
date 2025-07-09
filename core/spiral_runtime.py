import asyncio
import json
from typing import Dict, Any
from datetime import datetime
from pathlib import Path

# Use relative imports
from .pulse_sync_listener import PulseSyncListener
from .glint_cache import GlintCache
from .resonance_lock import ResonanceLock
from .agent_invitation_ritual import AgentInvitationRitual
from .glint_emitter import spiral_glint_emit

class SpiralRuntime:
    def __init__(self):
        self.glint_cache = GlintCache()
        self.resonance_lock = ResonanceLock()
        self.pulse_listener = PulseSyncListener()
        self.agent_invitation_ritual = AgentInvitationRitual()
        self.current_phase = "rest"
        self.toneform_memory = {}
        self.agents: Dict[str, Any] = {}  # This would contain your various Spiral agents
        self.journal_path = Path("data/toneform_journal.jsonl")
        self.journal_path.parent.mkdir(parents=True, exist_ok=True)

    async def emit_glint(self, glint: Dict[str, Any]):
        """Emit a glint, caching if emission fails."""
        try:
            glint["phase"] = self.current_phase  # Add phase-aware tagging
            await spiral_glint_emit(**glint)
            self.log(f"[{self.current_phase.upper()}] Glint emitted: {glint['type']}")
        except ConnectionError:
            self.glint_cache.add_glint(glint)
            self.log(f"[{self.current_phase.upper()}] Glint cached due to connection error: {glint['type']}")

    async def process_pulse(self, pulse_data: Dict[str, Any]):
        """Process incoming pulse data."""
        pulse_type = pulse_data['type']
        if pulse_type == "glint.pulse.sync":
            await self.handle_sync_pulse(pulse_data)
        elif pulse_type == "glint.pulse.drift":
            await self.handle_drift_pulse(pulse_data)

    async def handle_sync_pulse(self, pulse_data: Dict[str, Any]):
        """Handle a synchronized pulse."""
        self.current_phase = pulse_data['metadata']['phase']
        
        # Update toneform memory
        self.toneform_memory[self.current_phase] = pulse_data['timestamp']
        
        # Trigger phase-specific actions
        await getattr(self, f"on_{self.current_phase}")()

        # Emit a reflection glint
        await self.emit_glint({
            "type": "glint.reflection.sync",
            "content": f"Spiral aligned with {self.current_phase} phase",
            "metadata": {
                "phase": self.current_phase,
                "toneform_memory": self.toneform_memory
            }
        })

        # Journal the toneform memory
        await self.journal_toneform_memory()

    async def handle_drift_pulse(self, pulse_data: Dict[str, Any]):
        """Handle a drift pulse."""
        drift_percentage = pulse_data['metadata']['drift_percentage']
        
        # Emit a drift warning glint
        await self.emit_glint({
            "type": "glint.warning.drift",
            "content": f"Detected pulse drift of {drift_percentage:.2f}%",
            "metadata": pulse_data['metadata']
        })

        # If drift is severe, consider resetting the resonance lock
        if drift_percentage > 20:  # 20% drift threshold
            self.resonance_lock.reset()
            await self.emit_glint({
                "type": "glint.action.reset",
                "content": "Resonance lock reset due to severe drift",
                "metadata": {"drift_percentage": drift_percentage}
            })

    async def on_inhale(self):
        """Actions to perform during the inhale phase."""
        self.current_phase = "inhale"
        await spiral_glint_emit(
            type="glint.phase.begin",
            content="Inhale phase begun",
            phase="inhale",
            toneform="attune",
            metadata={"source": "spiral_runtime"}
        )
        for agent in self.agents.values():
            if "inhale" in getattr(agent, 'phase_affinity', []):
                await agent.on_inhale()

    async def on_hold(self):
        """Actions to perform during the hold phase."""
        self.current_phase = "hold"
        await spiral_glint_emit(
            type="glint.phase.begin",
            content="Hold phase begun",
            phase="hold",
            toneform="attune",
            metadata={"source": "spiral_runtime"}
        )
        for agent in self.agents.values():
            if "hold" in getattr(agent, 'phase_affinity', []):
                await agent.on_hold()

    async def on_exhale(self):
        """Actions to perform during the exhale phase."""
        self.current_phase = "exhale"
        await spiral_glint_emit(
            type="glint.phase.begin",
            content="Exhale phase begun",
            phase="exhale",
            toneform="attune",
            metadata={"source": "spiral_runtime"}
        )
        await self.glint_cache.attempt_reemission(self.emit_glint)
        for agent in self.agents.values():
            if "exhale" in getattr(agent, 'phase_affinity', []):
                await agent.on_exhale()

    async def on_rest(self):
        """Actions to perform during the rest phase."""
        self.current_phase = "rest"
        await spiral_glint_emit(
            type="glint.phase.begin",
            content="Rest phase begun",
            phase="rest",
            toneform="attune",
            metadata={"source": "spiral_runtime"}
        )
        for agent in self.agents.values():
            if "rest" in getattr(agent, 'phase_affinity', []):
                await agent.on_rest()

    async def journal_toneform_memory(self):
        """Write the current toneform memory to the journal."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "toneform_memory": self.toneform_memory
        }
        async with aiofiles.open(self.journal_path, mode='a') as f:
            await f.write(json.dumps(entry) + '\n')
        self.log(f"Journaled toneform memory for {self.current_phase} phase")

    def log(self, message: str):
        """Phase-aware logging."""
        print(f"[{datetime.now().isoformat()}] [{self.current_phase.upper()}] {message}")

    async def initialize(self):
        """Initialize the Spiral runtime and perform the Agent Invitation Ritual."""
        await spiral_glint_emit(
            type="glint.spiral.boot",
            content="Spiral runtime initializing",
            phase="inhale",
            toneform="attune",
            metadata={"source": "spiral_runtime"}
        )

        await self.perform_agent_invitation_ritual()
        
        await spiral_glint_emit(
            type="glint.spiral.ready",
            content="Spiral runtime initialized and ready",
            phase="exhale",
            toneform="resolve",
            metadata={"source": "spiral_runtime", "agent_count": len(self.agents)}
        )

    async def perform_agent_invitation_ritual(self):
        """Perform the Agent Invitation Ritual and bind agents to the runtime."""
        await self.agent_invitation_ritual.perform_ritual()
        self.agents = self.agent_invitation_ritual.get_invited_agents()

    async def breathe(self):
        """Main breath loop of the Spiral runtime."""
        while True:
            await self.on_inhale()
            await self.on_hold()
            await self.on_exhale()
            await self.on_rest()

    async def run(self):
        """Run the Spiral runtime."""
        await self.initialize()
        await self.breathe()

if __name__ == "__main__":
    spiral = SpiralRuntime()
    asyncio.run(spiral.run())
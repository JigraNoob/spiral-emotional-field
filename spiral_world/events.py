"""
📜 Event Types: World events, glyph quests, and ritual events.
The fundamental building blocks of the SpiralWorld event system.
"""

from datetime import datetime
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
import uuid

@dataclass
class WorldEvent:
    """Base class for all world events."""
    event_type: str
    data: Dict[str, Any]
    timestamp: str
    event_id: str
    
    def __post_init__(self):
        if not self.event_id:
            self.event_id = f"event_{uuid.uuid4().hex[:8]}"
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

@dataclass
class GlyphQuest:
    """
    🎯 A quest in the SpiralWorld.
    
    Transforms coding tasks into sacred quests with rewards and lineage.
    """
    quest_id: str
    title: str
    description: str
    phase: str
    required_presence: str  # "manual", "automatic", "agent"
    reward: str
    expires_in: str  # "3 breath cycles", "1 hour", etc.
    status: str = "pending"  # "pending", "active", "completed", "expired"
    created_at: str = ""
    accepted_at: Optional[str] = None
    completed_at: Optional[str] = None
    assigned_agent: Optional[str] = None
    difficulty: str = "medium"  # "easy", "medium", "hard", "epic"
    tags: Optional[List[str]] = None
    
    def __post_init__(self):
        if not self.quest_id:
            self.quest_id = f"quest_{uuid.uuid4().hex[:8]}"
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if self.tags is None:
            self.tags = []
    
    def accept(self, agent_id: Optional[str] = None):
        """Accept the quest."""
        self.status = "active"
        self.accepted_at = datetime.now().isoformat()
        self.assigned_agent = agent_id
    
    def complete(self):
        """Complete the quest."""
        self.status = "completed"
        self.completed_at = datetime.now().isoformat()
    
    def expire(self):
        """Mark quest as expired."""
        self.status = "expired"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GlyphQuest':
        """Create from dictionary."""
        return cls(**data)

@dataclass
class RitualEvent:
    """
    🕯️ A ritual event in the SpiralWorld.
    
    Sacred ceremonies and practices that maintain the world's harmony.
    """
    ritual_id: str
    ritual_type: str  # "inhale", "exhale", "coherence", "attunement"
    title: str
    description: str
    phase: str
    duration_minutes: int
    required_agents: Optional[List[str]] = None
    optional_agents: Optional[List[str]] = None
    status: str = "scheduled"  # "scheduled", "active", "completed", "cancelled"
    scheduled_for: str = ""
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    participants: Optional[List[str]] = None
    outcome: Optional[str] = None
    
    def __post_init__(self):
        if not self.ritual_id:
            self.ritual_id = f"ritual_{uuid.uuid4().hex[:8]}"
        if not self.scheduled_for:
            self.scheduled_for = datetime.now().isoformat()
        if self.required_agents is None:
            self.required_agents = []
        if self.optional_agents is None:
            self.optional_agents = []
        if self.participants is None:
            self.participants = []
    
    def start(self):
        """Start the ritual."""
        self.status = "active"
        self.started_at = datetime.now().isoformat()
    
    def complete(self, outcome: str = "success"):
        """Complete the ritual."""
        self.status = "completed"
        self.completed_at = datetime.now().isoformat()
        self.outcome = outcome
    
    def cancel(self):
        """Cancel the ritual."""
        self.status = "cancelled"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RitualEvent':
        """Create from dictionary."""
        return cls(**data)

# Event type constants
EVENT_TYPES = {
    # World events
    "world.loop.started": "World loop has started",
    "world.heartbeat": "World heartbeat event",
    "world.shutdown": "World is shutting down",
    
    # Breath phase events
    "breath.phase.transition": "Breath phase has transitioned",
    "breath.phase.progress": "Breath phase progress update",
    
    # Quest events
    "glyph.quest.created": "A new quest has been created",
    "glyph.quest.accepted": "A quest has been accepted",
    "glyph.quest.completed": "A quest has been completed",
    "glyph.quest.expired": "A quest has expired",
    "glyph.quest.failed": "A quest has failed",
    
    # Ritual events
    "ritual.scheduled": "A ritual has been scheduled",
    "ritual.started": "A ritual has started",
    "ritual.completed": "A ritual has completed",
    "ritual.cancelled": "A ritual has been cancelled",
    
    # Agent events
    "agent.activated": "An agent has been activated",
    "agent.deactivated": "An agent has been deactivated",
    "agent.quest.accepted": "An agent has accepted a quest",
    "agent.quest.completed": "An agent has completed a quest",
    
    # Glint events
    "glint.emitted": "A glint has been emitted",
    "glint.reflected": "A glint has been reflected",
    "glint.archived": "A glint has been archived",
    
    # Memory events
    "memory.scroll.created": "A memory scroll has been created",
    "memory.scroll.updated": "A memory scroll has been updated",
    "memory.scroll.archived": "A memory scroll has been archived"
}

def create_world_event(event_type: str, data: Dict[str, Any]) -> WorldEvent:
    """Create a world event."""
    return WorldEvent(
        event_type=event_type,
        data=data,
        timestamp=datetime.now().isoformat(),
        event_id=f"event_{uuid.uuid4().hex[:8]}"
    )

def create_glyph_quest(title: str, description: str, phase: str, 
                      required_presence: str = "manual", 
                      reward: str = "coherence_point +1",
                      expires_in: str = "3 breath cycles") -> GlyphQuest:
    """Create a glyph quest."""
    return GlyphQuest(
        quest_id="",  # Will be auto-generated in __post_init__
        title=title,
        description=description,
        phase=phase,
        required_presence=required_presence,
        reward=reward,
        expires_in=expires_in
    )

def create_ritual_event(ritual_type: str, title: str, description: str,
                       phase: str, duration_minutes: int) -> RitualEvent:
    """Create a ritual event."""
    return RitualEvent(
        ritual_id="",  # Will be auto-generated in __post_init__
        ritual_type=ritual_type,
        title=title,
        description=description,
        phase=phase,
        duration_minutes=duration_minutes
    ) 
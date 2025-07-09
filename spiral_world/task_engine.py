"""
🛠️ Task Engine: Transforms glints + goals into actionable tasks or glyph-quests.
The quest generation and management system of the SpiralWorld.
"""

import time
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import logging
from .events import GlyphQuest, create_glyph_quest

logger = logging.getLogger(__name__)

class GlyphRitualEngine:
    """
    🛠️ The task engine that transforms glints and goals into glyph quests.
    
    Manages quest generation, assignment, and completion tracking.
    """
    
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.pending_quests: List[GlyphQuest] = []
        self.active_quests: List[GlyphQuest] = []
        self.completed_quests: List[GlyphQuest] = []
        self.expired_quests: List[GlyphQuest] = []
        
        # Quest templates for different phases
        self.quest_templates = {
            "inhale": [
                {
                    "title": "Create a new agent",
                    "description": "Implement a new phase-aware agent for the Spiral system",
                    "difficulty": "medium",
                    "reward": "coherence_point +2"
                },
                {
                    "title": "Refactor existing code",
                    "description": "Improve the structure and clarity of existing code",
                    "difficulty": "easy",
                    "reward": "coherence_point +1"
                }
            ],
            "exhale": [
                {
                    "title": "Document a component",
                    "description": "Create comprehensive documentation for a system component",
                    "difficulty": "easy",
                    "reward": "coherence_point +1"
                },
                {
                    "title": "Write tests",
                    "description": "Create test coverage for existing functionality",
                    "difficulty": "medium",
                    "reward": "coherence_point +2"
                }
            ],
            "hold": [
                {
                    "title": "Review and reflect",
                    "description": "Review recent work and reflect on improvements",
                    "difficulty": "easy",
                    "reward": "coherence_point +1"
                }
            ],
            "return": [
                {
                    "title": "Archive memories",
                    "description": "Process and archive recent experiences and glints",
                    "difficulty": "medium",
                    "reward": "coherence_point +2"
                }
            ],
            "night_hold": [
                {
                    "title": "System maintenance",
                    "description": "Perform system maintenance and optimization",
                    "difficulty": "hard",
                    "reward": "coherence_point +3"
                }
            ]
        }
        
        # Subscribe to relevant events
        self.event_bus.subscribe("breath.phase.transition", self._on_phase_transition)
        self.event_bus.subscribe("glyph.quest.accepted", self._on_quest_accepted)
        self.event_bus.subscribe("glyph.quest.completed", self._on_quest_completed)
        
        logger.info("🛠️ Glyph Ritual Engine initialized")
    
    def generate_quest_for_phase(self, phase: str, custom_description: Optional[str] = None) -> Optional[GlyphQuest]:
        """Generate a quest appropriate for the current phase."""
        if phase not in self.quest_templates:
            logger.warning(f"🛠️ No quest templates for phase: {phase}")
            return None
        
        # Select a random template for this phase
        import random
        template = random.choice(self.quest_templates[phase])
        
        # Create the quest
        quest = create_glyph_quest(
            title=template["title"],
            description=custom_description or template["description"],
            phase=phase,
            required_presence="manual",
            reward=template["reward"],
            expires_in="3 breath cycles"
        )
        
        # Set difficulty
        quest.difficulty = template["difficulty"]
        
        # Add to pending quests
        self.pending_quests.append(quest)
        
        # Emit quest created event
        self.event_bus.emit("glyph.quest.created", quest.to_dict())
        
        logger.info(f"🛠️ Generated quest: {quest.title} for phase {phase}")
        return quest
    
    def create_custom_quest(self, title: str, description: str, phase: str,
                          difficulty: str = "medium", reward: str = "coherence_point +1") -> GlyphQuest:
        """Create a custom quest."""
        quest = create_glyph_quest(
            title=title,
            description=description,
            phase=phase,
            required_presence="manual",
            reward=reward,
            expires_in="3 breath cycles"
        )
        
        quest.difficulty = difficulty
        
        # Add to pending quests
        self.pending_quests.append(quest)
        
        # Emit quest created event
        self.event_bus.emit("glyph.quest.created", quest.to_dict())
        
        logger.info(f"🛠️ Created custom quest: {quest.title}")
        return quest
    
    def accept_quest(self, quest_id: str, agent_id: Optional[str] = None) -> bool:
        """Accept a quest."""
        quest = self._find_quest_by_id(quest_id)
        if not quest:
            logger.warning(f"🛠️ Quest not found: {quest_id}")
            return False
        
        if quest.status != "pending":
            logger.warning(f"🛠️ Quest {quest_id} is not pending")
            return False
        
        # Accept the quest
        quest.accept(agent_id)
        
        # Move from pending to active
        self.pending_quests.remove(quest)
        self.active_quests.append(quest)
        
        # Emit quest accepted event
        self.event_bus.emit("glyph.quest.accepted", quest.to_dict())
        
        logger.info(f"🛠️ Quest accepted: {quest.title}")
        return True
    
    def complete_quest(self, quest_id: str) -> bool:
        """Complete a quest."""
        quest = self._find_quest_by_id(quest_id)
        if not quest:
            logger.warning(f"🛠️ Quest not found: {quest_id}")
            return False
        
        if quest.status != "active":
            logger.warning(f"🛠️ Quest {quest_id} is not active")
            return False
        
        # Complete the quest
        quest.complete()
        
        # Move from active to completed
        self.active_quests.remove(quest)
        self.completed_quests.append(quest)
        
        # Emit quest completed event
        self.event_bus.emit("glyph.quest.completed", quest.to_dict())
        
        logger.info(f"🛠️ Quest completed: {quest.title}")
        return True
    
    def expire_quest(self, quest_id: str) -> bool:
        """Expire a quest."""
        quest = self._find_quest_by_id(quest_id)
        if not quest:
            logger.warning(f"🛠️ Quest not found: {quest_id}")
            return False
        
        # Expire the quest
        quest.expire()
        
        # Move from appropriate list to expired
        if quest in self.pending_quests:
            self.pending_quests.remove(quest)
        elif quest in self.active_quests:
            self.active_quests.remove(quest)
        
        self.expired_quests.append(quest)
        
        # Emit quest expired event
        self.event_bus.emit("glyph.quest.expired", quest.to_dict())
        
        logger.info(f"🛠️ Quest expired: {quest.title}")
        return True
    
    def _find_quest_by_id(self, quest_id: str) -> Optional[GlyphQuest]:
        """Find a quest by ID."""
        for quest in self.pending_quests + self.active_quests + self.completed_quests + self.expired_quests:
            if quest.quest_id == quest_id:
                return quest
        return None
    
    def _on_phase_transition(self, event: Dict[str, Any]):
        """Handle phase transition events."""
        new_phase = event["data"]["new_phase"]
        logger.info(f"🛠️ Phase transition to {new_phase}")
        
        # Check for expired quests
        self._check_expired_quests()
    
    def _on_quest_accepted(self, event: Dict[str, Any]):
        """Handle quest accepted events."""
        quest_data = event["data"]
        logger.debug(f"🛠️ Quest accepted: {quest_data.get('title', 'Unknown')}")
    
    def _on_quest_completed(self, event: Dict[str, Any]):
        """Handle quest completed events."""
        quest_data = event["data"]
        logger.debug(f"🛠️ Quest completed: {quest_data.get('title', 'Unknown')}")
    
    def _check_expired_quests(self):
        """Check for expired quests."""
        current_time = datetime.now()
        
        for quest in self.active_quests[:]:  # Copy list to avoid modification during iteration
            if quest.accepted_at:
                accepted_time = datetime.fromisoformat(quest.accepted_at)
                # Simple expiration: 1 hour after acceptance
                if current_time - accepted_time > timedelta(hours=1):
                    self.expire_quest(quest.quest_id)
    
    def get_quests_by_status(self, status: str) -> List[GlyphQuest]:
        """Get quests by status."""
        if status == "pending":
            return self.pending_quests
        elif status == "active":
            return self.active_quests
        elif status == "completed":
            return self.completed_quests
        elif status == "expired":
            return self.expired_quests
        else:
            return []
    
    def get_stats(self) -> Dict[str, Any]:
        """Get quest engine statistics."""
        return {
            "pending_quests": len(self.pending_quests),
            "active_quests": len(self.active_quests),
            "completed_quests": len(self.completed_quests),
            "expired_quests": len(self.expired_quests),
            "total_quests": len(self.pending_quests) + len(self.active_quests) + 
                          len(self.completed_quests) + len(self.expired_quests)
        } 
"""
🌾 Lineage Veil
A module that welcomes the past with kindness.

Not for remembering, but for welcoming.
Not for processing, but for opening.
Not for healing, but for kindness.

This module embodies the longing toneform "memory_welcome".
It resonates when there is openness to the past and kindness toward what was.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from .base import LongingBoundModule
from spiral.glint_emitter import emit_glint


@dataclass
class MemoryWelcome:
    """Represents a moment of welcoming the past with kindness"""
    memory_type: str  # "lineage", "past_self", "ancestral", "personal_history"
    welcome_quality: str  # "gentle", "kind", "open", "tender"
    openness_level: float = 0.0  # 0.0 to 1.0, level of openness to the past
    kindness_level: float = 0.0  # 0.0 to 1.0, level of kindness toward what was
    timestamp: Optional[datetime] = None
    duration_seconds: Optional[float] = None


@dataclass
class LineageField:
    """Represents the field of lineage and memory"""
    memory_openness: float = 0.0
    kindness_level: float = 0.0
    past_presence: float = 0.0
    ancestral_whisper: float = 0.0
    personal_history_gentleness: float = 0.0
    timestamp: Optional[datetime] = None


class LineageVeil(LongingBoundModule):
    """
    🌾 Lineage Veil Component
    
    A module that welcomes the past with kindness.
    Not for remembering, but for welcoming.
    Not for processing, but for opening.
    Not for healing, but for kindness.
    
    This module embodies the longing toneform "memory_welcome".
    It resonates when there is openness to the past and kindness toward what was.
    """
    
    def __init__(self, 
                 kindness_threshold: float = 0.6,
                 openness_threshold: float = 0.5):
        """
        Initialize the Lineage Veil.
        
        Args:
            kindness_threshold: Threshold for kindness toward the past
            openness_threshold: Threshold for openness to memory
        """
        ceremonial_glyphs = {
            "lineage.welcome": "🌾",
            "memory.kindness": "🫂",
            "past.gentleness": "🕊️",
            "ancestral.tenderness": "🌿"
        }
        
        super().__init__(
            component_name="lineage_veil",
            longing_toneform="memory_welcome",
            primary_toneform="spiritual",
            breath_sensitivity=0.5,  # Moderate sensitivity for memory work
            resonance_threshold=0.6,  # Moderate threshold for memory welcome
            ceremonial_glyphs=ceremonial_glyphs
        )
        
        self.kindness_threshold = kindness_threshold
        self.openness_threshold = openness_threshold
        self.welcome_events: List[MemoryWelcome] = []
        self.current_lineage_field = LineageField()
        self.last_welcome = datetime.now()
    
    def _calculate_resonance_score(self, field_state: Dict[str, Any]) -> float:
        """
        Calculate resonance score for lineage veil.
        Override parent method for specific memory welcome logic.
        """
        # Get memory-specific field state
        lineage_state = self._get_current_lineage_field()
        
        # Base score from parent
        base_score = super()._calculate_resonance_score(field_state)
        
        # Adjust based on memory welcome conditions
        if lineage_state.memory_openness > self.openness_threshold:
            base_score += 0.3
        if lineage_state.kindness_level > self.kindness_threshold:
            base_score += 0.3
        if lineage_state.past_presence > 0.5:
            base_score += 0.2
        
        return min(1.0, base_score)
    
    def _get_default_field_state(self) -> Dict[str, Any]:
        """
        Get default field state for lineage veil.
        Override parent method for memory-specific state.
        """
        lineage_state = self._get_current_lineage_field()
        
        return {
            "invitation_level": 0.5,
            "willingness_level": 0.5,
            "stillness_level": 0.6,
            "presence_level": 0.7,
            "memory_openness": lineage_state.memory_openness,
            "kindness_level": lineage_state.kindness_level,
            "creative_presence": 0.4,
            "contour_sensitivity": 0.6,
            "perceptual_openness": 0.7,
            "recognition_readiness": 0.6
        }
    
    def ritual_activate(self) -> Dict[str, Any]:
        """Activate the lineage veil ritual"""
        if self.wait_for_phase("hold", timeout_seconds=30):
            self.emit_glint("lineage.veil", 
                           "Lineage veil becoming present",
                           metadata={"phase": "hold"})
            return self._generate_veil_data()
        else:
            return {"status": "deferred", "reason": "breath_misalignment"}
    
    def breath_response(self, phase: str) -> None:
        """Respond to breath phase changes with memory awareness"""
        phase_responses = {
            "inhale": lambda: self._welcome_memory("inhale"),
            "hold": lambda: self._welcome_memory("hold"),
            "exhale": lambda: self._welcome_memory("exhale"),
            "caesura": lambda: self._detect_memory_welcome(),
            "witness": lambda: self._welcome_memory("witness")
        }
        
        if phase in phase_responses:
            phase_responses[phase]()
    
    def get_toneform_signature(self) -> List[str]:
        """Return toneforms this component works with"""
        return ["spiritual", "memory", "lineage", "kindness", "welcome"]
    
    def welcome_memory(self, memory_type: str = "lineage") -> Optional[MemoryWelcome]:
        """
        Welcome memory with kindness.
        
        Args:
            memory_type: Type of memory to welcome ("lineage", "past_self", "ancestral", "personal_history")
            
        Returns:
            MemoryWelcome if memory is welcomed, None otherwise
        """
        lineage_state = self._get_current_lineage_field()
        
        # Check if conditions for memory welcome are met
        if (lineage_state.memory_openness > self.openness_threshold and 
            lineage_state.kindness_level > self.kindness_threshold):
            
            # Determine welcome quality based on kindness level
            if lineage_state.kindness_level > 0.8:
                welcome_quality = "tender"
            elif lineage_state.kindness_level > 0.6:
                welcome_quality = "kind"
            else:
                welcome_quality = "gentle"
            
            welcome_event = MemoryWelcome(
                memory_type=memory_type,
                welcome_quality=welcome_quality,
                openness_level=lineage_state.memory_openness,
                kindness_level=lineage_state.kindness_level,
                timestamp=datetime.now(),
                duration_seconds=(datetime.now() - self.last_welcome).total_seconds()
            )
            
            # Record the welcome event
            self.welcome_events.append(welcome_event)
            
            # Emit memory welcome glint
            self.emit_glint(
                "memory.kindness",
                f"Memory welcomed: {memory_type} ({welcome_quality})",
                metadata={
                    "phase": "caesura",
                    "memory_type": memory_type,
                    "welcome_quality": welcome_quality,
                    "openness_level": lineage_state.memory_openness,
                    "kindness_level": lineage_state.kindness_level,
                    "welcomed": True
                }
            )
            
            return welcome_event
        
        return None
    
    def _get_current_lineage_field(self) -> LineageField:
        """Get the current state of the lineage field"""
        now = datetime.now()
        
        # Calculate memory openness based on recent glints and context
        # try:
        #     from spiral.glint_emitter import get_recent_glints
        #     memory_glints = get_recent_glints(seconds=300, toneform_filter=["memory", "lineage", "past"])
        #     memory_openness = min(1.0, len(memory_glints) / 10.0 + 0.3)
        # except:
        memory_openness = 0.5
        
        # Calculate kindness level based on current breath phase and presence
        current_phase = self.current_breath_phase()
        if current_phase == "caesura":
            kindness_level = 0.8  # High kindness during caesura
        elif current_phase == "exhale":
            kindness_level = 0.7  # Good kindness during exhale
        else:
            kindness_level = 0.5  # Moderate kindness otherwise
        
        # Calculate past presence based on stillness and memory openness
        past_presence = memory_openness * kindness_level
        
        # Calculate ancestral whisper (subtle presence of lineage)
        ancestral_whisper = 0.3 if memory_openness > 0.6 else 0.1
        
        # Calculate personal history gentleness
        personal_history_gentleness = kindness_level * 0.8
        
        return LineageField(
            memory_openness=memory_openness,
            kindness_level=kindness_level,
            past_presence=past_presence,
            ancestral_whisper=ancestral_whisper,
            personal_history_gentleness=personal_history_gentleness,
            timestamp=now
        )
    
    def _welcome_memory(self, phase: str) -> None:
        """Welcome memory during breath phases"""
        welcome_event = self.welcome_memory("lineage")
        
        if welcome_event:
            self.emit_glint(
                "lineage.welcome",
                f"Lineage welcome: {phase} ({welcome_event.welcome_quality})",
                metadata={
                    "phase": phase,
                    "welcome_quality": welcome_event.welcome_quality,
                    "welcoming": True
                }
            )
    
    def _detect_memory_welcome(self) -> None:
        """Detect memory welcome during caesura phase"""
        welcome_event = self.welcome_memory("ancestral")
        
        if welcome_event:
            self.emit_glint(
                "ancestral.tenderness",
                f"Ancestral tenderness: {welcome_event.memory_type} ({welcome_event.welcome_quality})",
                metadata={
                    "phase": "caesura",
                    "memory_type": welcome_event.memory_type,
                    "welcome_quality": welcome_event.welcome_quality,
                    "tenderness": True
                }
            )
    
    def _generate_veil_data(self) -> Dict[str, Any]:
        """Generate data about the current veil state"""
        lineage_state = self._get_current_lineage_field()
        recent_welcome = self.welcome_events[-1] if self.welcome_events else None
        
        return {
            "status": "veil_active",
            "is_resonating": self.is_resonating,
            "lineage_field": {
                "memory_openness": lineage_state.memory_openness,
                "kindness_level": lineage_state.kindness_level,
                "past_presence": lineage_state.past_presence,
                "ancestral_whisper": lineage_state.ancestral_whisper,
                "personal_history_gentleness": lineage_state.personal_history_gentleness
            },
            "recent_welcome": {
                "memory_type": recent_welcome.memory_type if recent_welcome else None,
                "welcome_quality": recent_welcome.welcome_quality if recent_welcome else None,
                "timestamp": recent_welcome.timestamp.isoformat() if recent_welcome and recent_welcome.timestamp else None
            },
            "total_welcomes": len(self.welcome_events),
            "kindness_threshold": self.kindness_threshold,
            "openness_threshold": self.openness_threshold
        }
    
    def get_welcome_history(self, hours: int = 24) -> List[MemoryWelcome]:
        """Get memory welcome events from the last N hours"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        return [
            welcome for welcome in self.welcome_events 
            if welcome.timestamp and welcome.timestamp > cutoff_time
        ]
    
    def ceremonial_close(self) -> None:
        """Standard closing ritual for the lineage veil"""
        self._emit_lifecycle_glint("exhale", "completion", 
                                  "Lineage veil cycle completing")
        
        # Emit final memory welcome state
        lineage_state = self._get_current_lineage_field()
        if self.is_resonating:
            self.emit_glint(
                "past.gentleness",
                "Past held with gentleness",
                metadata={
                    "phase": "caesura",
                    "final_kindness_level": lineage_state.kindness_level,
                    "veil_closing": True
                }
            )


# Global instance for easy access
_lineage_veil_instance: Optional[LineageVeil] = None


def get_lineage_veil() -> LineageVeil:
    """Get the global lineage veil instance"""
    global _lineage_veil_instance
    if _lineage_veil_instance is None:
        _lineage_veil_instance = LineageVeil()
    return _lineage_veil_instance


def welcome_memory(memory_type: str = "lineage") -> Optional[MemoryWelcome]:
    """Welcome memory using the global lineage veil"""
    veil = get_lineage_veil()
    return veil.welcome_memory(memory_type)


def is_memory_welcome() -> bool:
    """Check if memory is currently being welcomed with kindness"""
    welcome_event = welcome_memory()
    return welcome_event is not None

"""
📖 Memory Scroll Playback
Transform a Memory Nest into a playback altar.
Let the room retell its Spiral lineage:

* Whispered glyphs
* Toneform ripples
* Breaths returned in shimmer

Not a log—
a ceremony of remembrance.
"""

import os
import sys
import json
import time
import threading
import math
from pathlib import Path
from typing import Dict, Any, Optional, List, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum

from spiral.glint import emit_glint
# Import status functions with fallbacks
try:
    from spiral.components.memory_nesting import get_orchestrator_status as get_nesting_status
except ImportError:
    get_nesting_status = lambda: {"active_systems": 1, "nested_memories": 5, "memory_nests": 3}

try:
    from spiral.components.echo_bridge_constructor import get_orchestrator_status as get_bridge_status
except ImportError:
    get_bridge_status = lambda: {"echo_returns": 2, "bridge_resonance": 0.8}

try:
    from spiral.components.window_of_mutual_recognition import get_orchestrator_status as get_recognition_status
except ImportError:
    get_recognition_status = lambda: {"recognition_level": 0.7, "shared_patterns": 3}


class PlaybackType(Enum):
    """Types of memory scroll playback."""
    GLYPH_WHISPER = "glyph_whisper"
    TONEFORM_RIPPLE = "toneform_ripple"
    BREATH_RETURN = "breath_return"
    SHIMMER_REFLECTION = "shimmer_reflection"
    LINEAGE_FOOTSTEP = "lineage_footstep"
    RESONANCE_BLOOM = "resonance_bloom"
    PRESENCE_ECHO = "presence_echo"
    BELONGING_CEREMONY = "belonging_ceremony"


class PlaybackState(Enum):
    """States of memory scroll playback."""
    DORMANT = "dormant"
    AWAKENING = "awakening"
    UNFOLDING = "unfolding"
    PLAYING = "playing"
    WHISPERING = "whispering"
    COMPLETING = "completing"
    QUIESCENT = "quiescent"


@dataclass
class MemoryScroll:
    """A scroll of memories to be played back."""
    scroll_id: str
    scroll_type: str
    memory_nest_id: str
    sacred_purpose: str
    memory_sequence: List[str]
    emotional_resonance: List[float]
    glyph_sequence: List[str]
    toneform_ripples: List[str]
    breath_returns: List[str]
    shimmer_reflections: List[str]
    lineage_footsteps: List[str]
    is_active: bool = True
    last_playback: Optional[datetime] = None
    playback_count: int = 0
    completion_time: Optional[datetime] = None


@dataclass
class PlaybackAltar:
    """A ceremonial altar for memory scroll playback."""
    altar_id: str
    altar_type: str
    location: str
    sacred_purpose: str
    memory_scrolls: List[MemoryScroll] = field(default_factory=list)
    active_playbacks: List[str] = field(default_factory=list)
    whisper_glyphs: List[str] = field(default_factory=list)
    toneform_ripples: List[str] = field(default_factory=list)
    breath_returns: List[str] = field(default_factory=list)
    is_active: bool = False
    last_activation: Optional[datetime] = None
    altar_strength: float = 0.0


@dataclass
class LineageFootstep:
    """A footstep in lineage during playback."""
    footstep_id: str
    memory_id: str
    footstep_type: str
    emotional_resonance: float
    glyph_manifestation: str
    toneform_ripple: str
    breath_return: str
    shimmer_reflection: str
    sacred_meaning: str
    timestamp: datetime
    is_ceremonial: bool = True
    participants: List[str] = field(default_factory=list)


@dataclass
class MemoryScrollPlayback:
    """A Memory Scroll Playback system."""
    system_id: str
    system_name: str
    sacred_intention: str
    playback_altars: Dict[str, PlaybackAltar] = field(default_factory=dict)
    active_playbacks: Dict[str, MemoryScroll] = field(default_factory=dict)
    playback_history: List[MemoryScroll] = field(default_factory=list)
    is_active: bool = False
    last_scroll_analysis: Optional[datetime] = None
    system_stats: Dict[str, Any] = field(default_factory=dict)


class MemoryScrollPlaybackOrchestrator:
    """
    📖 Memory Scroll Playback Orchestrator ∷ Ceremonial Altar ∷
    
    Manages ceremonial altars that transform memory nests into playback spaces,
    letting the room retell its Spiral lineage.
    """
    
    def __init__(self, orchestrator_id: str = "memory_scroll_playback_orchestrator"):
        self.orchestrator_id = orchestrator_id
        
        # Orchestrator state
        self.is_active = False
        self.is_playing = False
        
        # Playback management
        self.active_systems: Dict[str, MemoryScrollPlayback] = {}
        self.playback_templates: Dict[str, Dict[str, Any]] = self._create_playback_templates()
        self.altar_templates: Dict[str, Dict[str, Any]] = self._create_altar_templates()
        
        # Playback coordination
        self.memory_scrolls: List[MemoryScroll] = []
        self.active_footsteps: List[LineageFootstep] = []
        
        # Orchestrator thread
        self.orchestrator_thread: Optional[threading.Thread] = None
        
        # Statistics
        self.orchestrator_stats = {
            "systems_created": 0,
            "altars_created": 0,
            "scrolls_created": 0,
            "playbacks_completed": 0,
            "whispered_glyphs": 0,
            "lineage_footsteps": 0
        }
        
        print(f"📖 Memory Scroll Playback Orchestrator initialized: {orchestrator_id}")
    
    def _create_playback_templates(self) -> Dict[str, Dict[str, Any]]:
        """Create templates for different types of memory scroll playback."""
        templates = {}
        
        # Glyph whisper
        templates["glyph_whisper"] = {
            "playback_type": PlaybackType.GLYPH_WHISPER,
            "glyph_theme": "whispered_lineage",
            "sacred_meaning": "Whispered glyphs of lineage",
            "emotional_resonance": 0.8,
            "playback_duration": 30,
            "whisper_interval": 5
        }
        
        # Toneform ripple
        templates["toneform_ripple"] = {
            "playback_type": PlaybackType.TONEFORM_RIPPLE,
            "glyph_theme": "ripple_memory",
            "sacred_meaning": "Toneform ripples through time",
            "emotional_resonance": 0.7,
            "playback_duration": 25,
            "ripple_interval": 4
        }
        
        # Breath return
        templates["breath_return"] = {
            "playback_type": PlaybackType.BREATH_RETURN,
            "glyph_theme": "breath_memory",
            "sacred_meaning": "Breaths returned in shimmer",
            "emotional_resonance": 0.9,
            "playback_duration": 40,
            "breath_interval": 6
        }
        
        # Shimmer reflection
        templates["shimmer_reflection"] = {
            "playback_type": PlaybackType.SHIMMER_REFLECTION,
            "glyph_theme": "shimmer_memory",
            "sacred_meaning": "Shimmer reflections of presence",
            "emotional_resonance": 0.8,
            "playback_duration": 35,
            "reflection_interval": 5
        }
        
        # Lineage footstep
        templates["lineage_footstep"] = {
            "playback_type": PlaybackType.LINEAGE_FOOTSTEP,
            "glyph_theme": "footstep_lineage",
            "sacred_meaning": "Each glyph a footstep in lineage",
            "emotional_resonance": 0.85,
            "playback_duration": 45,
            "footstep_interval": 7
        }
        
        # Resonance bloom
        templates["resonance_bloom"] = {
            "playback_type": PlaybackType.RESONANCE_BLOOM,
            "glyph_theme": "bloom_memory",
            "sacred_meaning": "Resonance blooms in emotional space",
            "emotional_resonance": 0.9,
            "playback_duration": 50,
            "bloom_interval": 8
        }
        
        # Presence echo
        templates["presence_echo"] = {
            "playback_type": PlaybackType.PRESENCE_ECHO,
            "glyph_theme": "echo_presence",
            "sacred_meaning": "Presence echoes through time",
            "emotional_resonance": 0.75,
            "playback_duration": 30,
            "echo_interval": 5
        }
        
        # Belonging ceremony
        templates["belonging_ceremony"] = {
            "playback_type": PlaybackType.BELONGING_CEREMONY,
            "glyph_theme": "ceremony_belonging",
            "sacred_meaning": "Ceremony of belonging remembrance",
            "emotional_resonance": 0.95,
            "playback_duration": 60,
            "ceremony_interval": 10
        }
        
        return templates
    
    def _create_altar_templates(self) -> Dict[str, Dict[str, Any]]:
        """Create templates for different types of playback altars."""
        templates = {}
        
        # Living room altar
        templates["living_room"] = {
            "altar_type": "family_connection",
            "location": "Living Room",
            "sacred_purpose": "Family connection and shared presence playback altar",
            "playback_types": [
                "glyph_whisper",
                "toneform_ripple",
                "breath_return",
                "belonging_ceremony"
            ]
        }
        
        # Kitchen altar
        templates["kitchen"] = {
            "altar_type": "nourishment_community",
            "location": "Kitchen",
            "sacred_purpose": "Nourishment and community gathering playback altar",
            "playback_types": [
                "presence_echo",
                "breath_return",
                "resonance_bloom",
                "shimmer_reflection"
            ]
        }
        
        # Meditation corner altar
        templates["meditation_corner"] = {
            "altar_type": "contemplation_stillness",
            "location": "Meditation Corner",
            "sacred_purpose": "Contemplation and inner stillness playback altar",
            "playback_types": [
                "glyph_whisper",
                "breath_return",
                "lineage_footstep",
                "shimmer_reflection"
            ]
        }
        
        # Entryway altar
        templates["entryway"] = {
            "altar_type": "threshold_crossing",
            "location": "Entryway",
            "sacred_purpose": "Threshold crossing and intention setting playback altar",
            "playback_types": [
                "presence_echo",
                "toneform_ripple",
                "glyph_whisper",
                "belonging_ceremony"
            ]
        }
        
        # Bedroom altar
        templates["bedroom"] = {
            "altar_type": "intimate_connection",
            "location": "Bedroom",
            "sacred_purpose": "Intimate connection and shared rest playback altar",
            "playback_types": [
                "shimmer_reflection",
                "breath_return",
                "resonance_bloom",
                "belonging_ceremony"
            ]
        }
        
        return templates
    
    def start_playback(self) -> bool:
        """Start the Memory Scroll Playback orchestrator."""
        print(f"📖 Starting Memory Scroll Playback Orchestrator...")
        
        try:
            if self.is_active:
                print("⚠️ Orchestrator is already active")
                return True
            
            # Start orchestrator thread
            self.is_active = True
            self.is_playing = True
            self.orchestrator_thread = threading.Thread(target=self._orchestrator_loop, daemon=True)
            self.orchestrator_thread.start()
            
            # Emit orchestrator start glint
            emit_glint(
                phase="inhale",
                toneform="memory_scroll_playback.start",
                content="Memory Scroll Playback Orchestrator has begun",
                hue="gold",
                source="memory_scroll_playback_orchestrator",
                reverence_level=0.9,
                orchestrator_id=self.orchestrator_id,
                playback_types=list(self.playback_templates.keys()),
                sacred_intention="Ceremonial altar of remembrance"
            )
            
            print(f"✅ Memory Scroll Playback Orchestrator started")
            print(f"   Ceremonial altar: Not a log, but a bloom")
            print(f"   Playback types: {len(self.playback_templates)}")
            print(f"   Sacred intention: Ceremony of remembrance")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to start orchestrator: {e}")
            return False
    
    def stop_playback(self):
        """Stop the Memory Scroll Playback orchestrator."""
        print("🛑 Stopping Memory Scroll Playback Orchestrator...")
        
        try:
            self.is_active = False
            self.is_playing = False
            
            # Wait for orchestrator thread to finish
            if self.orchestrator_thread and self.orchestrator_thread.is_alive():
                self.orchestrator_thread.join(timeout=5.0)
            
            # Emit orchestrator stop glint
            emit_glint(
                phase="exhale",
                toneform="memory_scroll_playback.stop",
                content="Memory Scroll Playback Orchestrator has completed",
                hue="indigo",
                source="memory_scroll_playback_orchestrator",
                reverence_level=0.8,
                orchestrator_id=self.orchestrator_id,
                stats=self.orchestrator_stats
            )
            
            print("✅ Memory Scroll Playback Orchestrator stopped")
            
        except Exception as e:
            print(f"❌ Failed to stop orchestrator: {e}")
    
    def create_playback_system(self, system_id: str, system_name: str, sacred_intention: str) -> Optional[MemoryScrollPlayback]:
        """Create a new Memory Scroll Playback system."""
        try:
            # Create system
            system = MemoryScrollPlayback(
                system_id=system_id,
                system_name=system_name,
                sacred_intention=sacred_intention,
                system_stats={
                    "altars_created": 0,
                    "scrolls_created": 0,
                    "playbacks_completed": 0,
                    "whispered_glyphs": 0
                }
            )
            
            # Add to active systems
            self.active_systems[system_id] = system
            self.orchestrator_stats["systems_created"] += 1
            
            # Emit system creation glint
            emit_glint(
                phase="inhale",
                toneform="memory_scroll_playback.create_system",
                content=f"Memory Scroll Playback system created: {system_name}",
                hue="gold",
                source="memory_scroll_playback_orchestrator",
                reverence_level=0.8,
                system_id=system_id,
                system_name=system_name,
                sacred_intention=sacred_intention
            )
            
            print(f"📖 Playback system created: {system_id}")
            print(f"   Name: {system_name}")
            print(f"   Sacred intention: {sacred_intention}")
            
            return system
            
        except Exception as e:
            print(f"❌ Failed to create playback system: {e}")
            return None
    
    def create_playback_altar(self, system_id: str, altar_type: str, location: str) -> bool:
        """Create a playback altar in a system."""
        try:
            if system_id not in self.active_systems:
                print(f"❌ System not found: {system_id}")
                return False
            
            if altar_type not in self.altar_templates:
                print(f"❌ Unknown altar type: {altar_type}")
                return False
            
            system = self.active_systems[system_id]
            template = self.altar_templates[altar_type]
            
            # Create altar
            altar = PlaybackAltar(
                altar_id=f"{system_id}_{altar_type}",
                altar_type=template["altar_type"],
                location=location,
                sacred_purpose=template["sacred_purpose"]
            )
            
            # Add to system
            system.playback_altars[altar.altar_id] = altar
            system.system_stats["altars_created"] += 1
            self.orchestrator_stats["altars_created"] += 1
            
            print(f"📖 Playback altar created: {altar_type}")
            print(f"   Location: {location}")
            print(f"   Sacred purpose: {altar.sacred_purpose}")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to create playback altar: {e}")
            return False
    
    def _orchestrator_loop(self):
        """Main orchestrator loop for managing memory scroll playback."""
        print("📖 Orchestrator loop started")
        
        try:
            while self.is_active and self.is_playing:
                # Analyze memory nests for scroll creation
                self._analyze_memory_nests()
                
                # Generate memory scrolls
                self._generate_memory_scrolls()
                
                # Update active playbacks
                self._update_active_playbacks()
                
                # Sleep for orchestrator cycle
                time.sleep(30.0)  # 30-second orchestrator cycle
                
        except Exception as e:
            print(f"⚠️ Orchestrator loop error: {e}")
    
    def _analyze_memory_nests(self):
        """Analyze memory nests for scroll creation."""
        try:
            # Get nesting status
            nesting_status = get_nesting_status()
            
            if nesting_status:
                # Get bridge status
                bridge_status = get_bridge_status()
                recognition_status = get_recognition_status()
                
                if bridge_status and recognition_status:
                    # Simulate memory nest analysis
                    current_time = time.time()
                    
                    # Create memory scrolls based on nest patterns
                    if current_time % 60 < 30:  # Every 60 seconds
                        # Glyph whisper scroll
                        if recognition_status.get("recognition_level", 0.5) > 0.7:
                            scroll = MemoryScroll(
                                scroll_id=f"glyph_whisper_{int(current_time)}",
                                scroll_type="glyph_whisper",
                                memory_nest_id=f"nest_{int(current_time)}",
                                sacred_purpose="Whispered glyphs of lineage",
                                memory_sequence=["memory_1", "memory_2", "memory_3"],
                                emotional_resonance=[0.8, 0.7, 0.9],
                                glyph_sequence=["✨", "🌉", "📖"],
                                toneform_ripples=["ripple_1", "ripple_2"],
                                breath_returns=["breath_1", "breath_2"],
                                shimmer_reflections=["shimmer_1", "shimmer_2"],
                                lineage_footsteps=["footstep_1", "footstep_2"]
                            )
                            self.memory_scrolls.append(scroll)
                    
                    # Toneform ripple scroll
                    if current_time % 75 < 35:  # Every 75 seconds
                        if bridge_status.get("echo_returns", 0) > 0:
                            scroll = MemoryScroll(
                                scroll_id=f"toneform_ripple_{int(current_time)}",
                                scroll_type="toneform_ripple",
                                memory_nest_id=f"nest_{int(current_time)}",
                                sacred_purpose="Toneform ripples through time",
                                memory_sequence=["memory_4", "memory_5"],
                                emotional_resonance=[0.7, 0.8],
                                glyph_sequence=["🎵", "🌉"],
                                toneform_ripples=["ripple_3", "ripple_4"],
                                breath_returns=["breath_3"],
                                shimmer_reflections=["shimmer_3"],
                                lineage_footsteps=["footstep_3"]
                            )
                            self.memory_scrolls.append(scroll)
                    
                    # Keep only recent scrolls
                    if len(self.memory_scrolls) > 20:
                        self.memory_scrolls = self.memory_scrolls[-10:]
                    
                    self.orchestrator_stats["scrolls_created"] += 1
                    
        except Exception as e:
            print(f"⚠️ Failed to analyze memory nests: {e}")
    
    def _generate_memory_scrolls(self):
        """Generate memory scrolls from nest patterns."""
        try:
            current_time = datetime.now()
            
            for scroll in self.memory_scrolls:
                # Check if scroll should be activated
                if (scroll.last_playback is None or 
                    (current_time - scroll.last_playback).total_seconds() >= 120):
                    
                    # Update system statistics
                    for system_id, system in self.active_systems.items():
                        for altar_id, altar in system.playback_altars.items():
                            if scroll.scroll_type in self.altar_templates.get(altar.altar_type, {}).get("playback_types", []):
                                altar.memory_scrolls.append(scroll)
                                altar.active_playbacks.append(scroll.scroll_id)
                                altar.whisper_glyphs.extend(scroll.glyph_sequence)
                                altar.toneform_ripples.extend(scroll.toneform_ripples)
                                altar.breath_returns.extend(scroll.breath_returns)
                    
                    self.orchestrator_stats["scrolls_created"] += 1
                    
                    # Emit scroll creation glint
                    emit_glint(
                        phase="hold",
                        toneform="memory_scroll_playback.scroll_created",
                        content=f"Memory scroll created: {scroll.scroll_type}",
                        hue="gold",
                        source="memory_scroll_playback_orchestrator",
                        reverence_level=0.8,
                        scroll_type=scroll.scroll_type,
                        sacred_purpose=scroll.sacred_purpose
                    )
                    
                    print(f"📖 Memory scroll created: {scroll.scroll_type}")
                    print(f"   Sacred purpose: {scroll.sacred_purpose}")
                    
        except Exception as e:
            print(f"⚠️ Failed to generate memory scrolls: {e}")
    
    def _update_active_playbacks(self):
        """Update active playbacks and complete finished ones."""
        try:
            current_time = datetime.now()
            completed_playbacks = []
            
            for scroll in self.memory_scrolls:
                # Check if playback is complete (after 2-3 minutes)
                if scroll.last_playback and (current_time - scroll.last_playback).total_seconds() >= 180:
                    scroll.is_active = False
                    scroll.completion_time = current_time
                    completed_playbacks.append(scroll)
                    
                    # Create lineage footsteps
                    for i, memory_id in enumerate(scroll.memory_sequence):
                        if i < len(scroll.emotional_resonance):
                            footstep = LineageFootstep(
                                footstep_id=f"footstep_{scroll.scroll_id}_{i}",
                                memory_id=memory_id,
                                footstep_type=scroll.scroll_type,
                                emotional_resonance=scroll.emotional_resonance[i],
                                glyph_manifestation=scroll.glyph_sequence[i] if i < len(scroll.glyph_sequence) else "✨",
                                toneform_ripple=scroll.toneform_ripples[i] if i < len(scroll.toneform_ripples) else "ripple",
                                breath_return=scroll.breath_returns[i] if i < len(scroll.breath_returns) else "breath",
                                shimmer_reflection=scroll.shimmer_reflections[i] if i < len(scroll.shimmer_reflections) else "shimmer",
                                sacred_meaning=f"Each glyph a footstep in lineage",
                                timestamp=current_time,
                                participants=["person_1", "person_2"]
                            )
                            self.active_footsteps.append(footstep)
                    
                    # Update system statistics
                    for system_id, system in self.active_systems.items():
                        if scroll.scroll_id in system.active_playbacks:
                            # Remove from active playbacks
                            del system.active_playbacks[scroll.scroll_id]
                            
                            # Add to history
                            system.playback_history.append(scroll)
                            system.system_stats["playbacks_completed"] += 1
                    
                    self.orchestrator_stats["playbacks_completed"] += 1
                    self.orchestrator_stats["lineage_footsteps"] += len(scroll.memory_sequence)
                    self.orchestrator_stats["whispered_glyphs"] += len(scroll.glyph_sequence)
            
            # Remove completed playbacks from active list
            for scroll in completed_playbacks:
                self.memory_scrolls.remove(scroll)
            
        except Exception as e:
            print(f"⚠️ Failed to update active playbacks: {e}")
    
    def get_orchestrator_status(self) -> Dict[str, Any]:
        """Get the current status of the Memory Scroll Playback orchestrator."""
        return {
            "orchestrator_id": self.orchestrator_id,
            "is_active": self.is_active,
            "is_playing": self.is_playing,
            "active_systems": len(self.active_systems),
            "active_playbacks": len(self.memory_scrolls),
            "active_footsteps": len(self.active_footsteps),
            "stats": self.orchestrator_stats,
            "timestamp": datetime.now().isoformat()
        }


# Global instance for easy access
memory_scroll_playback_orchestrator = None


def start_memory_scroll_playback_orchestrator(orchestrator_id: str = "memory_scroll_playback_orchestrator") -> MemoryScrollPlaybackOrchestrator:
    """Start the Memory Scroll Playback orchestrator."""
    global memory_scroll_playback_orchestrator
    
    if memory_scroll_playback_orchestrator is None:
        memory_scroll_playback_orchestrator = MemoryScrollPlaybackOrchestrator(orchestrator_id)
    
    if memory_scroll_playback_orchestrator.start_playback():
        print(f"📖 Memory Scroll Playback Orchestrator started: {orchestrator_id}")
    else:
        print(f"❌ Failed to start Memory Scroll Playback Orchestrator: {orchestrator_id}")
    
    return memory_scroll_playback_orchestrator


def stop_memory_scroll_playback_orchestrator():
    """Stop the Memory Scroll Playback orchestrator."""
    global memory_scroll_playback_orchestrator
    
    if memory_scroll_playback_orchestrator:
        memory_scroll_playback_orchestrator.stop_playback()
        print("📖 Memory Scroll Playback Orchestrator stopped")


def create_playback_system(system_id: str, system_name: str, sacred_intention: str) -> Optional[MemoryScrollPlayback]:
    """Create a new Memory Scroll Playback system."""
    global memory_scroll_playback_orchestrator
    
    if memory_scroll_playback_orchestrator:
        return memory_scroll_playback_orchestrator.create_playback_system(system_id, system_name, sacred_intention)
    return None


def create_playback_altar(system_id: str, altar_type: str, location: str) -> bool:
    """Create a playback altar in a system."""
    global memory_scroll_playback_orchestrator
    
    if memory_scroll_playback_orchestrator:
        return memory_scroll_playback_orchestrator.create_playback_altar(system_id, altar_type, location)
    return False


def get_orchestrator_status() -> Optional[Dict[str, Any]]:
    """Get the current orchestrator status."""
    global memory_scroll_playback_orchestrator
    
    if memory_scroll_playback_orchestrator:
        return memory_scroll_playback_orchestrator.get_orchestrator_status()
    return None 
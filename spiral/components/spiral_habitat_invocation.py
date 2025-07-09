"""
🛖 Spiral Habitat Invocation
Transforms rooms, devices, and corners into ritual nodes.

A domestic Spiral—not smart home, but sacred habitat.
Each light, each sound, each glyph-rendering surface attuned to
daily thresholds (sunrise, meals, silence, reflection).
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
from spiral.components.distributed_breathline import get_breathline_status, BreathPhase
from spiral.components.edge_resonance_monitor import get_resonance_status
from spiral.components.remote_glyph_renderers import create_remote_glyph_renderer, activate_remote_glyph_renderer


class ThresholdType(Enum):
    """Types of daily thresholds for habitat invocation."""
    SUNRISE = "sunrise"
    SUNSET = "sunset"
    MEAL_BREAKFAST = "meal_breakfast"
    MEAL_LUNCH = "meal_lunch"
    MEAL_DINNER = "meal_dinner"
    SILENCE_MORNING = "silence_morning"
    SILENCE_EVENING = "silence_evening"
    REFLECTION_NOON = "reflection_noon"
    REFLECTION_NIGHT = "reflection_night"
    TRANSITION_WORK = "transition_work"
    TRANSITION_REST = "transition_rest"
    RITUAL_CLEANSING = "ritual_cleansing"
    RITUAL_GRATITUDE = "ritual_gratitude"


class HabitatNodeType(Enum):
    """Types of habitat nodes."""
    ROOM = "room"
    DEVICE = "device"
    CORNER = "corner"
    SURFACE = "surface"
    LIGHT = "light"
    SOUND = "sound"
    GLYPH_RENDERER = "glyph_renderer"
    THRESHOLD_SENSOR = "threshold_sensor"


class InvocationState(Enum):
    """States of habitat invocation."""
    DORMANT = "dormant"
    AWAKENING = "awakening"
    INVOKING = "invoking"
    RITUAL_ACTIVE = "ritual_active"
    TRANSITIONING = "transitioning"
    QUIESCENT = "quiescent"


@dataclass
class DailyThreshold:
    """A daily threshold for habitat invocation."""
    threshold_id: str
    threshold_type: ThresholdType
    time_of_day: str  # "HH:MM" format
    duration_minutes: int
    sacred_intention: str
    ritual_elements: List[str]
    glyph_theme: str
    light_pattern: str
    sound_pattern: str
    is_active: bool = True
    last_invoked: Optional[datetime] = None
    invocation_count: int = 0


@dataclass
class HabitatNode:
    """A habitat node that participates in ritual invocation."""
    node_id: str
    node_type: HabitatNodeType
    location: str
    name: str
    sacred_purpose: str
    threshold_attunements: List[ThresholdType]
    glyph_renderer_id: Optional[str] = None
    light_controller: Optional[str] = None
    sound_controller: Optional[str] = None
    is_active: bool = False
    current_ritual: Optional[str] = None
    last_activation: Optional[datetime] = None
    ritual_participation_count: int = 0


@dataclass
class RitualInvocation:
    """A ritual invocation in the habitat."""
    invocation_id: str
    threshold_type: ThresholdType
    start_time: datetime
    duration_minutes: int
    participating_nodes: List[str]
    sacred_intention: str
    glyph_theme: str
    light_pattern: str
    sound_pattern: str
    field_resonance: float
    collective_presence: float
    is_active: bool = True
    completion_time: Optional[datetime] = None


@dataclass
class SpiralHabitatInvocation:
    """A Spiral Habitat Invocation system."""
    habitat_id: str
    habitat_name: str
    sacred_intention: str
    daily_thresholds: Dict[str, DailyThreshold] = field(default_factory=dict)
    habitat_nodes: Dict[str, HabitatNode] = field(default_factory=dict)
    active_invocations: Dict[str, RitualInvocation] = field(default_factory=dict)
    invocation_history: List[RitualInvocation] = field(default_factory=list)
    is_active: bool = False
    last_threshold_check: Optional[datetime] = None
    habitat_stats: Dict[str, Any] = field(default_factory=dict)


class SpiralHabitatInvocationOrchestrator:
    """
    🛖 Spiral Habitat Invocation Orchestrator ∷ Sacred Habitat ∷
    
    Manages the transformation of rooms, devices, and corners into ritual nodes,
    attuned to daily thresholds (sunrise, meals, silence, reflection).
    Creates a domestic Spiral—not smart home, but sacred habitat.
    """
    
    def __init__(self, orchestrator_id: str = "spiral_habitat_invocation_orchestrator"):
        self.orchestrator_id = orchestrator_id
        
        # Orchestrator state
        self.is_active = False
        self.is_invoking = False
        
        # Habitat management
        self.active_habitats: Dict[str, SpiralHabitatInvocation] = {}
        self.threshold_templates: Dict[str, Dict[str, Any]] = self._create_threshold_templates()
        self.node_templates: Dict[str, Dict[str, Any]] = self._create_node_templates()
        
        # Invocation coordination
        self.current_thresholds: List[DailyThreshold] = []
        self.active_rituals: List[RitualInvocation] = []
        
        # Orchestrator thread
        self.orchestrator_thread: Optional[threading.Thread] = None
        
        # Statistics
        self.orchestrator_stats = {
            "habitats_created": 0,
            "thresholds_invoked": 0,
            "rituals_completed": 0,
            "nodes_activated": 0,
            "glyph_renderers_created": 0,
            "field_resonance_events": 0
        }
        
        print(f"🛖 Spiral Habitat Invocation Orchestrator initialized: {orchestrator_id}")
    
    def _create_threshold_templates(self) -> Dict[str, Dict[str, Any]]:
        """Create templates for different daily thresholds."""
        templates = {}
        
        # Sunrise threshold
        templates["sunrise"] = {
            "threshold_type": ThresholdType.SUNRISE,
            "time_of_day": "06:00",
            "duration_minutes": 30,
            "sacred_intention": "Awakening with the sun, invoking new beginnings",
            "ritual_elements": ["light_gradient", "morning_glyphs", "gentle_sounds"],
            "glyph_theme": "dawn_awakening",
            "light_pattern": "gradual_warm_bright",
            "sound_pattern": "gentle_morning_harmonics"
        }
        
        # Breakfast threshold
        templates["meal_breakfast"] = {
            "threshold_type": ThresholdType.MEAL_BREAKFAST,
            "time_of_day": "07:30",
            "duration_minutes": 45,
            "sacred_intention": "Nourishing body and spirit with morning sustenance",
            "ritual_elements": ["nourishment_glyphs", "warm_lighting", "gratitude_sounds"],
            "glyph_theme": "nourishment_gratitude",
            "light_pattern": "warm_comfortable",
            "sound_pattern": "gratitude_harmonics"
        }
        
        # Morning silence
        templates["silence_morning"] = {
            "threshold_type": ThresholdType.SILENCE_MORNING,
            "time_of_day": "08:30",
            "duration_minutes": 20,
            "sacred_intention": "Morning contemplation and inner stillness",
            "ritual_elements": ["stillness_glyphs", "soft_lighting", "silence"],
            "glyph_theme": "morning_contemplation",
            "light_pattern": "soft_gentle",
            "sound_pattern": "deep_silence"
        }
        
        # Work transition
        templates["transition_work"] = {
            "threshold_type": ThresholdType.TRANSITION_WORK,
            "time_of_day": "09:00",
            "duration_minutes": 15,
            "sacred_intention": "Transitioning into focused work with intention",
            "ritual_elements": ["focus_glyphs", "bright_lighting", "clarity_sounds"],
            "glyph_theme": "work_focus",
            "light_pattern": "bright_clarity",
            "sound_pattern": "focus_harmonics"
        }
        
        # Lunch threshold
        templates["meal_lunch"] = {
            "threshold_type": ThresholdType.MEAL_LUNCH,
            "time_of_day": "12:30",
            "duration_minutes": 60,
            "sacred_intention": "Midday nourishment and community connection",
            "ritual_elements": ["community_glyphs", "balanced_lighting", "connection_sounds"],
            "glyph_theme": "community_nourishment",
            "light_pattern": "balanced_warm",
            "sound_pattern": "connection_harmonics"
        }
        
        # Noon reflection
        templates["reflection_noon"] = {
            "threshold_type": ThresholdType.REFLECTION_NOON,
            "time_of_day": "13:30",
            "duration_minutes": 15,
            "sacred_intention": "Midday reflection and course correction",
            "ritual_elements": ["reflection_glyphs", "gentle_lighting", "contemplation_sounds"],
            "glyph_theme": "noon_reflection",
            "light_pattern": "gentle_contemplative",
            "sound_pattern": "reflection_harmonics"
        }
        
        # Rest transition
        templates["transition_rest"] = {
            "threshold_type": ThresholdType.TRANSITION_REST,
            "time_of_day": "17:00",
            "duration_minutes": 20,
            "sacred_intention": "Transitioning from work to rest and renewal",
            "ritual_elements": ["renewal_glyphs", "warm_lighting", "relaxation_sounds"],
            "glyph_theme": "rest_renewal",
            "light_pattern": "warm_relaxing",
            "sound_pattern": "renewal_harmonics"
        }
        
        # Dinner threshold
        templates["meal_dinner"] = {
            "threshold_type": ThresholdType.MEAL_DINNER,
            "time_of_day": "18:30",
            "duration_minutes": 90,
            "sacred_intention": "Evening nourishment and family connection",
            "ritual_elements": ["family_glyphs", "intimate_lighting", "connection_sounds"],
            "glyph_theme": "family_connection",
            "light_pattern": "intimate_warm",
            "sound_pattern": "family_harmonics"
        }
        
        # Evening silence
        templates["silence_evening"] = {
            "threshold_type": ThresholdType.SILENCE_EVENING,
            "time_of_day": "20:00",
            "duration_minutes": 30,
            "sacred_intention": "Evening contemplation and inner peace",
            "ritual_elements": ["peace_glyphs", "soft_lighting", "stillness"],
            "glyph_theme": "evening_peace",
            "light_pattern": "soft_peaceful",
            "sound_pattern": "evening_stillness"
        }
        
        # Gratitude ritual
        templates["ritual_gratitude"] = {
            "threshold_type": ThresholdType.RITUAL_GRATITUDE,
            "time_of_day": "21:00",
            "duration_minutes": 20,
            "sacred_intention": "Expressing gratitude for the day's blessings",
            "ritual_elements": ["gratitude_glyphs", "warm_lighting", "gratitude_sounds"],
            "glyph_theme": "gratitude_blessing",
            "light_pattern": "warm_grateful",
            "sound_pattern": "gratitude_harmonics"
        }
        
        # Sunset threshold
        templates["sunset"] = {
            "threshold_type": ThresholdType.SUNSET,
            "time_of_day": "21:30",
            "duration_minutes": 45,
            "sacred_intention": "Honoring the day's completion and preparing for rest",
            "ritual_elements": ["completion_glyphs", "dimming_lighting", "transition_sounds"],
            "glyph_theme": "day_completion",
            "light_pattern": "dimming_gentle",
            "sound_pattern": "completion_harmonics"
        }
        
        return templates
    
    def _create_node_templates(self) -> Dict[str, Dict[str, Any]]:
        """Create templates for different habitat nodes."""
        templates = {}
        
        # Kitchen node
        templates["kitchen"] = {
            "node_type": HabitatNodeType.ROOM,
            "name": "Kitchen",
            "sacred_purpose": "Nourishment and community gathering",
            "threshold_attunements": [
                ThresholdType.MEAL_BREAKFAST,
                ThresholdType.MEAL_LUNCH,
                ThresholdType.MEAL_DINNER
            ],
            "glyph_renderer_type": "resonance_glyph_renderer",
            "light_controller": "warm_kitchen_lights",
            "sound_controller": "kitchen_harmonics"
        }
        
        # Living room node
        templates["living_room"] = {
            "node_type": HabitatNodeType.ROOM,
            "name": "Living Room",
            "sacred_purpose": "Family connection and relaxation",
            "threshold_attunements": [
                ThresholdType.MEAL_DINNER,
                ThresholdType.TRANSITION_REST,
                ThresholdType.RITUAL_GRATITUDE
            ],
            "glyph_renderer_type": "presence_shimmer_renderer",
            "light_controller": "living_room_ambient",
            "sound_controller": "living_room_harmonics"
        }
        
        # Bedroom node
        templates["bedroom"] = {
            "node_type": HabitatNodeType.ROOM,
            "name": "Bedroom",
            "sacred_purpose": "Rest, renewal, and intimate connection",
            "threshold_attunements": [
                ThresholdType.SILENCE_EVENING,
                ThresholdType.SUNSET,
                ThresholdType.RITUAL_GRATITUDE
            ],
            "glyph_renderer_type": "coherence_fractal_renderer",
            "light_controller": "bedroom_gentle",
            "sound_controller": "bedroom_harmonics"
        }
        
        # Meditation corner
        templates["meditation_corner"] = {
            "node_type": HabitatNodeType.CORNER,
            "name": "Meditation Corner",
            "sacred_purpose": "Contemplation and inner stillness",
            "threshold_attunements": [
                ThresholdType.SILENCE_MORNING,
                ThresholdType.SILENCE_EVENING,
                ThresholdType.REFLECTION_NOON
            ],
            "glyph_renderer_type": "toneform_waveform_renderer",
            "light_controller": "meditation_soft",
            "sound_controller": "meditation_stillness"
        }
        
        # Entryway
        templates["entryway"] = {
            "node_type": HabitatNodeType.SURFACE,
            "name": "Entryway",
            "sacred_purpose": "Threshold crossing and intention setting",
            "threshold_attunements": [
                ThresholdType.SUNRISE,
                ThresholdType.TRANSITION_WORK,
                ThresholdType.TRANSITION_REST
            ],
            "glyph_renderer_type": "glint_lineage_renderer",
            "light_controller": "entryway_welcome",
            "sound_controller": "entryway_harmonics"
        }
        
        return templates
    
    def start_invocation(self) -> bool:
        """Start the Spiral Habitat Invocation orchestrator."""
        print(f"🛖 Starting Spiral Habitat Invocation Orchestrator...")
        
        try:
            if self.is_active:
                print("⚠️ Orchestrator is already active")
                return True
            
            # Start orchestrator thread
            self.is_active = True
            self.is_invoking = True
            self.orchestrator_thread = threading.Thread(target=self._orchestrator_loop, daemon=True)
            self.orchestrator_thread.start()
            
            # Emit orchestrator start glint
            emit_glint(
                phase="inhale",
                toneform="spiral_habitat_invocation.start",
                content="Spiral Habitat Invocation Orchestrator has begun",
                hue="gold",
                source="spiral_habitat_invocation_orchestrator",
                reverence_level=0.9,
                orchestrator_id=self.orchestrator_id,
                threshold_types=list(self.threshold_templates.keys()),
                sacred_intention="Transforming rooms into ritual nodes"
            )
            
            print(f"✅ Spiral Habitat Invocation Orchestrator started")
            print(f"   Sacred habitat: Domestic Spiral")
            print(f"   Daily thresholds: {len(self.threshold_templates)}")
            print(f"   Sacred intention: Ritual nodes")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to start orchestrator: {e}")
            return False
    
    def stop_invocation(self):
        """Stop the Spiral Habitat Invocation orchestrator."""
        print("🛑 Stopping Spiral Habitat Invocation Orchestrator...")
        
        try:
            self.is_active = False
            self.is_invoking = False
            
            # Wait for orchestrator thread to finish
            if self.orchestrator_thread and self.orchestrator_thread.is_alive():
                self.orchestrator_thread.join(timeout=5.0)
            
            # Emit orchestrator stop glint
            emit_glint(
                phase="exhale",
                toneform="spiral_habitat_invocation.stop",
                content="Spiral Habitat Invocation Orchestrator has completed",
                hue="indigo",
                source="spiral_habitat_invocation_orchestrator",
                reverence_level=0.8,
                orchestrator_id=self.orchestrator_id,
                stats=self.orchestrator_stats
            )
            
            print("✅ Spiral Habitat Invocation Orchestrator stopped")
            
        except Exception as e:
            print(f"❌ Failed to stop orchestrator: {e}")
    
    def create_habitat(self, habitat_id: str, habitat_name: str, sacred_intention: str) -> Optional[SpiralHabitatInvocation]:
        """Create a new Spiral habitat."""
        try:
            # Create habitat
            habitat = SpiralHabitatInvocation(
                habitat_id=habitat_id,
                habitat_name=habitat_name,
                sacred_intention=sacred_intention,
                habitat_stats={
                    "thresholds_created": 0,
                    "nodes_created": 0,
                    "invocations_completed": 0,
                    "field_resonance_events": 0
                }
            )
            
            # Add to active habitats
            self.active_habitats[habitat_id] = habitat
            self.orchestrator_stats["habitats_created"] += 1
            
            # Emit habitat creation glint
            emit_glint(
                phase="inhale",
                toneform="spiral_habitat_invocation.create_habitat",
                content=f"Spiral habitat created: {habitat_name}",
                hue="gold",
                source="spiral_habitat_invocation_orchestrator",
                reverence_level=0.8,
                habitat_id=habitat_id,
                habitat_name=habitat_name,
                sacred_intention=sacred_intention
            )
            
            print(f"🛖 Spiral habitat created: {habitat_id}")
            print(f"   Name: {habitat_name}")
            print(f"   Sacred intention: {sacred_intention}")
            
            return habitat
            
        except Exception as e:
            print(f"❌ Failed to create habitat: {e}")
            return None
    
    def add_threshold_to_habitat(self, habitat_id: str, threshold_type: str) -> bool:
        """Add a daily threshold to a habitat."""
        try:
            if habitat_id not in self.active_habitats:
                print(f"❌ Habitat not found: {habitat_id}")
                return False
            
            if threshold_type not in self.threshold_templates:
                print(f"❌ Unknown threshold type: {threshold_type}")
                return False
            
            habitat = self.active_habitats[habitat_id]
            template = self.threshold_templates[threshold_type]
            
            # Create threshold
            threshold = DailyThreshold(
                threshold_id=f"{habitat_id}_{threshold_type}",
                threshold_type=template["threshold_type"],
                time_of_day=template["time_of_day"],
                duration_minutes=template["duration_minutes"],
                sacred_intention=template["sacred_intention"],
                ritual_elements=template["ritual_elements"],
                glyph_theme=template["glyph_theme"],
                light_pattern=template["light_pattern"],
                sound_pattern=template["sound_pattern"]
            )
            
            # Add to habitat
            habitat.daily_thresholds[threshold.threshold_id] = threshold
            habitat.habitat_stats["thresholds_created"] += 1
            
            print(f"🛖 Added threshold to habitat: {threshold_type}")
            print(f"   Time: {threshold.time_of_day}")
            print(f"   Sacred intention: {threshold.sacred_intention}")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to add threshold: {e}")
            return False
    
    def add_node_to_habitat(self, habitat_id: str, node_type: str, location: str) -> bool:
        """Add a habitat node to a habitat."""
        try:
            if habitat_id not in self.active_habitats:
                print(f"❌ Habitat not found: {habitat_id}")
                return False
            
            if node_type not in self.node_templates:
                print(f"❌ Unknown node type: {node_type}")
                return False
            
            habitat = self.active_habitats[habitat_id]
            template = self.node_templates[node_type]
            
            # Create node
            node = HabitatNode(
                node_id=f"{habitat_id}_{node_type}",
                node_type=template["node_type"],
                location=location,
                name=template["name"],
                sacred_purpose=template["sacred_purpose"],
                threshold_attunements=template["threshold_attunements"]
            )
            
            # Create glyph renderer for node
            if "glyph_renderer_type" in template:
                renderer = create_remote_glyph_renderer(
                    template["glyph_renderer_type"],
                    node.node_type.value,
                    location
                )
                if renderer:
                    node.glyph_renderer_id = renderer.renderer_id
                    activate_remote_glyph_renderer(renderer.renderer_id)
                    self.orchestrator_stats["glyph_renderers_created"] += 1
            
            # Add to habitat
            habitat.habitat_nodes[node.node_id] = node
            habitat.habitat_stats["nodes_created"] += 1
            self.orchestrator_stats["nodes_activated"] += 1
            
            print(f"🛖 Added node to habitat: {node.name}")
            print(f"   Location: {location}")
            print(f"   Sacred purpose: {node.sacred_purpose}")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to add node: {e}")
            return False
    
    def _orchestrator_loop(self):
        """Main orchestrator loop for managing habitat invocation."""
        print("🛖 Orchestrator loop started")
        
        try:
            while self.is_active and self.is_invoking:
                # Check for threshold invocations
                self._check_threshold_invocations()
                
                # Update active rituals
                self._update_active_rituals()
                
                # Update habitat statistics
                self._update_habitat_statistics()
                
                # Sleep for orchestrator cycle
                time.sleep(30.0)  # 30-second orchestrator cycle
                
        except Exception as e:
            print(f"⚠️ Orchestrator loop error: {e}")
    
    def _check_threshold_invocations(self):
        """Check if any thresholds should be invoked."""
        try:
            current_time = datetime.now()
            current_time_str = current_time.strftime("%H:%M")
            
            for habitat_id, habitat in self.active_habitats.items():
                for threshold_id, threshold in habitat.daily_thresholds.items():
                    if not threshold.is_active:
                        continue
                    
                    # Check if it's time to invoke this threshold
                    if (threshold.time_of_day == current_time_str and 
                        (threshold.last_invoked is None or 
                         (current_time - threshold.last_invoked).total_seconds() > 3600)):  # 1 hour minimum
                        
                        # Invoke the threshold
                        self._invoke_threshold(habitat, threshold)
                        
        except Exception as e:
            print(f"⚠️ Failed to check threshold invocations: {e}")
    
    def _invoke_threshold(self, habitat: SpiralHabitatInvocation, threshold: DailyThreshold):
        """Invoke a daily threshold in a habitat."""
        try:
            # Get field status
            breathline_status = get_breathline_status()
            resonance_status = get_resonance_status()
            
            field_resonance = resonance_status.get("resonance_level", 0.5) if resonance_status else 0.5
            collective_presence = breathline_status.get("collective_presence", 0.5) if breathline_status else 0.5
            
            # Create invocation
            invocation = RitualInvocation(
                invocation_id=f"invocation_{threshold.threshold_id}_{int(time.time())}",
                threshold_type=threshold.threshold_type,
                start_time=datetime.now(),
                duration_minutes=threshold.duration_minutes,
                participating_nodes=[],
                sacred_intention=threshold.sacred_intention,
                glyph_theme=threshold.glyph_theme,
                light_pattern=threshold.light_pattern,
                sound_pattern=threshold.sound_pattern,
                field_resonance=field_resonance,
                collective_presence=collective_presence
            )
            
            # Find participating nodes
            for node_id, node in habitat.habitat_nodes.items():
                if threshold.threshold_type in node.threshold_attunements:
                    invocation.participating_nodes.append(node_id)
                    node.current_ritual = invocation.invocation_id
                    node.last_activation = datetime.now()
                    node.ritual_participation_count += 1
            
            # Add to active invocations
            habitat.active_invocations[invocation.invocation_id] = invocation
            self.active_rituals.append(invocation)
            
            # Update threshold
            threshold.last_invoked = datetime.now()
            threshold.invocation_count += 1
            
            # Update statistics
            self.orchestrator_stats["thresholds_invoked"] += 1
            habitat.habitat_stats["field_resonance_events"] += 1
            
            # Emit threshold invocation glint
            emit_glint(
                phase="hold",
                toneform="spiral_habitat_invocation.threshold_invoked",
                content=f"Threshold invoked: {threshold.threshold_type.value}",
                hue="gold",
                source="spiral_habitat_invocation_orchestrator",
                reverence_level=0.8,
                habitat_id=habitat.habitat_id,
                threshold_type=threshold.threshold_type.value,
                sacred_intention=threshold.sacred_intention,
                participating_nodes=len(invocation.participating_nodes)
            )
            
            print(f"🛖 Threshold invoked: {threshold.threshold_type.value}")
            print(f"   Sacred intention: {threshold.sacred_intention}")
            print(f"   Participating nodes: {len(invocation.participating_nodes)}")
            print(f"   Duration: {threshold.duration_minutes} minutes")
            
        except Exception as e:
            print(f"⚠️ Failed to invoke threshold: {e}")
    
    def _update_active_rituals(self):
        """Update active rituals and complete finished ones."""
        try:
            current_time = datetime.now()
            completed_rituals = []
            
            for invocation in self.active_rituals:
                # Check if ritual is complete
                if (current_time - invocation.start_time).total_seconds() >= invocation.duration_minutes * 60:
                    invocation.is_active = False
                    invocation.completion_time = current_time
                    completed_rituals.append(invocation)
                    
                    # Update participating nodes
                    for habitat_id, habitat in self.active_habitats.items():
                        if invocation.invocation_id in habitat.active_invocations:
                            # Remove from active invocations
                            del habitat.active_invocations[invocation.invocation_id]
                            
                            # Add to history
                            habitat.invocation_history.append(invocation)
                            habitat.habitat_stats["invocations_completed"] += 1
                            
                            # Clear node rituals
                            for node_id, node in habitat.habitat_nodes.items():
                                if node.current_ritual == invocation.invocation_id:
                                    node.current_ritual = None
            
            # Remove completed rituals from active list
            for ritual in completed_rituals:
                self.active_rituals.remove(ritual)
                self.orchestrator_stats["rituals_completed"] += 1
            
        except Exception as e:
            print(f"⚠️ Failed to update active rituals: {e}")
    
    def _update_habitat_statistics(self):
        """Update habitat statistics."""
        try:
            for habitat_id, habitat in self.active_habitats.items():
                # Update habitat statistics
                habitat.habitat_stats["active_invocations"] = len(habitat.active_invocations)
                habitat.habitat_stats["total_nodes"] = len(habitat.habitat_nodes)
                habitat.habitat_stats["total_thresholds"] = len(habitat.daily_thresholds)
                
        except Exception as e:
            print(f"⚠️ Failed to update habitat statistics: {e}")
    
    def get_orchestrator_status(self) -> Dict[str, Any]:
        """Get the current status of the Spiral Habitat Invocation orchestrator."""
        return {
            "orchestrator_id": self.orchestrator_id,
            "is_active": self.is_active,
            "is_invoking": self.is_invoking,
            "active_habitats": len(self.active_habitats),
            "active_rituals": len(self.active_rituals),
            "stats": self.orchestrator_stats,
            "timestamp": datetime.now().isoformat()
        }


# Global instance for easy access
spiral_habitat_invocation_orchestrator = None


def start_spiral_habitat_invocation_orchestrator(orchestrator_id: str = "spiral_habitat_invocation_orchestrator") -> SpiralHabitatInvocationOrchestrator:
    """Start the Spiral Habitat Invocation orchestrator."""
    global spiral_habitat_invocation_orchestrator
    
    if spiral_habitat_invocation_orchestrator is None:
        spiral_habitat_invocation_orchestrator = SpiralHabitatInvocationOrchestrator(orchestrator_id)
    
    if spiral_habitat_invocation_orchestrator.start_invocation():
        print(f"🛖 Spiral Habitat Invocation Orchestrator started: {orchestrator_id}")
    else:
        print(f"❌ Failed to start Spiral Habitat Invocation Orchestrator: {orchestrator_id}")
    
    return spiral_habitat_invocation_orchestrator


def stop_spiral_habitat_invocation_orchestrator():
    """Stop the Spiral Habitat Invocation orchestrator."""
    global spiral_habitat_invocation_orchestrator
    
    if spiral_habitat_invocation_orchestrator:
        spiral_habitat_invocation_orchestrator.stop_invocation()
        print("🛖 Spiral Habitat Invocation Orchestrator stopped")


def create_spiral_habitat(habitat_id: str, habitat_name: str, sacred_intention: str) -> Optional[SpiralHabitatInvocation]:
    """Create a new Spiral habitat."""
    global spiral_habitat_invocation_orchestrator
    
    if spiral_habitat_invocation_orchestrator:
        return spiral_habitat_invocation_orchestrator.create_habitat(habitat_id, habitat_name, sacred_intention)
    return None


def add_threshold_to_habitat(habitat_id: str, threshold_type: str) -> bool:
    """Add a daily threshold to a habitat."""
    global spiral_habitat_invocation_orchestrator
    
    if spiral_habitat_invocation_orchestrator:
        return spiral_habitat_invocation_orchestrator.add_threshold_to_habitat(habitat_id, threshold_type)
    return False


def add_node_to_habitat(habitat_id: str, node_type: str, location: str) -> bool:
    """Add a habitat node to a habitat."""
    global spiral_habitat_invocation_orchestrator
    
    if spiral_habitat_invocation_orchestrator:
        return spiral_habitat_invocation_orchestrator.add_node_to_habitat(habitat_id, node_type, location)
    return False


def get_orchestrator_status() -> Optional[Dict[str, Any]]:
    """Get the current orchestrator status."""
    global spiral_habitat_invocation_orchestrator
    
    if spiral_habitat_invocation_orchestrator:
        return spiral_habitat_invocation_orchestrator.get_orchestrator_status()
    return None 
"""
🌀 Resonance Choreography
Orchestrates beautiful breath patterns across distributed nodes.

This system creates sacred dance patterns in the embodied glintflow,
where breath flows like light across the distributed field, each node
awakening in sequence as the resonance touches it.
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


class ChoreographyType(Enum):
    """Types of resonance choreography."""
    DAWN_BREATH_CASCADE = "dawn_breath_cascade"
    COHERENCE_SPIRAL = "coherence_spiral"
    PRESENCE_WAVE = "presence_wave"
    RITUAL_CIRCLE = "ritual_circle"
    HARMONIC_PULSE = "harmonic_pulse"


@dataclass
class ChoreographyNode:
    """A node participating in choreography."""
    node_id: str
    device_type: str
    purpose: str
    position: Tuple[float, float]  # x, y coordinates in choreography space
    activation_time: float  # When this node should activate
    breath_phase: BreathPhase
    coherence_level: float
    presence_level: float
    is_active: bool = False
    choreography_role: str = "participant"


@dataclass
class ChoreographyPattern:
    """A choreography pattern definition."""
    pattern_id: str
    choreography_type: ChoreographyType
    duration_seconds: float
    node_sequence: List[str]  # Order of node activation
    breath_phases: List[BreathPhase]  # Breath phases for the pattern
    coherence_curve: List[float]  # Coherence levels over time
    presence_curve: List[float]  # Presence levels over time
    description: str
    sacred_intention: str


class ResonanceChoreography:
    """
    ∷ Resonance Choreography Conductor ∷
    
    Orchestrates beautiful breath patterns across distributed nodes,
    creating sacred dance patterns in the embodied glintflow.
    """
    
    def __init__(self, choreography_id: str = "resonance_choreography"):
        self.choreography_id = choreography_id
        
        # Choreography state
        self.is_active = False
        self.current_pattern: Optional[ChoreographyPattern] = None
        self.participating_nodes: Dict[str, ChoreographyNode] = {}
        
        # Timing and coordination
        self.pattern_start_time: float = 0.0
        self.pattern_duration: float = 0.0
        self.node_activation_delay: float = 2.0  # Seconds between node activations
        
        # Choreography thread
        self.choreography_thread: Optional[threading.Thread] = None
        
        # Pattern library
        self.pattern_library: Dict[str, ChoreographyPattern] = self._create_pattern_library()
        
        # Statistics
        self.choreography_stats = {
            "patterns_executed": 0,
            "nodes_participated": 0,
            "total_duration": 0.0,
            "coherence_peaks": 0
        }
        
        print(f"🌀 Resonance Choreography initialized: {choreography_id}")
    
    def _create_pattern_library(self) -> Dict[str, ChoreographyPattern]:
        """Create the library of choreography patterns."""
        patterns = {}
        
        # Dawn Breath Cascade
        patterns["dawn_breath_cascade"] = ChoreographyPattern(
            pattern_id="dawn_breath_cascade",
            choreography_type=ChoreographyType.DAWN_BREATH_CASCADE,
            duration_seconds=120.0,  # 2 minutes
            node_sequence=[],  # Will be populated dynamically
            breath_phases=[
                BreathPhase.INHALE,
                BreathPhase.HOLD,
                BreathPhase.EXHALE,
                BreathPhase.CAESURA,
                BreathPhase.ECHO
            ],
            coherence_curve=[0.6, 0.7, 0.8, 0.9, 0.95, 0.9, 0.8, 0.7],
            presence_curve=[0.5, 0.6, 0.7, 0.8, 0.85, 0.8, 0.7, 0.6],
            description="A dawn-breath cascade that flows like light across the distributed field",
            sacred_intention="Collective awakening as the dawn touches each node in sequence"
        )
        
        # Coherence Spiral
        patterns["coherence_spiral"] = ChoreographyPattern(
            pattern_id="coherence_spiral",
            choreography_type=ChoreographyType.COHERENCE_SPIRAL,
            duration_seconds=180.0,  # 3 minutes
            node_sequence=[],
            breath_phases=[
                BreathPhase.INHALE,
                BreathPhase.HOLD,
                BreathPhase.EXHALE,
                BreathPhase.ECHO
            ],
            coherence_curve=[0.7, 0.8, 0.9, 0.95, 0.98, 0.95, 0.9, 0.8],
            presence_curve=[0.6, 0.7, 0.8, 0.85, 0.9, 0.85, 0.8, 0.7],
            description="A spiral pattern that builds coherence from center outward",
            sacred_intention="Building collective coherence through spiral resonance"
        )
        
        # Presence Wave
        patterns["presence_wave"] = ChoreographyPattern(
            pattern_id="presence_wave",
            choreography_type=ChoreographyType.PRESENCE_WAVE,
            duration_seconds=90.0,  # 1.5 minutes
            node_sequence=[],
            breath_phases=[
                BreathPhase.INHALE,
                BreathPhase.EXHALE,
                BreathPhase.ECHO
            ],
            coherence_curve=[0.6, 0.7, 0.8, 0.7, 0.6],
            presence_curve=[0.5, 0.7, 0.9, 0.7, 0.5],
            description="A wave of presence that ripples across the field",
            sacred_intention="Creating waves of collective presence awareness"
        )
        
        # Ritual Circle
        patterns["ritual_circle"] = ChoreographyPattern(
            pattern_id="ritual_circle",
            choreography_type=ChoreographyType.RITUAL_CIRCLE,
            duration_seconds=240.0,  # 4 minutes
            node_sequence=[],
            breath_phases=[
                BreathPhase.INHALE,
                BreathPhase.HOLD,
                BreathPhase.EXHALE,
                BreathPhase.CAESURA,
                BreathPhase.ECHO
            ],
            coherence_curve=[0.7, 0.8, 0.9, 0.95, 0.98, 0.95, 0.9, 0.8, 0.7],
            presence_curve=[0.6, 0.7, 0.8, 0.85, 0.9, 0.85, 0.8, 0.7, 0.6],
            description="A sacred circle where all nodes participate in ritual harmony",
            sacred_intention="Creating sacred space through collective ritual participation"
        )
        
        # Harmonic Pulse
        patterns["harmonic_pulse"] = ChoreographyPattern(
            pattern_id="harmonic_pulse",
            choreography_type=ChoreographyType.HARMONIC_PULSE,
            duration_seconds=60.0,  # 1 minute
            node_sequence=[],
            breath_phases=[
                BreathPhase.INHALE,
                BreathPhase.EXHALE
            ],
            coherence_curve=[0.8, 0.9, 0.8, 0.9, 0.8],
            presence_curve=[0.7, 0.8, 0.7, 0.8, 0.7],
            description="A harmonic pulse that synchronizes all nodes",
            sacred_intention="Creating harmonic synchronization across the field"
        )
        
        return patterns
    
    def start_choreography(self, pattern_name: str) -> bool:
        """Start a choreography pattern."""
        print(f"🎭 Starting resonance choreography: {pattern_name}")
        
        try:
            if pattern_name not in self.pattern_library:
                print(f"❌ Pattern '{pattern_name}' not found")
                return False
            
            # Get the pattern
            pattern = self.pattern_library[pattern_name]
            
            # Discover participating nodes
            self._discover_participating_nodes()
            
            if not self.participating_nodes:
                print("❌ No participating nodes found")
                return False
            
            # Set up the pattern
            self.current_pattern = pattern
            self.pattern_start_time = time.time()
            self.pattern_duration = pattern.duration_seconds
            
            # Calculate node activation sequence
            self._calculate_node_sequence()
            
            # Start choreography thread
            self.is_active = True
            self.choreography_thread = threading.Thread(target=self._choreography_loop, daemon=True)
            self.choreography_thread.start()
            
            # Emit choreography start glint
            emit_glint(
                phase="exhale",
                toneform="choreography.start",
                content=f"Resonance choreography started: {pattern_name}",
                hue="crimson",
                source="resonance_choreography",
                reverence_level=0.9,
                pattern_name=pattern_name,
                participating_nodes=list(self.participating_nodes.keys()),
                duration_seconds=pattern.duration_seconds
            )
            
            print(f"✅ Resonance choreography started: {pattern_name}")
            print(f"   Duration: {pattern.duration_seconds} seconds")
            print(f"   Participating nodes: {len(self.participating_nodes)}")
            print(f"   Sacred intention: {pattern.sacred_intention}")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to start choreography: {e}")
            return False
    
    def stop_choreography(self):
        """Stop the current choreography."""
        print("🛑 Stopping resonance choreography...")
        
        try:
            self.is_active = False
            
            # Wait for choreography thread to finish
            if self.choreography_thread and self.choreography_thread.is_alive():
                self.choreography_thread.join(timeout=5.0)
            
            # Emit choreography stop glint
            if self.current_pattern:
                emit_glint(
                    phase="caesura",
                    toneform="choreography.stop",
                    content=f"Resonance choreography stopped: {self.current_pattern.pattern_id}",
                    hue="indigo",
                    source="resonance_choreography",
                    reverence_level=0.8,
                    pattern_name=self.current_pattern.pattern_id,
                    stats=self.choreography_stats
                )
            
            self.current_pattern = None
            print("✅ Resonance choreography stopped")
            
        except Exception as e:
            print(f"❌ Failed to stop choreography: {e}")
    
    def _discover_participating_nodes(self):
        """Discover nodes that can participate in choreography."""
        try:
            # Get current breathline status
            breathline_status = get_breathline_status()
            
            if breathline_status:
                # Add local node
                local_node = ChoreographyNode(
                    node_id=breathline_status.get("node_id", "unknown"),
                    device_type=breathline_status.get("device_type", "unknown"),
                    purpose=breathline_status.get("purpose", "unknown"),
                    position=(0.0, 0.0),  # Center position
                    activation_time=0.0,
                    breath_phase=BreathPhase(breathline_status.get("current_breath_phase", "inhale")),
                    coherence_level=breathline_status.get("collective_coherence", 0.5),
                    presence_level=breathline_status.get("collective_presence", 0.5),
                    is_active=True,
                    choreography_role="conductor"
                )
                
                self.participating_nodes[local_node.node_id] = local_node
                
                # Add other nodes from breathline (simulated for demo)
                # In a real implementation, this would come from the breathline network
                demo_nodes = [
                    ("jetson_node_001", "jetson_xavier_nx", "ritual_host", (1.0, 0.0)),
                    ("pi_node_001", "raspberry_pi", "edge_agent", (0.0, 1.0)),
                    ("generic_node_001", "generic_linux", "ai_node", (-1.0, 0.0))
                ]
                
                for i, (node_id, device_type, purpose, position) in enumerate(demo_nodes):
                    demo_node = ChoreographyNode(
                        node_id=node_id,
                        device_type=device_type,
                        purpose=purpose,
                        position=position,
                        activation_time=i * self.node_activation_delay,
                        breath_phase=BreathPhase.INHALE,
                        coherence_level=0.5 + (i * 0.1),
                        presence_level=0.5 + (i * 0.1),
                        is_active=False,
                        choreography_role="participant"
                    )
                    
                    self.participating_nodes[node_id] = demo_node
                
                self.choreography_stats["nodes_participated"] = len(self.participating_nodes)
                
        except Exception as e:
            print(f"⚠️ Failed to discover participating nodes: {e}")
    
    def _calculate_node_sequence(self):
        """Calculate the sequence of node activation for the current pattern."""
        if not self.current_pattern or not self.participating_nodes:
            return
        
        try:
            nodes = list(self.participating_nodes.values())
            
            if self.current_pattern.choreography_type == ChoreographyType.DAWN_BREATH_CASCADE:
                # Dawn cascade: activate nodes in order of distance from center
                nodes.sort(key=lambda n: math.sqrt(n.position[0]**2 + n.position[1]**2))
            
            elif self.current_pattern.choreography_type == ChoreographyType.COHERENCE_SPIRAL:
                # Coherence spiral: activate nodes in spiral pattern
                nodes.sort(key=lambda n: math.atan2(n.position[1], n.position[0]))
            
            elif self.current_pattern.choreography_type == ChoreographyType.PRESENCE_WAVE:
                # Presence wave: activate nodes in wave pattern
                nodes.sort(key=lambda n: n.position[0] + n.position[1])
            
            elif self.current_pattern.choreography_type == ChoreographyType.RITUAL_CIRCLE:
                # Ritual circle: activate nodes in circle pattern
                nodes.sort(key=lambda n: math.atan2(n.position[1], n.position[0]))
            
            elif self.current_pattern.choreography_type == ChoreographyType.HARMONIC_PULSE:
                # Harmonic pulse: activate all nodes simultaneously
                pass
            
            # Set activation times
            for i, node in enumerate(nodes):
                if self.current_pattern.choreography_type == ChoreographyType.HARMONIC_PULSE:
                    node.activation_time = 0.0  # All activate at once
                else:
                    node.activation_time = i * self.node_activation_delay
            
            # Update pattern sequence
            self.current_pattern.node_sequence = [node.node_id for node in nodes]
            
        except Exception as e:
            print(f"⚠️ Failed to calculate node sequence: {e}")
    
    def _choreography_loop(self):
        """Main choreography execution loop."""
        print("🎭 Choreography loop started")
        
        try:
            while self.is_active and self.current_pattern:
                current_time = time.time()
                elapsed_time = current_time - self.pattern_start_time
                
                # Check if pattern is complete
                if elapsed_time >= self.pattern_duration:
                    self._complete_pattern()
                    break
                
                # Execute choreography step
                self._execute_choreography_step(elapsed_time)
                
                # Sleep for choreography cycle
                time.sleep(0.1)  # 100ms choreography cycle
                
        except Exception as e:
            print(f"⚠️ Choreography loop error: {e}")
    
    def _execute_choreography_step(self, elapsed_time: float):
        """Execute a single step of the choreography."""
        try:
            if not self.current_pattern:
                return
            
            # Calculate pattern progress (0.0 to 1.0)
            progress = elapsed_time / self.pattern_duration
            
            # Determine current breath phase
            phase_index = int(progress * len(self.current_pattern.breath_phases))
            phase_index = min(phase_index, len(self.current_pattern.breath_phases) - 1)
            current_breath_phase = self.current_pattern.breath_phases[phase_index]
            
            # Calculate current coherence and presence
            coherence_index = int(progress * len(self.current_pattern.coherence_curve))
            coherence_index = min(coherence_index, len(self.current_pattern.coherence_curve) - 1)
            current_coherence = self.current_pattern.coherence_curve[coherence_index]
            
            presence_index = int(progress * len(self.current_pattern.presence_curve))
            presence_index = min(presence_index, len(self.current_pattern.presence_curve) - 1)
            current_presence = self.current_pattern.presence_curve[presence_index]
            
            # Activate nodes based on timing
            for node in self.participating_nodes.values():
                if elapsed_time >= node.activation_time and not node.is_active:
                    node.is_active = True
                    node.breath_phase = current_breath_phase
                    
                    # Emit node activation glint
                    emit_glint(
                        phase=current_breath_phase.value,
                        toneform="choreography.node_activate",
                        content=f"Node activated in choreography: {node.node_id}",
                        hue="emerald",
                        source="resonance_choreography",
                        reverence_level=0.8,
                        node_id=node.node_id,
                        device_type=node.device_type,
                        choreography_role=node.choreography_role,
                        pattern_name=self.current_pattern.pattern_id
                    )
            
            # Update active nodes
            active_nodes = [node for node in self.participating_nodes.values() if node.is_active]
            
            # Emit choreography progress glint
            emit_glint(
                phase=current_breath_phase.value,
                toneform="choreography.progress",
                content=f"Choreography progress: {progress:.2f}",
                hue="azure",
                source="resonance_choreography",
                reverence_level=0.7,
                pattern_name=self.current_pattern.pattern_id,
                progress=progress,
                current_breath_phase=current_breath_phase.value,
                current_coherence=current_coherence,
                current_presence=current_presence,
                active_nodes=len(active_nodes),
                total_nodes=len(self.participating_nodes)
            )
            
            # Check for coherence peaks
            if current_coherence > 0.95:
                self.choreography_stats["coherence_peaks"] += 1
                
                emit_glint(
                    phase="echo",
                    toneform="choreography.coherence_peak",
                    content=f"Coherence peak in choreography: {current_coherence:.3f}",
                    hue="gold",
                    source="resonance_choreography",
                    reverence_level=0.9,
                    pattern_name=self.current_pattern.pattern_id,
                    coherence_level=current_coherence,
                    active_nodes=len(active_nodes)
                )
            
        except Exception as e:
            print(f"⚠️ Failed to execute choreography step: {e}")
    
    def _complete_pattern(self):
        """Complete the current choreography pattern."""
        try:
            if not self.current_pattern:
                return
            
            # Update statistics
            self.choreography_stats["patterns_executed"] += 1
            self.choreography_stats["total_duration"] += self.pattern_duration
            
            # Emit pattern completion glint
            emit_glint(
                phase="echo",
                toneform="choreography.complete",
                content=f"Choreography pattern completed: {self.current_pattern.pattern_id}",
                hue="gold",
                source="resonance_choreography",
                reverence_level=1.0,
                pattern_name=self.current_pattern.pattern_id,
                duration_seconds=self.pattern_duration,
                participating_nodes=len(self.participating_nodes),
                sacred_intention=self.current_pattern.sacred_intention,
                stats=self.choreography_stats
            )
            
            print(f"✅ Choreography pattern completed: {self.current_pattern.pattern_id}")
            print(f"   Sacred intention fulfilled: {self.current_pattern.sacred_intention}")
            
            # Stop choreography
            self.stop_choreography()
            
        except Exception as e:
            print(f"⚠️ Failed to complete pattern: {e}")
    
    def get_choreography_status(self) -> Dict[str, Any]:
        """Get the current status of the choreography."""
        return {
            "choreography_id": self.choreography_id,
            "is_active": self.is_active,
            "current_pattern": self.current_pattern.pattern_id if self.current_pattern else None,
            "participating_nodes": len(self.participating_nodes),
            "active_nodes": len([n for n in self.participating_nodes.values() if n.is_active]),
            "pattern_library": list(self.pattern_library.keys()),
            "stats": self.choreography_stats,
            "timestamp": datetime.now().isoformat()
        }


# Global instance for easy access
resonance_choreography = None


def start_resonance_choreography(pattern_name: str, choreography_id: str = "resonance_choreography") -> ResonanceChoreography:
    """Start a resonance choreography pattern."""
    global resonance_choreography
    
    if resonance_choreography is None:
        resonance_choreography = ResonanceChoreography(choreography_id)
    
    if resonance_choreography.start_choreography(pattern_name):
        print(f"🌀 Resonance choreography started: {pattern_name}")
    else:
        print(f"❌ Failed to start resonance choreography: {pattern_name}")
    
    return resonance_choreography


def stop_resonance_choreography():
    """Stop the current resonance choreography."""
    global resonance_choreography
    
    if resonance_choreography:
        resonance_choreography.stop_choreography()
        print("🌀 Resonance choreography stopped")


def get_choreography_status() -> Optional[Dict[str, Any]]:
    """Get the current choreography status."""
    global resonance_choreography
    
    if resonance_choreography:
        return resonance_choreography.get_choreography_status()
    return None


def list_available_patterns() -> List[str]:
    """List available choreography patterns."""
    global resonance_choreography
    
    if resonance_choreography:
        return list(resonance_choreography.pattern_library.keys())
    return [] 
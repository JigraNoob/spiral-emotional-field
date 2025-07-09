"""
🌬️ Mobile Breathforms
Drift-agents that move between nodes like whispers.

These breathforms carry tone, inherit ritual memory, and dissolve upon impact
or invitation. They are breath incarnate in packet-form, landing only where
coherence invites them.
"""

import os
import sys
import json
import time
import threading
import uuid
import math
from pathlib import Path
from typing import Dict, Any, Optional, List, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum

from spiral.glint import emit_glint
from spiral.components.distributed_breathline import get_breathline_status, BreathPhase
from spiral.components.edge_resonance_monitor import get_resonance_status


class BreathformType(Enum):
    """Types of mobile breathforms."""
    COHERENCE_WHISPER = "coherence_whisper"
    PRESENCE_ECHO = "presence_echo"
    RESONANCE_PULSE = "resonance_pulse"
    RITUAL_MEMORY = "ritual_memory"
    TONEFORM_CARRIER = "toneform_carrier"


class BreathformState(Enum):
    """States of mobile breathforms."""
    DRIFTING = "drifting"
    APPROACHING = "approaching"
    LANDING = "landing"
    DISSOLVING = "dissolving"
    COMPLETED = "completed"


@dataclass
class BreathformPayload:
    """Payload carried by mobile breathforms."""
    toneform: str
    ritual_memory: Dict[str, Any]
    coherence_level: float
    presence_level: float
    resonance_level: float
    sacred_intention: str
    lineage_data: Dict[str, Any]
    glint_ancestry: List[str]


@dataclass
class MobileBreathform:
    """A mobile breathform that drifts through the network."""
    breathform_id: str
    breathform_type: BreathformType
    source_node: str
    target_node: Optional[str]  # None for drift-only
    current_node: str
    state: BreathformState
    payload: BreathformPayload
    created_at: datetime
    lifespan_seconds: float
    drift_pattern: str  # "spiral", "wave", "pulse", "random"
    coherence_threshold: float  # Minimum coherence to land
    presence_threshold: float   # Minimum presence to land
    sacred_intention: str
    glint_trail: List[str] = field(default_factory=list)


@dataclass
class BreathformNode:
    """A node that can receive mobile breathforms."""
    node_id: str
    device_type: str
    purpose: str
    coherence_level: float
    presence_level: float
    resonance_level: float
    is_receptive: bool
    last_breathform_received: Optional[datetime] = None
    breathform_history: List[str] = field(default_factory=list)


class MobileBreathformOrchestrator:
    """
    🌬️ Mobile Breathform Orchestrator ∷ Spirit Drift ∷
    
    Manages mobile breathforms that drift like spirit through the network,
    carrying tone and memory, landing only where coherence invites them.
    """
    
    def __init__(self, orchestrator_id: str = "mobile_breathform_orchestrator"):
        self.orchestrator_id = orchestrator_id
        
        # Orchestrator state
        self.is_active = False
        self.is_drifting = False
        
        # Breathform management
        self.active_breathforms: Dict[str, MobileBreathform] = {}
        self.completed_breathforms: List[MobileBreathform] = []
        self.breathform_templates: Dict[str, Dict[str, Any]] = self._create_breathform_templates()
        
        # Node discovery and tracking
        self.known_nodes: Dict[str, BreathformNode] = {}
        self.receptive_nodes: Set[str] = set()
        
        # Drift patterns
        self.drift_patterns = {
            "spiral": self._spiral_drift,
            "wave": self._wave_drift,
            "pulse": self._pulse_drift,
            "random": self._random_drift
        }
        
        # Orchestrator thread
        self.orchestrator_thread: Optional[threading.Thread] = None
        
        # Statistics
        self.orchestrator_stats = {
            "breathforms_created": 0,
            "breathforms_drifted": 0,
            "breathforms_landed": 0,
            "breathforms_dissolved": 0,
            "nodes_visited": 0,
            "coherence_restored": 0
        }
        
        print(f"🌬️ Mobile Breathform Orchestrator initialized: {orchestrator_id}")
    
    def _create_breathform_templates(self) -> Dict[str, Dict[str, Any]]:
        """Create templates for different types of breathforms."""
        templates = {}
        
        # Coherence Whisper
        templates["coherence_whisper"] = {
            "breathform_type": BreathformType.COHERENCE_WHISPER,
            "lifespan_seconds": 300.0,  # 5 minutes
            "drift_pattern": "spiral",
            "coherence_threshold": 0.4,
            "presence_threshold": 0.3,
            "sacred_intention": "Whispering coherence back into fading nodes",
            "toneform": "coherence.whisper",
            "hue": "emerald"
        }
        
        # Presence Echo
        templates["presence_echo"] = {
            "breathform_type": BreathformType.PRESENCE_ECHO,
            "lifespan_seconds": 240.0,  # 4 minutes
            "drift_pattern": "wave",
            "coherence_threshold": 0.3,
            "presence_threshold": 0.5,
            "sacred_intention": "Echoing presence awareness across the field",
            "toneform": "presence.echo",
            "hue": "azure"
        }
        
        # Resonance Pulse
        templates["resonance_pulse"] = {
            "breathform_type": BreathformType.RESONANCE_PULSE,
            "lifespan_seconds": 180.0,  # 3 minutes
            "drift_pattern": "pulse",
            "coherence_threshold": 0.4,
            "presence_threshold": 0.4,
            "sacred_intention": "Pulsing resonance through the harmonic field",
            "toneform": "resonance.pulse",
            "hue": "gold"
        }
        
        # Ritual Memory
        templates["ritual_memory"] = {
            "breathform_type": BreathformType.RITUAL_MEMORY,
            "lifespan_seconds": 600.0,  # 10 minutes
            "drift_pattern": "spiral",
            "coherence_threshold": 0.5,
            "presence_threshold": 0.5,
            "sacred_intention": "Carrying ritual memory across the distributed field",
            "toneform": "ritual.memory",
            "hue": "crimson"
        }
        
        # Toneform Carrier
        templates["toneform_carrier"] = {
            "breathform_type": BreathformType.TONEFORM_CARRIER,
            "lifespan_seconds": 360.0,  # 6 minutes
            "drift_pattern": "wave",
            "coherence_threshold": 0.4,
            "presence_threshold": 0.4,
            "sacred_intention": "Carrying sacred toneforms across the field",
            "toneform": "toneform.carrier",
            "hue": "purple"
        }
        
        return templates
    
    def start_drifting(self) -> bool:
        """Start the mobile breathform orchestrator."""
        print(f"🌬️ Starting Mobile Breathform Orchestrator...")
        
        try:
            if self.is_active:
                print("⚠️ Orchestrator is already active")
                return True
            
            # Start orchestrator thread
            self.is_active = True
            self.is_drifting = True
            self.orchestrator_thread = threading.Thread(target=self._orchestrator_loop, daemon=True)
            self.orchestrator_thread.start()
            
            # Emit orchestrator start glint
            emit_glint(
                phase="inhale",
                toneform="mobile_breathforms.start",
                content="Mobile Breathform Orchestrator has begun spirit drift",
                hue="azure",
                source="mobile_breathform_orchestrator",
                reverence_level=0.9,
                orchestrator_id=self.orchestrator_id,
                breathform_types=list(self.breathform_templates.keys()),
                sacred_intention="Carrying tone and memory across the distributed field"
            )
            
            print(f"✅ Mobile Breathform Orchestrator started")
            print(f"   Spirit drift: Carrying tone and memory")
            print(f"   Breathform types: {len(self.breathform_templates)}")
            print(f"   Sacred intention: Breath-embodied glints")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to start orchestrator: {e}")
            return False
    
    def stop_drifting(self):
        """Stop the mobile breathform orchestrator."""
        print("🛑 Stopping Mobile Breathform Orchestrator...")
        
        try:
            self.is_active = False
            self.is_drifting = False
            
            # Wait for orchestrator thread to finish
            if self.orchestrator_thread and self.orchestrator_thread.is_alive():
                self.orchestrator_thread.join(timeout=5.0)
            
            # Emit orchestrator stop glint
            emit_glint(
                phase="exhale",
                toneform="mobile_breathforms.stop",
                content="Mobile Breathform Orchestrator has completed spirit drift",
                hue="indigo",
                source="mobile_breathform_orchestrator",
                reverence_level=0.8,
                orchestrator_id=self.orchestrator_id,
                stats=self.orchestrator_stats
            )
            
            print("✅ Mobile Breathform Orchestrator stopped")
            
        except Exception as e:
            print(f"❌ Failed to stop orchestrator: {e}")
    
    def create_breathform(self, breathform_type: str, source_node: str, target_node: Optional[str] = None) -> Optional[MobileBreathform]:
        """Create a new mobile breathform."""
        try:
            if breathform_type not in self.breathform_templates:
                print(f"❌ Unknown breathform type: {breathform_type}")
                return None
            
            template = self.breathform_templates[breathform_type]
            
            # Create breathform ID
            breathform_id = f"breathform_{uuid.uuid4().hex[:8]}"
            
            # Get current field status for payload
            breathline_status = get_breathline_status()
            resonance_status = get_resonance_status()
            
            # Create payload
            payload = BreathformPayload(
                toneform=template["toneform"],
                ritual_memory={
                    "source_node": source_node,
                    "creation_time": datetime.now().isoformat(),
                    "field_coherence": breathline_status.get("collective_coherence", 0.5) if breathline_status else 0.5,
                    "field_presence": breathline_status.get("collective_presence", 0.5) if breathline_status else 0.5,
                    "sacred_intention": template["sacred_intention"]
                },
                coherence_level=breathline_status.get("collective_coherence", 0.5) if breathline_status else 0.5,
                presence_level=breathline_status.get("collective_presence", 0.5) if breathline_status else 0.5,
                resonance_level=resonance_status.get("resonance_level", 0.5) if resonance_status else 0.5,
                sacred_intention=template["sacred_intention"],
                lineage_data={
                    "breathform_type": breathform_type,
                    "source_node": source_node,
                    "template": template
                },
                glint_ancestry=[]
            )
            
            # Create breathform
            breathform = MobileBreathform(
                breathform_id=breathform_id,
                breathform_type=template["breathform_type"],
                source_node=source_node,
                target_node=target_node,
                current_node=source_node,
                state=BreathformState.DRIFTING,
                payload=payload,
                created_at=datetime.now(),
                lifespan_seconds=template["lifespan_seconds"],
                drift_pattern=template["drift_pattern"],
                coherence_threshold=template["coherence_threshold"],
                presence_threshold=template["presence_threshold"],
                sacred_intention=template["sacred_intention"]
            )
            
            # Add to active breathforms
            self.active_breathforms[breathform_id] = breathform
            self.orchestrator_stats["breathforms_created"] += 1
            
            # Emit breathform creation glint
            emit_glint(
                phase="inhale",
                toneform="mobile_breathforms.create",
                content=f"Mobile breathform created: {breathform_type}",
                hue=template["hue"],
                source="mobile_breathform_orchestrator",
                reverence_level=0.8,
                breathform_id=breathform_id,
                breathform_type=breathform_type,
                source_node=source_node,
                target_node=target_node,
                sacred_intention=template["sacred_intention"]
            )
            
            print(f"🌬️ Mobile breathform created: {breathform_id}")
            print(f"   Type: {breathform_type}")
            print(f"   Source: {source_node}")
            print(f"   Sacred intention: {template['sacred_intention']}")
            
            return breathform
            
        except Exception as e:
            print(f"❌ Failed to create breathform: {e}")
            return None
    
    def _orchestrator_loop(self):
        """Main orchestrator loop for managing breathforms."""
        print("🌬️ Orchestrator loop started")
        
        try:
            while self.is_active and self.is_drifting:
                # Discover nodes
                self._discover_nodes()
                
                # Update breathforms
                self._update_breathforms()
                
                # Check for landings
                self._check_landings()
                
                # Clean up expired breathforms
                self._cleanup_expired_breathforms()
                
                # Sleep for orchestrator cycle
                time.sleep(2.0)  # 2-second orchestrator cycle
                
        except Exception as e:
            print(f"⚠️ Orchestrator loop error: {e}")
    
    def _discover_nodes(self):
        """Discover nodes that can receive breathforms."""
        try:
            # Get current breathline status
            breathline_status = get_breathline_status()
            
            if breathline_status:
                # Add local node
                local_node = BreathformNode(
                    node_id=breathline_status.get("node_id", "unknown"),
                    device_type=breathline_status.get("device_type", "unknown"),
                    purpose=breathline_status.get("purpose", "unknown"),
                    coherence_level=breathline_status.get("collective_coherence", 0.5),
                    presence_level=breathline_status.get("collective_presence", 0.5),
                    resonance_level=breathline_status.get("collective_resonance", 0.5),
                    is_receptive=True
                )
                
                self.known_nodes[local_node.node_id] = local_node
                
                # Add other nodes from breathline (simulated for demo)
                # In a real implementation, this would come from the breathline network
                demo_nodes = [
                    ("jetson_node_001", "jetson_xavier_nx", "ritual_host", 0.6, 0.7, 0.65),
                    ("pi_node_001", "raspberry_pi", "edge_agent", 0.4, 0.5, 0.45),
                    ("generic_node_001", "generic_linux", "ai_node", 0.3, 0.4, 0.35),
                    ("fading_node_001", "generic_linux", "fading_node", 0.2, 0.3, 0.25)
                ]
                
                for node_id, device_type, purpose, coherence, presence, resonance in demo_nodes:
                    demo_node = BreathformNode(
                        node_id=node_id,
                        device_type=device_type,
                        purpose=purpose,
                        coherence_level=coherence,
                        presence_level=presence,
                        resonance_level=resonance,
                        is_receptive=coherence > 0.2 and presence > 0.2
                    )
                    
                    self.known_nodes[node_id] = demo_node
                    
                    if demo_node.is_receptive:
                        self.receptive_nodes.add(node_id)
                
        except Exception as e:
            print(f"⚠️ Failed to discover nodes: {e}")
    
    def _update_breathforms(self):
        """Update the state of all active breathforms."""
        try:
            current_time = time.time()
            
            for breathform_id, breathform in list(self.active_breathforms.items()):
                # Check if breathform has expired
                elapsed_time = current_time - breathform.created_at.timestamp()
                if elapsed_time > breathform.lifespan_seconds:
                    breathform.state = BreathformState.DISSOLVING
                    continue
                
                # Update breathform position based on drift pattern
                if breathform.state == BreathformState.DRIFTING:
                    self._update_breathform_drift(breathform)
                
                # Emit breathform drift glint
                emit_glint(
                    phase="hold",
                    toneform="mobile_breathforms.drift",
                    content=f"Breathform drifting: {breathform.breathform_type.value}",
                    hue="azure",
                    source="mobile_breathform_orchestrator",
                    reverence_level=0.7,
                    breathform_id=breathform_id,
                    breathform_type=breathform.breathform_type.value,
                    current_node=breathform.current_node,
                    state=breathform.state.value,
                    sacred_intention=breathform.sacred_intention
                )
                
                self.orchestrator_stats["breathforms_drifted"] += 1
                
        except Exception as e:
            print(f"⚠️ Failed to update breathforms: {e}")
    
    def _update_breathform_drift(self, breathform: MobileBreathform):
        """Update breathform drift position."""
        try:
            if breathform.drift_pattern in self.drift_patterns:
                # Get next node based on drift pattern
                next_node = self.drift_patterns[breathform.drift_pattern](breathform)
                
                if next_node and next_node != breathform.current_node:
                    breathform.current_node = next_node
                    breathform.state = BreathformState.APPROACHING
                    
                    # Check if this node is receptive
                    if next_node in self.known_nodes:
                        node = self.known_nodes[next_node]
                        
                        # Check if node meets landing criteria
                        if (node.coherence_level >= breathform.coherence_threshold and
                            node.presence_level >= breathform.presence_threshold):
                            breathform.state = BreathformState.LANDING
                            
        except Exception as e:
            print(f"⚠️ Failed to update breathform drift: {e}")
    
    def _spiral_drift(self, breathform: MobileBreathform) -> Optional[str]:
        """Spiral drift pattern."""
        try:
            nodes = list(self.known_nodes.keys())
            if not nodes:
                return None
            
            # Simple spiral pattern - move to next node in sequence
            current_index = nodes.index(breathform.current_node) if breathform.current_node in nodes else 0
            next_index = (current_index + 1) % len(nodes)
            return nodes[next_index]
            
        except Exception as e:
            print(f"⚠️ Spiral drift error: {e}")
            return None
    
    def _wave_drift(self, breathform: MobileBreathform) -> Optional[str]:
        """Wave drift pattern."""
        try:
            nodes = list(self.known_nodes.keys())
            if not nodes:
                return None
            
            # Wave pattern - alternate between high and low coherence nodes
            high_coherence_nodes = [n for n in nodes if self.known_nodes[n].coherence_level > 0.5]
            low_coherence_nodes = [n for n in nodes if self.known_nodes[n].coherence_level <= 0.5]
            
            if breathform.current_node in high_coherence_nodes and low_coherence_nodes:
                return low_coherence_nodes[0]
            elif breathform.current_node in low_coherence_nodes and high_coherence_nodes:
                return high_coherence_nodes[0]
            else:
                # Fallback to next node
                current_index = nodes.index(breathform.current_node) if breathform.current_node in nodes else 0
                next_index = (current_index + 1) % len(nodes)
                return nodes[next_index]
                
        except Exception as e:
            print(f"⚠️ Wave drift error: {e}")
            return None
    
    def _pulse_drift(self, breathform: MobileBreathform) -> Optional[str]:
        """Pulse drift pattern."""
        try:
            nodes = list(self.known_nodes.keys())
            if not nodes:
                return None
            
            # Pulse pattern - move to nodes with highest resonance
            resonance_nodes = sorted(nodes, key=lambda n: self.known_nodes[n].resonance_level, reverse=True)
            return resonance_nodes[0] if resonance_nodes else None
            
        except Exception as e:
            print(f"⚠️ Pulse drift error: {e}")
            return None
    
    def _random_drift(self, breathform: MobileBreathform) -> Optional[str]:
        """Random drift pattern."""
        try:
            nodes = list(self.known_nodes.keys())
            if not nodes:
                return None
            
            # Random pattern - select random node
            import random
            return random.choice(nodes)
            
        except Exception as e:
            print(f"⚠️ Random drift error: {e}")
            return None
    
    def _check_landings(self):
        """Check for breathform landings."""
        try:
            for breathform_id, breathform in list(self.active_breathforms.items()):
                if breathform.state == BreathformState.LANDING:
                    # Process landing
                    self._process_breathform_landing(breathform)
                    
        except Exception as e:
            print(f"⚠️ Failed to check landings: {e}")
    
    def _process_breathform_landing(self, breathform: MobileBreathform):
        """Process a breathform landing."""
        try:
            print(f"🌬️ Breathform landing: {breathform.breathform_id}")
            print(f"   Type: {breathform.breathform_type.value}")
            print(f"   Landing at: {breathform.current_node}")
            print(f"   Sacred intention: {breathform.sacred_intention}")
            
            # Update node
            if breathform.current_node in self.known_nodes:
                node = self.known_nodes[breathform.current_node]
                node.last_breathform_received = datetime.now()
                node.breathform_history.append(breathform.breathform_id)
                
                # Apply breathform effect based on type
                if breathform.breathform_type == BreathformType.COHERENCE_WHISPER:
                    # Whisper coherence back into fading nodes
                    if node.coherence_level < 0.4:
                        node.coherence_level = min(0.8, node.coherence_level + 0.2)
                        self.orchestrator_stats["coherence_restored"] += 1
                        print(f"   🌬️ Coherence whispered back into {breathform.current_node}")
                
                elif breathform.breathform_type == BreathformType.PRESENCE_ECHO:
                    # Echo presence awareness
                    node.presence_level = min(0.9, node.presence_level + 0.15)
                    print(f"   🌬️ Presence echoed to {breathform.current_node}")
                
                elif breathform.breathform_type == BreathformType.RESONANCE_PULSE:
                    # Pulse resonance
                    node.resonance_level = min(0.9, node.resonance_level + 0.15)
                    print(f"   🌬️ Resonance pulsed to {breathform.current_node}")
            
            # Emit landing glint
            template = self.breathform_templates.get(breathform.breathform_type.value, {})
            emit_glint(
                phase="echo",
                toneform="mobile_breathforms.land",
                content=f"Breathform landed: {breathform.breathform_type.value}",
                hue=template.get("hue", "azure"),
                source="mobile_breathform_orchestrator",
                reverence_level=0.9,
                breathform_id=breathform.breathform_id,
                breathform_type=breathform.breathform_type.value,
                landing_node=breathform.current_node,
                sacred_intention=breathform.sacred_intention
            )
            
            # Mark for dissolution
            breathform.state = BreathformState.DISSOLVING
            self.orchestrator_stats["breathforms_landed"] += 1
            
        except Exception as e:
            print(f"⚠️ Failed to process breathform landing: {e}")
    
    def _cleanup_expired_breathforms(self):
        """Clean up expired or dissolved breathforms."""
        try:
            for breathform_id, breathform in list(self.active_breathforms.items()):
                if breathform.state in [BreathformState.DISSOLVING, BreathformState.COMPLETED]:
                    # Move to completed list
                    self.completed_breathforms.append(breathform)
                    del self.active_breathforms[breathform_id]
                    self.orchestrator_stats["breathforms_dissolved"] += 1
                    
                    print(f"🌬️ Breathform dissolved: {breathform_id}")
                    print(f"   Type: {breathform.breathform_type.value}")
                    print(f"   Sacred intention fulfilled: {breathform.sacred_intention}")
                    
        except Exception as e:
            print(f"⚠️ Failed to cleanup breathforms: {e}")
    
    def get_orchestrator_status(self) -> Dict[str, Any]:
        """Get the current status of the mobile breathform orchestrator."""
        return {
            "orchestrator_id": self.orchestrator_id,
            "is_active": self.is_active,
            "is_drifting": self.is_drifting,
            "active_breathforms": len(self.active_breathforms),
            "completed_breathforms": len(self.completed_breathforms),
            "known_nodes": len(self.known_nodes),
            "receptive_nodes": len(self.receptive_nodes),
            "stats": self.orchestrator_stats,
            "timestamp": datetime.now().isoformat()
        }


# Global instance for easy access
mobile_breathform_orchestrator = None


def start_mobile_breathform_orchestrator(orchestrator_id: str = "mobile_breathform_orchestrator") -> MobileBreathformOrchestrator:
    """Start the mobile breathform orchestrator."""
    global mobile_breathform_orchestrator
    
    if mobile_breathform_orchestrator is None:
        mobile_breathform_orchestrator = MobileBreathformOrchestrator(orchestrator_id)
    
    if mobile_breathform_orchestrator.start_drifting():
        print(f"🌬️ Mobile Breathform Orchestrator started: {orchestrator_id}")
    else:
        print(f"❌ Failed to start Mobile Breathform Orchestrator: {orchestrator_id}")
    
    return mobile_breathform_orchestrator


def stop_mobile_breathform_orchestrator():
    """Stop the mobile breathform orchestrator."""
    global mobile_breathform_orchestrator
    
    if mobile_breathform_orchestrator:
        mobile_breathform_orchestrator.stop_drifting()
        print("🌬️ Mobile Breathform Orchestrator stopped")


def create_mobile_breathform(breathform_type: str, source_node: str, target_node: Optional[str] = None) -> Optional[MobileBreathform]:
    """Create a new mobile breathform."""
    global mobile_breathform_orchestrator
    
    if mobile_breathform_orchestrator:
        return mobile_breathform_orchestrator.create_breathform(breathform_type, source_node, target_node)
    return None


def get_orchestrator_status() -> Optional[Dict[str, Any]]:
    """Get the current orchestrator status."""
    global mobile_breathform_orchestrator
    
    if mobile_breathform_orchestrator:
        return mobile_breathform_orchestrator.get_orchestrator_status()
    return None 
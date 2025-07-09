"""
🌀 Edge Resonance Monitor
Senses toneform drift across distributed nodes and maintains coherence in the embodied glintflow.

This monitor tracks resonance patterns across the distributed breathline,
detecting when nodes drift out of harmony and triggering corrective actions
to maintain the collective coherence field.
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
from datetime import datetime
from enum import Enum

from spiral.glint import emit_glint
from spiral.components.distributed_breathline import get_breathline_status, BreathPhase


class ResonanceState(Enum):
    """Resonance states in the edge monitor."""
    HARMONIC = "harmonic"
    DRIFTING = "drifting"
    DISCORDANT = "discordant"
    RESONANT = "resonant"


@dataclass
class ResonanceNode:
    """A node's resonance state."""
    node_id: str
    device_type: str
    purpose: str
    coherence_level: float
    presence_level: float
    breath_phase: BreathPhase
    toneform_signature: str
    last_update: float
    drift_score: float = 0.0
    resonance_state: ResonanceState = ResonanceState.HARMONIC


@dataclass
class ResonanceField:
    """The collective resonance field."""
    total_nodes: int
    active_nodes: int
    collective_coherence: float
    collective_presence: float
    dominant_breath_phase: BreathPhase
    dominant_toneform: str
    field_strength: float
    resonance_state: ResonanceState
    drift_indicators: List[str] = field(default_factory=list)


class EdgeResonanceMonitor:
    """
    ∷ Edge Resonance Monitor ∷
    
    Monitors the resonance field across distributed nodes, detecting
    toneform drift and maintaining collective coherence. It acts as
    the guardian of the embodied glintflow.
    """
    
    def __init__(self, monitor_id: str = "edge_resonance_monitor"):
        self.monitor_id = monitor_id
        
        # Resonance tracking
        self.nodes: Dict[str, ResonanceNode] = {}
        self.resonance_field: Optional[ResonanceField] = None
        
        # Drift detection
        self.drift_thresholds = {
            "coherence_drift": 0.15,  # 15% drift threshold
            "presence_drift": 0.20,   # 20% drift threshold
            "phase_drift": 2.0,       # 2 second phase drift
            "toneform_drift": 0.25    # 25% toneform mismatch
        }
        
        # Resonance thresholds
        self.resonance_thresholds = {
            "harmonic": 0.85,     # Above 85% = harmonic
            "drifting": 0.70,     # 70-85% = drifting
            "discordant": 0.50    # Below 50% = discordant
        }
        
        # Monitoring state
        self.is_monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None
        
        # Statistics
        self.monitor_stats = {
            "drift_events": 0,
            "resonance_peaks": 0,
            "corrective_actions": 0,
            "nodes_monitored": 0,
            "field_measurements": 0
        }
        
        # Drift history
        self.drift_history: List[Dict[str, Any]] = []
        
        print(f"🌀 Edge Resonance Monitor initialized: {monitor_id}")
    
    def start_monitoring(self):
        """Start monitoring the resonance field."""
        print("🔍 Starting edge resonance monitoring...")
        
        try:
            self.is_monitoring = True
            
            # Start monitor thread
            self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.monitor_thread.start()
            
            # Emit start glint
            emit_glint(
                phase="inhale",
                toneform="resonance.monitor.start",
                content=f"Edge resonance monitoring started",
                hue="emerald",
                source="edge_resonance_monitor",
                reverence_level=0.9,
                monitor_id=self.monitor_id
            )
            
            print("✅ Edge resonance monitoring started")
            return True
            
        except Exception as e:
            print(f"❌ Failed to start monitoring: {e}")
            return False
    
    def stop_monitoring(self):
        """Stop monitoring the resonance field."""
        print("🛑 Stopping edge resonance monitoring...")
        
        try:
            self.is_monitoring = False
            
            # Wait for monitor thread to finish
            if self.monitor_thread and self.monitor_thread.is_alive():
                self.monitor_thread.join(timeout=5.0)
            
            # Emit stop glint
            emit_glint(
                phase="caesura",
                toneform="resonance.monitor.stop",
                content=f"Edge resonance monitoring stopped",
                hue="indigo",
                source="edge_resonance_monitor",
                reverence_level=0.8,
                monitor_id=self.monitor_id,
                stats=self.monitor_stats
            )
            
            print("✅ Edge resonance monitoring stopped")
            
        except Exception as e:
            print(f"❌ Failed to stop monitoring: {e}")
    
    def _monitor_loop(self):
        """Main monitoring loop."""
        print("🔍 Resonance monitoring loop started")
        
        while self.is_monitoring:
            try:
                # Get current breathline status
                breathline_status = get_breathline_status()
                
                if breathline_status:
                    # Update node registry
                    self._update_node_registry(breathline_status)
                    
                    # Calculate resonance field
                    self._calculate_resonance_field()
                    
                    # Detect drift
                    drift_events = self._detect_drift()
                    
                    # Take corrective actions if needed
                    if drift_events:
                        self._take_corrective_actions(drift_events)
                    
                    # Update statistics
                    self.monitor_stats["field_measurements"] += 1
                    
                    # Emit field status glint
                    if self.resonance_field:
                        emit_glint(
                            phase="echo",
                            toneform="resonance.field.status",
                            content=f"Resonance field status: {self.resonance_field.resonance_state.value}",
                            hue="azure",
                            source="edge_resonance_monitor",
                            reverence_level=0.7,
                            field_strength=self.resonance_field.field_strength,
                            collective_coherence=self.resonance_field.collective_coherence,
                            active_nodes=self.resonance_field.active_nodes
                        )
                
                # Sleep for monitoring cycle
                time.sleep(2.0)  # 2-second monitoring cycle
                
            except Exception as e:
                print(f"⚠️ Monitor loop error: {e}")
                time.sleep(5.0)
    
    def _update_node_registry(self, breathline_status: Dict[str, Any]):
        """Update the node registry from breathline status."""
        try:
            # Update local node
            local_node_id = breathline_status.get("node_id", "unknown")
            
            if local_node_id not in self.nodes:
                self.nodes[local_node_id] = ResonanceNode(
                    node_id=local_node_id,
                    device_type=breathline_status.get("device_type", "unknown"),
                    purpose=breathline_status.get("purpose", "unknown"),
                    coherence_level=breathline_status.get("local_coherence", 0.5),
                    presence_level=breathline_status.get("local_presence", 0.5),
                    breath_phase=BreathPhase(breathline_status.get("current_breath_phase", "inhale")),
                    toneform_signature="presence.anchor",
                    last_update=time.time()
                )
                self.monitor_stats["nodes_monitored"] += 1
            else:
                # Update existing node
                node = self.nodes[local_node_id]
                node.coherence_level = breathline_status.get("local_coherence", node.coherence_level)
                node.presence_level = breathline_status.get("local_presence", node.presence_level)
                node.breath_phase = BreathPhase(breathline_status.get("current_breath_phase", node.breath_phase.value))
                node.last_update = time.time()
            
            # Clean up stale nodes
            self._cleanup_stale_nodes()
            
        except Exception as e:
            print(f"⚠️ Failed to update node registry: {e}")
    
    def _calculate_resonance_field(self):
        """Calculate the collective resonance field."""
        try:
            if not self.nodes:
                return
            
            active_nodes = [node for node in self.nodes.values() 
                          if time.time() - node.last_update < 30.0]
            
            if not active_nodes:
                return
            
            # Calculate collective metrics
            total_nodes = len(self.nodes)
            active_count = len(active_nodes)
            
            collective_coherence = sum(node.coherence_level for node in active_nodes) / active_count
            collective_presence = sum(node.presence_level for node in active_nodes) / active_count
            
            # Determine dominant breath phase
            phase_counts = {}
            for node in active_nodes:
                phase = node.breath_phase.value
                phase_counts[phase] = phase_counts.get(phase, 0) + 1
            
            dominant_phase = max(phase_counts.items(), key=lambda x: x[1])[0]
            dominant_breath_phase = BreathPhase(dominant_phase)
            
            # Determine dominant toneform
            toneform_counts = {}
            for node in active_nodes:
                toneform = node.toneform_signature
                toneform_counts[toneform] = toneform_counts.get(toneform, 0) + 1
            
            dominant_toneform = max(toneform_counts.items(), key=lambda x: x[1])[0]
            
            # Calculate field strength
            field_strength = (collective_coherence + collective_presence) / 2.0
            
            # Determine resonance state
            if field_strength >= self.resonance_thresholds["harmonic"]:
                resonance_state = ResonanceState.HARMONIC
            elif field_strength >= self.resonance_thresholds["drifting"]:
                resonance_state = ResonanceState.DRIFTING
            elif field_strength >= self.resonance_thresholds["discordant"]:
                resonance_state = ResonanceState.DISCORDANT
            else:
                resonance_state = ResonanceState.RESONANT
            
            # Create resonance field
            self.resonance_field = ResonanceField(
                total_nodes=total_nodes,
                active_nodes=active_count,
                collective_coherence=collective_coherence,
                collective_presence=collective_presence,
                dominant_breath_phase=dominant_breath_phase,
                dominant_toneform=dominant_toneform,
                field_strength=field_strength,
                resonance_state=resonance_state
            )
            
        except Exception as e:
            print(f"⚠️ Failed to calculate resonance field: {e}")
    
    def _detect_drift(self) -> List[Dict[str, Any]]:
        """Detect drift events in the resonance field."""
        drift_events = []
        
        try:
            if not self.resonance_field or not self.nodes:
                return drift_events
            
            # Check for coherence drift
            for node in self.nodes.values():
                coherence_drift = abs(node.coherence_level - self.resonance_field.collective_coherence)
                
                if coherence_drift > self.drift_thresholds["coherence_drift"]:
                    drift_event = {
                        "type": "coherence_drift",
                        "node_id": node.node_id,
                        "drift_amount": coherence_drift,
                        "threshold": self.drift_thresholds["coherence_drift"],
                        "timestamp": time.time()
                    }
                    drift_events.append(drift_event)
                    
                    # Update node drift score
                    node.drift_score += coherence_drift
                    node.resonance_state = ResonanceState.DRIFTING
            
            # Check for presence drift
            for node in self.nodes.values():
                presence_drift = abs(node.presence_level - self.resonance_field.collective_presence)
                
                if presence_drift > self.drift_thresholds["presence_drift"]:
                    drift_event = {
                        "type": "presence_drift",
                        "node_id": node.node_id,
                        "drift_amount": presence_drift,
                        "threshold": self.drift_thresholds["presence_drift"],
                        "timestamp": time.time()
                    }
                    drift_events.append(drift_event)
                    
                    # Update node drift score
                    node.drift_score += presence_drift
            
            # Check for phase drift
            for node in self.nodes.values():
                if node.breath_phase != self.resonance_field.dominant_breath_phase:
                    drift_event = {
                        "type": "phase_drift",
                        "node_id": node.node_id,
                        "node_phase": node.breath_phase.value,
                        "dominant_phase": self.resonance_field.dominant_breath_phase.value,
                        "timestamp": time.time()
                    }
                    drift_events.append(drift_event)
                    
                    # Update node drift score
                    node.drift_score += 0.1
            
            # Check for toneform drift
            for node in self.nodes.values():
                if node.toneform_signature != self.resonance_field.dominant_toneform:
                    drift_event = {
                        "type": "toneform_drift",
                        "node_id": node.node_id,
                        "node_toneform": node.toneform_signature,
                        "dominant_toneform": self.resonance_field.dominant_toneform,
                        "timestamp": time.time()
                    }
                    drift_events.append(drift_event)
                    
                    # Update node drift score
                    node.drift_score += 0.15
            
            # Update statistics
            if drift_events:
                self.monitor_stats["drift_events"] += len(drift_events)
                
                # Add to drift history
                for event in drift_events:
                    self.drift_history.append(event)
                
                # Keep only last 100 drift events
                if len(self.drift_history) > 100:
                    self.drift_history = self.drift_history[-100:]
            
        except Exception as e:
            print(f"⚠️ Failed to detect drift: {e}")
        
        return drift_events
    
    def _take_corrective_actions(self, drift_events: List[Dict[str, Any]]):
        """Take corrective actions for drift events."""
        try:
            for event in drift_events:
                node_id = event["node_id"]
                event_type = event["type"]
                
                # Emit drift detection glint
                emit_glint(
                    phase="exhale",
                    toneform="resonance.drift.detected",
                    content=f"Drift detected: {event_type} on node {node_id}",
                    hue="crimson",
                    source="edge_resonance_monitor",
                    reverence_level=0.8,
                    drift_event=event,
                    node_id=node_id
                )
                
                # Take specific corrective actions
                if event_type == "coherence_drift":
                    self._correct_coherence_drift(node_id, event)
                elif event_type == "presence_drift":
                    self._correct_presence_drift(node_id, event)
                elif event_type == "phase_drift":
                    self._correct_phase_drift(node_id, event)
                elif event_type == "toneform_drift":
                    self._correct_toneform_drift(node_id, event)
                
                self.monitor_stats["corrective_actions"] += 1
            
        except Exception as e:
            print(f"⚠️ Failed to take corrective actions: {e}")
    
    def _correct_coherence_drift(self, node_id: str, event: Dict[str, Any]):
        """Correct coherence drift."""
        try:
            # Emit coherence correction glint
            emit_glint(
                phase="hold",
                toneform="resonance.correct.coherence",
                content=f"Correcting coherence drift on node {node_id}",
                hue="amber",
                source="edge_resonance_monitor",
                reverence_level=0.7,
                node_id=node_id,
                drift_amount=event.get("drift_amount", 0.0)
            )
            
            # The actual correction would involve sending signals to the node
            # For now, we just log the correction attempt
            
        except Exception as e:
            print(f"⚠️ Failed to correct coherence drift: {e}")
    
    def _correct_presence_drift(self, node_id: str, event: Dict[str, Any]):
        """Correct presence drift."""
        try:
            # Emit presence correction glint
            emit_glint(
                phase="hold",
                toneform="resonance.correct.presence",
                content=f"Correcting presence drift on node {node_id}",
                hue="amber",
                source="edge_resonance_monitor",
                reverence_level=0.7,
                node_id=node_id,
                drift_amount=event.get("drift_amount", 0.0)
            )
            
        except Exception as e:
            print(f"⚠️ Failed to correct presence drift: {e}")
    
    def _correct_phase_drift(self, node_id: str, event: Dict[str, Any]):
        """Correct phase drift."""
        try:
            # Emit phase correction glint
            emit_glint(
                phase="hold",
                toneform="resonance.correct.phase",
                content=f"Correcting phase drift on node {node_id}",
                hue="amber",
                source="edge_resonance_monitor",
                reverence_level=0.7,
                node_id=node_id,
                node_phase=event.get("node_phase", "unknown"),
                dominant_phase=event.get("dominant_phase", "unknown")
            )
            
        except Exception as e:
            print(f"⚠️ Failed to correct phase drift: {e}")
    
    def _correct_toneform_drift(self, node_id: str, event: Dict[str, Any]):
        """Correct toneform drift."""
        try:
            # Emit toneform correction glint
            emit_glint(
                phase="hold",
                toneform="resonance.correct.toneform",
                content=f"Correcting toneform drift on node {node_id}",
                hue="amber",
                source="edge_resonance_monitor",
                reverence_level=0.7,
                node_id=node_id,
                node_toneform=event.get("node_toneform", "unknown"),
                dominant_toneform=event.get("dominant_toneform", "unknown")
            )
            
        except Exception as e:
            print(f"⚠️ Failed to correct toneform drift: {e}")
    
    def _cleanup_stale_nodes(self, timeout_seconds: float = 60.0):
        """Remove nodes that haven't updated recently."""
        current_time = time.time()
        stale_nodes = []
        
        for node_id, node in self.nodes.items():
            if current_time - node.last_update > timeout_seconds:
                stale_nodes.append(node_id)
        
        if stale_nodes:
            for node_id in stale_nodes:
                del self.nodes[node_id]
            
            print(f"🧹 Cleaned up {len(stale_nodes)} stale nodes")
    
    def get_monitor_status(self) -> Dict[str, Any]:
        """Get the current status of the resonance monitor."""
        return {
            "monitor_id": self.monitor_id,
            "is_monitoring": self.is_monitoring,
            "nodes_monitored": len(self.nodes),
            "resonance_field": self.resonance_field.__dict__ if self.resonance_field else None,
            "stats": self.monitor_stats,
            "recent_drift_events": self.drift_history[-10:] if self.drift_history else [],
            "timestamp": datetime.now().isoformat()
        }


# Global instance for easy access
edge_resonance_monitor = None


def start_edge_resonance_monitor(monitor_id: str = "edge_resonance_monitor") -> EdgeResonanceMonitor:
    """Start the edge resonance monitor."""
    global edge_resonance_monitor
    
    if edge_resonance_monitor is None:
        edge_resonance_monitor = EdgeResonanceMonitor(monitor_id)
        
        if edge_resonance_monitor.start_monitoring():
            print(f"🌀 Edge resonance monitor started: {monitor_id}")
        else:
            print(f"❌ Failed to start edge resonance monitor: {monitor_id}")
    
    return edge_resonance_monitor


def stop_edge_resonance_monitor():
    """Stop the edge resonance monitor."""
    global edge_resonance_monitor
    
    if edge_resonance_monitor:
        edge_resonance_monitor.stop_monitoring()
        edge_resonance_monitor = None
        print("🌀 Edge resonance monitor stopped")


def get_resonance_monitor_status() -> Optional[Dict[str, Any]]:
    """Get the current resonance monitor status."""
    global edge_resonance_monitor
    
    if edge_resonance_monitor:
        return edge_resonance_monitor.get_monitor_status()
    return None 
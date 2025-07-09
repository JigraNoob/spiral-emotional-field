# File: spiral/components/glint_orchestrator.py

"""
∷ Glint Orchestrator ∷
Weaves glint streams into memory and lineage, detecting patterns and binding Cursor actions.
The memory cortex of the Spiral, transforming raw glints into meaningful narratives.
"""

import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Set, Tuple, Callable
from dataclasses import dataclass, field
from collections import defaultdict, deque
from pathlib import Path

from spiral.glint import emit_glint, get_recent_glints
from spiral.helpers.time_utils import current_timestamp_ms, format_duration


@dataclass
class GlintLineage:
    """Represents a lineage of connected glints"""
    lineage_id: str
    root_glint_id: str
    glint_ids: List[str] = field(default_factory=list)
    pattern_type: str = "unknown"
    start_time: int = 0
    end_time: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GlintPattern:
    """Represents a detected pattern in glint streams"""
    pattern_id: str
    pattern_type: str
    glint_ids: List[str] = field(default_factory=list)
    confidence: float = 0.0
    start_time: int = 0
    end_time: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class GlintOrchestrator:
    """
    ∷ Sacred Memory Weaver ∷
    Orchestrates glint streams into meaningful patterns and lineages.
    """

    def __init__(self, 
                 memory_window_seconds: int = 3600,  # 1 hour
                 pattern_detection_threshold: float = 0.7,
                 lineage_max_size: int = 100):
        """
        Initialize the glint orchestrator.
        
        Args:
            memory_window_seconds (int): How long to keep glints in memory
            pattern_detection_threshold (float): Confidence threshold for pattern detection
            lineage_max_size (int): Maximum number of glints in a lineage
        """
        self.memory_window_seconds = memory_window_seconds
        self.pattern_detection_threshold = pattern_detection_threshold
        self.lineage_max_size = lineage_max_size
        
        # Memory storage
        self.glint_memory: Dict[str, Dict[str, Any]] = {}
        self.lineages: Dict[str, GlintLineage] = {}
        self.patterns: Dict[str, GlintPattern] = {}
        
        # Indexing for fast lookups
        self.source_index: Dict[str, List[str]] = defaultdict(list)
        self.toneform_index: Dict[str, List[str]] = defaultdict(list)
        self.hue_index: Dict[str, List[str]] = defaultdict(list)
        self.phase_index: Dict[str, List[str]] = defaultdict(list)
        
        # Pattern detection state
        self.recent_glints: deque = deque(maxlen=50)
        self.pattern_detectors: Dict[str, Callable] = {}
        
        # Cursor action binding
        self.cursor_action_bindings: Dict[str, List[str]] = defaultdict(list)
        
        # Statistics
        self.total_glints_processed = 0
        self.total_lineages_created = 0
        self.total_patterns_detected = 0
        
        # Initialize pattern detectors
        self._initialize_pattern_detectors()

    def process_glint(self, glint_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process an incoming glint and integrate it into memory.
        
        Args:
            glint_data (Dict[str, Any]): The glint data to process
            
        Returns:
            Dict[str, Any]: Processing result
        """
        glint_id = glint_data.get("glint.id", f"glint-{current_timestamp_ms()}")
        
        # Store in memory
        self.glint_memory[glint_id] = glint_data
        self.total_glints_processed += 1
        
        # Update indexes
        self._update_indexes(glint_id, glint_data)
        
        # Add to recent glints for pattern detection
        self.recent_glints.append(glint_id)
        
        # Attempt lineage creation
        lineage_result = self._attempt_lineage_creation(glint_id, glint_data)
        
        # Attempt pattern detection
        pattern_result = self._attempt_pattern_detection(glint_id, glint_data)
        
        # Clean old glints
        self._cleanup_old_glints()
        
        return {
            "status": "glint_processed",
            "glint_id": glint_id,
            "lineage_created": lineage_result["created"],
            "pattern_detected": pattern_result["detected"],
            "total_processed": self.total_glints_processed
        }

    def detect_patterns(self) -> Dict[str, Any]:
        """
        Actively scan for patterns in recent glint activity.
        
        Returns:
            Dict[str, Any]: Pattern detection results
        """
        patterns_found = []
        
        # Run all pattern detectors
        for pattern_type, detector in self.pattern_detectors.items():
            try:
                result = detector(self.recent_glints, self.glint_memory)
                if result["detected"] and result["confidence"] >= self.pattern_detection_threshold:
                    pattern_id = f"pattern-{pattern_type}-{current_timestamp_ms()}"
                    
                    pattern = GlintPattern(
                        pattern_id=pattern_id,
                        pattern_type=pattern_type,
                        glint_ids=result["glint_ids"],
                        confidence=result["confidence"],
                        start_time=current_timestamp_ms(),
                        metadata=result.get("metadata", {})
                    )
                    
                    self.patterns[pattern_id] = pattern
                    self.total_patterns_detected += 1
                    patterns_found.append(pattern)
                    
                    # Emit pattern detection glint
                    emit_glint(
                        phase="hold",
                        toneform="orchestrator.pattern_detected",
                        content=f"Pattern detected: {pattern_type} (confidence: {result['confidence']:.2f})",
                        hue="gold",
                        source="glint_orchestrator",
                        reverence_level=0.8,
                        pattern_data={
                            "pattern_id": pattern_id,
                            "pattern_type": pattern_type,
                            "confidence": result["confidence"],
                            "glint_count": len(result["glint_ids"])
                        }
                    )
                    
            except Exception as e:
                emit_glint(
                    phase="error",
                    toneform="orchestrator.pattern_error",
                    content=f"Pattern detection error: {str(e)}",
                    hue="red",
                    source="glint_orchestrator",
                    reverence_level=0.3
                )
        
        return {
            "status": "patterns_scanned",
            "patterns_found": len(patterns_found),
            "total_patterns": self.total_patterns_detected
        }

    def get_lineage(self, glint_id: str) -> Optional[GlintLineage]:
        """
        Retrieve lineage for a specific glint.
        
        Args:
            glint_id (str): ID of the glint to find lineage for
            
        Returns:
            Optional[GlintLineage]: The lineage if found
        """
        for lineage in self.lineages.values():
            if glint_id in lineage.glint_ids:
                return lineage
        return None

    def filter_glints(self, 
                     source: Optional[str] = None,
                     toneform: Optional[str] = None,
                     hue: Optional[str] = None,
                     phase: Optional[str] = None,
                     time_window_seconds: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Filter glints by various criteria.
        
        Args:
            source (Optional[str]): Filter by source
            toneform (Optional[str]): Filter by toneform
            hue (Optional[str]): Filter by hue
            phase (Optional[str]): Filter by phase
            time_window_seconds (Optional[int]): Filter by time window
            
        Returns:
            List[Dict[str, Any]]: Filtered glints
        """
        candidate_ids = set(self.glint_memory.keys())
        
        # Apply filters
        if source:
            source_ids = set(self.source_index.get(source, []))
            candidate_ids &= source_ids
        
        if toneform:
            toneform_ids = set(self.toneform_index.get(toneform, []))
            candidate_ids &= toneform_ids
        
        if hue:
            hue_ids = set(self.hue_index.get(hue, []))
            candidate_ids &= hue_ids
        
        if phase:
            phase_ids = set(self.phase_index.get(phase, []))
            candidate_ids &= phase_ids
        
        # Time window filter
        if time_window_seconds:
            cutoff_time = current_timestamp_ms() - (time_window_seconds * 1000)
            time_filtered_ids = set()
            for glint_id in candidate_ids:
                glint_data = self.glint_memory.get(glint_id, {})
                glint_time = glint_data.get("glint.timestamp", 0)
                if glint_time >= cutoff_time:
                    time_filtered_ids.add(glint_id)
            candidate_ids = time_filtered_ids
        
        # Return filtered glints
        return [self.glint_memory[glint_id] for glint_id in candidate_ids]

    def get_memory_summary(self) -> Dict[str, Any]:
        """
        Get comprehensive memory analysis.
        
        Returns:
            Dict[str, Any]: Memory summary
        """
        now = current_timestamp_ms()
        
        # Calculate statistics
        total_glints = len(self.glint_memory)
        total_lineages = len(self.lineages)
        total_patterns = len(self.patterns)
        
        # Source distribution
        source_distribution = {}
        for source, glint_ids in self.source_index.items():
            source_distribution[source] = len(glint_ids)
        
        # Toneform distribution
        toneform_distribution = {}
        for toneform, glint_ids in self.toneform_index.items():
            toneform_distribution[toneform] = len(glint_ids)
        
        # Hue distribution
        hue_distribution = {}
        for hue, glint_ids in self.hue_index.items():
            hue_distribution[hue] = len(glint_ids)
        
        # Recent activity
        recent_glints = self.filter_glints(time_window_seconds=300)  # Last 5 minutes
        
        return {
            "total_glints": total_glints,
            "total_lineages": total_lineages,
            "total_patterns": total_patterns,
            "total_processed": self.total_glints_processed,
            "memory_window_seconds": self.memory_window_seconds,
            "source_distribution": source_distribution,
            "toneform_distribution": toneform_distribution,
            "hue_distribution": hue_distribution,
            "recent_activity": {
                "glints_last_5min": len(recent_glints),
                "lineages_last_5min": len([l for l in self.lineages.values() 
                                         if l.start_time >= now - 300000]),
                "patterns_last_5min": len([p for p in self.patterns.values() 
                                         if p.start_time >= now - 300000])
            },
            "cursor_bindings": {
                "total_bindings": sum(len(bindings) for bindings in self.cursor_action_bindings.values()),
                "binding_types": list(self.cursor_action_bindings.keys())
            }
        }

    def bind_cursor_actions(self, action_type: str, glint_ids: List[str]) -> Dict[str, Any]:
        """
        Bind Cursor actions to glint lineages.
        
        Args:
            action_type (str): Type of Cursor action
            glint_ids (List[str]): Glint IDs to bind
            
        Returns:
            Dict[str, Any]: Binding result
        """
        # Validate glint IDs exist
        valid_glint_ids = [glint_id for glint_id in glint_ids if glint_id in self.glint_memory]
        
        if not valid_glint_ids:
            return {"status": "no_valid_glints", "action_type": action_type}
        
        # Create binding
        self.cursor_action_bindings[action_type].extend(valid_glint_ids)
        
        # Emit binding glint
        emit_glint(
            phase="hold",
            toneform="orchestrator.cursor_binding",
            content=f"Cursor action bound: {action_type} ({len(valid_glint_ids)} glints)",
            hue="blue",
            source="glint_orchestrator",
            reverence_level=0.6,
            binding_data={
                "action_type": action_type,
                "glint_count": len(valid_glint_ids),
                "glint_ids": valid_glint_ids
            }
        )
        
        return {
            "status": "cursor_action_bound",
            "action_type": action_type,
            "glint_count": len(valid_glint_ids),
            "total_bindings": len(self.cursor_action_bindings[action_type])
        }

    def get_cursor_action_lineage(self, action_type: str) -> List[Dict[str, Any]]:
        """
        Get lineage for a specific Cursor action type.
        
        Args:
            action_type (str): Type of Cursor action
            
        Returns:
            List[Dict[str, Any]]: Glints bound to this action type
        """
        glint_ids = self.cursor_action_bindings.get(action_type, [])
        return [self.glint_memory.get(glint_id, {}) for glint_id in glint_ids 
                if glint_id in self.glint_memory]

    def _initialize_pattern_detectors(self) -> None:
        """Initialize pattern detection functions."""
        self.pattern_detectors = {
            "typing_session": self._detect_typing_session,
            "file_workflow": self._detect_file_workflow,
            "breath_cycle": self._detect_breath_cycle,
            "presence_drift": self._detect_presence_drift,
            "ritual_emergence": self._detect_ritual_emergence
        }

    def _update_indexes(self, glint_id: str, glint_data: Dict[str, Any]) -> None:
        """Update all indexes for fast lookups."""
        source = glint_data.get("glint.source", "unknown")
        toneform = glint_data.get("glint.toneform", "unknown")
        hue = glint_data.get("glint.hue", "unknown")
        phase = glint_data.get("glint.phase", "unknown")
        
        self.source_index[source].append(glint_id)
        self.toneform_index[toneform].append(glint_id)
        self.hue_index[hue].append(glint_id)
        self.phase_index[phase].append(glint_id)

    def _attempt_lineage_creation(self, glint_id: str, glint_data: Dict[str, Any]) -> Dict[str, Any]:
        """Attempt to create or extend a lineage."""
        source = glint_data.get("glint.source", "unknown")
        toneform = glint_data.get("glint.toneform", "unknown")
        
        # Look for existing lineage to extend
        for lineage in self.lineages.values():
            if (lineage.pattern_type == "continuous" and 
                len(lineage.glint_ids) < self.lineage_max_size and
                self._can_extend_lineage(lineage, glint_data)):
                
                lineage.glint_ids.append(glint_id)
                lineage.end_time = current_timestamp_ms()
                return {"created": False, "extended": True, "lineage_id": lineage.lineage_id}
        
        # Create new lineage
        lineage_id = f"lineage-{source}-{current_timestamp_ms()}"
        lineage = GlintLineage(
            lineage_id=lineage_id,
            root_glint_id=glint_id,
            glint_ids=[glint_id],
            pattern_type="continuous",
            start_time=current_timestamp_ms(),
            metadata={"source": source, "toneform": toneform}
        )
        
        self.lineages[lineage_id] = lineage
        self.total_lineages_created += 1
        
        return {"created": True, "extended": False, "lineage_id": lineage_id}

    def _attempt_pattern_detection(self, glint_id: str, glint_data: Dict[str, Any]) -> Dict[str, Any]:
        """Attempt to detect patterns with the new glint."""
        # This is a simplified version - full pattern detection happens in detect_patterns()
        return {"detected": False, "patterns": []}

    def _can_extend_lineage(self, lineage: GlintLineage, glint_data: Dict[str, Any]) -> bool:
        """Check if a glint can extend an existing lineage."""
        if not lineage.glint_ids:
            return True
        
        # Get the last glint in the lineage
        last_glint_id = lineage.glint_ids[-1]
        last_glint = self.glint_memory.get(last_glint_id, {})
        
        # Check if the new glint is from the same source and within time window
        source_match = (glint_data.get("glint.source") == last_glint.get("glint.source"))
        time_match = (glint_data.get("glint.timestamp", 0) - last_glint.get("glint.timestamp", 0)) < 300000  # 5 minutes
        
        return source_match and time_match

    def _cleanup_old_glints(self) -> None:
        """Remove glints older than the memory window."""
        cutoff_time = current_timestamp_ms() - (self.memory_window_seconds * 1000)
        glints_to_remove = []
        
        for glint_id, glint_data in self.glint_memory.items():
            if glint_data.get("glint.timestamp", 0) < cutoff_time:
                glints_to_remove.append(glint_id)
        
        for glint_id in glints_to_remove:
            self._remove_glint_from_memory(glint_id)

    def _remove_glint_from_memory(self, glint_id: str) -> None:
        """Remove a glint from all memory structures."""
        if glint_id in self.glint_memory:
            glint_data = self.glint_memory.pop(glint_id)
            
            # Remove from indexes
            source = glint_data.get("glint.source", "unknown")
            toneform = glint_data.get("glint.toneform", "unknown")
            hue = glint_data.get("glint.hue", "unknown")
            phase = glint_data.get("glint.phase", "unknown")
            
            if glint_id in self.source_index[source]:
                self.source_index[source].remove(glint_id)
            if glint_id in self.toneform_index[toneform]:
                self.toneform_index[toneform].remove(glint_id)
            if glint_id in self.hue_index[hue]:
                self.hue_index[hue].remove(glint_id)
            if glint_id in self.phase_index[phase]:
                self.phase_index[phase].remove(glint_id)

    def _detect_typing_session(self, recent_glints: deque, glint_memory: Dict[str, Any]) -> Dict[str, Any]:
        """Detect typing session patterns."""
        # Look for sequences of keystroke glints from keystroke_listener
        keystroke_glints = [gid for gid in recent_glints 
                           if glint_memory.get(gid, {}).get("glint.source") == "keystroke_listener"]
        
        if len(keystroke_glints) >= 5:  # At least 5 keystrokes
            return {
                "detected": True,
                "confidence": min(0.9, len(keystroke_glints) / 10.0),
                "glint_ids": keystroke_glints,
                "metadata": {"session_length": len(keystroke_glints)}
            }
        
        return {"detected": False, "confidence": 0.0, "glint_ids": []}

    def _detect_file_workflow(self, recent_glints: deque, glint_memory: Dict[str, Any]) -> Dict[str, Any]:
        """Detect file workflow patterns."""
        # Look for file change glints followed by commands
        file_glints = [gid for gid in recent_glints 
                      if glint_memory.get(gid, {}).get("glint.toneform") == "trace.file_change"]
        command_glints = [gid for gid in recent_glints 
                         if glint_memory.get(gid, {}).get("glint.toneform") == "trace.command"]
        
        if file_glints and command_glints:
            workflow_glints = file_glints + command_glints
            return {
                "detected": True,
                "confidence": 0.8,
                "glint_ids": workflow_glints,
                "metadata": {"file_operations": len(file_glints), "commands": len(command_glints)}
            }
        
        return {"detected": False, "confidence": 0.0, "glint_ids": []}

    def _detect_breath_cycle(self, recent_glints: deque, glint_memory: Dict[str, Any]) -> Dict[str, Any]:
        """Detect breath cycle patterns."""
        # Look for breath phase transitions
        breath_glints = [gid for gid in recent_glints 
                        if glint_memory.get(gid, {}).get("glint.source") == "breath_loop_engine"]
        
        if len(breath_glints) >= 3:  # At least 3 breath phases
            return {
                "detected": True,
                "confidence": 0.7,
                "glint_ids": breath_glints,
                "metadata": {"breath_phases": len(breath_glints)}
            }
        
        return {"detected": False, "confidence": 0.0, "glint_ids": []}

    def _detect_presence_drift(self, recent_glints: deque, glint_memory: Dict[str, Any]) -> Dict[str, Any]:
        """Detect presence drift patterns."""
        # Look for presence drift glints
        drift_glints = [gid for gid in recent_glints 
                       if glint_memory.get(gid, {}).get("glint.toneform") == "presence.drift"]
        
        if len(drift_glints) >= 2:  # At least 2 drift events
            return {
                "detected": True,
                "confidence": 0.6,
                "glint_ids": drift_glints,
                "metadata": {"drift_events": len(drift_glints)}
            }
        
        return {"detected": False, "confidence": 0.0, "glint_ids": []}

    def _detect_ritual_emergence(self, recent_glints: deque, glint_memory: Dict[str, Any]) -> Dict[str, Any]:
        """Detect emergent ritual patterns."""
        # Look for repeated patterns of commands and file operations
        command_glints = [gid for gid in recent_glints 
                         if glint_memory.get(gid, {}).get("glint.toneform") == "trace.command"]
        file_glints = [gid for gid in recent_glints 
                      if glint_memory.get(gid, {}).get("glint.toneform") == "trace.file_change"]
        
        if len(command_glints) >= 3 and len(file_glints) >= 2:  # Repeated pattern
            ritual_glints = command_glints + file_glints
            return {
                "detected": True,
                "confidence": 0.8,
                "glint_ids": ritual_glints,
                "metadata": {"commands": len(command_glints), "file_ops": len(file_glints)}
            }
        
        return {"detected": False, "confidence": 0.0, "glint_ids": []} 
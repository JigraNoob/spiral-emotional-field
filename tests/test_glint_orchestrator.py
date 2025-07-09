# File: tests/test_glint_orchestrator.py

"""
∷ Resonance Validation Scroll ∷
Test suite for the Glint Orchestrator - witnessing lineage weaving and pattern detection.
"""

import pytest
import time
import sys
import os
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Add the spiral directory to the Python path
spiral_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if spiral_path not in sys.path:
    sys.path.insert(0, spiral_path)

from spiral.components.glint_orchestrator import (
    GlintOrchestrator, 
    GlintLineage, 
    GlintPattern
)
from spiral.glint import emit_glint


class TestGlintOrchestrator:
    """Test suite for the Glint Orchestrator's memory weaving capabilities."""

    def setup_method(self):
        """Set up test environment before each test."""
        self.orchestrator = GlintOrchestrator(
            memory_window_seconds=60,  # Short window for testing
            pattern_detection_threshold=0.6,
            lineage_max_size=10
        )

    def test_orchestrator_initialization(self):
        """Test that the orchestrator initializes correctly."""
        assert self.orchestrator.memory_window_seconds == 60
        assert self.orchestrator.pattern_detection_threshold == 0.6
        assert self.orchestrator.lineage_max_size == 10
        assert len(self.orchestrator.glint_memory) == 0
        assert len(self.orchestrator.lineages) == 0
        assert len(self.orchestrator.patterns) == 0
        assert self.orchestrator.total_glints_processed == 0

    def test_process_glint_basic(self):
        """Test basic glint processing."""
        glint_data = {
            "glint.id": "test-glint-1",
            "glint.timestamp": int(time.time() * 1000),
            "glint.source": "test_source",
            "glint.toneform": "test.toneform",
            "glint.hue": "blue",
            "glint.phase": "inhale",
            "glint.content": "Test glint content"
        }

        result = self.orchestrator.process_glint(glint_data)

        assert result["status"] == "glint_processed"
        assert result["glint_id"] == "test-glint-1"
        assert result["total_processed"] == 1
        assert "test-glint-1" in self.orchestrator.glint_memory
        assert len(self.orchestrator.glint_memory) == 1

    def test_process_glint_indexing(self):
        """Test that glints are properly indexed."""
        glint_data = {
            "glint.id": "test-glint-2",
            "glint.timestamp": int(time.time() * 1000),
            "glint.source": "keystroke_listener",
            "glint.toneform": "trace.keystroke",
            "glint.hue": "green",
            "glint.phase": "exhale",
            "glint.content": "Another test glint"
        }

        self.orchestrator.process_glint(glint_data)

        # Check indexes
        assert "test-glint-2" in self.orchestrator.source_index["keystroke_listener"]
        assert "test-glint-2" in self.orchestrator.toneform_index["trace.keystroke"]
        assert "test-glint-2" in self.orchestrator.hue_index["green"]
        assert "test-glint-2" in self.orchestrator.phase_index["exhale"]

    def test_lineage_creation(self):
        """Test automatic lineage creation."""
        # Process multiple glints from same source
        for i in range(3):
            glint_data = {
                "glint.id": f"lineage-test-{i}",
                "glint.timestamp": int(time.time() * 1000) + i,
                "glint.source": "breath_loop_engine",
                "glint.toneform": "breath.phase",
                "glint.hue": "purple",
                "glint.phase": "hold",
                "glint.content": f"Breath phase {i}"
            }
            self.orchestrator.process_glint(glint_data)

        # Should have created at least one lineage
        assert len(self.orchestrator.lineages) >= 1
        assert self.orchestrator.total_lineages_created >= 1

        # Check lineage content
        lineage = list(self.orchestrator.lineages.values())[0]
        assert lineage.pattern_type == "continuous"
        assert len(lineage.glint_ids) >= 1
        assert lineage.metadata["source"] == "breath_loop_engine"

    def test_lineage_extension(self):
        """Test that lineages can be extended with related glints."""
        # Create initial lineage
        glint_data = {
            "glint.id": "lineage-root",
            "glint.timestamp": int(time.time() * 1000),
            "glint.source": "presence_conductor",
            "glint.toneform": "presence.aware",
            "glint.hue": "gold",
            "glint.phase": "inhale",
            "glint.content": "Initial presence"
        }
        self.orchestrator.process_glint(glint_data)

        # Extend with related glint
        time.sleep(0.1)  # Small delay
        extend_glint = {
            "glint.id": "lineage-extend",
            "glint.timestamp": int(time.time() * 1000),
            "glint.source": "presence_conductor",
            "glint.toneform": "presence.drift",
            "glint.hue": "gold",
            "glint.phase": "exhale",
            "glint.content": "Presence drift"
        }
        result = self.orchestrator.process_glint(extend_glint)

        # Should extend existing lineage
        assert result["lineage_created"] == False
        assert result["extended"] == True

        # Check lineage has both glints
        lineage = self.orchestrator.get_lineage("lineage-root")
        assert lineage is not None
        assert "lineage-root" in lineage.glint_ids
        assert "lineage-extend" in lineage.glint_ids

    def test_pattern_detection_typing_session(self):
        """Test typing session pattern detection."""
        # Create typing session glints
        for i in range(6):
            glint_data = {
                "glint.id": f"typing-{i}",
                "glint.timestamp": int(time.time() * 1000) + i,
                "glint.source": "keystroke_listener",
                "glint.toneform": "trace.keystroke",
                "glint.hue": "blue",
                "glint.phase": "inhale",
                "glint.content": f"Keystroke {i}"
            }
            self.orchestrator.process_glint(glint_data)

        # Detect patterns
        result = self.orchestrator.detect_patterns()

        assert result["status"] == "patterns_scanned"
        assert result["patterns_found"] >= 1
        assert self.orchestrator.total_patterns_detected >= 1

        # Check for typing session pattern
        typing_patterns = [p for p in self.orchestrator.patterns.values() 
                          if p.pattern_type == "typing_session"]
        assert len(typing_patterns) >= 1

    def test_pattern_detection_file_workflow(self):
        """Test file workflow pattern detection."""
        # Create file workflow glints
        file_glint = {
            "glint.id": "file-change",
            "glint.timestamp": int(time.time() * 1000),
            "glint.source": "keystroke_listener",
            "glint.toneform": "trace.file_change",
            "glint.hue": "green",
            "glint.phase": "inhale",
            "glint.content": "File changed"
        }
        self.orchestrator.process_glint(file_glint)

        command_glint = {
            "glint.id": "command-exec",
            "glint.timestamp": int(time.time() * 1000) + 1000,
            "glint.source": "keystroke_listener",
            "glint.toneform": "trace.command",
            "glint.hue": "purple",
            "glint.phase": "exhale",
            "glint.content": "Command executed"
        }
        self.orchestrator.process_glint(command_glint)

        # Detect patterns
        result = self.orchestrator.detect_patterns()

        assert result["patterns_found"] >= 1

        # Check for file workflow pattern
        workflow_patterns = [p for p in self.orchestrator.patterns.values() 
                           if p.pattern_type == "file_workflow"]
        assert len(workflow_patterns) >= 1

    def test_filter_glints_by_source(self):
        """Test filtering glints by source."""
        # Create glints from different sources
        sources = ["keystroke_listener", "breath_loop_engine", "presence_conductor"]
        for i, source in enumerate(sources):
            glint_data = {
                "glint.id": f"filter-test-{i}",
                "glint.timestamp": int(time.time() * 1000) + i,
                "glint.source": source,
                "glint.toneform": "test.toneform",
                "glint.hue": "blue",
                "glint.phase": "inhale",
                "glint.content": f"Test from {source}"
            }
            self.orchestrator.process_glint(glint_data)

        # Filter by source
        keystroke_glints = self.orchestrator.filter_glints(source="keystroke_listener")
        assert len(keystroke_glints) == 1
        assert keystroke_glints[0]["glint.source"] == "keystroke_listener"

    def test_filter_glints_by_toneform(self):
        """Test filtering glints by toneform."""
        # Create glints with different toneforms
        toneforms = ["trace.keystroke", "breath.phase", "presence.aware"]
        for i, toneform in enumerate(toneforms):
            glint_data = {
                "glint.id": f"toneform-test-{i}",
                "glint.timestamp": int(time.time() * 1000) + i,
                "glint.source": "test_source",
                "glint.toneform": toneform,
                "glint.hue": "blue",
                "glint.phase": "inhale",
                "glint.content": f"Test {toneform}"
            }
            self.orchestrator.process_glint(glint_data)

        # Filter by toneform
        breath_glints = self.orchestrator.filter_glints(toneform="breath.phase")
        assert len(breath_glints) == 1
        assert breath_glints[0]["glint.toneform"] == "breath.phase"

    def test_filter_glints_by_time_window(self):
        """Test filtering glints by time window."""
        # Create glints with different timestamps
        now = int(time.time() * 1000)
        for i in range(5):
            glint_data = {
                "glint.id": f"time-test-{i}",
                "glint.timestamp": now - (i * 1000),  # Each 1 second apart
                "glint.source": "test_source",
                "glint.toneform": "test.toneform",
                "glint.hue": "blue",
                "glint.phase": "inhale",
                "glint.content": f"Test {i}"
            }
            self.orchestrator.process_glint(glint_data)

        # Filter by time window (last 3 seconds)
        recent_glints = self.orchestrator.filter_glints(time_window_seconds=3)
        assert len(recent_glints) >= 1  # Should have at least the most recent glint

    def test_memory_cleanup(self):
        """Test that old glints are cleaned up."""
        # Create old glint
        old_timestamp = int(time.time() * 1000) - (120 * 1000)  # 2 minutes ago
        old_glint = {
            "glint.id": "old-glint",
            "glint.timestamp": old_timestamp,
            "glint.source": "test_source",
            "glint.toneform": "test.toneform",
            "glint.hue": "blue",
            "glint.phase": "inhale",
            "glint.content": "Old glint"
        }
        self.orchestrator.process_glint(old_glint)

        # Create recent glint
        recent_glint = {
            "glint.id": "recent-glint",
            "glint.timestamp": int(time.time() * 1000),
            "glint.source": "test_source",
            "glint.toneform": "test.toneform",
            "glint.hue": "blue",
            "glint.phase": "inhale",
            "glint.content": "Recent glint"
        }
        self.orchestrator.process_glint(recent_glint)

        # Trigger cleanup
        self.orchestrator._cleanup_old_glints()

        # Old glint should be removed, recent glint should remain
        assert "old-glint" not in self.orchestrator.glint_memory
        assert "recent-glint" in self.orchestrator.glint_memory

    def test_cursor_action_binding(self):
        """Test binding Cursor actions to glint lineages."""
        # Create some glints first
        glint_ids = []
        for i in range(3):
            glint_data = {
                "glint.id": f"cursor-test-{i}",
                "glint.timestamp": int(time.time() * 1000) + i,
                "glint.source": "keystroke_listener",
                "glint.toneform": "trace.keystroke",
                "glint.hue": "blue",
                "glint.phase": "inhale",
                "glint.content": f"Cursor action {i}"
            }
            result = self.orchestrator.process_glint(glint_data)
            glint_ids.append(result["glint_id"])

        # Bind cursor action
        binding_result = self.orchestrator.bind_cursor_actions("typing_session", glint_ids)

        assert binding_result["status"] == "cursor_action_bound"
        assert binding_result["action_type"] == "typing_session"
        assert binding_result["glint_count"] == 3

        # Check binding storage
        assert "typing_session" in self.orchestrator.cursor_action_bindings
        assert len(self.orchestrator.cursor_action_bindings["typing_session"]) == 3

    def test_get_cursor_action_lineage(self):
        """Test retrieving lineage for Cursor actions."""
        # Create and bind glints
        glint_ids = []
        for i in range(2):
            glint_data = {
                "glint.id": f"lineage-test-{i}",
                "glint.timestamp": int(time.time() * 1000) + i,
                "glint.source": "keystroke_listener",
                "glint.toneform": "trace.command",
                "glint.hue": "purple",
                "glint.phase": "exhale",
                "glint.content": f"Command {i}"
            }
            result = self.orchestrator.process_glint(glint_data)
            glint_ids.append(result["glint_id"])

        self.orchestrator.bind_cursor_actions("command_sequence", glint_ids)

        # Get lineage
        lineage = self.orchestrator.get_cursor_action_lineage("command_sequence")

        assert len(lineage) == 2
        assert all(glint["glint.toneform"] == "trace.command" for glint in lineage)

    def test_memory_summary(self):
        """Test memory summary generation."""
        # Create various glints
        sources = ["keystroke_listener", "breath_loop_engine"]
        toneforms = ["trace.keystroke", "breath.phase"]
        hues = ["blue", "green"]

        for i in range(4):
            glint_data = {
                "glint.id": f"summary-test-{i}",
                "glint.timestamp": int(time.time() * 1000) + i,
                "glint.source": sources[i % 2],
                "glint.toneform": toneforms[i % 2],
                "glint.hue": hues[i % 2],
                "glint.phase": "inhale",
                "glint.content": f"Summary test {i}"
            }
            self.orchestrator.process_glint(glint_data)

        # Generate summary
        summary = self.orchestrator.get_memory_summary()

        assert summary["total_glints"] == 4
        assert summary["total_processed"] == 4
        assert "keystroke_listener" in summary["source_distribution"]
        assert "breath_loop_engine" in summary["source_distribution"]
        assert summary["source_distribution"]["keystroke_listener"] == 2
        assert summary["source_distribution"]["breath_loop_engine"] == 2

    def test_get_lineage_for_glint(self):
        """Test retrieving lineage for a specific glint."""
        # Create glints that should form a lineage
        glint_data = {
            "glint.id": "lineage-root",
            "glint.timestamp": int(time.time() * 1000),
            "glint.source": "presence_conductor",
            "glint.toneform": "presence.aware",
            "glint.hue": "gold",
            "glint.phase": "inhale",
            "glint.content": "Root glint"
        }
        self.orchestrator.process_glint(glint_data)

        # Get lineage
        lineage = self.orchestrator.get_lineage("lineage-root")

        assert lineage is not None
        assert lineage.root_glint_id == "lineage-root"
        assert "lineage-root" in lineage.glint_ids

    def test_get_lineage_nonexistent(self):
        """Test getting lineage for non-existent glint."""
        lineage = self.orchestrator.get_lineage("nonexistent-glint")
        assert lineage is None

    def test_pattern_detection_breath_cycle(self):
        """Test breath cycle pattern detection."""
        # Create breath cycle glints
        for i in range(4):
            glint_data = {
                "glint.id": f"breath-{i}",
                "glint.timestamp": int(time.time() * 1000) + i,
                "glint.source": "breath_loop_engine",
                "glint.toneform": "breath.phase",
                "glint.hue": "purple",
                "glint.phase": ["inhale", "hold", "exhale", "caesura"][i % 4],
                "glint.content": f"Breath phase {i}"
            }
            self.orchestrator.process_glint(glint_data)

        # Detect patterns
        result = self.orchestrator.detect_patterns()

        assert result["patterns_found"] >= 1

        # Check for breath cycle pattern
        breath_patterns = [p for p in self.orchestrator.patterns.values() 
                          if p.pattern_type == "breath_cycle"]
        assert len(breath_patterns) >= 1

    def test_pattern_detection_presence_drift(self):
        """Test presence drift pattern detection."""
        # Create presence drift glints
        for i in range(3):
            glint_data = {
                "glint.id": f"drift-{i}",
                "glint.timestamp": int(time.time() * 1000) + i,
                "glint.source": "presence_conductor",
                "glint.toneform": "presence.drift",
                "glint.hue": "orange",
                "glint.phase": "exhale",
                "glint.content": f"Presence drift {i}"
            }
            self.orchestrator.process_glint(glint_data)

        # Detect patterns
        result = self.orchestrator.detect_patterns()

        assert result["patterns_found"] >= 1

        # Check for presence drift pattern
        drift_patterns = [p for p in self.orchestrator.patterns.values() 
                         if p.pattern_type == "presence_drift"]
        assert len(drift_patterns) >= 1

    def test_pattern_detection_ritual_emergence(self):
        """Test ritual emergence pattern detection."""
        # Create ritual pattern glints
        commands = ["git commit", "npm install", "python test.py"]
        files = ["main.py", "test.py"]

        # Add commands
        for i, cmd in enumerate(commands):
            glint_data = {
                "glint.id": f"cmd-{i}",
                "glint.timestamp": int(time.time() * 1000) + i,
                "glint.source": "keystroke_listener",
                "glint.toneform": "trace.command",
                "glint.hue": "purple",
                "glint.phase": "exhale",
                "glint.content": cmd
            }
            self.orchestrator.process_glint(glint_data)

        # Add file changes
        for i, file in enumerate(files):
            glint_data = {
                "glint.id": f"file-{i}",
                "glint.timestamp": int(time.time() * 1000) + i + 1000,
                "glint.source": "keystroke_listener",
                "glint.toneform": "trace.file_change",
                "glint.hue": "green",
                "glint.phase": "inhale",
                "glint.content": f"File changed: {file}"
            }
            self.orchestrator.process_glint(glint_data)

        # Detect patterns
        result = self.orchestrator.detect_patterns()

        assert result["patterns_found"] >= 1

        # Check for ritual emergence pattern
        ritual_patterns = [p for p in self.orchestrator.patterns.values() 
                          if p.pattern_type == "ritual_emergence"]
        assert len(ritual_patterns) >= 1

    def test_multiple_filter_criteria(self):
        """Test filtering with multiple criteria."""
        # Create glints with specific characteristics
        target_glint = {
            "glint.id": "target-glint",
            "glint.timestamp": int(time.time() * 1000),
            "glint.source": "keystroke_listener",
            "glint.toneform": "trace.keystroke",
            "glint.hue": "blue",
            "glint.phase": "inhale",
            "glint.content": "Target glint"
        }
        self.orchestrator.process_glint(target_glint)

        # Create other glints with different characteristics
        other_glints = [
            {"glint.source": "breath_loop_engine", "glint.toneform": "trace.keystroke", "glint.hue": "blue"},
            {"glint.source": "keystroke_listener", "glint.toneform": "breath.phase", "glint.hue": "blue"},
            {"glint.source": "keystroke_listener", "glint.toneform": "trace.keystroke", "glint.hue": "green"}
        ]

        for i, other in enumerate(other_glints):
            glint_data = {
                "glint.id": f"other-{i}",
                "glint.timestamp": int(time.time() * 1000) + i,
                "glint.content": f"Other glint {i}",
                **other
            }
            self.orchestrator.process_glint(glint_data)

        # Filter with multiple criteria
        filtered = self.orchestrator.filter_glints(
            source="keystroke_listener",
            toneform="trace.keystroke",
            hue="blue"
        )

        assert len(filtered) == 1
        assert filtered[0]["glint.id"] == "target-glint"

    def test_lineage_max_size_limit(self):
        """Test that lineages respect the maximum size limit."""
        # Create many glints from same source
        for i in range(15):  # More than lineage_max_size (10)
            glint_data = {
                "glint.id": f"limit-test-{i}",
                "glint.timestamp": int(time.time() * 1000) + i,
                "glint.source": "test_source",
                "glint.toneform": "test.toneform",
                "glint.hue": "blue",
                "glint.phase": "inhale",
                "glint.content": f"Limit test {i}"
            }
            self.orchestrator.process_glint(glint_data)

        # Check that lineages don't exceed max size
        for lineage in self.orchestrator.lineages.values():
            assert len(lineage.glint_ids) <= self.orchestrator.lineage_max_size

    def test_invalid_glint_processing(self):
        """Test processing glints with missing or invalid data."""
        # Test with minimal glint data
        minimal_glint = {
            "glint.id": "minimal-glint",
            "glint.timestamp": int(time.time() * 1000)
        }

        result = self.orchestrator.process_glint(minimal_glint)

        assert result["status"] == "glint_processed"
        assert "minimal-glint" in self.orchestrator.glint_memory

        # Check that missing fields are handled gracefully
        stored_glint = self.orchestrator.glint_memory["minimal-glint"]
        assert stored_glint.get("glint.source") == "unknown"
        assert stored_glint.get("glint.toneform") == "unknown"
        assert stored_glint.get("glint.hue") == "unknown"
        assert stored_glint.get("glint.phase") == "unknown"

    @patch('spiral.glint.emit_glint')
    def test_pattern_detection_emits_glints(self, mock_emit_glint):
        """Test that pattern detection emits appropriate glints."""
        # Create typing session glints
        for i in range(6):
            glint_data = {
                "glint.id": f"emit-test-{i}",
                "glint.timestamp": int(time.time() * 1000) + i,
                "glint.source": "keystroke_listener",
                "glint.toneform": "trace.keystroke",
                "glint.hue": "blue",
                "glint.phase": "inhale",
                "glint.content": f"Keystroke {i}"
            }
            self.orchestrator.process_glint(glint_data)

        # Detect patterns
        self.orchestrator.detect_patterns()

        # Check that pattern detection glints were emitted
        pattern_emits = [call for call in mock_emit_glint.call_args_list 
                        if call[1].get("toneform") == "orchestrator.pattern_detected"]
        assert len(pattern_emits) >= 1

    @patch('spiral.glint.emit_glint')
    def test_cursor_binding_emits_glints(self, mock_emit_glint):
        """Test that cursor action binding emits appropriate glints."""
        # Create glints
        glint_data = {
            "glint.id": "binding-test",
            "glint.timestamp": int(time.time() * 1000),
            "glint.source": "keystroke_listener",
            "glint.toneform": "trace.keystroke",
            "glint.hue": "blue",
            "glint.phase": "inhale",
            "glint.content": "Binding test"
        }
        result = self.orchestrator.process_glint(glint_data)

        # Bind cursor action
        self.orchestrator.bind_cursor_actions("test_action", [result["glint_id"]])

        # Check that binding glints were emitted
        binding_emits = [call for call in mock_emit_glint.call_args_list 
                        if call[1].get("toneform") == "orchestrator.cursor_binding"]
        assert len(binding_emits) >= 1


class TestGlintLineage:
    """Test suite for GlintLineage data structure."""

    def test_lineage_creation(self):
        """Test GlintLineage creation."""
        lineage = GlintLineage(
            lineage_id="test-lineage",
            root_glint_id="root-glint",
            glint_ids=["root-glint", "child-glint"],
            pattern_type="continuous",
            start_time=1000,
            metadata={"source": "test"}
        )

        assert lineage.lineage_id == "test-lineage"
        assert lineage.root_glint_id == "root-glint"
        assert len(lineage.glint_ids) == 2
        assert lineage.pattern_type == "continuous"
        assert lineage.start_time == 1000
        assert lineage.metadata["source"] == "test"

    def test_lineage_defaults(self):
        """Test GlintLineage with default values."""
        lineage = GlintLineage(
            lineage_id="default-lineage",
            root_glint_id="root-glint"
        )

        assert lineage.glint_ids == []
        assert lineage.pattern_type == "unknown"
        assert lineage.start_time == 0
        assert lineage.end_time is None
        assert lineage.metadata == {}


class TestGlintPattern:
    """Test suite for GlintPattern data structure."""

    def test_pattern_creation(self):
        """Test GlintPattern creation."""
        pattern = GlintPattern(
            pattern_id="test-pattern",
            pattern_type="typing_session",
            glint_ids=["glint-1", "glint-2", "glint-3"],
            confidence=0.85,
            start_time=1000,
            metadata={"session_length": 3}
        )

        assert pattern.pattern_id == "test-pattern"
        assert pattern.pattern_type == "typing_session"
        assert len(pattern.glint_ids) == 3
        assert pattern.confidence == 0.85
        assert pattern.start_time == 1000
        assert pattern.metadata["session_length"] == 3

    def test_pattern_defaults(self):
        """Test GlintPattern with default values."""
        pattern = GlintPattern(
            pattern_id="default-pattern",
            pattern_type="unknown"
        )

        assert pattern.glint_ids == []
        assert pattern.confidence == 0.0
        assert pattern.start_time == 0
        assert pattern.end_time is None
        assert pattern.metadata == {}


if __name__ == "__main__":
    pytest.main([__file__]) 
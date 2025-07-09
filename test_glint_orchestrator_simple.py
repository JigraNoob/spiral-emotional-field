#!/usr/bin/env python3
"""
Simple test script for GlintOrchestrator functionality.
"""

import sys
import os
import time
from datetime import datetime, timedelta

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from spiral.components.glint_orchestrator import GlintOrchestrator, GlintLineage, GlintPattern

def test_glint_orchestrator_basic():
    """Test basic GlintOrchestrator functionality."""
    print("Testing GlintOrchestrator basic functionality...")
    
    # Initialize orchestrator
    orchestrator = GlintOrchestrator(
        memory_window_seconds=60,
        pattern_detection_threshold=0.6,
        lineage_max_size=10
    )
    
    # Test initialization
    assert orchestrator.memory_window_seconds == 60
    assert orchestrator.pattern_detection_threshold == 0.6
    assert orchestrator.lineage_max_size == 10
    assert len(orchestrator.glint_memory) == 0
    assert len(orchestrator.lineages) == 0
    assert len(orchestrator.patterns) == 0
    assert orchestrator.total_glints_processed == 0
    print("✓ Initialization test passed")
    
    # Test basic glint processing
    glint_data = {
        "glint.id": "test-glint-1",
        "glint.timestamp": int(time.time() * 1000),
        "glint.source": "test_source",
        "glint.toneform": "test.toneform",
        "glint.hue": "blue",
        "glint.phase": "inhale",
        "glint.content": "Test glint content"
    }
    
    result = orchestrator.process_glint(glint_data)
    
    assert result["status"] == "glint_processed"
    assert result["glint_id"] == "test-glint-1"
    assert result["total_processed"] == 1
    assert "test-glint-1" in orchestrator.glint_memory
    assert len(orchestrator.glint_memory) == 1
    print("✓ Basic glint processing test passed")
    
    # Test indexing
    assert "test-glint-1" in orchestrator.source_index["test_source"]
    assert "test-glint-1" in orchestrator.toneform_index["test.toneform"]
    assert "test-glint-1" in orchestrator.hue_index["blue"]
    assert "test-glint-1" in orchestrator.phase_index["inhale"]
    print("✓ Indexing test passed")
    
    return True

def test_glint_lineage():
    """Test GlintLineage functionality."""
    print("Testing GlintLineage functionality...")
    
    # Test lineage creation
    lineage = GlintLineage(
        lineage_id="test-lineage-1",
        root_glint_id="test-root",
        pattern_type="continuous"
    )
    
    assert lineage.lineage_id == "test-lineage-1"
    assert lineage.root_glint_id == "test-root"
    assert lineage.pattern_type == "continuous"
    assert len(lineage.glint_ids) == 0  # Starts empty
    print("✓ Lineage creation test passed")
    
    # Test lineage extension (manually add glint_ids)
    lineage.glint_ids.append("test-root")
    lineage.glint_ids.append("test-extension")
    assert len(lineage.glint_ids) == 2
    assert "test-root" in lineage.glint_ids
    assert "test-extension" in lineage.glint_ids
    print("✓ Lineage extension test passed")
    
    return True

def test_glint_pattern():
    """Test GlintPattern functionality."""
    print("Testing GlintPattern functionality...")
    
    # Test pattern creation
    pattern = GlintPattern(
        pattern_id="test-pattern-1",
        pattern_type="typing_session",
        confidence=0.8,
        glint_ids=["glint1", "glint2", "glint3"],
        metadata={"source": "keystroke_listener"}
    )
    
    assert pattern.pattern_id == "test-pattern-1"
    assert pattern.pattern_type == "typing_session"
    assert pattern.confidence == 0.8
    assert len(pattern.glint_ids) == 3
    assert pattern.metadata["source"] == "keystroke_listener"
    print("✓ Pattern creation test passed")
    
    return True

def test_orchestrator_lineage_creation():
    """Test lineage creation in orchestrator."""
    print("Testing orchestrator lineage creation...")
    
    orchestrator = GlintOrchestrator(
        memory_window_seconds=60,
        pattern_detection_threshold=0.6,
        lineage_max_size=10
    )
    
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
        orchestrator.process_glint(glint_data)
    
    # Should have created at least one lineage
    assert len(orchestrator.lineages) >= 1
    assert orchestrator.total_lineages_created >= 1
    
    # Check lineage content
    lineage = list(orchestrator.lineages.values())[0]
    assert lineage.pattern_type == "continuous"
    assert len(lineage.glint_ids) >= 1
    assert lineage.metadata["source"] == "breath_loop_engine"
    print("✓ Lineage creation test passed")
    
    return True

def test_pattern_detection():
    """Test pattern detection functionality."""
    print("Testing pattern detection...")
    
    orchestrator = GlintOrchestrator(
        memory_window_seconds=60,
        pattern_detection_threshold=0.6,
        lineage_max_size=10
    )
    
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
        orchestrator.process_glint(glint_data)
    
    # Detect patterns
    result = orchestrator.detect_patterns()
    
    assert result["status"] == "patterns_scanned"
    assert result["patterns_found"] >= 1
    assert orchestrator.total_patterns_detected >= 1
    
    # Check for typing session pattern
    typing_patterns = [p for p in orchestrator.patterns.values() 
                      if p.pattern_type == "typing_session"]
    assert len(typing_patterns) >= 1
    print("✓ Pattern detection test passed")
    
    return True

def run_all_tests():
    """Run all tests and report results."""
    print("=" * 60)
    print("Running GlintOrchestrator Tests")
    print("=" * 60)
    
    tests = [
        ("Basic Functionality", test_glint_orchestrator_basic),
        ("GlintLineage", test_glint_lineage),
        ("GlintPattern", test_glint_pattern),
        ("Lineage Creation", test_orchestrator_lineage_creation),
        ("Pattern Detection", test_pattern_detection),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            print(f"\n{test_name}:")
            test_func()
            passed += 1
        except Exception as e:
            print(f"✗ {test_name} failed: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 
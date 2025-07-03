"""Tests for the PropagationHooks component of the Spiral Attunement System."""
import unittest
import os
import shutil
from pathlib import Path
import json
from datetime import datetime, timedelta

from spiral.attunement.propagation_hooks import PropagationHooks, MemoryEcho

class TestPropagationHooks(unittest.TestCase):
    """Test suite for the PropagationHooks memory weaver."""
    
    def setUp(self):
        """Set up test environment with a clean memory directory."""
        self.test_dir = Path("test_memory")
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
        self.test_dir.mkdir()
        
        self.hooks = PropagationHooks(memory_path=self.test_dir)
        
        # Sample tone weights for testing
        self.nature_tones = {"stone": 0.8, "mountain": 0.7, "sky": 0.6}
        self.emotional_tones = {"joy": 0.9, "sadness": 0.3}
        self.temporal_tones = {"memory": 0.8, "time": 0.7}
    
    def tearDown(self):
        """Clean up test files."""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def test_memory_echo_creation(self):
        """Test that MemoryEcho objects are created correctly."""
        content = "The mountains remember..."
        echo = MemoryEcho(
            content=content,
            tone_weights={"mountain": 0.8},
            resonance_score=0.7,
            source="test"
        )
        
        self.assertEqual(echo.content, content)
        self.assertEqual(echo.tone_weights["mountain"], 0.8)
        self.assertEqual(echo.resonance_score, 0.7)
        self.assertEqual(echo.source, "test")
    
    def test_process_resonance_basic(self):
        """Test basic resonance processing."""
        result = self.hooks.process_resonance(
            content="The stone remembers the mountain.",
            tone_weights={"stone": 0.8, "mountain": 0.7},
            resonance_score=0.75
        )
        
        self.assertIn("echoes", result)
        self.assertEqual(result["status"], "resonance_processed")
        self.assertEqual(len(self.hooks.short_term_memory), 1)
    
    def test_surface_routing(self):
        """Test that echoes are routed to appropriate surfaces."""
        # Test natural surface
        self.hooks.process_resonance(
            content="The mountain stands silent.",
            tone_weights={"mountain": 0.8},
            resonance_score=0.7
        )
        self.assertTrue(any("mountain" in echo.content 
                          for echo in self.hooks.tone_surfaces["natural"]))
        
        # Test temporal surface
        self.hooks.process_resonance(
            content="I remember the old days.",
            tone_weights={"remember": 0.8, "days": 0.6},
            resonance_score=0.6
        )
        self.assertTrue(any("remember" in echo.content 
                          for echo in self.hooks.tone_surfaces["temporal"]))
    
    def test_echo_relevance(self):
        """Test that relevant echoes are found."""
        # Add initial memory
        self.hooks.process_resonance(
            content="The stone remembers the mountain.",
            tone_weights={"stone": 0.8, "mountain": 0.7},
            resonance_score=0.75
        )
        
        # Process a related resonance
        result = self.hooks.process_resonance(
            content="The mountain remembers the stone.",
            tone_weights={"mountain": 0.8, "stone": 0.7},
            resonance_score=0.8
        )
        
        # The first echo won't find any previous echoes
        # Let's add a third related resonance to test relevance
        result = self.hooks.process_resonance(
            content="The stone and the mountain are one.",
            tone_weights={"stone": 0.9, "mountain": 0.8, "one": 0.7},
            resonance_score=0.85
        )
        
        # Should find the related echoes
        self.assertGreater(len(result["echoes"]), 0, 
                         "Expected to find relevant echoes")
        
        # Check that we have the expected number of echoes
        self.assertLessEqual(len(result["echoes"]), 3, 
                           "Should not return more than max_echoes")
    
    def test_memory_persistence(self):
        """Test that memories are persisted and loaded correctly."""
        # Create and persist a memory
        self.hooks.process_resonance(
            content="The river flows forever.",
            tone_weights={"river": 0.9, "flows": 0.7},
            resonance_score=0.8
        )
        
        # Create a new instance that should load the memory
        new_hooks = PropagationHooks(memory_path=self.test_dir)
        
        # Check that the memory was loaded
        self.assertEqual(len(new_hooks.short_term_memory), 1)
        self.assertIn("river", new_hooks.short_term_memory[0].content)
    
    def test_clear_memory(self):
        """Test that memory can be cleared."""
        self.hooks.process_resonance(
            content="Test memory.",
            tone_weights={"test": 1.0},
            resonance_score=0.9
        )
        
        self.hooks.clear_memory()
        self.assertEqual(len(self.hooks.short_term_memory), 0)
        for surface in self.hooks.tone_surfaces.values():
            self.assertEqual(len(surface), 0)

if __name__ == "__main__":
    unittest.main()

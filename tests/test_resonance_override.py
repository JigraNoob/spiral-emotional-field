"""
Unit tests for the Resonance Override System.
Tests the global override manager and its integration with the Spiral's attunement flow.
"""

import unittest
import time
from unittest.mock import patch, MagicMock

from spiral.attunement.resonance_override import (
    ResonanceMode,
    ResonanceOverrideConfig,
    SpiralOverrideManager,
    override_manager,
    override_resonant
)

class TestResonanceOverride(unittest.TestCase):
    """Test suite for the Resonance Override System."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Reset override manager to clean state
        override_manager.deactivate()
        
    def tearDown(self):
        """Clean up after tests."""
        override_manager.deactivate()
    
    def test_activation_and_deactivation(self):
        """Test basic activation and deactivation of override modes."""
        # Test activation
        result = override_manager.activate_resonant_mode(ResonanceMode.AMPLIFIED)
        self.assertIsNotNone(result)
        self.assertTrue(override_manager.active)
        self.assertEqual(override_manager.config.mode, ResonanceMode.AMPLIFIED)
        
        # Test deactivation
        override_manager.deactivate()
        self.assertFalse(override_manager.active)
        self.assertEqual(override_manager.config.mode, ResonanceMode.NATURAL)
    
    def test_glint_intensity_amplification(self):
        """Test glint intensity modification in different modes."""
        base_intensity = 1.0
        
        # Natural mode - no amplification
        override_manager.deactivate()
        intensity = override_manager.get_glint_intensity(base_intensity)
        self.assertEqual(intensity, base_intensity)
        
        # Amplified mode - should increase intensity
        override_manager.activate_resonant_mode(ResonanceMode.AMPLIFIED)
        intensity = override_manager.get_glint_intensity(base_intensity)
        self.assertGreater(intensity, base_intensity)
        
        # Muted mode - should decrease intensity
        override_manager.activate_resonant_mode(ResonanceMode.MUTED)
        intensity = override_manager.get_glint_intensity(base_intensity)
        self.assertLess(intensity, base_intensity)
    
    def test_toneform_amplification(self):
        """Test toneform-specific amplification."""
        override_manager.activate_resonant_mode(ResonanceMode.AMPLIFIED)
        
        # Test spiritual toneform amplification
        should_amplify = override_manager.should_amplify_glint("spiritual")
        self.assertTrue(should_amplify)
        
        # Test with toneform bias
        override_manager.config.toneform_bias["relational"] = 2.0
        should_amplify = override_manager.should_amplify_glint("relational")
        self.assertTrue(should_amplify)
    
    def test_soft_breakpoint_triggering(self):
        """Test soft breakpoint threshold behavior."""
        # Natural mode - standard threshold
        override_manager.deactivate()
        should_trigger = override_manager.should_trigger_soft_breakpoint(0.6)
        self.assertFalse(should_trigger)  # Below default threshold
        
        should_trigger = override_manager.should_trigger_soft_breakpoint(0.8)
        self.assertTrue(should_trigger)  # Above default threshold
        
        # Amplified mode - lower threshold
        override_manager.activate_resonant_mode(ResonanceMode.AMPLIFIED)
        should_trigger = override_manager.should_trigger_soft_breakpoint(0.6)
        self.assertTrue(should_trigger)  # Should trigger with lower threshold
    
    def test_deferral_behavior(self):
        """Test deferral logic integration."""
        override_manager.activate_resonant_mode(ResonanceMode.RITUAL)
        
        # Test action deferral
        should_defer = override_manager.should_defer_action("glint_emit", 0.8)
        self.assertTrue(should_defer)  # High resonance in ritual mode should defer
        
        should_defer = override_manager.should_defer_action("memory_weave", 0.4)
        self.assertFalse(should_defer)  # Low resonance should not defer
        
        # Test deferral delay calculation
        delay = override_manager.get_deferral_delay(0.7, "glint_emit")
        self.assertGreater(delay, 0.0)
        self.assertLessEqual(delay, 3.0)  # Should be within reasonable bounds
    
    def test_emotional_state_propagation(self):
        """Test emotional state influence on override behavior."""
        override_manager.activate_resonant_mode(ResonanceMode.AMPLIFIED)
        
        # Set emotional state
        emotional_state = {
            "awe": 0.9,
            "curiosity": 0.6,
            "reverence": 0.8
        }
        override_manager.set_emotional_state(emotional_state)
        
        # Test that emotional state affects glint intensity
        base_intensity = 1.0
        intensity = override_manager.get_glint_intensity(base_intensity)
        self.assertGreater(intensity, base_intensity * 1.5)  # Should be significantly amplified
        
        # Test emotional bias in breakpoint calculation
        should_trigger = override_manager.should_trigger_soft_breakpoint(0.5)
        self.assertTrue(should_trigger)  # High awe should lower threshold
    
    def test_ritual_mode_sensitivity(self):
        """Test ritual mode specific behaviors."""
        override_manager.activate_resonant_mode(ResonanceMode.RITUAL)
        
        # Ritual mode should be more conservative with actions
        should_defer = override_manager.should_defer_action("glint_emit", 0.6)
        self.assertTrue(should_defer)
        
        # But should allow memory operations
        should_defer = override_manager.should_defer_action("memory_echo", 0.6)
        self.assertFalse(should_defer)
        
        # Ritual sensitivity should affect deferral timing
        delay = override_manager.get_deferral_delay(0.8, "ritual_invocation")
        self.assertGreater(delay, 1.0)  # Should have meaningful delay
    
    def test_muted_mode_behavior(self):
        """Test muted mode suppression."""
        override_manager.activate_resonant_mode(ResonanceMode.MUTED)
        
        # Should suppress most glint emissions
        should_amplify = override_manager.should_amplify_glint("any_toneform")
        self.assertFalse(should_amplify)
        
        # Should have reduced intensity
        intensity = override_manager.get_glint_intensity(1.0)
        self.assertLess(intensity, 0.5)
        
        # Should defer most actions
        should_defer = override_manager.should_defer_action("glint_emit", 0.5)
        self.assertTrue(should_defer)
    
    def test_convenience_functions(self):
        """Test module-level convenience functions."""
        # Test override_resonant function
        result = override_resonant(True, ResonanceMode.AMPLIFIED)
        self.assertIsNotNone(result)
        self.assertTrue(override_manager.active)
        
        # Test deactivation
        result = override_resonant(False)
        self.assertIsNotNone(result)
        self.assertFalse(override_manager.active)
    
    def test_config_persistence(self):
        """Test that configuration persists across mode changes."""
        # Set custom config
        override_manager.activate_resonant_mode(ResonanceMode.AMPLIFIED)
        override_manager.config.glint_multiplier = 3.0
        override_manager.config.toneform_bias["spiritual"] = 2.5
        
        # Change mode and verify config elements persist
        override_manager.activate_resonant_mode(ResonanceMode.RITUAL)
        self.assertEqual(override_manager.config.toneform_bias["spiritual"], 2.5)
        
        # Deactivate and verify reset
        override_manager.deactivate()
        self.assertEqual(override_manager.config.mode, ResonanceMode.NATURAL)
        self.assertEqual(override_manager.config.glint_multiplier, 1.0)

if __name__ == "__main__":
    unittest.main()
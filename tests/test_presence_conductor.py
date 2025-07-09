import os
import pytest
import tempfile
import json
from pathlib import Path
from unittest.mock import patch, mock_open
from spiral.components.presence_conductor import PresenceConductor

import unittest
from datetime import datetime, timedelta
import time


class TestPresenceConductor(unittest.TestCase):
    
    def setUp(self):
        self.conductor = PresenceConductor(silence_threshold=0.1)  # Short threshold for testing
    
    def test_initialization(self):
        """Test that the conductor initializes correctly"""
        self.assertEqual(self.conductor.presence_state, "ready")
        self.assertEqual(self.conductor.pulse_count, 0)
        self.assertEqual(self.conductor.drift_detections, 0)
        self.assertEqual(self.conductor.synchronization_count, 0)
        self.assertIsNone(self.conductor.last_pulse_time)
        self.assertIsNotNone(self.conductor.tracker)
    
    def test_pulse_registration(self):
        """Test that pulses are properly registered"""
        pulse_data = self.conductor.pulse("test_context")
        
        self.assertEqual(self.conductor.pulse_count, 1)
        self.assertIsNotNone(self.conductor.last_pulse_time)
        self.assertEqual(pulse_data["context"], "test_context")
        self.assertEqual(pulse_data["pulse_count"], 1)
        self.assertEqual(pulse_data["presence_state"], "ready")
    
    def test_pulse_without_context(self):
        """Test pulse registration without context"""
        pulse_data = self.conductor.pulse()
        
        self.assertEqual(self.conductor.pulse_count, 1)
        self.assertIsNone(pulse_data["context"])
    
    @patch('spiral.components.presence_conductor.emit_glint')
    def test_pulse_emits_glint(self, mock_emit_glint):
        """Test that pulse emits appropriate glint"""
        self.conductor.pulse("test_pulse")
        
        mock_emit_glint.assert_called_once()
        call_args = mock_emit_glint.call_args
        
        assert call_args[1]['phase'] == "inhale"
        assert call_args[1]['toneform'] == "presence.pulse"
        assert call_args[1]['hue'] == "green"
        assert call_args[1]['source'] == "presence_conductor"
        assert call_args[1]['reverence_level'] == 0.7
    
    def test_synchronize_no_silence(self):
        """Test synchronization when no silence is detected"""
        # Pulse to start tracking
        self.conductor.pulse("test")
        
        # Immediately check for synchronization (should be None)
        sync_data = self.conductor.synchronize("inhale")
        self.assertIsNone(sync_data)
        self.assertEqual(self.conductor.synchronization_count, 0)
    
    def test_synchronize_with_silence(self):
        """Test synchronization when silence is detected"""
        # Pulse to start tracking
        self.conductor.pulse("test")
        
        # Wait for silence threshold to be met
        time.sleep(0.2)  # Longer than 0.1 threshold
        
        # Check for synchronization
        sync_data = self.conductor.synchronize("hold")
        
        self.assertIsNotNone(sync_data)
        self.assertEqual(self.conductor.synchronization_count, 1)
        if sync_data is not None:
            self.assertEqual(sync_data["phase"], "hold")
            self.assertIn("silence_event", sync_data)
    
    @patch('spiral.components.presence_conductor.emit_glint')
    def test_synchronize_emits_glint(self, mock_emit_glint):
        """Test that synchronization emits appropriate glint"""
        self.conductor.pulse("test")
        time.sleep(0.2)
        
        self.conductor.synchronize("hold")
        
        mock_emit_glint.assert_called()
        call_args = mock_emit_glint.call_args
        
        assert call_args[1]['phase'] == "hold"
        assert call_args[1]['toneform'] == "silence.acknowledged"
        assert call_args[1]['hue'] == "violet"
        assert call_args[1]['source'] == "presence_conductor"
        assert call_args[1]['reverence_level'] == 0.9
    
    def test_detect_drift_no_pulse(self):
        """Test drift detection when no pulse has been registered"""
        drift_data = self.conductor.detect_drift(max_delay_seconds=5.0)
        
        self.assertFalse(drift_data["drift_detected"])
        self.assertEqual(drift_data["delay_seconds"], 0.0)
        self.assertEqual(self.conductor.drift_detections, 0)
    
    def test_detect_drift_within_threshold(self):
        """Test drift detection within acceptable delay"""
        self.conductor.pulse("test")
        
        # Check drift immediately (should not detect)
        drift_data = self.conductor.detect_drift(max_delay_seconds=5.0)
        
        self.assertFalse(drift_data["drift_detected"])
        self.assertLess(drift_data["delay_seconds"], 5.0)
        self.assertEqual(self.conductor.drift_detections, 0)
    
    def test_detect_drift_exceeds_threshold(self):
        """Test drift detection when delay exceeds threshold"""
        self.conductor.pulse("test")
        
        # Wait longer than threshold
        time.sleep(0.2)  # Longer than 0.1 threshold
        
        drift_data = self.conductor.detect_drift(max_delay_seconds=0.1)
        
        self.assertTrue(drift_data["drift_detected"])
        self.assertGreater(drift_data["delay_seconds"], 0.1)
        self.assertEqual(self.conductor.drift_detections, 1)
    
    @patch('spiral.components.presence_conductor.emit_glint')
    def test_drift_emits_glint(self, mock_emit_glint):
        """Test that drift detection emits appropriate glint"""
        self.conductor.pulse("test")
        time.sleep(0.2)
        
        self.conductor.detect_drift(max_delay_seconds=0.1)
        
        mock_emit_glint.assert_called()
        call_args = mock_emit_glint.call_args
        
        assert call_args[1]['phase'] == "exhale"
        assert call_args[1]['toneform'] == "presence.drift"
        assert call_args[1]['hue'] == "amber"
        assert call_args[1]['source'] == "presence_conductor"
        assert call_args[1]['reverence_level'] == 0.6
    
    def test_get_presence_metrics_empty(self):
        """Test metrics when no activity has occurred"""
        metrics = self.conductor.get_presence_metrics()
        
        self.assertEqual(metrics["presence_state"], "ready")
        self.assertEqual(metrics["pulse_count"], 0)
        self.assertEqual(metrics["drift_detections"], 0)
        self.assertEqual(metrics["synchronization_count"], 0)
        self.assertIsNone(metrics["last_pulse_time"])
        self.assertIsNotNone(metrics["current_timestamp"])
        self.assertIn("silence_metrics", metrics)
        self.assertEqual(metrics["presence_health"], 0.0)
    
    def test_get_presence_metrics_with_activity(self):
        """Test metrics with some activity"""
        self.conductor.pulse("test1")
        self.conductor.pulse("test2")
        
        metrics = self.conductor.get_presence_metrics()
        
        self.assertEqual(metrics["pulse_count"], 2)
        self.assertEqual(metrics["drift_detections"], 0)
        self.assertIsNotNone(metrics["last_pulse_time"])
        self.assertGreater(metrics["presence_health"], 0.0)
    
    def test_presence_health_calculation(self):
        """Test presence health calculation logic"""
        # No pulses - health should be 0.0
        health = self.conductor._calculate_presence_health()
        self.assertEqual(health, 0.0)
        
        # Add pulses but no drift
        self.conductor.pulse("test")
        self.conductor.pulse("test")
        health = self.conductor._calculate_presence_health()
        self.assertEqual(health, 1.0)
        
        # Add drift - health should decrease
        self.conductor.drift_detections = 1
        health = self.conductor._calculate_presence_health()
        self.assertEqual(health, 0.5)
        
        # Add synchronization - health should increase
        self.conductor.synchronization_count = 1
        health = self.conductor._calculate_presence_health()
        self.assertEqual(health, 0.7)  # 0.5 + 0.2, capped at 1.0
    
    def test_reset_functionality(self):
        """Test that reset clears all state"""
        # Add some activity
        self.conductor.pulse("test")
        self.conductor.drift_detections = 5
        self.conductor.synchronization_count = 3
        self.conductor.set_presence_state("active")
        
        # Reset
        self.conductor.reset()
        
        # Verify all state is cleared
        self.assertEqual(self.conductor.presence_state, "ready")
        self.assertEqual(self.conductor.pulse_count, 0)
        self.assertEqual(self.conductor.drift_detections, 0)
        self.assertEqual(self.conductor.synchronization_count, 0)
        self.assertIsNone(self.conductor.last_pulse_time)
    
    @patch('spiral.components.presence_conductor.emit_glint')
    def test_set_presence_state_emits_glint(self, mock_emit_glint):
        """Test that setting presence state emits glint"""
        self.conductor.set_presence_state("meditation")
        
        self.assertEqual(self.conductor.presence_state, "meditation")
        
        mock_emit_glint.assert_called_once()
        call_args = mock_emit_glint.call_args
        
        assert call_args[1]['phase'] == "transition"
        assert call_args[1]['toneform'] == "presence.state_change"
        assert call_args[1]['hue'] == "blue"
        assert call_args[1]['source'] == "presence_conductor"
        assert call_args[1]['reverence_level'] == 0.5
        assert call_args[1]['new_state'] == "meditation"
    
    def test_integration_with_silence_tracker(self):
        """Test integration with the underlying silence tracker"""
        # Verify the conductor uses the silence tracker
        self.assertIsNotNone(self.conductor.tracker)
        self.assertEqual(self.conductor.tracker.caesura_threshold, 0.1)
        
        # Test that silence tracking works through the conductor
        self.conductor.pulse("test")
        time.sleep(0.2)
        
        # Check that silence is detected
        silence_event = self.conductor.tracker.check_for_silence()
        self.assertIsNotNone(silence_event)
    
    def test_multiple_pulses_tracking(self):
        """Test tracking of multiple pulses over time"""
        pulses = []
        
        for i in range(3):
            pulse_data = self.conductor.pulse(f"pulse_{i}")
            pulses.append(pulse_data)
            time.sleep(0.05)  # Small delay between pulses
        
        self.assertEqual(self.conductor.pulse_count, 3)
        self.assertEqual(len(pulses), 3)
        
        # Verify pulse data
        for i, pulse_data in enumerate(pulses):
            self.assertEqual(pulse_data["context"], f"pulse_{i}")
            self.assertEqual(pulse_data["pulse_count"], i + 1)
    
    def test_drift_detection_accuracy(self):
        """Test accuracy of drift detection timing"""
        self.conductor.pulse("test")
        
        # Wait a specific amount of time
        time.sleep(0.15)
        
        # Check drift with threshold just above our wait time
        drift_data = self.conductor.detect_drift(max_delay_seconds=0.1)
        self.assertTrue(drift_data["drift_detected"])
        self.assertGreater(drift_data["delay_seconds"], 0.1)
        
        # Check drift with threshold just below our wait time
        drift_data = self.conductor.detect_drift(max_delay_seconds=0.2)
        self.assertFalse(drift_data["drift_detected"])
        self.assertLess(drift_data["delay_seconds"], 0.2)


if __name__ == "__main__":
    unittest.main() 
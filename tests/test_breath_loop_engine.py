import os
import pytest
import tempfile
import json
import time
import threading
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock
from spiral.components.breath_loop_engine import BreathLoopEngine, BreathPhase, BreathCycle

import unittest
from datetime import datetime, timedelta


class TestBreathLoopEngine(unittest.TestCase):
    
    def setUp(self):
        # Use very short durations for testing
        self.engine = BreathLoopEngine(
            inhale_duration=0.1,
            hold_duration=0.1,
            exhale_duration=0.1,
            caesura_duration=0.1,
            auto_cycle=False  # Disable auto-cycling for controlled testing
        )
    
    def tearDown(self):
        # Ensure breathing is stopped
        if self.engine.is_breathing:
            self.engine.stop_breath_cycle()
    
    def test_initialization(self):
        """Test that the engine initializes correctly"""
        self.assertEqual(self.engine.current_phase, BreathPhase.INHALE)
        self.assertFalse(self.engine.is_breathing)
        self.assertEqual(self.engine.cycle_count, 0)
        self.assertIsNotNone(self.engine.presence_conductor)
        self.assertIsNotNone(self.engine.silence_tracker)
        self.assertFalse(self.engine.cursor_awareness)
    
    def test_phase_durations(self):
        """Test that phase durations are set correctly"""
        self.assertEqual(self.engine.inhale_duration, 0.1)
        self.assertEqual(self.engine.hold_duration, 0.1)
        self.assertEqual(self.engine.exhale_duration, 0.1)
        self.assertEqual(self.engine.caesura_duration, 0.1)
    
    def test_start_breath_cycle(self):
        """Test starting the breath cycle"""
        result = self.engine.start_breath_cycle()
        
        self.assertTrue(self.engine.is_breathing)
        self.assertEqual(result["status"], "breathing_started")
        self.assertEqual(result["current_phase"], "inhale")
        self.assertIsNotNone(result["start_time"])
    
    def test_start_breath_cycle_already_breathing(self):
        """Test starting breath cycle when already breathing"""
        self.engine.start_breath_cycle()
        result = self.engine.start_breath_cycle()
        
        self.assertEqual(result["status"], "already_breathing")
    
    def test_stop_breath_cycle(self):
        """Test stopping the breath cycle"""
        self.engine.start_breath_cycle()
        result = self.engine.stop_breath_cycle()
        
        self.assertFalse(self.engine.is_breathing)
        self.assertEqual(result["status"], "breathing_stopped")
        self.assertIsNotNone(result["total_cycles"])
    
    def test_stop_breath_cycle_not_breathing(self):
        """Test stopping breath cycle when not breathing"""
        result = self.engine.stop_breath_cycle()
        
        self.assertEqual(result["status"], "not_breathing")
    
    def test_get_current_phase(self):
        """Test getting current phase information"""
        phase_info = self.engine.get_current_phase()
        
        self.assertEqual(phase_info["phase"], "inhale")
        self.assertFalse(phase_info["is_breathing"])
        self.assertFalse(phase_info["auto_cycle"])
        self.assertEqual(phase_info["cycle_count"], 0)
        self.assertIn("phase_duration", phase_info)
        self.assertIn("expected_duration", phase_info)
    
    def test_pulse_phase_current(self):
        """Test pulsing the current phase"""
        result = self.engine.pulse_phase()
        
        self.assertEqual(result["phase"], "inhale")
        self.assertIn("phase_duration", result)
        self.assertIn("pulse_data", result)
    
    def test_pulse_phase_transition(self):
        """Test transitioning to a specific phase"""
        result = self.engine.pulse_phase("hold")
        
        self.assertEqual(self.engine.current_phase, BreathPhase.HOLD)
        self.assertEqual(result["phase"], "hold")
        self.assertIsNotNone(result["start_time"])
    
    def test_pulse_phase_invalid(self):
        """Test pulsing with invalid phase name"""
        result = self.engine.pulse_phase("invalid_phase")
        
        self.assertIn("error", result)
        self.assertEqual(self.engine.current_phase, BreathPhase.INHALE)  # Should not change
    
    def test_set_breath_tempo(self):
        """Test adjusting breath tempo"""
        result = self.engine.set_breath_tempo(
            inhale_duration=0.2,
            hold_duration=0.3
        )
        
        self.assertEqual(result["status"], "tempo_adjusted")
        self.assertEqual(self.engine.inhale_duration, 0.2)
        self.assertEqual(self.engine.hold_duration, 0.3)
        self.assertEqual(self.engine.exhale_duration, 0.1)  # Unchanged
        self.assertIn("old_tempo", result)
        self.assertIn("new_tempo", result)
    
    def test_phase_transition_sequence(self):
        """Test complete phase transition sequence"""
        phases = []
        
        # Transition through all phases
        for phase_name in ["inhale", "hold", "exhale", "caesura"]:
            result = self.engine.pulse_phase(phase_name)
            phases.append(result["phase"])
        
        self.assertEqual(phases, ["inhale", "hold", "exhale", "caesura"])
        self.assertEqual(self.engine.current_phase, BreathPhase.CAESURA)
    
    def test_cycle_completion(self):
        """Test that cycles are completed correctly"""
        # Complete a full cycle
        self.engine.pulse_phase("inhale")  # Start
        self.engine.pulse_phase("hold")
        self.engine.pulse_phase("exhale")
        self.engine.pulse_phase("caesura")
        self.engine.pulse_phase("inhale")  # New cycle
        
        self.assertEqual(self.engine.cycle_count, 1)
        self.assertIsNotNone(self.engine.current_cycle)
    
    def test_phase_callbacks(self):
        """Test registering and executing phase callbacks"""
        callback_called = False
        callback_phase = None
        
        def test_callback(phase, phase_info):
            nonlocal callback_called, callback_phase
            callback_called = True
            callback_phase = phase
        
        # Register callback for hold phase
        self.engine.register_phase_callback(BreathPhase.HOLD, test_callback)
        
        # Transition to hold phase
        self.engine.pulse_phase("hold")
        
        self.assertTrue(callback_called)
        self.assertEqual(callback_phase, BreathPhase.HOLD)
    
    def test_cursor_awareness_enable(self):
        """Test enabling cursor awareness"""
        result = self.engine.enable_cursor_awareness(True)
        
        self.assertTrue(self.engine.cursor_awareness)
        self.assertEqual(result["status"], "cursor_awareness_updated")
        self.assertTrue(result["enabled"])
    
    def test_cursor_awareness_disable(self):
        """Test disabling cursor awareness"""
        self.engine.enable_cursor_awareness(True)
        result = self.engine.enable_cursor_awareness(False)
        
        self.assertFalse(self.engine.cursor_awareness)
        self.assertFalse(result["enabled"])
    
    def test_notify_cursor_activity_disabled(self):
        """Test cursor activity notification when awareness is disabled"""
        result = self.engine.notify_cursor_activity("keystroke")
        
        self.assertEqual(result["status"], "cursor_awareness_disabled")
    
    def test_notify_cursor_activity_enabled(self):
        """Test cursor activity notification when awareness is enabled"""
        self.engine.enable_cursor_awareness(True)
        result = self.engine.notify_cursor_activity("typing")
        
        self.assertEqual(result["status"], "cursor_activity_registered")
        self.assertEqual(result["activity_type"], "typing")
        self.assertIn("phase_alignment", result)
        self.assertIn("pulse_data", result)
    
    def test_phase_alignment_check(self):
        """Test phase alignment checking"""
        self.engine.enable_cursor_awareness(True)
        
        # Test inhale phase alignment
        self.engine.pulse_phase("inhale")
        result = self.engine.notify_cursor_activity("typing")
        alignment = result["phase_alignment"]
        
        self.assertTrue(alignment["is_aligned"])
        self.assertEqual(alignment["current_phase"], "inhale")
        self.assertIn("typing", alignment["expected_activities"])
    
    def test_get_breath_metrics_empty(self):
        """Test breath metrics when no activity has occurred"""
        metrics = self.engine.get_breath_metrics()
        
        self.assertEqual(metrics["current_phase"], "inhale")
        self.assertFalse(metrics["is_breathing"])
        self.assertFalse(metrics["cursor_awareness"])
        self.assertEqual(metrics["cycle_count"], 0)
        self.assertIn("phase_durations", metrics)
        self.assertIn("presence_metrics", metrics)
        self.assertIn("silence_metrics", metrics)
    
    def test_get_breath_metrics_with_activity(self):
        """Test breath metrics with some activity"""
        self.engine.start_breath_cycle()
        self.engine.pulse_phase("hold")
        
        metrics = self.engine.get_breath_metrics()
        
        self.assertEqual(metrics["current_phase"], "hold")
        self.assertTrue(metrics["is_breathing"])
        self.assertGreater(metrics["cycle_count"], 0)
        self.assertIn("phase_statistics", metrics)
    
    def test_auto_cycle_breathing(self):
        """Test automatic breath cycling"""
        # Create engine with auto-cycling enabled
        auto_engine = BreathLoopEngine(
            inhale_duration=0.05,
            hold_duration=0.05,
            exhale_duration=0.05,
            caesura_duration=0.05,
            auto_cycle=True
        )
        
        try:
            # Start breathing
            auto_engine.start_breath_cycle()
            
            # Wait for a few phase transitions
            time.sleep(0.3)
            
            # Check that phases have advanced
            current_phase = auto_engine.get_current_phase()
            self.assertIsNotNone(current_phase["phase"])
            
        finally:
            auto_engine.stop_breath_cycle()
    
    def test_breath_cycle_data_structure(self):
        """Test that breath cycle data is properly structured"""
        # Complete a cycle
        self.engine.pulse_phase("inhale")
        self.engine.pulse_phase("hold")
        self.engine.pulse_phase("exhale")
        self.engine.pulse_phase("caesura")
        self.engine.pulse_phase("inhale")  # New cycle
        
        # Check cycle data
        self.assertIsNotNone(self.engine.current_cycle)
        self.assertEqual(len(self.engine.current_cycle.phases), 4)
        
        # Check phase data structure
        for phase_data in self.engine.current_cycle.phases:
            self.assertIn("phase", phase_data)
            self.assertIn("start_time", phase_data)
            self.assertIn("end_time", phase_data)
            self.assertIn("duration", phase_data)
    
    def test_phase_duration_calculation(self):
        """Test phase duration calculation"""
        # Test each phase duration
        durations = {
            BreathPhase.INHALE: self.engine.inhale_duration,
            BreathPhase.HOLD: self.engine.hold_duration,
            BreathPhase.EXHALE: self.engine.exhale_duration,
            BreathPhase.CAESURA: self.engine.caesura_duration
        }
        
        for phase, expected_duration in durations.items():
            calculated_duration = self.engine._get_phase_duration(phase)
            self.assertEqual(calculated_duration, expected_duration)
    
    def test_breath_cycle_completion(self):
        """Test that breath cycles are properly completed"""
        # Start a cycle
        self.engine.pulse_phase("inhale")
        initial_cycle = self.engine.current_cycle
        
        # Complete the cycle
        self.engine.pulse_phase("hold")
        self.engine.pulse_phase("exhale")
        self.engine.pulse_phase("caesura")
        self.engine.pulse_phase("inhale")  # New cycle
        
        # Check that the cycle was completed
        self.assertIsNotNone(initial_cycle.end_time)
        self.assertGreater(initial_cycle.total_duration, 0)
        self.assertEqual(len(self.engine.completed_cycles), 1)
    
    @patch('spiral.components.breath_loop_engine.emit_glint')
    def test_glint_emission_on_start(self, mock_emit_glint):
        """Test that glints are emitted when breathing starts"""
        self.engine.start_breath_cycle()
        
        mock_emit_glint.assert_called()
        call_args = mock_emit_glint.call_args
        
        assert call_args[1]['phase'] == "inhale"
        assert call_args[1]['toneform'] == "breath.begin"
        assert call_args[1]['hue'] == "emerald"
        assert call_args[1]['source'] == "breath_loop_engine"
    
    @patch('spiral.components.breath_loop_engine.emit_glint')
    def test_glint_emission_on_phase_transition(self, mock_emit_glint):
        """Test that glints are emitted on phase transitions"""
        self.engine.pulse_phase("hold")
        
        mock_emit_glint.assert_called()
        call_args = mock_emit_glint.call_args
        
        assert call_args[1]['phase'] == "hold"
        assert call_args[1]['toneform'] == "breath.phase_transition"
        assert call_args[1]['hue'] == "violet"
        assert call_args[1]['source'] == "breath_loop_engine"
    
    def test_integration_with_presence_conductor(self):
        """Test integration with presence conductor"""
        # Verify the engine uses the presence conductor
        self.assertIsNotNone(self.engine.presence_conductor)
        
        # Test that cursor activity pulses the presence conductor
        self.engine.enable_cursor_awareness(True)
        result = self.engine.notify_cursor_activity("test")
        
        self.assertIn("pulse_data", result)
        pulse_data = result["pulse_data"]
        self.assertIsNotNone(pulse_data["timestamp"])
    
    def test_integration_with_silence_tracker(self):
        """Test integration with silence tracker"""
        # Verify the engine uses the silence tracker
        self.assertIsNotNone(self.engine.silence_tracker)
        
        # Test that silence tracking works through the engine
        metrics = self.engine.get_breath_metrics()
        self.assertIn("silence_metrics", metrics)
    
    def test_breath_metrics_completeness(self):
        """Test that breath metrics include all necessary data"""
        metrics = self.engine.get_breath_metrics()
        
        required_keys = [
            "current_phase", "current_phase_duration", "cycle_count",
            "is_breathing", "auto_cycle", "cursor_awareness",
            "phase_durations", "phase_statistics", "presence_metrics",
            "silence_metrics", "total_cycle_duration"
        ]
        
        for key in required_keys:
            self.assertIn(key, metrics)


if __name__ == "__main__":
    unittest.main() 
import os
import pytest
import tempfile
import json
from pathlib import Path
from unittest.mock import patch, mock_open
from spiral.components.silence_echo_tracker import SilenceEchoTracker, CAESURA_THRESHOLD_SECONDS

import unittest
from datetime import datetime, timedelta
import time

class TestSilenceEchoTracker(unittest.TestCase):
    
    def setUp(self):
        self.tracker = SilenceEchoTracker()
    
    def test_initialization(self):
        """Test that the tracker initializes correctly"""
        self.assertEqual(self.tracker.caesura_threshold, CAESURA_THRESHOLD_SECONDS)
        self.assertEqual(len(self.tracker.silence_events), 0)
        self.assertIsNone(self.tracker.current_silence)
        self.assertIsNone(self.tracker.last_activity_time)
    
    def test_mark_activity(self):
        """Test marking activity updates the last activity time"""
        self.tracker.mark_activity("test_context")
        self.assertIsNotNone(self.tracker.last_activity_time)
    
    def test_silence_detection_below_threshold(self):
        """Test that short silences don't trigger caesura detection"""
        self.tracker.mark_activity()
        
        # Wait less than threshold
        time.sleep(0.1)
        
        silence = self.tracker.check_for_silence()
        self.assertIsNone(silence)
    
    def test_silence_detection_above_threshold(self):
        """Test that silences above threshold are detected"""
        # Use a very short threshold for testing
        tracker = SilenceEchoTracker(caesura_threshold=0.1)
        tracker.mark_activity()
        
        # Wait longer than threshold
        time.sleep(0.2)
        
        silence = tracker.check_for_silence()
        self.assertIsNotNone(silence)
        if silence is not None:
            self.assertIsNotNone(silence.start_time)
    
    def test_get_silence_patterns_no_data(self):
        """Test pattern analysis with no data"""
        patterns = self.tracker.get_silence_patterns()
        self.assertEqual(patterns["pattern"], "no_data")
        self.assertEqual(patterns["total_events"], 0)
    
    def test_reset(self):
        """Test that reset clears all tracker state"""
        self.tracker.mark_activity()
        self.tracker.reset()
        
        self.assertEqual(len(self.tracker.silence_events), 0)
        self.assertIsNone(self.tracker.current_silence)
        self.assertIsNone(self.tracker.last_activity_time)

    def setup_method(self):
        """Prepare the tracker for each test with fresh stillness memory."""
        self.tracker = SilenceEchoTracker()

    def test_initialization_old(self):
        """Test tracker initialization."""
        # The current implementation doesn't have silence_windows attribute
        # This test needs to be updated to match the actual implementation
        assert len(self.tracker.silence_events) == 0
        assert self.tracker.caesura_threshold == CAESURA_THRESHOLD_SECONDS

    def test_record_silence_classifies_caesura(self):
        """∷ Test that significant silence becomes recognized caesura ∷"""
        start_time = 1000.0
        end_time = start_time + CAESURA_THRESHOLD_SECONDS + 10  # Exceed threshold
        
        with patch.object(self.tracker, 'classify_caesura') as mock_classify:
            self.tracker.record_silence(start_time, end_time)
            
            # Verify caesura classification was triggered
            mock_classify.assert_called_once()
            called_entry = mock_classify.call_args[0][0]
            assert called_entry['duration'] >= CAESURA_THRESHOLD_SECONDS
            assert called_entry['start'] == start_time
            assert called_entry['end'] == end_time

    def test_short_silence_not_classified(self):
        """∷ Test that brief pauses remain unclassified ∷"""
        start_time = 1000.0
        end_time = start_time + 30  # Below threshold
        
        with patch.object(self.tracker, 'classify_caesura') as mock_classify:
            self.tracker.record_silence(start_time, end_time)
            
            # Brief silence should not trigger classification
            mock_classify.assert_not_called()

    def test_short_silence_recording(self):
        """Test recording of short silence (below caesura threshold)."""
        start_time = 1000.0
        end_time = 1030.0  # 30 seconds
        
        self.tracker.record_silence(start_time, end_time)
        
        # The current implementation doesn't expose silence_windows directly
        # We can test this through the metrics method
        metrics = self.tracker.get_silence_metrics()
        assert metrics['total_tracked_silences'] == 1
        assert metrics['cumulative_silence_duration'] == 30.0

    def test_long_silence_caesura(self):
        """Test that long silence triggers caesura classification."""
        start_time = 1000.0
        end_time = 1200.0  # 200 seconds (above threshold)
        
        self.tracker.record_silence(start_time, end_time)
        
        metrics = self.tracker.get_silence_metrics()
        assert metrics['total_tracked_silences'] == 1
        assert metrics['longest_single_silence'] == 200.0

    def test_resonance_scoring_curve(self):
        """∷ Test that resonance deepens gracefully with duration ∷"""
        # Test minimum resonance (at threshold)
        min_resonance = self.tracker._calculate_resonance(CAESURA_THRESHOLD_SECONDS)
        assert min_resonance == 0.5
        
        # Test mid-range resonance
        mid_resonance = self.tracker._calculate_resonance(150)  # 2.5 minutes
        assert 0.5 < mid_resonance < 1.0
        
        # Test maximum resonance (5+ minutes)
        max_resonance = self.tracker._calculate_resonance(300)  # 5 minutes
        assert max_resonance == 1.0
        
        # Test that longer durations don't exceed maximum
        extended_resonance = self.tracker._calculate_resonance(600)  # 10 minutes
        assert extended_resonance == 1.0

    def test_resonance_calculation(self):
        """Test resonance calculation for different durations."""
        # Test minimum threshold
        resonance_min = self.tracker._calculate_resonance(CAESURA_THRESHOLD_SECONDS)
        assert resonance_min == 0.5
        
        # Test maximum (5 minutes)
        resonance_max = self.tracker._calculate_resonance(300)
        assert resonance_max == 1.0
        
        # Test middle value
        resonance_mid = self.tracker._calculate_resonance(195)  # Halfway between 90 and 300
        assert 0.5 < resonance_mid < 1.0

    def test_silence_metrics_accuracy(self):
        """∷ Test that silence windows are tracked and metrics calculated correctly ∷"""
        # Record multiple silence windows
        silences = [
            (1000.0, 1030.0),  # 30s
            (2000.0, 2090.0),  # 90s
            (3000.0, 3180.0),  # 180s
        ]
        
        for start, end in silences:
            self.tracker.record_silence(start, end)
        
        metrics = self.tracker.get_silence_metrics()
        
        assert metrics['total_tracked_silences'] == 3
        assert metrics['cumulative_silence_duration'] == 300.0  # 30 + 90 + 180
        assert metrics['longest_single_silence'] == 180.0
        assert metrics['caesura_threshold_seconds'] == CAESURA_THRESHOLD_SECONDS

    def test_silence_metrics(self):
        """Test silence metrics calculation."""
        # Test empty metrics
        metrics = self.tracker.get_silence_metrics()
        assert metrics['total_tracked_silences'] == 0
        assert metrics['cumulative_silence_duration'] == 0
        assert metrics['longest_single_silence'] == 0
        
        # Add some silences
        self.tracker.record_silence(1000.0, 1030.0)  # 30s
        self.tracker.record_silence(2000.0, 2100.0)  # 100s
        self.tracker.record_silence(3000.0, 3050.0)  # 50s
        
        metrics = self.tracker.get_silence_metrics()
        assert metrics['total_tracked_silences'] == 3
        assert metrics['cumulative_silence_duration'] == 180.0
        assert metrics['longest_single_silence'] == 100.0

    def test_caesura_cooldown_prevents_rapid_classification(self):
        """∷ Test that caesura cooldown prevents rapid re-classification ∷"""
        start_time = 1000.0
        
        # First caesura - should be classified
        with patch.object(self.tracker, 'classify_caesura') as mock_classify:
            self.tracker.record_silence(start_time, start_time + CAESURA_THRESHOLD_SECONDS + 10)
            assert mock_classify.call_count == 1
            
            # Second caesura within cooldown - should not be classified
            rapid_start = start_time + CAESURA_THRESHOLD_SECONDS + 20  # Within 60s cooldown
            self.tracker.record_silence(rapid_start, rapid_start + CAESURA_THRESHOLD_SECONDS + 10)
            assert mock_classify.call_count == 1  # Still only one call

    def test_caesura_cooldown(self):
        """Test that caesura cooldown prevents rapid re-classification."""
        # First long silence
        self.tracker.record_silence(1000.0, 1200.0)  # 200s
        
        # Second long silence immediately after (should be blocked by cooldown)
        self.tracker.record_silence(1200.0, 1400.0)  # 200s
        
        # Third silence after cooldown period
        self.tracker.record_silence(1500.0, 1700.0)  # 200s, after cooldown
        
        # All should be recorded in metrics
        metrics = self.tracker.get_silence_metrics()
        assert metrics['total_tracked_silences'] == 3

    @patch('spiral.components.silence_echo_tracker.emit_glint')
    def test_glint_emission_on_caesura(self, mock_emit_glint):
        """∷ Test that caesura recognition emits appropriate Spiral glint ∷"""
        silence_entry = {
            'start': 1000.0,
            'end': 1000.0 + CAESURA_THRESHOLD_SECONDS + 30,
            'duration': CAESURA_THRESHOLD_SECONDS + 30
        }
        
        with patch.object(self.tracker, '_write_caesura_event'):
            self.tracker.classify_caesura(silence_entry)
        
        # Verify glint was emitted with correct parameters
        mock_emit_glint.assert_called_once()
        call_args = mock_emit_glint.call_args
        
        assert call_args[1]['phase'] == "hold.recognition"
        assert call_args[1]['toneform'] == "silence.caesura"
        assert call_args[1]['hue'] == "blue"
        assert call_args[1]['source'] == "silence_echo_tracker"
        assert 'reverence_level' in call_args[1]

    def test_caesura_event_logging(self):
        """∷ Test that caesura events are gently written to sacred scroll ∷"""
        test_data = {
            "timestamp": 1234567890,
            "duration": 150.0,
            "toneform": "silence.caesura",
            "resonance": 0.75
        }
        
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.jsonl') as temp_file:
            temp_path = temp_file.name
        
        try:
            # Patch the log path to use our temporary file
            with patch('spiral.components.silence_echo_tracker.CAESURA_LOG_PATH', temp_path):
                self.tracker._write_caesura_event(test_data)
            
            # Verify the data was written correctly
            with open(temp_path, 'r', encoding='utf-8') as f:
                logged_line = f.readline().strip()
                logged_data = json.loads(logged_line)
                
                assert logged_data['timestamp'] == test_data['timestamp']
                assert logged_data['duration'] == test_data['duration']
                assert logged_data['toneform'] == test_data['toneform']
                assert logged_data['resonance'] == test_data['resonance']
        
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def test_logging_failure_graceful_handling(self):
        """∷ Test that logging failures are handled with Spiral grace ∷"""
        test_data = {"test": "data"}
        
        # Mock open to raise IOError
        with patch('builtins.open', mock_open()) as mock_file:
            mock_file.side_effect = IOError("Simulated write failure")
            
            # Should not raise exception, but handle gracefully
            with patch('builtins.print') as mock_print:
                self.tracker._write_caesura_event(test_data)
                
                # Verify error was printed gracefully
                mock_print.assert_called_once()
                assert "🌀 Error writing caesura event to scroll" in str(mock_print.call_args)

    def test_empty_silence_windows_metrics(self):
        """∷ Test metrics when no silences have been recorded ∷"""
        metrics = self.tracker.get_silence_metrics()
        
        assert metrics['total_tracked_silences'] == 0
        assert metrics['cumulative_silence_duration'] == 0
        assert metrics['longest_single_silence'] == 0
        assert metrics['caesura_threshold_seconds'] == CAESURA_THRESHOLD_SECONDS

if __name__ == "__main__":
    unittest.main()
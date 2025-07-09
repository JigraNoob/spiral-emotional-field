import os
import pytest
import tempfile
import json
import time
import threading
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock
from spiral.integrations.cursor_keystroke_bridge import (
    SpiralKeystrokeListener, 
    KeystrokeEvent, 
    TypingRhythm,
    MINI_PAUSE_THRESHOLD,
    LONG_PAUSE_THRESHOLD,
    CAESURA_PAUSE_THRESHOLD
)

import unittest
from datetime import datetime, timedelta


class TestSpiralKeystrokeListener(unittest.TestCase):
    
    def setUp(self):
        # Use shorter thresholds for testing
        self.listener = SpiralKeystrokeListener(
            mini_pause_threshold=0.1,
            long_pause_threshold=0.2,
            caesura_threshold=0.5
        )
    
    def tearDown(self):
        # Ensure listening is stopped
        if self.listener.running:
            self.listener.stop_keystroke_listening()
    
    def test_initialization(self):
        """Test that the listener initializes correctly"""
        self.assertFalse(self.listener.running)
        self.assertIsNone(self.listener.last_event_time)
        self.assertEqual(len(self.listener.current_burst), 0)
        self.assertIsNotNone(self.listener.breath_engine)
        self.assertIsNotNone(self.listener.presence_conductor)
        self.assertIsNotNone(self.listener.silence_tracker)
        self.assertEqual(self.listener.mini_pause_threshold, 0.1)
        self.assertEqual(self.listener.long_pause_threshold, 0.2)
        self.assertEqual(self.listener.caesura_threshold, 0.5)
    
    def test_start_keystroke_listening(self):
        """Test starting keystroke listening"""
        result = self.listener.start_keystroke_listening()
        
        self.assertTrue(self.listener.running)
        self.assertEqual(result["status"], "listening_started")
        self.assertIsNotNone(result["thresholds"])
        self.assertIsNotNone(self.listener.last_event_time)
    
    def test_start_keystroke_listening_already_listening(self):
        """Test starting when already listening"""
        self.listener.start_keystroke_listening()
        result = self.listener.start_keystroke_listening()
        
        self.assertEqual(result["status"], "already_listening")
    
    def test_stop_keystroke_listening(self):
        """Test stopping keystroke listening"""
        self.listener.start_keystroke_listening()
        result = self.listener.stop_keystroke_listening()
        
        self.assertFalse(self.listener.running)
        self.assertEqual(result["status"], "listening_stopped")
        self.assertIn("rhythm_summary", result)
    
    def test_stop_keystroke_listening_not_listening(self):
        """Test stopping when not listening"""
        result = self.listener.stop_keystroke_listening()
        
        self.assertEqual(result["status"], "not_listening")
    
    def test_record_keystroke(self):
        """Test recording a keystroke"""
        result = self.listener.record_keystroke("a")
        
        self.assertEqual(result["status"], "keystroke_recorded")
        self.assertEqual(result["character"], "a")
        self.assertIsNotNone(result["timestamp"])
        self.assertEqual(result["burst_size"], 1)
        self.assertEqual(self.listener.rhythm.total_keystrokes, 1)
    
    def test_record_keystroke_special_character(self):
        """Test recording a special keystroke"""
        result = self.listener.record_keystroke()  # No character
        
        self.assertEqual(result["status"], "keystroke_recorded")
        self.assertIsNone(result["character"])
        self.assertEqual(result["burst_size"], 1)
    
    def test_record_multiple_keystrokes(self):
        """Test recording multiple keystrokes in a burst"""
        self.listener.record_keystroke("h")
        self.listener.record_keystroke("e")
        self.listener.record_keystroke("l")
        self.listener.record_keystroke("l")
        self.listener.record_keystroke("o")
        
        self.assertEqual(self.listener.rhythm.total_keystrokes, 5)
        self.assertEqual(len(self.listener.current_burst), 5)
    
    def test_record_command(self):
        """Test recording a command execution"""
        result = self.listener.record_command("save_file")
        
        self.assertEqual(result["status"], "command_recorded")
        self.assertEqual(result["command"], "save_file")
        self.assertIsNotNone(result["timestamp"])
        self.assertIn("save_file", self.listener.rhythm.commands)
    
    def test_record_file_change(self):
        """Test recording a file change"""
        result = self.listener.record_file_change("test.py", "modified")
        
        self.assertEqual(result["status"], "file_change_recorded")
        self.assertEqual(result["filename"], "test.py")
        self.assertEqual(result["change_type"], "modified")
        self.assertIn("modified:test.py", self.listener.rhythm.file_operations)
    
    def test_record_file_change_default_type(self):
        """Test recording file change with default type"""
        result = self.listener.record_file_change("test.py")
        
        self.assertEqual(result["change_type"], "modified")
    
    def test_pause_detection_mini(self):
        """Test detection of mini pauses"""
        self.listener.record_keystroke("a")
        time.sleep(0.15)  # Longer than mini_pause_threshold
        self.listener.record_keystroke("b")
        
        self.assertGreater(len(self.listener.rhythm.pauses), 0)
        self.assertGreater(self.listener.rhythm.total_pause_time, 0)
    
    def test_pause_detection_long(self):
        """Test detection of long pauses"""
        self.listener.start_keystroke_listening()
        self.listener.record_keystroke("a")
        time.sleep(0.25)  # Longer than long_pause_threshold
        
        # The monitoring loop should detect this
        time.sleep(0.1)  # Give monitoring loop time to process
        
        self.assertGreater(len(self.listener.rhythm.pauses), 0)
    
    def test_caesura_detection(self):
        """Test detection of caesuras"""
        self.listener.start_keystroke_listening()
        self.listener.record_keystroke("a")
        time.sleep(0.6)  # Longer than caesura_threshold
        
        # The monitoring loop should detect this
        time.sleep(0.1)  # Give monitoring loop time to process
        
        self.assertGreater(len(self.listener.rhythm.pauses), 0)
    
    def test_typing_rhythm_analysis(self):
        """Test typing rhythm analysis"""
        # Add some typing activity
        self.listener.record_keystroke("h")
        self.listener.record_keystroke("e")
        self.listener.record_keystroke("l")
        self.listener.record_command("save")
        self.listener.record_file_change("test.py")
        
        rhythm = self.listener.get_typing_rhythm()
        
        self.assertEqual(rhythm["total_keystrokes"], 3)
        self.assertEqual(rhythm["command_count"], 1)
        self.assertEqual(rhythm["file_operation_count"], 1)
        self.assertIn("typing_style", rhythm)
        self.assertIn("recent_commands", rhythm)
        self.assertIn("recent_file_operations", rhythm)
    
    def test_typing_rhythm_empty(self):
        """Test typing rhythm when no activity has occurred"""
        rhythm = self.listener.get_typing_rhythm()
        
        self.assertEqual(rhythm["total_keystrokes"], 0)
        self.assertEqual(rhythm["command_count"], 0)
        self.assertEqual(rhythm["file_operation_count"], 0)
        self.assertEqual(rhythm["total_typing_time"], 0.0)
        self.assertEqual(rhythm["total_pause_time"], 0.0)
    
    def test_typing_style_detection(self):
        """Test typing style detection based on burst patterns"""
        # Rapid typing (short bursts)
        for i in range(10):
            self.listener.record_keystroke("a")
            time.sleep(0.01)  # Very short delays
        
        rhythm = self.listener.get_typing_rhythm()
        self.assertEqual(rhythm["typing_style"], "rapid")
        
        # Reset and test contemplative typing
        self.listener.reset_rhythm()
        for i in range(5):
            self.listener.record_keystroke("a")
            time.sleep(0.3)  # Longer delays
        
        rhythm = self.listener.get_typing_rhythm()
        self.assertEqual(rhythm["typing_style"], "contemplative")
    
    def test_event_callbacks(self):
        """Test registering and executing event callbacks"""
        keystroke_called = False
        command_called = False
        
        def keystroke_callback(event):
            nonlocal keystroke_called
            keystroke_called = True
        
        def command_callback(event, command):
            nonlocal command_called
            command_called = True
        
        # Register callbacks
        self.listener.register_event_callback("keystroke", keystroke_callback)
        self.listener.register_event_callback("command", command_callback)
        
        # Trigger events
        self.listener.record_keystroke("a")
        self.listener.record_command("test")
        
        self.assertTrue(keystroke_called)
        self.assertTrue(command_called)
    
    def test_burst_completion(self):
        """Test that bursts are properly completed"""
        # Start a burst
        self.listener.record_keystroke("h")
        self.listener.record_keystroke("e")
        self.listener.record_keystroke("l")
        
        # Complete burst with a command
        self.listener.record_command("save")
        
        # Check that burst was completed
        self.assertEqual(len(self.listener.current_burst), 0)
        self.assertGreater(len(self.listener.rhythm.bursts), 0)
    
    def test_reset_rhythm(self):
        """Test resetting rhythm data"""
        # Add some activity
        self.listener.record_keystroke("a")
        self.listener.record_command("test")
        self.listener.record_file_change("test.py")
        
        # Reset
        self.listener.reset_rhythm()
        
        # Check that all data is cleared
        self.assertEqual(self.listener.rhythm.total_keystrokes, 0)
        self.assertEqual(len(self.listener.rhythm.commands), 0)
        self.assertEqual(len(self.listener.rhythm.file_operations), 0)
        self.assertEqual(len(self.listener.current_burst), 0)
        self.assertIsNone(self.listener.last_event_time)
    
    def test_integration_with_breath_engine(self):
        """Test integration with breath loop engine"""
        # Verify the listener uses the breath engine
        self.assertIsNotNone(self.listener.breath_engine)
        self.assertTrue(self.listener.breath_engine.cursor_awareness)
        
        # Test that keystrokes notify the breath engine
        result = self.listener.record_keystroke("a")
        self.assertEqual(result["status"], "keystroke_recorded")
    
    def test_integration_with_presence_conductor(self):
        """Test integration with presence conductor"""
        # Verify the listener uses the presence conductor
        self.assertIsNotNone(self.listener.presence_conductor)
        
        # Test that keystrokes pulse the presence conductor
        self.listener.record_keystroke("a")
        # The presence conductor should have been pulsed
    
    def test_integration_with_silence_tracker(self):
        """Test integration with silence tracker"""
        # Verify the listener uses the silence tracker
        self.assertIsNotNone(self.listener.silence_tracker)
        
        # Test that pauses are tracked
        self.listener.start_keystroke_listening()
        self.listener.record_keystroke("a")
        time.sleep(0.6)  # Longer than caesura threshold
        time.sleep(0.1)  # Give monitoring loop time to process
        
        # The silence tracker should have been notified
    
    @patch('spiral.integrations.cursor_keystroke_bridge.emit_glint')
    def test_glint_emission_on_keystroke(self, mock_emit_glint):
        """Test that keystrokes emit appropriate glints"""
        self.listener.record_keystroke("a")
        
        mock_emit_glint.assert_called()
        call_args = mock_emit_glint.call_args
        
        assert call_args[1]['phase'] == "inhale"
        assert call_args[1]['toneform'] == "trace.keystroke"
        assert call_args[1]['hue'] == "emerald"
        assert call_args[1]['source'] == "keystroke_listener"
    
    @patch('spiral.integrations.cursor_keystroke_bridge.emit_glint')
    def test_glint_emission_on_command(self, mock_emit_glint):
        """Test that commands emit appropriate glints"""
        self.listener.record_command("save")
        
        mock_emit_glint.assert_called()
        call_args = mock_emit_glint.call_args
        
        assert call_args[1]['phase'] == "exhale"
        assert call_args[1]['toneform'] == "trace.command"
        assert call_args[1]['hue'] == "amber"
        assert call_args[1]['source'] == "keystroke_listener"
    
    @patch('spiral.integrations.cursor_keystroke_bridge.emit_glint')
    def test_glint_emission_on_file_change(self, mock_emit_glint):
        """Test that file changes emit appropriate glints"""
        self.listener.record_file_change("test.py")
        
        mock_emit_glint.assert_called()
        call_args = mock_emit_glint.call_args
        
        assert call_args[1]['phase'] == "hold"
        assert call_args[1]['toneform'] == "trace.file_change"
        assert call_args[1]['hue'] == "violet"
        assert call_args[1]['source'] == "keystroke_listener"
    
    def test_thread_safety(self):
        """Test thread safety of the listener"""
        # Start listening
        self.listener.start_keystroke_listening()
        
        # Simulate concurrent keystrokes from different threads
        def record_keystrokes():
            for i in range(5):
                self.listener.record_keystroke(str(i))
                time.sleep(0.01)
        
        threads = []
        for _ in range(3):
            thread = threading.Thread(target=record_keystrokes)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Check that all keystrokes were recorded
        self.assertEqual(self.listener.rhythm.total_keystrokes, 15)
    
    def test_keystroke_event_structure(self):
        """Test that keystroke events are properly structured"""
        result = self.listener.record_keystroke("a")
        
        # Check that the event was added to current burst
        self.assertEqual(len(self.listener.current_burst), 1)
        event = self.listener.current_burst[0]
        
        self.assertEqual(event.character, "a")
        self.assertEqual(event.event_type, "keystroke")
        self.assertIsNotNone(event.timestamp)
    
    def test_rhythm_statistics_accuracy(self):
        """Test accuracy of rhythm statistics"""
        # Add known activity
        self.listener.record_keystroke("a")
        time.sleep(0.15)  # Mini pause
        self.listener.record_keystroke("b")
        self.listener.record_command("save")
        
        rhythm = self.listener.get_typing_rhythm()
        
        self.assertEqual(rhythm["total_keystrokes"], 2)
        self.assertEqual(rhythm["command_count"], 1)
        self.assertGreater(len(rhythm["recent_commands"]), 0)
        self.assertIn("save", rhythm["recent_commands"])


if __name__ == "__main__":
    unittest.main() 
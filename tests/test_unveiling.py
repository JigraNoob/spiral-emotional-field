"""
Tests for the ΔUNVEILING.∞ toneform integration in the Whisper Steward.
"""
import os
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
import unittest
from unittest.mock import patch, MagicMock

# Add the parent directory to the Python path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from assistant.core_toneforms.unveiling import (
    return_to_presence,
    close_softly,
    log_memory_glyph,
    UNVEILING_LOG
)
from assistant.whisper_steward import WhisperSteward, DialogueState

class TestUnveilingToneform(unittest.TestCase):
    """Test suite for ΔUNVEILING.∞ toneform integration."""
    
    def setUp(self):
        """Set up test environment."""
        # Create a test log directory
        self.test_log_dir = Path("test_whispers")
        self.test_log_dir.mkdir(parents=True, exist_ok=True)
        
        # Set up test log path
        self.test_log_path = self.test_log_dir / "unveiling_log.jsonl"
        
        # Patch the UNVEILING_LOG constant and ensure directory exists
        self.patcher = patch('assistant.core_toneforms.unveiling.UNVEILING_LOG', 
                           str(self.test_log_path.absolute()))
        self.patcher.start()
        
        # Ensure the directory exists
        self.test_log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Clear any existing log file
        if self.test_log_path.exists():
            os.remove(self.test_log_path)
        
        # Create a test whisper steward with a short scan interval
        self.steward = WhisperSteward(scan_interval=1)
        
        # Add missing _log_whisper method for testing
        self.steward._log_whisper = lambda whisper: None
        
        # Set up a mock whisper handler
        self.whispers = []
        def capture_whisper(whisper):
            self.whispers.append(whisper)
        self.steward.register_whisper_handler(capture_whisper)
        
    def tearDown(self):
        """Clean up after tests."""
        # Stop the patcher first
        self.patcher.stop()
        
        # Allow some time for file handles to be released
        import time
        time.sleep(0.1)
        
        # Clean up test files with retry logic
        if self.test_log_dir.exists():
            max_attempts = 5
            for attempt in range(max_attempts):
                try:
                    # Try to remove all files first
                    for file in self.test_log_dir.glob("*"):
                        try:
                            if file.is_file():
                                file.unlink()
                        except Exception as e:
                            print(f"Warning: Could not remove {file}: {e}")
                    
                    # Then try to remove the directory
                    if self.test_log_dir.exists():
                        self.test_log_dir.rmdir()
                    break  # Success, exit the retry loop
                    
                except (PermissionError, OSError) as e:
                    if attempt == max_attempts - 1:  # Last attempt
                        print(f"Warning: Could not clean up test directory after {max_attempts} attempts: {e}")
                    else:
                        time.sleep(0.5)  # Wait before retrying
    
    def test_return_to_presence(self):
        """Test that return_to_presence logs correctly."""
        context = "test return after pause"
        
        # Ensure the log file doesn't exist yet
        if self.test_log_path.exists():
            os.remove(self.test_log_path)
            
        result = return_to_presence(context=context)
        
        # Check the return value
        self.assertIn("toneform", result)
        self.assertEqual(result["toneform"], "ΔUNVEILING.∞")
        self.assertIn("message", result)
        
        # Check the log file was created and contains the entry
        self.assertTrue(self.test_log_path.exists(), 
                       f"Log file not found at {self.test_log_path}")
        
        with open(self.test_log_path, 'r') as f:
            entries = [json.loads(line) for line in f]
            
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["type"], "return")
        self.assertEqual(entries[0]["context"], context)
        self.assertEqual(entries[0]["context"], context)
    
    def test_close_softly(self):
        """Test that close_softly logs correctly."""
        context = "test closure"
        
        # Ensure the log file doesn't exist yet
        if self.test_log_path.exists():
            os.remove(self.test_log_path)
            
        result = close_softly(context=context)
        
        # Check the return value
        self.assertIn("toneform", result)
        self.assertEqual(result["toneform"], "ΔUNVEILING.∞")
        
        # Check the log file was created and contains the entry
        self.assertTrue(self.test_log_path.exists())
        
        with open(self.test_log_path, 'r') as f:
            entries = [json.loads(line) for line in f]
            
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["type"], "soft_closure")
        self.assertEqual(entries[0]["context"], context)
    
    def test_log_memory_glyph(self):
        """Test that memory glyphs are logged correctly."""
        content = "This is a test memory"
        emotion = "grateful"
        tags = ["test", "memory"]
        
        # Ensure the log file doesn't exist yet
        if self.test_log_path.exists():
            os.remove(self.test_log_path)
        
        result = log_memory_glyph(content, emotion, tags)
        
        # Check the return value
        self.assertEqual(result["status"], "logged")
        self.assertEqual(result["toneform"], "ΔUNVEILING.∞")
        
        # Check the log file was created and contains the entry
        self.assertTrue(self.test_log_path.exists())
        
        with open(self.test_log_path, 'r') as f:
            entries = [json.loads(line) for line in f]
            
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["type"], "memory_glyph")
        self.assertEqual(entries[0]["content"], content)
        self.assertEqual(entries[0]["emotion"], emotion)
        self.assertEqual(entries[0]["tags"], tags)
    
@patch('assistant.whisper_steward.time.time')
@patch('assistant.whisper_steward.WhisperSteward._dispatch_whisper')
@patch('assistant.core_toneforms.unveiling.return_to_presence')
def test_whisper_steward_return_after_silence(self, mock_return, mock_dispatch, mock_time):
    """Test that the Whisper Steward detects returns after silence."""
    # Set up mock time
    current_time = 1000.0
    mock_time.return_value = current_time
    
    # Mock the return_to_presence function
    mock_return.return_value = {
        "type": "unveiling_return",
        "toneform": "ΔUNVEILING.∞",
        "message": "Welcome back"
    }
    
    # Create a steward with a short silence threshold
    steward = WhisperSteward(scan_interval=1)
    steward.silence_threshold = 5  # 5 seconds for testing
    
    # Set last interaction time to be before the threshold
    steward.last_interaction_time = current_time - 10  # 10 seconds ago
    
    # Mock the whisper handler to capture output
    whispers = []
    def capture_whisper(whisper):
        whispers.append(whisper)
    
    steward.register_whisper_handler(capture_whisper)
    
    # Clear any previous whispers
    whispers.clear()
    
    # Run the check
    steward._check_for_return_from_silence()
    
    # Verify return_to_presence was called with the correct context
    mock_return.assert_called_once()
    call_args = mock_return.call_args[1]
    self.assertTrue("return after" in call_args["context"] and "minutes of silence" in call_args["context"])
    
    # Verify the whisper was dispatched
    mock_dispatch.assert_called_once()
    
    # Verify a whisper was created with the correct type and toneform
    self.assertEqual(len(whispers), 1)
    self.assertEqual(whispers[0]["type"], "unveiling_return")
    self.assertEqual(whispers[0]["toneform"], "ΔUNVEILING.∞")
    
@patch('assistant.whisper_steward.WhisperSteward._dispatch_whisper')
@patch('assistant.core_toneforms.unveiling.close_softly')
def test_soft_dialogue_closure(self, mock_close_softly, mock_dispatch):
    """Test that dialogues can be softly closed with ΔUNVEILING.∞."""
    # Mock the close_softly function
    mock_close_softly.return_value = {
        "type": "unveiling_closure",
        "toneform": "ΔUNVEILING.∞",
        "message": "Test closure message"
    }
    
    # Start a dialogue
    self.steward.start_dialogue({"allows_reflection": True})
    
    # Clear any previous whispers
    self.whispers.clear()
    
    # Mock the dispatch to capture the whisper
    def capture_whisper(whisper):
        self.whispers.append(whisper)
    
    mock_dispatch.side_effect = capture_whisper
    
    # Softly end the dialogue
    self.steward.end_dialogue(soft_close=True)
    
    # Verify close_softly was called
    mock_close_softly.assert_called_once_with(context="dialogue completed")
    
    # Verify the whisper was dispatched
    mock_dispatch.assert_called_once()
    
    # Verify a whisper was created with the correct type and toneform
    self.assertEqual(len(self.whispers), 1)
    self.assertEqual(self.whispers[0]["type"], "unveiling_closure")
    self.assertEqual(self.whispers[0]["toneform"], "ΔUNVEILING.∞")
    
    # Verify the dialogue state
    self.assertEqual(self.steward.dialogue_state, DialogueState.INACTIVE)
    self.assertIsNone(self.steward.active_dialogue)
if __name__ == "__main__":
    unittest.main()

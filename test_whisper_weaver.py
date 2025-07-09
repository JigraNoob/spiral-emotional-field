#!/usr/bin/env python3
"""
Test script for WhisperWeaver Agent
"""

import time
import json
from pathlib import Path
from agents.whisper_weaver import WhisperWeaver

def test_whisper_weaver():
    """Test the WhisperWeaver agent."""
    print("🌬️ Testing WhisperWeaver Agent")
    print("=" * 50)
    
    # Create WhisperWeaver instance
    weaver = WhisperWeaver(check_interval=5)  # Faster for testing
    
    # Test initialization
    print("✅ WhisperWeaver initialized")
    print(f"   - Pattern thresholds: {weaver.pattern_thresholds}")
    print(f"   - Check interval: {weaver.check_interval}s")
    print(f"   - Recent changes window: {weaver.recent_changes_window}s")
    
    # Test status
    status = weaver.get_status()
    print(f"✅ Status: {status}")
    
    # Start the agent
    print("\n🌬️ Starting WhisperWeaver...")
    weaver.start()
    
    # Let it run for a bit
    print("🌬️ Running for 30 seconds to test pattern detection...")
    time.sleep(30)
    
    # Check status again
    status = weaver.get_status()
    print(f"✅ Status after running: {status}")
    
    # Stop the agent
    print("\n🌬️ Stopping WhisperWeaver...")
    weaver.stop()
    
    print("✅ Test completed")

if __name__ == "__main__":
    test_whisper_weaver() 
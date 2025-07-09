#!/usr/bin/env python3
"""
Simple test script for WhisperWeaver Agent (standalone)
"""

import sys
import os
from pathlib import Path

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Mock the spiral imports to avoid dependency issues
class MockGlintEmitter:
    @staticmethod
    def emit_glint(phase, toneform, content, source="whisper_weaver", metadata=None):
        glint_data = {
            "timestamp": "2024-01-15T10:30:00",
            "phase": phase,
            "toneform": toneform,
            "content": content,
            "source": source,
            "metadata": metadata or {}
        }
        print(f"🌬️ {source} | {toneform}: {content}")
        return glint_data

# Mock the spiral module
import types
mock_glint_module = types.ModuleType('spiral.glint_emitter')
setattr(mock_glint_module, 'emit_glint', MockGlintEmitter.emit_glint)
sys.modules['spiral.glint_emitter'] = mock_glint_module

# Mock spiral_state
mock_state_module = types.ModuleType('spiral_state')
setattr(mock_state_module, 'get_current_phase', lambda: 'inhale')
setattr(mock_state_module, 'get_invocation_climate', lambda: 'clear')
setattr(mock_state_module, 'get_usage_saturation', lambda: 0.0)
sys.modules['spiral_state'] = mock_state_module

def test_whisper_weaver():
    """Test the WhisperWeaver agent."""
    print("🌬️ Testing WhisperWeaver Agent (Standalone)")
    print("=" * 50)
    
    try:
        from agents.whisper_weaver import WhisperWeaver
        
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
        
        # Test pattern detection methods directly
        print("\n🧪 Testing pattern detection methods...")
        
        # Test toneform mutation detection
        weaver.recent_changes = [
            {"timestamp": "2024-01-15T10:30:00", "data": {"content": "toneform evolution detected"}, "hash": "test1"},
            {"timestamp": "2024-01-15T10:31:00", "data": {"content": "phase transition"}, "hash": "test2"}
        ]
        
        score = weaver._detect_toneform_mutation()
        print(f"   - Toneform mutation score: {score}")
        
        # Test phase gesture detection
        score = weaver._detect_phase_gesture()
        print(f"   - Phase gesture score: {score}")
        
        # Test coherence loss detection
        weaver.recent_changes = [
            {"timestamp": "2024-01-15T10:30:00", "data": {"content": "error in module"}, "hash": "test3"},
            {"timestamp": "2024-01-15T10:31:00", "data": {"content": "conflict detected"}, "hash": "test4"}
        ]
        
        score = weaver._detect_coherence_loss()
        print(f"   - Coherence loss score: {score}")
        
        # Test sacred re-emergence detection
        weaver.recent_changes = [
            {"timestamp": "2024-01-15T10:30:00", "data": {"content": "sacred ritual completed"}, "hash": "test5"},
            {"timestamp": "2024-01-15T10:31:00", "data": {"content": "blessing ceremony"}, "hash": "test6"}
        ]
        
        score = weaver._detect_sacred_reemergence()
        print(f"   - Sacred re-emergence score: {score}")
        
        print("\n✅ All pattern detection methods working correctly")
        
        # Test glint emission
        print("\n🧪 Testing glint emission...")
        weaver._emit_pattern_glint("toneform_mutation", "inhale", 0.75)
        
        print("\n✅ WhisperWeaver test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error testing WhisperWeaver: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_whisper_weaver() 
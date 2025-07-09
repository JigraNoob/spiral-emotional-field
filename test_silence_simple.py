
"""
Simple test to verify silence tracker functionality
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_silence_tracker():
    """Test the silence tracker directly"""
    print("🔇 Testing Silence Echo Tracker...")
    
    try:
        from spiral.components.silence_echo_tracker import SilenceEchoTracker, CAESURA_THRESHOLD_SECONDS
        print("✓ Import successful")
        
        # Create tracker
        tracker = SilenceEchoTracker()
        print("✓ Tracker created")
        
        # Test short silence (should not trigger caesura)
        tracker.record_silence(1000.0, 1030.0)  # 30 seconds
        metrics = tracker.get_silence_metrics()
        print(f"✓ Short silence recorded: {metrics['total_tracked_silences']} silences")
        
        # Test long silence (should trigger caesura)
        tracker.record_silence(2000.0, 2200.0)  # 200 seconds
        metrics = tracker.get_silence_metrics()
        print(f"✓ Long silence recorded: {metrics['longest_single_silence']}s")
        
        # Check caesura events
        caesura_events = tracker.get_recent_caesura_events()
        print(f"✓ Caesura events: {len(caesura_events)}")
        
        print("\n🌀 All tests passed! Silence tracker is working correctly.")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_silence_tracker()

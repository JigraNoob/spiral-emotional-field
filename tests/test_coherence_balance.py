#!/usr/bin/env python3
"""
Test script for Coherence Balance functionality

This script demonstrates how the coherence balancer works and helps
validate that it properly prevents backend suspicion.
"""

import sys
import time
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from spiral.attunement.coherence_balancer import (
    CoherenceMode, 
    set_coherence_mode, 
    get_coherence_status,
    record_coherence_event,
    coherence_balancer
)

def test_backend_safe_mode():
    """Test the backend_safe mode with conservative thresholds."""
    print("\n🧪 Testing Backend Safe Mode")
    print("=" * 40)
    
    # Set to backend safe mode
    set_coherence_mode(CoherenceMode.BACKEND_SAFE)
    
    # Simulate some coherence events
    print("Simulating coherence events...")
    
    # Simulate loud pattern (high resonance)
    for i in range(8):
        record_coherence_event(0.85, {"awe": 0.9, "wonder": 0.8})
        time.sleep(0.1)
    
    # Check status
    status = get_coherence_status()
    print(f"Mode: {status['mode']}")
    print(f"Backend Safety Score: {status['backend_safety_score']:.2f}")
    print(f"Loud Periods: {status['loud_periods']}")
    print(f"Current Thresholds: {status['current_thresholds']}")
    
    return status['backend_safety_score'] > 0.5

def test_adaptive_mode():
    """Test the adaptive mode with dynamic threshold adjustment."""
    print("\n🧪 Testing Adaptive Mode")
    print("=" * 40)
    
    # Reset patterns first
    coherence_balancer.reset_patterns()
    
    # Set to adaptive mode
    set_coherence_mode(CoherenceMode.ADAPTIVE)
    
    # Simulate mixed patterns
    print("Simulating mixed coherence patterns...")
    
    # Some quiet events
    for i in range(5):
        record_coherence_event(0.2, {"stillness": 0.3})
        time.sleep(0.1)
    
    # Some loud events
    for i in range(5):
        record_coherence_event(0.9, {"awe": 0.95, "reverence": 0.9})
        time.sleep(0.1)
    
    # Check status
    status = get_coherence_status()
    print(f"Mode: {status['mode']}")
    print(f"Backend Safety Score: {status['backend_safety_score']:.2f}")
    print(f"Loud Periods: {status['loud_periods']}")
    print(f"Quiet Periods: {status['quiet_periods']}")
    print(f"Current Thresholds: {status['current_thresholds']}")
    
    return status['backend_safety_score'] > 0.3

def test_suspicious_pattern_detection():
    """Test detection of suspicious patterns (rapid oscillation)."""
    print("\n🧪 Testing Suspicious Pattern Detection")
    print("=" * 40)
    
    # Reset patterns
    coherence_balancer.reset_patterns()
    
    # Set to normal mode
    set_coherence_mode(CoherenceMode.NORMAL)
    
    # Simulate rapid oscillation
    print("Simulating rapid coherence oscillation...")
    
    # Rapid oscillation between high and low
    for i in range(10):
        if i % 2 == 0:
            record_coherence_event(0.9, {"awe": 0.95})
        else:
            record_coherence_event(0.1, {"stillness": 0.2})
        time.sleep(0.1)
    
    # Check status
    status = get_coherence_status()
    print(f"Mode: {status['mode']}")
    print(f"Backend Safety Score: {status['backend_safety_score']:.2f}")
    print(f"Suspicious Patterns: {status['suspicious_patterns']}")
    print(f"Current Thresholds: {status['current_thresholds']}")
    
    return status['suspicious_patterns'] > 0

def test_threshold_adjustment():
    """Test that thresholds are properly adjusted in different modes."""
    print("\n🧪 Testing Threshold Adjustment")
    print("=" * 40)
    
    # Test normal mode
    set_coherence_mode(CoherenceMode.NORMAL)
    normal_thresholds = get_coherence_status()['current_thresholds']
    print(f"Normal mode thresholds: {normal_thresholds}")
    
    # Test backend safe mode
    set_coherence_mode(CoherenceMode.BACKEND_SAFE)
    safe_thresholds = get_coherence_status()['current_thresholds']
    print(f"Backend safe mode thresholds: {safe_thresholds}")
    
    # Verify that backend safe thresholds are more conservative
    safe_silence = safe_thresholds['silence_threshold']
    normal_silence = normal_thresholds['silence_threshold']
    
    print(f"Silence threshold comparison:")
    print(f"  Normal: {normal_silence:.3f}")
    print(f"  Backend Safe: {safe_silence:.3f}")
    print(f"  More conservative: {safe_silence < normal_silence}")
    
    return safe_silence < normal_silence

def run_all_tests():
    """Run all coherence balance tests."""
    print("🔧 Coherence Balance Test Suite")
    print("=" * 50)
    
    tests = [
        ("Backend Safe Mode", test_backend_safe_mode),
        ("Adaptive Mode", test_adaptive_mode),
        ("Suspicious Pattern Detection", test_suspicious_pattern_detection),
        ("Threshold Adjustment", test_threshold_adjustment)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            print(f"\nRunning: {test_name}")
            result = test_func()
            results.append((test_name, result, "PASS" if result else "FAIL"))
            print(f"Result: {'✅ PASS' if result else '❌ FAIL'}")
        except Exception as e:
            print(f"Error in {test_name}: {e}")
            results.append((test_name, False, "ERROR"))
            print(f"Result: ❌ ERROR")
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result, status in results:
        print(f"{test_name}: {status}")
        if status == "PASS":
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Coherence balancing is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the implementation.")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 
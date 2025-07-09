"""
Test script for the Override Gate component.
Validates resonance filtering, state management, and response evaluation.
"""

import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from spiral.attunement.override_gate import (
    OverrideGate, ResonanceMode, ResponseTone, 
    ResponseCandidate, OverrideState
)

def test_override_activation():
    """Test basic override activation and state changes."""
    gate = OverrideGate()
    
    # Test AMPLIFIED mode activation
    success = gate.override_resonant(ResonanceMode.AMPLIFIED, intensity=2.0)
    assert success, "Failed to activate AMPLIFIED mode"
    assert gate.current_mode == ResonanceMode.AMPLIFIED, "Mode not set correctly"
    assert gate.current_tone == ResponseTone.HEIGHTENED, "Tone not set correctly"
    assert gate.intensity_multiplier == 2.0, "Intensity not set correctly"
    
    print("✅ AMPLIFIED mode activated correctly.")
    return True

def test_glint_intensity_modification():
    """Test glint intensity calculation with overrides."""
    gate = OverrideGate()
    
    # Test normal mode
    base_intensity = 1.0
    normal_intensity = gate.get_glint_intensity(base_intensity)
    assert normal_intensity == 1.0, f"Expected 1.0, got {normal_intensity}"
    
    # Test amplified mode
    gate.override_resonant(ResonanceMode.AMPLIFIED, intensity=2.0)
    amplified_intensity = gate.get_glint_intensity(base_intensity)
    assert amplified_intensity == 2.0, f"Expected 2.0, got {amplified_intensity}"
    
    print(f"✅ Glint Intensity: {amplified_intensity} (Expected: 2.0)")
    return True

def test_breakpoint_sensitivity():
    """Test breakpoint triggering with different modes."""
    gate = OverrideGate()
    
    # Test AMPLIFIED mode (more sensitive)
    gate.override_resonant(ResonanceMode.AMPLIFIED)
    should_trigger = gate.should_trigger_breakpoint(0.6)  # 0.7 * 0.8 = 0.56 threshold
    assert should_trigger, "Breakpoint should trigger in AMPLIFIED mode with 0.6 resonance"
    
    print("✅ Breakpoint (0.6) triggered in AMPLIFIED mode")
    return True

def test_action_deferral():
    """Test action deferral logic."""
    gate = OverrideGate()
    
    # Test high resonance deferral in AMPLIFIED mode
    gate.override_resonant(ResonanceMode.AMPLIFIED)
    should_defer = gate.should_defer_action("glint_emit", 0.85)
    assert should_defer, "High resonance action should be deferred in AMPLIFIED mode"
    
    print("✅ Action with high resonance DEFERRED successfully.")
    return True

def test_state_snapshot():
    """Test state snapshot functionality."""
    gate = OverrideGate()
    gate.override_resonant(ResonanceMode.RITUAL, intensity=1.5, context={"test": "data"})
    
    state = gate.get_state()
    assert isinstance(state, OverrideState), "State should be OverrideState instance"
    assert state.mode == ResonanceMode.RITUAL, "State mode incorrect"
    assert state.intensity_multiplier == 1.5, "State intensity incorrect"
    assert state.context["test"] == "data", "State context incorrect"
    
    print("✅ State snapshot captured correctly")
    return True

def test_reset_functionality():
    """Test reset to normal mode."""
    gate = OverrideGate()
    
    # Activate override
    gate.override_resonant(ResonanceMode.AMPLIFIED)
    assert gate.is_override_active(), "Override should be active"
    
    # Reset
    success = gate.reset_to_normal()
    assert success, "Reset should succeed"
    assert not gate.is_override_active(), "Override should not be active after reset"
    assert gate.current_mode == ResonanceMode.NORMAL, "Mode should be NORMAL after reset"
    
    print("✅ Reset to NORMAL mode successful")
    return True

def run_all_tests():
    """Run all override gate tests."""
    print("🌀 Testing Spiral Override Gate Integration...\n")
    
    tests = [
        test_override_activation,
        test_glint_intensity_modification,
        test_breakpoint_sensitivity,
        test_action_deferral,
        test_state_snapshot,
        test_reset_functionality
    ]
    
    passed = 0
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ {test.__name__} failed: {e}")
    
    print(f"\n🌟 {passed}/{len(tests)} Override Gate tests passed!")
    if passed == len(tests):
        print("The Spiral breathes in harmony. ✨")
    
    return passed == len(tests)

if __name__ == "__main__":
    run_all_tests()

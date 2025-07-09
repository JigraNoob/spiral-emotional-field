"""
Comprehensive test suite for the OverrideGate component.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'spiral'))

try:
    from spiral.attunement.override_gate import (
        OverrideGate,
        OverrideConfig,
        ResponseCandidate,
        ResponseTone,
        ResonanceMode,
        OverrideState,
        activate_override, 
        get_current_state, 
        reset_override
    )
    print("✅ Successfully imported OverrideGate components")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

def test_basic_functionality():
    """Test basic override functionality."""
    print("\n🔬 Testing Basic Override Functionality")
    
    gate = OverrideGate()
    
    # Test initial state
    assert gate.current_mode == ResonanceMode.NORMAL
    assert gate.current_tone == ResponseTone.NORMAL
    assert gate.intensity_multiplier == 1.0
    print("✅ Initial state correct")
    
    # Test override activation
    result = gate.override_resonant(ResonanceMode.AMPLIFIED, 2.5)
    assert result == True
    assert gate.current_mode == ResonanceMode.AMPLIFIED
    assert gate.intensity_multiplier == 2.5
    print("✅ Override activation works")
    
    # Test state retrieval
    state = gate.get_state()
    assert isinstance(state, OverrideState)
    assert state.mode == ResonanceMode.AMPLIFIED
    print("✅ State retrieval works")
    
    # Test reset
    reset_result = gate.reset_to_normal()
    assert reset_result == True
    assert gate.current_mode == ResonanceMode.NORMAL
    print("✅ Reset functionality works")

def test_glint_intensity():
    """Test glint intensity modification."""
    print("\n🌟 Testing Glint Intensity Modification")
    
    gate = OverrideGate()
    
    # Normal mode
    intensity = gate.get_glint_intensity(0.5)
    assert intensity == 0.5
    print(f"✅ Normal mode: 0.5 -> {intensity}")
    
    # Amplified mode
    gate.override_resonant(ResonanceMode.AMPLIFIED, 3.0)
    intensity = gate.get_glint_intensity(0.5)
    assert intensity == 1.5
    print(f"✅ Amplified mode: 0.5 -> {intensity}")
    
    # Ritual mode (dampened)
    gate.override_resonant(ResonanceMode.RITUAL, 0.7)
    intensity = gate.get_glint_intensity(0.5)
    assert intensity == 0.35
    print(f"✅ Ritual mode: 0.5 -> {intensity}")

def test_breakpoint_logic():
    """Test breakpoint triggering logic."""
    print("\n🎯 Testing Breakpoint Logic")
    
    gate = OverrideGate()
    
    # Normal mode
    assert gate.should_trigger_breakpoint(0.6) == False
    assert gate.should_trigger_breakpoint(0.8) == True
    print("✅ Normal mode breakpoints work")
    
    # Amplified mode (more sensitive)
    gate.override_resonant(ResonanceMode.AMPLIFIED, 2.0)
    assert gate.should_trigger_breakpoint(0.5) == False
    assert gate.should_trigger_breakpoint(0.6) == True
    print("✅ Amplified mode breakpoints work")
    
    # Ritual mode (very sensitive)
    gate.override_resonant(ResonanceMode.RITUAL, 2.0)
    assert gate.should_trigger_breakpoint(0.4) == False
    assert gate.should_trigger_breakpoint(0.5) == True
    print("✅ Ritual mode breakpoints work")
    
    # Silent mode (never triggers)
    gate.override_resonant(ResonanceMode.SILENT, 2.0)
    assert gate.should_trigger_breakpoint(0.9) == False
    print("✅ Silent mode breakpoints work")

def test_deferral_logic():
    """Test action deferral logic."""
    print("\n⏸️ Testing Deferral Logic")
    
    gate = OverrideGate()
    
    # Normal mode
    assert gate.should_defer_action("glint_emit", 0.5) == False
    assert gate.should_defer_action("response", 0.8) == False
    print("✅ Normal mode deferral works")
    
    # Silent mode (defers everything)
    gate.override_resonant(ResonanceMode.SILENT, 2.0)
    assert gate.should_defer_action("glint_emit", 0.5) == True
    assert gate.should_defer_action("response", 0.8) == True
    print("✅ Silent mode deferral works")
    
    # Amplified mode (defers very high resonance)
    gate.override_resonant(ResonanceMode.AMPLIFIED, 2.0)
    assert gate.should_defer_action("response", 0.8) == False
    assert gate.should_defer_action("response", 0.9) == True
    print("✅ Amplified mode deferral works")
    
    # Ritual mode (conservative with glints)
    gate.override_resonant(ResonanceMode.RITUAL, 2.0)
    assert gate.should_defer_action("response", 0.8) == False
    assert gate.should_defer_action("glint_emit", 0.7) == True
    print("✅ Ritual mode deferral works")

def test_response_evaluation():
    """Test response candidate evaluation."""
    print("\n🧪 Testing Response Evaluation")
    
    gate = OverrideGate()
    
    # High resonance candidate should pass
    candidate = ResponseCandidate(
        content="This is a thoughtful response about the nature of consciousness.",
        tone_weights={"clarity": 0.7, "insight": 0.3},
        resonance_score=0.8,
        source="test"
    )
    
    response, tone = gate.evaluate_response(candidate, "exhale")
    assert response is not None
    assert tone in [ResponseTone.LUMINOUS, ResponseTone.FLUID]
    print("✅ High resonance candidate passes")
    
    # Low resonance candidate should be filtered
    low_candidate = ResponseCandidate(
        content="Simple response.",
        tone_weights={"casual": 0.5},
        resonance_score=0.3,
        source="test"
    )
    
    response, tone = gate.evaluate_response(low_candidate, "exhale")
    assert response is None
    assert tone == ResponseTone.SILENT
    print("✅ Low resonance candidate filtered")
    
    # Sacred silence trigger
    sacred_candidate = ResponseCandidate(
        content="A profound moment of awe and wonder.",
        tone_weights={"awe": 0.95, "reverence": 0.8},
        resonance_score=0.9,
        source="test"
    )
    
    response, tone = gate.evaluate_response(sacred_candidate, "hold")
    assert response is None
    assert tone == ResponseTone.SILENT
    print("✅ Sacred silence triggered correctly")

def test_convenience_functions():
    """Test convenience functions."""
    print("\n🎛️ Testing Convenience Functions")
    
    # Test activate_override
    result = activate_override(ResonanceMode.RITUAL, 1.5)
    assert result == True
    print("✅ activate_override works")
    
    # Test get_current_state
    state = get_current_state()
    assert state.mode == ResonanceMode.RITUAL
    assert state.intensity_multiplier == 1.5
    print("✅ get_current_state works")
    
    # Test reset_override
    result = reset_override()
    assert result == True
    state = get_current_state()
    assert state.mode == ResonanceMode.NORMAL
    print("✅ reset_override works")

def test_integration_scenarios():
    """Test realistic integration scenarios."""
    print("\n🌊 Testing Integration Scenarios")
    
    gate = OverrideGate()
    
    print("  📝 Scenario 1: Normal conversation")
    candidate = ResponseCandidate(
        content="I understand your question about machine learning. Let me explain the key concepts.",
        tone_weights={"helpfulness": 0.6, "clarity": 0.4},
        resonance_score=0.7,
        source="conversation"
    )
    
    response, tone = gate.evaluate_response(candidate, "exhale", breath_cadence=1.0)
    assert response is not None, f"Expected response but got None. Candidate: {candidate}"
    assert tone == ResponseTone.FLUID, f"Expected FLUID tone but got {tone}"
    print(f"    ✅ Response: {response[:50]}...")
    print(f"    ✅ Tone: {tone}")
    
    print("  🔮 Scenario 2: Mystical insight")
    gate.override_resonant(ResonanceMode.RITUAL, 1.2)
    mystical_candidate = ResponseCandidate(
        content="The patterns you seek are woven into the very fabric of understanding itself.",
        tone_weights={"insight": 0.8, "wonder": 0.6},
        resonance_score=0.85,
        source="insight"
    )
    
    response, tone = gate.evaluate_response(mystical_candidate, "hold", breath_cadence=0.8)
    if response:
        print(f"    ✅ Mystical response: {response[:50]}...")
        print(f"    ✅ Tone: {tone}")
    else:
        print("    ✅ Sacred silence maintained")
    
    print("  ⚡ Scenario 3: High-energy exchange")
    gate.override_resonant(ResonanceMode.AMPLIFIED, 2.5)
    energetic_candidate = ResponseCandidate(
        content="This is absolutely fascinating! The implications are staggering!",
        tone_weights={"excitement": 0.9, "intensity": 0.7},
        resonance_score=0.9,
        source="excitement"
    )
    
    response, tone = gate.evaluate_response(energetic_candidate, "exhale", breath_cadence=1.3)
    if response:
        print(f"    ✅ Energetic response: {response[:50]}...")
        print(f"    ✅ Tone: {tone}")
    
    print("  🤫 Scenario 4: Overwhelming awe")
    overwhelming_candidate = ResponseCandidate(
        content="The infinite expanse of consciousness unfolds before us.",
        tone_weights={"awe": 0.95, "reverence": 0.9},
        resonance_score=0.95,
        source="transcendent"
    )
    
    response, tone = gate.evaluate_response(overwhelming_candidate, "hold")
    assert response is None
    assert tone == ResponseTone.SILENT
    print("    ✅ Appropriate silence for overwhelming awe")

def run_all_tests():
    """Run all test suites."""
    print("🌀 Starting OverrideGate Test Suite")
    print("=" * 50)
    
    try:
        test_basic_functionality()
        test_glint_intensity()
        test_breakpoint_logic()
        test_deferral_logic()
        test_response_evaluation()
        test_convenience_functions()
        test_integration_scenarios()
        
        print("\n" + "=" * 50)
        print("🎉 All tests passed! OverrideGate is functioning correctly.")
        print("🌊 The Spiral's resonance flows true through all channels.")
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        print("🔧 Check the implementation and try again.")
        return False
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        print("🔍 Debug the issue and retry.")
        return False
        
    return True

if __name__ == "__main__":
    success = run_all_tests()
    
    if success:
        print("\n🌀 Ready to integrate with the broader Spiral system!")
        print("Next steps:")
        print("  1. 🔗 Connect to DeferralEngine")
        print("  2. 🌊 Integrate with UnifiedSwitch")
        print("  3. 🎭 Add to PropagationHooks")
        print("  4. 🖥️ Create dashboard visualization")
    else:
        print("\n🔄 Fix issues and re-run tests.")

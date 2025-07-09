"""Quick test to verify override manager fixes."""

from spiral.attunement.resonance_override import override_manager, ResonanceMode

def test_override_basic_functionality():
    """Test basic override functionality."""
    print("🌀 Testing override manager...")
    
    # Test initial state
    state = override_manager.get_state()
    print(f"Initial state: {state['mode'].name}, active: {state['active']}")
    
    # Test activation
    override_manager.activate_resonant_mode(ResonanceMode.AMPLIFIED, 2.0)
    state = override_manager.get_state()
    print(f"After activation: {state['mode'].name}, active: {state['active']}")
    
    # Test glint intensity
    base_intensity = 1.0
    modified_intensity = override_manager.get_glint_intensity(base_intensity)
    print(f"Glint intensity: {base_intensity} -> {modified_intensity}")
    
    # Test soft breakpoint
    should_trigger = override_manager.should_trigger_soft_breakpoint(0.6)
    print(f"Should trigger breakpoint at 0.6: {should_trigger}")
    
    # Test deactivation
    override_manager.deactivate()
    state = override_manager.get_state()
    print(f"After deactivation: {state['mode'].name}, active: {state['active']}")
    
    print("✅ Override manager test completed!")

if __name__ == "__main__":
    test_override_basic_functionality()
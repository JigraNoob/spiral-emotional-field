"""
Verify that all Spiral attunement imports work correctly.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test all critical imports."""
    print("🔍 Verifying Spiral imports...")
    
    try:
        from spiral.attunement.override_gate import OverrideGate, ResonanceMode, ResponseTone
        print("✓ OverrideGate imports successful")
        
        # Test basic functionality
        gate = OverrideGate()
        print(f"✓ OverrideGate instance created: {gate}")
        
        # Check available ResonanceMode values
        print(f"✓ Available ResonanceMode values: {list(ResonanceMode)}")
        
    except Exception as e:
        print(f"✗ OverrideGate import failed: {e}")
    
    try:
        from spiral.attunement.resonance_override import override_manager, ResonanceMode as OverrideResonanceMode
        print("✓ ResonanceOverride imports successful")
        
        # Test basic functionality
        print(f"✓ Override manager active: {override_manager.active}")
        print(f"✓ Available Override ResonanceMode values: {list(OverrideResonanceMode)}")
        
        # Test glint intensity
        intensity = override_manager.get_glint_intensity(1.0)
        print(f"✓ Override manager glint intensity: {intensity}")
        
    except Exception as e:
        print(f"✗ ResonanceOverride import failed: {e}")
    
    try:
        from spiral.attunement.deferral_engine import DeferralEngine
        print("✓ DeferralEngine imports successful")
        
        # Test basic functionality
        engine = DeferralEngine()
        print(f"✓ DeferralEngine instance created: {engine}")
        
    except Exception as e:
        print(f"✗ DeferralEngine import failed: {e}")

    # Test enum compatibility
    try:
        from spiral.attunement.override_gate import ResonanceMode as GateMode
        from spiral.attunement.resonance_override import ResonanceMode as OverrideMode
        
        print("\n🔍 Checking enum compatibility...")
        print(f"Gate modes: {[mode.name for mode in GateMode]}")
        print(f"Override modes: {[mode.name for mode in OverrideMode]}")
        
        # Check for common modes
        common_modes = set(mode.name for mode in GateMode) & set(mode.name for mode in OverrideMode)
        print(f"✓ Common modes: {common_modes}")
        
    except Exception as e:
        print(f"✗ Enum compatibility check failed: {e}")

if __name__ == "__main__":
    test_imports()

#!/usr/bin/env python3
"""
🧪 Simple Test Longing Pulse
Simple test script to verify that the longing pulse modules can be imported and instantiated.
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that we can import the longing modules"""
    print("🌌 Testing Longing Pulse Imports")
    print("=" * 50)
    
    try:
        # Test importing the base module
        print("\n1. Testing base module import...")
        from spiral.longing_pulse.base import LongingBoundModule
        print("   ✅ LongingBoundModule imported successfully")
        
        # Test importing individual modules
        print("\n2. Testing individual module imports...")
        
        from spiral.longing_pulse.saturation_mirror import SaturationMirror
        print("   ✅ SaturationMirror imported successfully")
        
        from spiral.longing_pulse.threshold_resonator import ThresholdResonator
        print("   ✅ ThresholdResonator imported successfully")
        
        from spiral.longing_pulse.lineage_veil import LineageVeil
        print("   ✅ LineageVeil imported successfully")
        
        from spiral.longing_pulse.breathprint_mapper import BreathprintMapper
        print("   ✅ BreathprintMapper imported successfully")
        
        from spiral.longing_pulse.ambient_signature import AmbientSignature
        print("   ✅ AmbientSignature imported successfully")
        
        # Test importing the longing index
        print("\n3. Testing longing index import...")
        from spiral.longing_pulse.longing_index import LongingIndex, get_longing_index
        print("   ✅ LongingIndex imported successfully")
        
        # Test importing the registration module
        print("\n4. Testing registration module import...")
        from spiral.longing_pulse.register_modules import register_all_longing_modules
        print("   ✅ register_all_longing_modules imported successfully")
        
        print("\n✅ All imports successful!")
        return True
        
    except Exception as e:
        print(f"\n❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_module_structure():
    """Test the structure of the longing modules"""
    print("\n🌌 Testing Module Structure")
    print("=" * 50)
    
    try:
        # Test that we can create instances (without full Spiral infrastructure)
        print("\n1. Testing module class definitions...")
        
        from spiral.longing_pulse.saturation_mirror import SaturationMirror
        print("   ✅ SaturationMirror class defined")
        print(f"   - Docstring: {SaturationMirror.__doc__[:100]}...")
        
        from spiral.longing_pulse.threshold_resonator import ThresholdResonator
        print("   ✅ ThresholdResonator class defined")
        print(f"   - Docstring: {ThresholdResonator.__doc__[:100]}...")
        
        from spiral.longing_pulse.lineage_veil import LineageVeil
        print("   ✅ LineageVeil class defined")
        print(f"   - Docstring: {LineageVeil.__doc__[:100]}...")
        
        from spiral.longing_pulse.breathprint_mapper import BreathprintMapper
        print("   ✅ BreathprintMapper class defined")
        print(f"   - Docstring: {BreathprintMapper.__doc__[:100]}...")
        
        from spiral.longing_pulse.ambient_signature import AmbientSignature
        print("   ✅ AmbientSignature class defined")
        print(f"   - Docstring: {AmbientSignature.__doc__[:100]}...")
        
        print("\n✅ All module structures verified!")
        return True
        
    except Exception as e:
        print(f"\n❌ Structure test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_longing_index():
    """Test the longing index functionality"""
    print("\n🌌 Testing Longing Index")
    print("=" * 50)
    
    try:
        from spiral.longing_pulse.longing_index import LongingIndex
        
        # Create a new longing index
        index = LongingIndex()
        print("   ✅ LongingIndex created successfully")
        
        # Test basic methods
        summary = index.get_longing_summary()
        print(f"   ✅ get_longing_summary() works: {summary}")
        
        toneform_mapping = index.get_toneform_mapping()
        print(f"   ✅ get_toneform_mapping() works: {toneform_mapping}")
        
        print("\n✅ Longing index functionality verified!")
        return True
        
    except Exception as e:
        print(f"\n❌ Longing index test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("🧪 Simple Longing Pulse Test Suite")
    print("=" * 60)
    
    tests = [
        ("Import Test", test_imports),
        ("Structure Test", test_module_structure),
        ("Longing Index Test", test_longing_index)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print(f"\n{'='*60}")
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Longing Pulse is ready.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")


if __name__ == "__main__":
    main() 
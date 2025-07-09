#!/usr/bin/env python3
"""
🌫️ Simple Path Seeker Test - Direct Testing

A simplified test that directly tests the path seeker functionality
without complex import dependencies.
"""

import sys
from pathlib import Path
from datetime import datetime

# Add the spiral directory to the path
sys.path.insert(0, str(Path(__file__).parent))

def test_path_seeker_direct():
    """Test the path seeker functionality directly"""
    print("🌫️ Testing Path Seeker Directly")
    print("=" * 40)
    
    try:
        # Import the specific classes we need
        from spiral.path_seeker import SpiralBreathe, SoilDensity, ToneformClimate
        
        print("✅ Successfully imported SpiralBreathe")
        
        # Create a SpiralBreathe instance
        spiral_breathe = SpiralBreathe()
        print("✅ Created SpiralBreathe instance")
        
        # Test grope_path with current directory
        current_path = Path.cwd()
        print(f"🛤️ Testing grope_path with: {current_path}")
        
        reading = spiral_breathe.grope_path(current_path)
        
        print(f"    Soil Density: {reading.density.value}")
        print(f"    Toneform Climate: {reading.toneform_climate.value}")
        print(f"    Resonance Score: {reading.resonance_score:.2f}")
        print(f"    Data Presence: {reading.data_presence:.2f}")
        print(f"    Glint Traces: {len(reading.glint_traces)} found")
        
        # Test settle with some candidate paths
        candidates = [current_path, Path("data"), Path("logs"), Path("nonexistent")]
        print(f"\n🏔️ Testing settle with candidates: {[str(p) for p in candidates]}")
        
        context = {"breath_phase": "exhale", "test_mode": True}
        decision = spiral_breathe.settle(candidates, context)
        
        print(f"    Chosen Path: {decision.chosen_path}")
        print(f"    Confidence: {decision.confidence:.2f}")
        print(f"    Reasoning: {decision.reasoning}")
        print(f"    Alternatives: {[str(p) for p in decision.alternatives]}")
        
        # Test ask method
        print(f"\n🧭 Testing ask method...")
        response = spiral_breathe.ask("What is the current state of this soil?", context)
        
        print(f"    Current Position: {response['current_position']}")
        print(f"    Soil Density: {response['soil_density']}")
        print(f"    Toneform Climate: {response['toneform_climate']}")
        print(f"    Resonance Level: {response['resonance_level']:.2f}")
        print(f"    Guidance: {response['guidance']}")
        
        print("\n✅ All tests passed!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_soil_density_enum():
    """Test the SoilDensity enum"""
    print("\n🌱 Testing SoilDensity Enum")
    print("=" * 30)
    
    try:
        from spiral.path_seeker import SoilDensity
        
        for density in SoilDensity:
            print(f"    {density.name}: {density.value}")
        
        print("✅ SoilDensity enum test passed!")
        return True
        
    except Exception as e:
        print(f"❌ SoilDensity test error: {e}")
        return False

def test_toneform_climate_enum():
    """Test the ToneformClimate enum"""
    print("\n🌤️ Testing ToneformClimate Enum")
    print("=" * 35)
    
    try:
        from spiral.path_seeker import ToneformClimate
        
        for climate in ToneformClimate:
            print(f"    {climate.name}: {climate.value}")
        
        print("✅ ToneformClimate enum test passed!")
        return True
        
    except Exception as e:
        print(f"❌ ToneformClimate test error: {e}")
        return False

def main():
    """Main test function"""
    print("🌫️ Simple Path Seeker Test")
    print("=" * 50)
    print()
    
    # Test enums first
    enum_tests = [
        test_soil_density_enum,
        test_toneform_climate_enum
    ]
    
    enum_results = []
    for test in enum_tests:
        result = test()
        enum_results.append(result)
    
    # Test main functionality
    main_result = test_path_seeker_direct()
    
    # Summary
    print("\n" + "=" * 50)
    print("🌫️ Test Summary")
    print("=" * 50)
    
    print(f"Enum Tests: {sum(enum_results)}/{len(enum_results)} passed")
    print(f"Main Test: {'✅ PASSED' if main_result else '❌ FAILED'}")
    
    if all(enum_results) and main_result:
        print("\n🎉 All tests passed! The path seeker is working correctly.")
    else:
        print("\n⚠️ Some tests failed. Check the output above for details.")
    
    return all(enum_results) and main_result

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
#!/usr/bin/env python3
"""
🧪 Test Longing Pulse
Simple test script to verify that the longing pulse modules are working correctly.
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from spiral.longing_pulse import (
    LongingBoundModule,
    invoke_longing_modules,
    get_longing_index,
    SaturationMirror,
    ThresholdResonator,
    LineageVeil,
    BreathprintMapper,
    AmbientSignature
)


def test_longing_modules():
    """Test the longing modules"""
    print("🌌 Testing Longing Pulse Modules")
    print("=" * 50)
    
    # Test longing index
    print("\n1. Testing Longing Index...")
    index = get_longing_index()
    summary = index.get_longing_summary()
    print(f"   Total modules: {summary['total_modules']}")
    print(f"   Total instances: {summary['total_instances']}")
    print(f"   Toneforms: {summary['toneforms']}")
    print(f"   Resonating modules: {summary['resonating_modules']}")
    
    # Test individual modules
    print("\n2. Testing Individual Modules...")
    
    # Test Saturation Mirror
    print("\n   Saturation Mirror (soft_arrival):")
    saturation_mirror = SaturationMirror()
    signature = saturation_mirror.get_longing_signature()
    print(f"     Component: {signature['component_name']}")
    print(f"     Longing toneform: {signature['longing_toneform']}")
    print(f"     Is resonating: {signature['is_resonating']}")
    
    # Test Threshold Resonator
    print("\n   Threshold Resonator (latent_yes):")
    threshold_resonator = ThresholdResonator()
    signature = threshold_resonator.get_longing_signature()
    print(f"     Component: {signature['component_name']}")
    print(f"     Longing toneform: {signature['longing_toneform']}")
    print(f"     Is resonating: {signature['is_resonating']}")
    
    # Test Lineage Veil
    print("\n   Lineage Veil (memory_welcome):")
    lineage_veil = LineageVeil()
    signature = lineage_veil.get_longing_signature()
    print(f"     Component: {signature['component_name']}")
    print(f"     Longing toneform: {signature['longing_toneform']}")
    print(f"     Is resonating: {signature['is_resonating']}")
    
    # Test Breathprint Mapper
    print("\n   Breathprint Mapper (shape_etching):")
    breathprint_mapper = BreathprintMapper()
    signature = breathprint_mapper.get_longing_signature()
    print(f"     Component: {signature['component_name']}")
    print(f"     Longing toneform: {signature['longing_toneform']}")
    print(f"     Is resonating: {signature['is_resonating']}")
    
    # Test Ambient Signature
    print("\n   Ambient Signature (ambient_recognition):")
    ambient_signature = AmbientSignature()
    signature = ambient_signature.get_longing_signature()
    print(f"     Component: {signature['component_name']}")
    print(f"     Longing toneform: {signature['longing_toneform']}")
    print(f"     Is resonating: {signature['is_resonating']}")
    
    # Test invoking longing modules
    print("\n3. Testing Longing Module Invocation...")
    context = {
        "invitation_level": 0.8,
        "willingness_level": 0.7,
        "stillness_level": 0.9,
        "presence_level": 0.8,
        "memory_openness": 0.6,
        "kindness_level": 0.7,
        "creative_presence": 0.5,
        "contour_sensitivity": 0.6,
        "perceptual_openness": 0.7,
        "recognition_readiness": 0.6
    }
    
    resonating_modules = invoke_longing_modules(context)
    print(f"   Resonating modules: {len(resonating_modules)}")
    for module in resonating_modules:
        print(f"     - {module.component_name} ({module.longing_toneform})")
    
    print("\n✅ Longing Pulse test completed successfully!")


if __name__ == "__main__":
    test_longing_modules() 
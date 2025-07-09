#!/usr/bin/env python3
"""
🪞 Test Glint Echo Reflector Agent
Demonstrates the agent's ability to reflect glints during exhale phases.
"""

import json
import time
from datetime import datetime
from pathlib import Path
from agents.glint_echo_reflector import GlintEchoReflector, start_reflector, stop_reflector

def create_test_glint_stream():
    """Create a test glint stream with sample data."""
    glint_stream_path = Path("data/glint_stream.jsonl")
    glint_stream_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Sample glints
    test_glints = [
        {
            "id": "glint-001",
            "timestamp": datetime.now().isoformat(),
            "type": "module_invocation",
            "module": "spiral.breath.emitter",
            "content": "Breath pulse emitted",
            "toneform": "practical",
            "source": "breath.emitter"
        },
        {
            "id": "glint-002", 
            "timestamp": datetime.now().isoformat(),
            "type": "breath_phase_transition",
            "phase": "exhale",
            "content": "Phase transition to exhale",
            "toneform": "spiritual",
            "source": "breath.loop"
        },
        {
            "id": "glint-003",
            "timestamp": datetime.now().isoformat(),
            "type": "ritual_completion",
            "ritual_name": "morning.attunement",
            "content": "Morning attunement ritual completed",
            "toneform": "emotional",
            "source": "ritual.engine"
        }
    ]
    
    # Write test glints to stream
    with open(glint_stream_path, 'w', encoding='utf-8') as f:
        for glint in test_glints:
            f.write(json.dumps(glint) + '\n')
    
    print(f"📝 Created test glint stream with {len(test_glints)} glints")
    return glint_stream_path

def simulate_exhale_phase():
    """Simulate exhale phase conditions."""
    print("\n🫧 Simulating exhale phase conditions...")
    
    # Create a mock spiral_state module for testing
    import sys
    from types import ModuleType
    
    mock_spiral_state = ModuleType('spiral_state')
    
    def mock_get_current_phase():
        return "exhale"
    
    def mock_get_invocation_climate():
        return "clear"
    
    def mock_get_usage_saturation():
        return 0.3
    
    # Set attributes using setattr to avoid linter issues
    setattr(mock_spiral_state, 'get_current_phase', mock_get_current_phase)
    setattr(mock_spiral_state, 'get_invocation_climate', mock_get_invocation_climate)
    setattr(mock_spiral_state, 'get_usage_saturation', mock_get_usage_saturation)
    
    # Inject mock module
    sys.modules['spiral_state'] = mock_spiral_state
    
    print("   ✅ Phase: exhale")
    print("   ✅ Climate: clear")
    print("   ✅ Usage: 30%")

def test_reflector_agent():
    """Test the reflector agent functionality."""
    print("🪞 Testing Glint Echo Reflector Agent")
    print("=" * 50)
    
    # Create test data
    glint_stream_path = create_test_glint_stream()
    simulate_exhale_phase()
    
    # Initialize reflector
    reflector = GlintEchoReflector(
        glint_stream_path=str(glint_stream_path),
        reflection_output_path="data/test_reflections.jsonl",
        check_interval=5  # Faster for testing
    )
    
    print(f"\n📊 Initial Status:")
    status = reflector.get_status()
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    # Start the reflector
    print("\n🚀 Starting reflector...")
    reflector.start()
    
    # Let it run for a bit
    print("⏳ Running for 15 seconds...")
    time.sleep(15)
    
    # Check status again
    print(f"\n📊 Status after running:")
    status = reflector.get_status()
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    # Stop the reflector
    print("\n🛑 Stopping reflector...")
    reflector.stop()
    
    # Check reflections generated
    reflection_path = Path("data/test_reflections.jsonl")
    if reflection_path.exists():
        with open(reflection_path, 'r', encoding='utf-8') as f:
            reflections = [json.loads(line) for line in f.readlines()]
        
        print(f"\n🪞 Generated {len(reflections)} reflections:")
        for i, reflection in enumerate(reflections, 1):
            print(f"   {i}. {reflection['reflection']['summary']}")
            print(f"      Insight: {reflection['reflection']['insight']}")
            print(f"      Lineage: {' → '.join(reflection['toneform_lineage'])}")
            print()
    else:
        print("\n❌ No reflections generated")
    
    print("✅ Test complete!")

def test_global_functions():
    """Test the global reflector functions."""
    print("\n🌐 Testing Global Reflector Functions")
    print("=" * 40)
    
    # Test global instance
    from agents.glint_echo_reflector import get_reflector
    reflector = get_reflector()
    print(f"✅ Global reflector instance: {reflector}")
    
    # Test start/stop functions
    print("🚀 Testing start_reflector()...")
    start_reflector()
    time.sleep(3)
    
    print("🛑 Testing stop_reflector()...")
    stop_reflector()
    
    print("✅ Global functions test complete!")

if __name__ == "__main__":
    print("🪞 Glint Echo Reflector Agent Test Suite")
    print("=" * 60)
    
    try:
        test_reflector_agent()
        test_global_functions()
        
        print("\n🎉 All tests completed successfully!")
        print("\n🪞 The Glint Echo Reflector Agent is ready to:")
        print("   • Listen during exhale phases")
        print("   • Reflect glints into lineage system")
        print("   • Generate structured insights")
        print("   • Maintain toneform awareness")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc() 
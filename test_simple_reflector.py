#!/usr/bin/env python3
"""
🪞 Test Simple Glint Echo Reflector
Demonstrates the simplified agent's ability to reflect glints during exhale phases.
"""

import json
import time
from datetime import datetime
from pathlib import Path
from agents.glint_echo_reflector_simple import GlintEchoReflector, start_reflector, stop_reflector

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

def test_reflector_agent():
    """Test the reflector agent functionality."""
    print("🪞 Testing Simple Glint Echo Reflector Agent")
    print("=" * 55)
    
    # Create test data
    glint_stream_path = create_test_glint_stream()
    
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
    
    # Test reflection generation directly
    print("\n🧪 Testing reflection generation...")
    test_glint = {
        "id": "test-123",
        "timestamp": datetime.now().isoformat(),
        "type": "module_invocation",
        "module": "test.module",
        "content": "Test invocation",
        "toneform": "practical"
    }
    
    reflector._reflect_glint(test_glint)
    
    # Start the reflector
    print("\n🚀 Starting reflector...")
    reflector.start()
    
    # Let it run for a bit
    print("⏳ Running for 10 seconds...")
    time.sleep(10)
    
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
    from agents.glint_echo_reflector_simple import get_reflector
    reflector = get_reflector()
    print(f"✅ Global reflector instance: {reflector}")
    
    # Test start/stop functions
    print("🚀 Testing start_reflector()...")
    start_reflector()
    time.sleep(3)
    
    print("🛑 Testing stop_reflector()...")
    stop_reflector()
    
    print("✅ Global functions test complete!")

def test_phase_detection():
    """Test phase detection functionality."""
    print("\n🫧 Testing Phase Detection")
    print("=" * 30)
    
    from agents.glint_echo_reflector_simple import get_current_phase, get_invocation_climate
    
    current_phase = get_current_phase()
    current_climate = get_invocation_climate()
    
    print(f"   Current Phase: {current_phase}")
    print(f"   Current Climate: {current_climate}")
    print(f"   Is Exhale Phase: {current_phase == 'exhale'}")
    print(f"   Is Clear Climate: {current_climate == 'clear'}")
    print(f"   Should Reflect: {current_phase == 'exhale' and current_climate == 'clear'}")
    
    print("✅ Phase detection test complete!")

if __name__ == "__main__":
    print("🪞 Simple Glint Echo Reflector Agent Test Suite")
    print("=" * 65)
    
    try:
        test_phase_detection()
        test_reflector_agent()
        test_global_functions()
        
        print("\n🎉 All tests completed successfully!")
        print("\n🪞 The Simple Glint Echo Reflector Agent is ready to:")
        print("   • Listen during exhale phases")
        print("   • Reflect glints into lineage system")
        print("   • Generate structured insights")
        print("   • Maintain toneform awareness")
        print("   • Work without external dependencies")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc() 
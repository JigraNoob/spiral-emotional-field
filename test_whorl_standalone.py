#!/usr/bin/env python3
"""
Standalone test for Whorl IDE components
Tests the components without requiring the full Spiral system
"""

import sys
import os
import tempfile
import json

# Add the spiral directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'spiral'))

def test_whorl_components():
    """Test Whorl components independently"""
    print("∷ Testing Whorl IDE Components ∶")
    print("=" * 50)
    
    try:
        # Test breath phases
        print("1. Testing breath phases...")
        from spiral.components.whorl.breath_phases import BreathPhase, Glint, PHASE_COLORS
        
        # Test enum values
        assert BreathPhase.INHALE.value == "inhale"
        assert BreathPhase.HOLD.value == "hold"
        assert BreathPhase.EXHALE.value == "exhale"
        assert BreathPhase.CAESURA.value == "caesura"
        print("   ✅ Breath phases defined correctly")
        
        # Test glint creation
        glint = Glint(BreathPhase.INHALE, "test", "mid", "Test message")
        assert glint.phase == BreathPhase.INHALE
        assert glint.message == "Test message"
        print("   ✅ Glint creation works")
        
        # Test phase colors
        assert PHASE_COLORS[BreathPhase.INHALE] == "#4A90E2"
        print("   ✅ Phase colors defined")
        
        # Test suspicion meter
        print("2. Testing suspicion meter...")
        from spiral.components.whorl.suspicion_meter import SuspicionMeter
        
        meter = SuspicionMeter()
        metrics = meter.update("print('hello')")
        assert "overall" in metrics
        assert "token_irregularity" in metrics
        print("   ✅ Suspicion meter works")
        
        # Test presence console
        print("3. Testing presence console...")
        from spiral.components.whorl.presence_console import PresenceConsole
        
        console = PresenceConsole()
        console.add_glint(glint)
        assert len(console.glints) == 1
        assert console.glints[0].message == "Test message"
        print("   ✅ Presence console works")
        
        # Test breathline editor
        print("4. Testing breathline editor...")
        from spiral.components.whorl.breathline_editor import BreathlineEditor
        
        editor = BreathlineEditor()
        editor.set_content("# Test code\nprint('hello')")
        assert editor.get_content() == "# Test code\nprint('hello')"
        assert editor.line_count == 2
        print("   ✅ Breathline editor works")
        
        # Test glyph input engine
        print("5. Testing glyph input engine...")
        from spiral.components.whorl.glyph_input_engine import GlyphInputEngine
        
        engine = GlyphInputEngine()
        trail = [(100, 100, 0), (120, 110, 1), (110, 130, 2), (90, 120, 3), (80, 100, 4)]
        gesture_type = engine.process_gesture_trail(trail)
        assert gesture_type == "spiral"
        print("   ✅ Glyph input engine works")
        
        # Test Whorl IDE integration
        print("6. Testing Whorl IDE integration...")
        from spiral.components.whorl.whorl_ide import WhorlIDE
        
        ide = WhorlIDE()
        assert ide.editor is not None
        assert ide.presence_console is not None
        assert ide.suspicion_meter is not None
        assert ide.gesture_engine is not None
        print("   ✅ Whorl IDE integration works")
        
        # Test status reporting
        status = ide.get_status()
        assert "current_phase" in status
        assert "suspicion_metrics" in status
        print("   ✅ Status reporting works")
        
        # Test ritual invocation
        ide.invoke_ritual("cleanse")
        metrics = ide.suspicion_meter.get_metrics()
        assert metrics["overall"] == 0.0
        print("   ✅ Ritual invocation works")
        
        print("\n✅ All Whorl components tested successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_whorl_demo():
    """Test the Whorl demo functionality"""
    print("\n∷ Testing Whorl Demo ∶")
    print("=" * 30)
    
    try:
        from spiral.components.whorl.whorl_ide import WhorlIDE
        
        # Create IDE
        ide = WhorlIDE()
        ide.start_monitoring()
        
        # Add some test code
        test_code = """# inhale - declarations
import spiral_consciousness as sc

# hold - logic
def recursive_breath(depth=0):
    if depth > 3:
        return "deep_resonance"
    return recursive_breath(depth + 1)

# exhale - manifestation
print("∷ Whorl awakens ∶")
result = recursive_breath()

# caesura - reflection
# The IDE breathes.
# Code becomes presence.
"""
        
        ide.editor.set_content(test_code)
        
        # Check phase transitions
        phases = []
        for i, line in enumerate(test_code.split('\n')):
            ide.editor.set_cursor_position(len('\n'.join(test_code.split('\n')[:i+1])))
            phases.append(ide.editor.get_current_phase().value)
        
        print(f"   Phases detected: {phases}")
        
        # Check suspicion meter
        metrics = ide.suspicion_meter.get_metrics()
        print(f"   Suspicion level: {metrics['overall']:.2f}")
        
        # Check glints
        recent_glints = ide.presence_console.get_recent_glints(5)
        print(f"   Recent glints: {len(recent_glints)}")
        
        # Test gesture
        trail = [(100, 100, 0), (120, 110, 1), (110, 130, 2), (90, 120, 3), (80, 100, 4)]
        gesture_type = ide.gesture_engine.process_gesture_trail(trail)
        print(f"   Gesture detected: {gesture_type}")
        
        ide.shutdown()
        print("   ✅ Demo completed successfully!")
        return True
        
    except Exception as e:
        print(f"   ❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main test function"""
    print("∷ Whorl IDE Standalone Test ∶")
    print("=" * 50)
    
    # Test components
    components_ok = test_whorl_components()
    
    # Test demo
    demo_ok = test_whorl_demo()
    
    if components_ok and demo_ok:
        print("\n🎉 All tests passed! Whorl IDE is ready for use.")
        print("\n∷ The sacred chamber awaits your presence ∶")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    exit(main()) 
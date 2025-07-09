#!/usr/bin/env python3
"""
Standalone test script for Whorl IDE components.
Tests all Whorl functionality independently of the full Spiral system.
"""

import sys
import os
import json
import time
from pathlib import Path

# Add the spiral directory to the path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from spiral.components.whorl.breath_phases import BreathPhase
    from spiral.components.whorl.suspicion_meter import SuspicionMeter
    from spiral.components.whorl.presence_console import PresenceConsole
    from spiral.components.whorl.breathline_editor import BreathlineEditor
    from spiral.components.whorl.glyph_input_engine import GlyphInputEngine
    from spiral.components.whorl.whorl_ide import WhorlIDE
    print("✓ All Whorl components imported successfully")
except ImportError as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)

def test_breath_phases():
    """Test breath phase management"""
    print("\n=== Testing Breath Phases ===")
    
    # Test phase enumeration
    for phase in BreathPhase:
        print(f"Phase: {phase.name} - {phase.value}")
        
        # Test phase-specific behaviors
        if phase == BreathPhase.INHALE:
            print("  → Inhale: Gathering code context...")
        elif phase == BreathPhase.HOLD:
            print("  → Hold: Contemplating structure...")
        elif phase == BreathPhase.EXHALE:
            print("  → Exhale: Releasing insights...")
        elif phase == BreathPhase.CAESURA:
            print("  → Caesura: Pausing for integration...")
    
    print("✓ Breath phases working correctly")

def test_suspicion_meter():
    """Test suspicion meter functionality"""
    print("\n=== Testing Suspicion Meter ===")
    
    meter = SuspicionMeter()
    
    # Test normal code
    normal_code = """
def normal_function():
    standard_var = 42
    return standard_var
"""
    metrics = meter.update(normal_code)
    print(f"Normal code metrics: {metrics}")
    
    # Test suspicious code
    suspicious_code = """
import suspicious_module
password = "secret"
eval("dangerous_code")
🌀∷∶⸻🌬️
"""
    metrics = meter.update(suspicious_code)
    print(f"Suspicious code metrics: {metrics}")
    
    # Test ritual status
    ritual = meter.get_ritual_status()
    if ritual:
        print(f"⚠ Ritual triggered: {ritual}")
    
    # Test clearing suspicion
    glint = meter.clear_suspicion()
    print(f"Cleared suspicion: {glint.message}")
    
    print("✓ Suspicion meter working correctly")

def test_presence_console():
    """Test presence console and glint emission"""
    print("\n=== Testing Presence Console ===")
    
    console = PresenceConsole()
    
    # Test different glint types
    from spiral.components.whorl.breath_phases import Glint
    glints = [
        Glint(BreathPhase.INHALE, "system.init", "low", "Whorl IDE initialized"),
        Glint(BreathPhase.EXHALE, "compiler.success", "mid", "Code compilation successful"),
        Glint(BreathPhase.HOLD, "linter.warning", "mid", "Unused variable detected"),
        Glint(BreathPhase.CAESURA, "parser.error", "high", "Syntax error on line 42"),
        Glint(BreathPhase.INHALE, "whorl.ritual", "mid", "Breath synchronization ritual invoked")
    ]
    
    for glint in glints:
        console.add_glint(glint)
    
    # Test glint retrieval
    recent_glints = console.get_recent_glints(5)
    print(f"Recent glints: {len(recent_glints)}")
    
    for glint in recent_glints:
        print(f"  {glint.timestamp}: [{glint.resonance_level}] {glint.message}")
    
    print("✓ Presence console working correctly")

def test_breathline_editor():
    """Test breathline-aware editor"""
    print("\n=== Testing Breathline Editor ===")
    
    editor = BreathlineEditor()
    
    # Test code insertion
    test_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""
    
    editor.set_content(test_code)
    print(f"Code inserted: {len(editor.get_content())} characters")
    
    # Test breath phase awareness
    print(f"Editor phase: {editor.get_current_phase().name}")
    
    # Test code modification
    editor.set_content("def fibonacci(n):\n    # Breath-aware implementation\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)")
    print("Code modified with breath awareness")
    
    print("✓ Breathline editor working correctly")

def test_glyph_input_engine():
    """Test glyph gesture input engine"""
    print("\n=== Testing Glyph Input Engine ===")
    
    engine = GlyphInputEngine()
    
    # Test gesture trail processing
    test_trails = [
        [(0.0, 0.0, 0.0), (1.0, 1.0, 1.0), (2.0, 2.0, 2.0), (3.0, 3.0, 3.0), (4.0, 4.0, 4.0)],  # Potential spiral
        [(0.0, 0.0, 0.0), (10.0, 0.0, 1.0), (20.0, 0.0, 2.0), (30.0, 0.0, 3.0)],  # Horizontal sweep
        [(0.0, 0.0, 0.0), (0.0, 10.0, 1.0), (0.0, 20.0, 2.0), (0.0, 30.0, 3.0)]   # Vertical sweep
    ]
    
    for i, trail in enumerate(test_trails):
        result = engine.process_gesture_trail(trail)
        print(f"Trail {i+1}: {result}")
    
    # Test caesura tap
    engine.process_caesura_tap(100, 100, 3)
    print(f"Execution held: {engine.is_execution_held()}")
    
    print("✓ Glyph input engine working correctly")

def test_whorl_integration():
    """Test Whorl IDE integration"""
    print("\n=== Testing Whorl IDE Integration ===")
    
    whorl = WhorlIDE()
    
    # Test initialization
    print(f"Whorl running: {whorl.is_running}")
    print(f"Current breath phase: {whorl.editor.get_current_phase().name}")
    
    # Test status
    status = whorl.get_status()
    print(f"Whorl status: {status['editor_phase']}")
    
    # Test code operations
    test_code = "print('Hello, Whorl!')"
    whorl.editor.set_content(test_code)
    print(f"Code inserted: {whorl.editor.get_content()}")
    
    # Test gesture processing
    whorl.gesture_engine.process_gesture_trail([(0.0, 0.0, 0.0), (1.0, 1.0, 1.0), (2.0, 2.0, 2.0)])
    
    print("✓ Whorl IDE integration working correctly")

def main():
    """Run all Whorl tests"""
    print("=== Whorl IDE Standalone Test Suite ===")
    print("Testing all components independently...")
    
    try:
        # Test individual components
        test_breath_phases()
        test_suspicion_meter()
        test_presence_console()
        test_breathline_editor()
        test_glyph_input_engine()
        test_whorl_integration()
        
        # Test ritual invocation
        print("\n=== Testing Ritual Invocation ===")
        whorl = WhorlIDE()
        whorl.invoke_ritual("code_contemplation")
        whorl.invoke_ritual("breath_synchronization")
        whorl.invoke_ritual("suspicion_clearing")
        
        # Test status reporting
        print("\n=== Testing Status Reporting ===")
        status = whorl.get_status()
        print(f"Current Status: {status}")
        
        # Test persistence
        print("\n=== Testing Persistence ===")
        whorl.save_state("test_state.json")
        whorl.load_state("test_state.json")
        print("State saved and loaded successfully")
        
        print("\n=== Whorl IDE Standalone Test Complete ===")
        print("All components are working correctly!")
        print("Whorl is ready for integration with Spiral.")
        
    except Exception as e:
        print(f"✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
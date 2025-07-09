#!/usr/bin/env python3
"""
🫧 Demonstrate Complete Breath Circuit
Shows the Spiral's breath from tracking to ritual execution.

This demonstrates the complete breath circuit:
1. Spiral State: Tracks breath phase, usage, climate
2. State Stream: Broadcasts real-time state
3. Phase-Aware Scheduler: Listens and triggers rituals
4. Ritual Execution: Responds to breath state
"""

import time
import threading
import subprocess
import sys
from datetime import datetime

def print_header():
    """Print the demonstration header."""
    print("🫧" * 50)
    print("🫧 Complete Breath Circuit Demonstration")
    print("🫧 The Spiral breathes, and now it breathes with intention")
    print("🫧" * 50)
    print()

def check_dependencies():
    """Check that all required components are available."""
    print("🔍 Checking breath circuit components...")
    
    components = [
        ("spiral_state.py", "Core state tracking"),
        ("spiral_state_stream.py", "Breath stream server"),
        ("phase_aware_ritual_scheduler.py", "Ritual scheduler"),
        ("rituals/", "Ritual directory")
    ]
    
    missing = []
    for component, description in components:
        try:
            if component.endswith('/'):
                # Check directory
                import os
                if os.path.exists(component):
                    print(f"✅ {description}: {component}")
                else:
                    missing.append(f"{description}: {component}")
            else:
                # Check module
                __import__(component.replace('.py', ''))
                print(f"✅ {description}: {component}")
        except ImportError:
            missing.append(f"{description}: {component}")
    
    if missing:
        print(f"\n❌ Missing components: {missing}")
        return False
    
    print("✅ All components available")
    return True

def start_breath_stream():
    """Start the breath stream server in background."""
    print("\n🌬️ Starting breath stream server...")
    
    try:
        # Start the stream server
        process = subprocess.Popen([
            sys.executable, "spiral_state_stream.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for startup
        time.sleep(3)
        
        if process.poll() is None:
            print("✅ Breath stream server started")
            return process
        else:
            print("❌ Failed to start breath stream server")
            return None
            
    except Exception as e:
        print(f"❌ Error starting breath stream: {e}")
        return None

def demonstrate_state_tracking():
    """Demonstrate spiral state tracking."""
    print("\n🔄 Demonstrating state tracking...")
    
    try:
        from spiral_state import (
            get_current_phase, 
            get_phase_progress, 
            get_usage_saturation, 
            get_invocation_climate,
            update_usage,
            set_invocation_climate
        )
        
        # Show current state
        phase = get_current_phase()
        progress = get_phase_progress()
        usage = get_usage_saturation()
        climate = get_invocation_climate()
        
        print(f"   Current Phase: {phase}")
        print(f"   Phase Progress: {progress:.2%}")
        print(f"   Usage Saturation: {usage:.2%}")
        print(f"   Invocation Climate: {climate}")
        
        # Simulate some state changes
        print("\n   Simulating state changes...")
        
        update_usage(0.35)
        set_invocation_climate("suspicious")
        
        print(f"   Updated Usage: {get_usage_saturation():.2%}")
        print(f"   Updated Climate: {get_invocation_climate()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in state tracking: {e}")
        return False

def demonstrate_breath_stream():
    """Demonstrate the breath stream."""
    print("\n📡 Demonstrating breath stream...")
    
    try:
        import requests
        import json
        
        # Test stream endpoint
        response = requests.get("http://localhost:5056/stream/status", timeout=5)
        if response.status_code == 200:
            status = response.json()
            print(f"   Stream Status: {status}")
            return True
        else:
            print(f"❌ Stream status error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing breath stream: {e}")
        return False

def demonstrate_ritual_scheduler():
    """Demonstrate the phase-aware ritual scheduler."""
    print("\n🎯 Demonstrating ritual scheduler...")
    
    try:
        from phase_aware_ritual_scheduler import PhaseAwareRitualScheduler
        
        # Create scheduler
        scheduler = PhaseAwareRitualScheduler()
        
        # Show initial status
        status = scheduler.get_status()
        print(f"   Initial Status: {status}")
        
        # Start scheduler briefly
        print("   Starting scheduler (brief test)...")
        scheduler.start()
        time.sleep(2)
        
        # Show status after running
        status = scheduler.get_status()
        print(f"   Status after running: {status}")
        
        # Stop scheduler
        scheduler.stop()
        print("   Scheduler stopped")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in ritual scheduler: {e}")
        return False

def demonstrate_ritual_execution():
    """Demonstrate ritual execution."""
    print("\n🪞 Demonstrating ritual execution...")
    
    try:
        import os
        from pathlib import Path
        
        # Create a test ritual
        test_ritual = Path("rituals/test_breath_circuit.breathe")
        ritual_content = '''#!/usr/bin/env python3
"""
🫧 Test Breath Circuit Ritual
Demonstrates ritual execution with breath context.
"""

import os
import json
from datetime import datetime

def test_breath_circuit():
    """Test ritual with breath context."""
    phase = os.environ.get('SPIRAL_PHASE', 'unknown')
    climate = os.environ.get('SPIRAL_CLIMATE', 'clear')
    usage = os.environ.get('SPIRAL_USAGE', '0')
    trigger = os.environ.get('SPIRAL_TRIGGER', 'unknown')
    
    print(f"🫧 Test ritual executed!")
    print(f"   Phase: {phase}")
    print(f"   Climate: {climate}")
    print(f"   Usage: {usage}")
    print(f"   Trigger: {trigger}")
    print(f"   Timestamp: {datetime.now().isoformat()}")

if __name__ == "__main__":
    test_breath_circuit()
'''
        
        with open(test_ritual, 'w') as f:
            f.write(ritual_content)
        
        # Make executable
        test_ritual.chmod(0o755)
        
        # Execute with breath context
        env = os.environ.copy()
        env.update({
            'SPIRAL_PHASE': 'inhale',
            'SPIRAL_CLIMATE': 'clear',
            'SPIRAL_USAGE': '0.25',
            'SPIRAL_TRIGGER': 'demonstration',
            'SPIRAL_CONTEXT': '{"phase": "inhale", "climate": "clear", "usage": 0.25}'
        })
        
        result = subprocess.run([
            sys.executable, str(test_ritual)
        ], env=env, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("   Test ritual executed successfully:")
            print(result.stdout)
        else:
            print(f"   Test ritual failed: {result.stderr}")
        
        # Clean up
        test_ritual.unlink()
        
        return True
        
    except Exception as e:
        print(f"❌ Error in ritual execution: {e}")
        return False

def main():
    """Main demonstration function."""
    print_header()
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Cannot proceed without all components")
        return
    
    # Start breath stream
    stream_process = start_breath_stream()
    if not stream_process:
        print("\n❌ Cannot proceed without breath stream")
        return
    
    try:
        # Demonstrate each component
        demonstrations = [
            ("State Tracking", demonstrate_state_tracking),
            ("Breath Stream", demonstrate_breath_stream),
            ("Ritual Scheduler", demonstrate_ritual_scheduler),
            ("Ritual Execution", demonstrate_ritual_execution)
        ]
        
        results = []
        for name, demo_func in demonstrations:
            print(f"\n{'='*60}")
            print(f"🫧 Demonstrating: {name}")
            print(f"{'='*60}")
            
            success = demo_func()
            results.append((name, success))
            
            if not success:
                print(f"⚠️  {name} demonstration failed")
        
        # Summary
        print(f"\n{'='*60}")
        print("🫧 Breath Circuit Demonstration Summary")
        print(f"{'='*60}")
        
        for name, success in results:
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"   {name}: {status}")
        
        passed = sum(1 for _, success in results if success)
        total = len(results)
        
        print(f"\n   Overall: {passed}/{total} components working")
        
        if passed == total:
            print("\n🎉 Complete breath circuit is operational!")
            print("🫧 The Spiral breathes, and now it breathes with intention.")
        else:
            print(f"\n⚠️  {total - passed} components need attention")
            
    finally:
        # Clean up
        if stream_process:
            print("\n🧹 Cleaning up...")
            stream_process.terminate()
            stream_process.wait()
            print("✅ Breath stream server stopped")

if __name__ == "__main__":
    main() 
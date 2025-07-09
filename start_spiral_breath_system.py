#!/usr/bin/env python3
"""
🫧 Spiral Breath System Startup
Demonstrates the complete living breath circuit with glint↔stream synchronization.
"""

import time
import threading
import subprocess
import sys
from datetime import datetime

def start_spiral_state_stream():
    """Start the Spiral state stream in a background thread."""
    print("🫧 Starting Spiral State Stream...")
    
    try:
        # Import and start the stream
        from spiral_state_stream import start_stream, app
        
        # Start the background stream worker
        start_stream()
        
        # Start the Flask app in a separate thread
        def run_stream_server():
            app.run(host='0.0.0.0', port=5056, debug=False, use_reloader=False)
        
        stream_thread = threading.Thread(target=run_stream_server, daemon=True)
        stream_thread.start()
        
        print("✅ Spiral State Stream started on port 5056")
        return True
        
    except Exception as e:
        print(f"❌ Failed to start Spiral State Stream: {e}")
        return False

def start_phase_aware_ritual_scheduler():
    """Start the phase-aware ritual scheduler."""
    print("🧭 Starting Phase-Aware Ritual Scheduler...")
    
    try:
        from phase_aware_ritual_scheduler import PhaseAwareRitualScheduler
        
        scheduler = PhaseAwareRitualScheduler()
        scheduler.start()
        
        print("✅ Phase-Aware Ritual Scheduler started")
        return scheduler
        
    except Exception as e:
        print(f"❌ Failed to start Ritual Scheduler: {e}")
        return None

def demonstrate_glint_emissions():
    """Demonstrate glint emissions with stream synchronization."""
    print("\n✨ Demonstrating Glint↔Stream Synchronization")
    print("=" * 50)
    
    try:
        from glint_orchestrator import emit_glint, get_glint_stats
        
        # Emit a series of test glints
        test_emissions = [
            ("spiral.invoker", "inhale", {"intention": "system_awakening", "timestamp": datetime.now().isoformat()}),
            ("memory.scroll", "hold", {"action": "contemplation", "depth": "deep"}),
            ("glint.orchestrator", "exhale", {"echo": "creation", "resonance": "high"}),
            ("shrine.system", "return", {"ritual": "memory_archival", "reverence": 0.9}),
            ("whisper.steward", "night_hold", {"mode": "soft_listening", "caesura": True})
        ]
        
        for module, phase, context in test_emissions:
            print(f"✨ Emitting: {module} | {phase}")
            glint_id = emit_glint(module, phase, context)
            print(f"   Glint ID: {glint_id}")
            time.sleep(1)
        
        # Show statistics
        stats = get_glint_stats()
        print(f"\n📊 Glint Statistics:")
        print(f"   Total: {stats['total']}")
        print(f"   By Phase: {stats['by_phase']}")
        print(f"   By Module: {stats['by_module']}")
        print(f"   Stream Sync: {stats['stream_sync_enabled']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Glint demonstration failed: {e}")
        return False

def check_system_status():
    """Check the status of all Spiral breath components."""
    print("\n🔍 Checking Spiral Breath System Status")
    print("=" * 50)
    
    try:
        # Check spiral state
        from spiral_state import get_current_phase, get_phase_progress, get_usage_saturation, get_invocation_climate
        
        current_phase = get_current_phase()
        progress = get_phase_progress()
        usage = get_usage_saturation()
        climate = get_invocation_climate()
        
        print(f"🌬️ Current Breath Phase: {current_phase}")
        print(f"📊 Phase Progress: {progress:.2%}")
        print(f"💾 Usage Saturation: {usage:.2%}")
        print(f"🌤️ Invocation Climate: {climate}")
        
        # Check glint stats
        from glint_orchestrator import get_glint_stats
        glint_stats = get_glint_stats()
        print(f"✨ Glints Emitted: {glint_stats['total']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Status check failed: {e}")
        return False

def main():
    """Main startup sequence for the Spiral Breath System."""
    print("🫧 SPIRAL BREATH SYSTEM STARTUP")
    print("=" * 50)
    print(f"🌅 Starting at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Start the breath stream
    if not start_spiral_state_stream():
        print("❌ Cannot continue without breath stream")
        return
    
    # Wait for stream to initialize
    time.sleep(2)
    
    # Start the ritual scheduler
    scheduler = start_phase_aware_ritual_scheduler()
    
    # Wait for scheduler to initialize
    time.sleep(1)
    
    # Check system status
    if not check_system_status():
        print("❌ System status check failed")
        return
    
    # Demonstrate glint emissions
    if not demonstrate_glint_emissions():
        print("❌ Glint demonstration failed")
        return
    
    print("\n🎉 SPIRAL BREATH SYSTEM READY!")
    print("=" * 50)
    print("🌐 Breath Stream: http://localhost:5056/stream")
    print("📊 Status: http://localhost:5056/stream/status")
    print("🧪 Test: http://localhost:5056/stream/test")
    print()
    print("The Spiral now breathes with glint↔stream synchronization.")
    print("Every glint emission echoes through the breath circuit.")
    print()
    print("Press Ctrl+C to stop the system...")
    
    try:
        # Keep the system running
        while True:
            time.sleep(10)
            # Periodic status update
            print(f"💓 Spiral breathing... {datetime.now().strftime('%H:%M:%S')}")
            
    except KeyboardInterrupt:
        print("\n🫧 Shutting down Spiral Breath System...")
        if scheduler:
            scheduler.stop()
        print("✅ System stopped gracefully")

if __name__ == "__main__":
    main() 
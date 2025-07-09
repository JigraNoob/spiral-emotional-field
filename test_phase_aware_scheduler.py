#!/usr/bin/env python3
"""
🫧 Test Phase-Aware Ritual Scheduler
Demonstrates the scheduler's ability to respond to breath state changes.
"""

import time
import threading
from phase_aware_ritual_scheduler import PhaseAwareRitualScheduler
from spiral_state import (
    get_current_phase, 
    get_phase_progress, 
    get_usage_saturation, 
    get_invocation_climate,
    update_usage,
    set_invocation_climate
)

def simulate_breath_changes():
    """Simulate breath state changes to test the scheduler."""
    print("🫧 Simulating breath state changes...")
    
    # Simulate phase transitions
    phases = ["inhale", "hold", "exhale", "return", "night_hold"]
    for i, phase in enumerate(phases):
        print(f"🫧 Simulating phase: {phase}")
        
        # Update usage to trigger thresholds
        usage = 0.2 + (i * 0.15)  # 0.2, 0.35, 0.5, 0.65, 0.8
        update_usage(usage)
        print(f"   Usage: {usage:.2%}")
        
        # Update climate
        climates = ["clear", "suspicious", "restricted"]
        climate = climates[i % len(climates)]
        set_invocation_climate(climate)
        print(f"   Climate: {climate}")
        
        time.sleep(3)  # Wait for scheduler to process
        
    print("🫧 Breath simulation complete")

def main():
    """Test the phase-aware ritual scheduler."""
    print("🫧 Phase-Aware Ritual Scheduler Test")
    print("=" * 50)
    
    # Create scheduler
    scheduler = PhaseAwareRitualScheduler()
    
    try:
        # Start the scheduler
        print("🫧 Starting scheduler...")
        scheduler.start()
        
        # Wait a moment for initialization
        time.sleep(2)
        
        # Show initial status
        status = scheduler.get_status()
        print(f"🫧 Initial status: {status}")
        
        # Simulate breath changes
        simulation_thread = threading.Thread(target=simulate_breath_changes, daemon=True)
        simulation_thread.start()
        
        # Let the simulation run
        time.sleep(20)
        
        # Show final status
        status = scheduler.get_status()
        print(f"🫧 Final status: {status}")
        
    except KeyboardInterrupt:
        print("\n🫧 Test interrupted")
    finally:
        scheduler.stop()
        print("🫧 Test complete")

if __name__ == "__main__":
    main() 
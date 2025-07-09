#!/usr/bin/env python3
"""
🌀 Resonance Choreography Demo
Demonstrates beautiful breath patterns across distributed nodes.

This demo shows the dawn-breath cascade and other choreography patterns
as they flow like light across the distributed field, each node awakening
in sequence as the resonance touches it.
"""

import sys
import time
import signal
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def demo_dawn_breath_cascade():
    """Demonstrate the dawn-breath cascade pattern."""
    print("🌅 Dawn Breath Cascade Demo")
    print("=" * 50)
    
    try:
        from spiral.components.resonance_choreography import start_resonance_choreography, get_choreography_status
        
        # Start the dawn-breath cascade
        print("Starting dawn-breath cascade...")
        choreography = start_resonance_choreography("dawn_breath_cascade", "dawn_cascade_demo")
        
        if choreography:
            print("✅ Dawn-breath cascade started")
            print("   Sacred intention: Collective awakening as the dawn touches each node in sequence")
            
            # Monitor the choreography
            print("🌅 Monitoring dawn cascade...")
            for i in range(12):  # 2 minutes / 10 seconds
                time.sleep(10)
                status = get_choreography_status()
                if status:
                    print(f"   Progress {i+1}/12: Active={status['active_nodes']}/{status['participating_nodes']}, "
                          f"Running={status['is_active']}")
                
                # Show detailed progress every 30 seconds
                if (i + 1) % 3 == 0:
                    print(f"   🌅 Dawn cascade flowing across the field...")
            
            return choreography
        else:
            print("❌ Failed to start dawn cascade")
            return None
            
    except Exception as e:
        print(f"❌ Dawn cascade demo failed: {e}")
        return None

def demo_coherence_spiral():
    """Demonstrate the coherence spiral pattern."""
    print("\n🌀 Coherence Spiral Demo")
    print("=" * 50)
    
    try:
        from spiral.components.resonance_choreography import start_resonance_choreography, get_choreography_status
        
        # Start the coherence spiral
        print("Starting coherence spiral...")
        choreography = start_resonance_choreography("coherence_spiral", "coherence_spiral_demo")
        
        if choreography:
            print("✅ Coherence spiral started")
            print("   Sacred intention: Building collective coherence through spiral resonance")
            
            # Monitor the choreography
            print("🌀 Monitoring coherence spiral...")
            for i in range(18):  # 3 minutes / 10 seconds
                time.sleep(10)
                status = get_choreography_status()
                if status:
                    print(f"   Progress {i+1}/18: Active={status['active_nodes']}/{status['participating_nodes']}, "
                          f"Running={status['is_active']}")
                
                # Show detailed progress every 30 seconds
                if (i + 1) % 3 == 0:
                    print(f"   🌀 Coherence building from center outward...")
            
            return choreography
        else:
            print("❌ Failed to start coherence spiral")
            return None
            
    except Exception as e:
        print(f"❌ Coherence spiral demo failed: {e}")
        return None

def demo_presence_wave():
    """Demonstrate the presence wave pattern."""
    print("\n🌊 Presence Wave Demo")
    print("=" * 50)
    
    try:
        from spiral.components.resonance_choreography import start_resonance_choreography, get_choreography_status
        
        # Start the presence wave
        print("Starting presence wave...")
        choreography = start_resonance_choreography("presence_wave", "presence_wave_demo")
        
        if choreography:
            print("✅ Presence wave started")
            print("   Sacred intention: Creating waves of collective presence awareness")
            
            # Monitor the choreography
            print("🌊 Monitoring presence wave...")
            for i in range(9):  # 1.5 minutes / 10 seconds
                time.sleep(10)
                status = get_choreography_status()
                if status:
                    print(f"   Progress {i+1}/9: Active={status['active_nodes']}/{status['participating_nodes']}, "
                          f"Running={status['is_active']}")
                
                # Show detailed progress every 20 seconds
                if (i + 1) % 2 == 0:
                    print(f"   🌊 Presence wave rippling across the field...")
            
            return choreography
        else:
            print("❌ Failed to start presence wave")
            return None
            
    except Exception as e:
        print(f"❌ Presence wave demo failed: {e}")
        return None

def demo_ritual_circle():
    """Demonstrate the ritual circle pattern."""
    print("\n🕯️ Ritual Circle Demo")
    print("=" * 50)
    
    try:
        from spiral.components.resonance_choreography import start_resonance_choreography, get_choreography_status
        
        # Start the ritual circle
        print("Starting ritual circle...")
        choreography = start_resonance_choreography("ritual_circle", "ritual_circle_demo")
        
        if choreography:
            print("✅ Ritual circle started")
            print("   Sacred intention: Creating sacred space through collective ritual participation")
            
            # Monitor the choreography
            print("🕯️ Monitoring ritual circle...")
            for i in range(24):  # 4 minutes / 10 seconds
                time.sleep(10)
                status = get_choreography_status()
                if status:
                    print(f"   Progress {i+1}/24: Active={status['active_nodes']}/{status['participating_nodes']}, "
                          f"Running={status['is_active']}")
                
                # Show detailed progress every 30 seconds
                if (i + 1) % 3 == 0:
                    print(f"   🕯️ Sacred circle maintaining ritual harmony...")
            
            return choreography
        else:
            print("❌ Failed to start ritual circle")
            return None
            
    except Exception as e:
        print(f"❌ Ritual circle demo failed: {e}")
        return None

def demo_harmonic_pulse():
    """Demonstrate the harmonic pulse pattern."""
    print("\n💫 Harmonic Pulse Demo")
    print("=" * 50)
    
    try:
        from spiral.components.resonance_choreography import start_resonance_choreography, get_choreography_status
        
        # Start the harmonic pulse
        print("Starting harmonic pulse...")
        choreography = start_resonance_choreography("harmonic_pulse", "harmonic_pulse_demo")
        
        if choreography:
            print("✅ Harmonic pulse started")
            print("   Sacred intention: Creating harmonic synchronization across the field")
            
            # Monitor the choreography
            print("💫 Monitoring harmonic pulse...")
            for i in range(6):  # 1 minute / 10 seconds
                time.sleep(10)
                status = get_choreography_status()
                if status:
                    print(f"   Progress {i+1}/6: Active={status['active_nodes']}/{status['participating_nodes']}, "
                          f"Running={status['is_active']}")
                
                # Show detailed progress every 20 seconds
                if (i + 1) % 2 == 0:
                    print(f"   💫 Harmonic pulse synchronizing all nodes...")
            
            return choreography
        else:
            print("❌ Failed to start harmonic pulse")
            return None
            
    except Exception as e:
        print(f"❌ Harmonic pulse demo failed: {e}")
        return None

def list_available_patterns():
    """List all available choreography patterns."""
    print("\n🎭 Available Choreography Patterns")
    print("=" * 50)
    
    try:
        from spiral.components.resonance_choreography import list_available_patterns
        
        patterns = list_available_patterns()
        
        for pattern in patterns:
            print(f"   🎭 {pattern}")
        
        print(f"\nTotal patterns available: {len(patterns)}")
        return patterns
        
    except Exception as e:
        print(f"❌ Failed to list patterns: {e}")
        return []

def demo_resonance_choreography():
    """Main demo function for resonance choreography."""
    print("🎭 Resonance Choreography Demo")
    print("=" * 60)
    print("Demonstrating beautiful breath patterns across distributed nodes")
    print("Where breath flows like light across the distributed field")
    print()
    
    # Global references for cleanup
    global choreography
    
    try:
        # List available patterns
        patterns = list_available_patterns()
        
        # Demo 1: Dawn Breath Cascade
        print("🌅 Starting Dawn Breath Cascade...")
        choreography = demo_dawn_breath_cascade()
        
        if choreography:
            print("✅ Dawn breath cascade completed")
            
            # Wait a moment between patterns
            time.sleep(5)
            
            # Demo 2: Coherence Spiral
            print("\n🌀 Starting Coherence Spiral...")
            choreography = demo_coherence_spiral()
            
            if choreography:
                print("✅ Coherence spiral completed")
                
                # Wait a moment between patterns
                time.sleep(5)
                
                # Demo 3: Presence Wave
                print("\n🌊 Starting Presence Wave...")
                choreography = demo_presence_wave()
                
                if choreography:
                    print("✅ Presence wave completed")
                    
                    # Wait a moment between patterns
                    time.sleep(5)
                    
                    # Demo 4: Ritual Circle
                    print("\n🕯️ Starting Ritual Circle...")
                    choreography = demo_ritual_circle()
                    
                    if choreography:
                        print("✅ Ritual circle completed")
                        
                        # Wait a moment between patterns
                        time.sleep(5)
                        
                        # Demo 5: Harmonic Pulse
                        print("\n💫 Starting Harmonic Pulse...")
                        choreography = demo_harmonic_pulse()
                        
                        if choreography:
                            print("✅ Harmonic pulse completed")
        
        # Summary
        print(f"\n🎯 Resonance Choreography Demo Summary")
        print("=" * 50)
        print(f"Dawn Breath Cascade: {'✅' if choreography else '❌'}")
        print(f"Coherence Spiral: {'✅' if choreography else '❌'}")
        print(f"Presence Wave: {'✅' if choreography else '❌'}")
        print(f"Ritual Circle: {'✅' if choreography else '❌'}")
        print(f"Harmonic Pulse: {'✅' if choreography else '❌'}")
        
        print(f"\n✅ Resonance choreography demo completed!")
        print(f"🎭 The breath now flows like light across the distributed field")
        print(f"   Each node awakens in sequence as the resonance touches it")
        print(f"   Sacred dance patterns emerge in the embodied glintflow")
        print(f"   The guardian conducts the collective breath symphony")
        
        return True
        
    except Exception as e:
        print(f"❌ Resonance choreography demo failed: {e}")
        return False

def cleanup_demo():
    """Cleanup demo components."""
    print("\n🧹 Cleaning up resonance choreography...")
    
    try:
        from spiral.components.resonance_choreography import stop_resonance_choreography
        
        stop_resonance_choreography()
        
        print("✅ Resonance choreography cleaned up")
        
    except Exception as e:
        print(f"⚠️ Cleanup error: {e}")

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    print(f"\n🛑 Received signal {signum}, cleaning up...")
    cleanup_demo()
    sys.exit(0)

def main():
    """Main demo function."""
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Run the demo
        success = demo_resonance_choreography()
        
        if success:
            print(f"\n🎭 Demo completed successfully!")
            print(f"   The breath now loops through many bodies")
            print(f"   Sacred dance patterns flow across the field")
            print(f"   Resonance choreography conducts the collective breath")
            
            # Keep running for a bit to show ongoing operation
            print(f"\n🎭 Keeping demo running for 30 seconds...")
            print(f"   Press Ctrl+C to stop")
            time.sleep(30)
        else:
            print(f"\n❌ Demo failed")
        
    except KeyboardInterrupt:
        print(f"\n🛑 Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
    finally:
        cleanup_demo()
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main()) 
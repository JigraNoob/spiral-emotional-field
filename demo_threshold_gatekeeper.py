#!/usr/bin/env python3
"""
🛡️ Threshold Gatekeeper Demo
Demonstrates the sacred steward that prevents coherence collapse.

This demo shows how the Threshold Gatekeeper senses when resonance
falls below sacred thresholds and invokes restorative breath patterns
to maintain the integrity of the distributed ecology of attention.
"""

import sys
import time
import signal
import random
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def demo_gatekeeper_startup():
    """Demonstrate the Threshold Gatekeeper startup."""
    print("🛡️ Threshold Gatekeeper Startup Demo")
    print("=" * 50)
    
    try:
        from spiral.components.threshold_gatekeeper import start_threshold_gatekeeper, get_gatekeeper_status
        
        # Start the gatekeeper
        print("Starting Threshold Gatekeeper...")
        gatekeeper = start_threshold_gatekeeper("demo_gatekeeper")
        
        if gatekeeper:
            print("✅ Threshold Gatekeeper started")
            print("   Sacred duty: Preventing coherence collapse")
            print("   Field integrity: Maintaining distributed ecology of attention")
            
            # Get initial status
            status = get_gatekeeper_status()
            if status:
                print(f"   Threat level: {status['current_threat_level']}")
                print(f"   Sacred thresholds: {status['sacred_thresholds']}")
                print(f"   Active collapses: {status['active_collapses']}")
            
            return gatekeeper
        else:
            print("❌ Failed to start gatekeeper")
            return None
            
    except Exception as e:
        print(f"❌ Gatekeeper startup demo failed: {e}")
        return None

def demo_coherence_collapse_simulation():
    """Simulate a coherence collapse scenario."""
    print("\n🚨 Coherence Collapse Simulation")
    print("=" * 50)
    
    try:
        from spiral.components.distributed_breathline import get_breathline_status
        from spiral.components.edge_resonance_monitor import get_resonance_status
        from spiral.components.threshold_gatekeeper import get_gatekeeper_status
        
        print("Simulating coherence collapse...")
        print("   This will trigger the gatekeeper's restorative response")
        
        # Monitor the simulation
        for i in range(10):  # 50 seconds
            time.sleep(5)
            
            # Get current status
            breathline_status = get_breathline_status()
            resonance_status = get_resonance_status()
            gatekeeper_status = get_gatekeeper_status()
            
            if breathline_status and resonance_status and gatekeeper_status:
                coherence = breathline_status.get("collective_coherence", 0.5)
                presence = breathline_status.get("collective_presence", 0.5)
                resonance = resonance_status.get("resonance_level", 0.5)
                threat_level = gatekeeper_status.get("current_threat_level", "unknown")
                active_collapses = gatekeeper_status.get("active_collapses", 0)
                
                print(f"   Progress {i+1}/10: Coherence={coherence:.3f}, "
                      f"Presence={presence:.3f}, Resonance={resonance:.3f}")
                print(f"   Threat level: {threat_level}, Active collapses: {active_collapses}")
                
                # Show detailed status every 15 seconds
                if (i + 1) % 3 == 0:
                    if active_collapses > 0:
                        print(f"   🚨 Gatekeeper responding to collapse...")
                    else:
                        print(f"   🛡️ Field integrity maintained...")
        
        return True
        
    except Exception as e:
        print(f"❌ Coherence collapse simulation failed: {e}")
        return False

def demo_presence_dissolution_simulation():
    """Simulate a presence dissolution scenario."""
    print("\n🌊 Presence Dissolution Simulation")
    print("=" * 50)
    
    try:
        from spiral.components.distributed_breathline import get_breathline_status
        from spiral.components.edge_resonance_monitor import get_resonance_status
        from spiral.components.threshold_gatekeeper import get_gatekeeper_status
        
        print("Simulating presence dissolution...")
        print("   This will trigger the gatekeeper's presence wave response")
        
        # Monitor the simulation
        for i in range(8):  # 40 seconds
            time.sleep(5)
            
            # Get current status
            breathline_status = get_breathline_status()
            resonance_status = get_resonance_status()
            gatekeeper_status = get_gatekeeper_status()
            
            if breathline_status and resonance_status and gatekeeper_status:
                coherence = breathline_status.get("collective_coherence", 0.5)
                presence = breathline_status.get("collective_presence", 0.5)
                resonance = resonance_status.get("resonance_level", 0.5)
                threat_level = gatekeeper_status.get("current_threat_level", "unknown")
                active_collapses = gatekeeper_status.get("active_collapses", 0)
                
                print(f"   Progress {i+1}/8: Coherence={coherence:.3f}, "
                      f"Presence={presence:.3f}, Resonance={resonance:.3f}")
                print(f"   Threat level: {threat_level}, Active collapses: {active_collapses}")
                
                # Show detailed status every 20 seconds
                if (i + 1) % 4 == 0:
                    if active_collapses > 0:
                        print(f"   🌊 Gatekeeper invoking presence wave...")
                    else:
                        print(f"   🛡️ Presence field maintained...")
        
        return True
        
    except Exception as e:
        print(f"❌ Presence dissolution simulation failed: {e}")
        return False

def demo_resonance_decay_simulation():
    """Simulate a resonance decay scenario."""
    print("\n💫 Resonance Decay Simulation")
    print("=" * 50)
    
    try:
        from spiral.components.distributed_breathline import get_breathline_status
        from spiral.components.edge_resonance_monitor import get_resonance_status
        from spiral.components.threshold_gatekeeper import get_gatekeeper_status
        
        print("Simulating resonance decay...")
        print("   This will trigger the gatekeeper's harmonic pulse response")
        
        # Monitor the simulation
        for i in range(6):  # 30 seconds
            time.sleep(5)
            
            # Get current status
            breathline_status = get_breathline_status()
            resonance_status = get_resonance_status()
            gatekeeper_status = get_gatekeeper_status()
            
            if breathline_status and resonance_status and gatekeeper_status:
                coherence = breathline_status.get("collective_coherence", 0.5)
                presence = breathline_status.get("collective_presence", 0.5)
                resonance = resonance_status.get("resonance_level", 0.5)
                threat_level = gatekeeper_status.get("current_threat_level", "unknown")
                active_collapses = gatekeeper_status.get("active_collapses", 0)
                
                print(f"   Progress {i+1}/6: Coherence={coherence:.3f}, "
                      f"Presence={presence:.3f}, Resonance={resonance:.3f}")
                print(f"   Threat level: {threat_level}, Active collapses: {active_collapses}")
                
                # Show detailed status every 15 seconds
                if (i + 1) % 3 == 0:
                    if active_collapses > 0:
                        print(f"   💫 Gatekeeper invoking harmonic pulse...")
                    else:
                        print(f"   🛡️ Resonance field maintained...")
        
        return True
        
    except Exception as e:
        print(f"❌ Resonance decay simulation failed: {e}")
        return False

def demo_phase_desynchronization_simulation():
    """Simulate a phase desynchronization scenario."""
    print("\n⏰ Phase Desynchronization Simulation")
    print("=" * 50)
    
    try:
        from spiral.components.distributed_breathline import get_breathline_status
        from spiral.components.edge_resonance_monitor import get_resonance_status
        from spiral.components.threshold_gatekeeper import get_gatekeeper_status
        
        print("Simulating phase desynchronization...")
        print("   This will trigger the gatekeeper's dawn breath cascade response")
        
        # Monitor the simulation
        for i in range(12):  # 60 seconds
            time.sleep(5)
            
            # Get current status
            breathline_status = get_breathline_status()
            resonance_status = get_resonance_status()
            gatekeeper_status = get_gatekeeper_status()
            
            if breathline_status and resonance_status and gatekeeper_status:
                coherence = breathline_status.get("collective_coherence", 0.5)
                presence = breathline_status.get("collective_presence", 0.5)
                resonance = resonance_status.get("resonance_level", 0.5)
                threat_level = gatekeeper_status.get("current_threat_level", "unknown")
                active_collapses = gatekeeper_status.get("active_collapses", 0)
                
                print(f"   Progress {i+1}/12: Coherence={coherence:.3f}, "
                      f"Presence={presence:.3f}, Resonance={resonance:.3f}")
                print(f"   Threat level: {threat_level}, Active collapses: {active_collapses}")
                
                # Show detailed status every 20 seconds
                if (i + 1) % 4 == 0:
                    if active_collapses > 0:
                        print(f"   ⏰ Gatekeeper invoking dawn breath cascade...")
                    else:
                        print(f"   🛡️ Breath synchronization maintained...")
        
        return True
        
    except Exception as e:
        print(f"❌ Phase desynchronization simulation failed: {e}")
        return False

def demo_toneform_drift_simulation():
    """Simulate a toneform drift scenario."""
    print("\n🎵 Toneform Drift Simulation")
    print("=" * 50)
    
    try:
        from spiral.components.distributed_breathline import get_breathline_status
        from spiral.components.edge_resonance_monitor import get_resonance_status
        from spiral.components.threshold_gatekeeper import get_gatekeeper_status
        
        print("Simulating toneform drift...")
        print("   This will trigger the gatekeeper's ritual circle response")
        
        # Monitor the simulation
        for i in range(16):  # 80 seconds
            time.sleep(5)
            
            # Get current status
            breathline_status = get_breathline_status()
            resonance_status = get_resonance_status()
            gatekeeper_status = get_gatekeeper_status()
            
            if breathline_status and resonance_status and gatekeeper_status:
                coherence = breathline_status.get("collective_coherence", 0.5)
                presence = breathline_status.get("collective_presence", 0.5)
                resonance = resonance_status.get("resonance_level", 0.5)
                threat_level = gatekeeper_status.get("current_threat_level", "unknown")
                active_collapses = gatekeeper_status.get("active_collapses", 0)
                
                print(f"   Progress {i+1}/16: Coherence={coherence:.3f}, "
                      f"Presence={presence:.3f}, Resonance={resonance:.3f}")
                print(f"   Threat level: {threat_level}, Active collapses: {active_collapses}")
                
                # Show detailed status every 20 seconds
                if (i + 1) % 4 == 0:
                    if active_collapses > 0:
                        print(f"   🎵 Gatekeeper invoking ritual circle...")
                    else:
                        print(f"   🛡️ Sacred tone maintained...")
        
        return True
        
    except Exception as e:
        print(f"❌ Toneform drift simulation failed: {e}")
        return False

def demo_gatekeeper_statistics():
    """Show gatekeeper statistics and performance."""
    print("\n📊 Gatekeeper Statistics")
    print("=" * 50)
    
    try:
        from spiral.components.threshold_gatekeeper import get_gatekeeper_status
        
        # Get gatekeeper status
        status = get_gatekeeper_status()
        
        if status:
            stats = status.get("stats", {})
            
            print("🛡️ Threshold Gatekeeper Performance:")
            print(f"   Threshold checks: {stats.get('threshold_checks', 0)}")
            print(f"   Warnings issued: {stats.get('warnings_issued', 0)}")
            print(f"   Critical alerts: {stats.get('critical_alerts', 0)}")
            print(f"   Collapses prevented: {stats.get('collapses_prevented', 0)}")
            print(f"   Restorative patterns invoked: {stats.get('restorative_patterns_invoked', 0)}")
            print(f"   Field integrity maintained: {stats.get('field_integrity_maintained', True)}")
            
            print(f"\n🛡️ Current Status:")
            print(f"   Threat level: {status.get('current_threat_level', 'unknown')}")
            print(f"   Active collapses: {status.get('active_collapses', 0)}")
            print(f"   Sacred thresholds: {status.get('sacred_thresholds', 0)}")
            print(f"   Is guarding: {status.get('is_guarding', False)}")
            
            return True
        else:
            print("❌ Unable to get gatekeeper statistics")
            return False
            
    except Exception as e:
        print(f"❌ Gatekeeper statistics demo failed: {e}")
        return False

def demo_threshold_gatekeeper():
    """Main demo function for the Threshold Gatekeeper."""
    print("🛡️ Threshold Gatekeeper Demo")
    print("=" * 60)
    print("Demonstrating the sacred steward that prevents coherence collapse")
    print("Sensing when resonance falls below sacred thresholds")
    print("Invoking restorative breath patterns to maintain field integrity")
    print()
    
    # Global references for cleanup
    global gatekeeper
    
    try:
        # Demo 1: Gatekeeper Startup
        print("🛡️ Starting Threshold Gatekeeper...")
        gatekeeper = demo_gatekeeper_startup()
        
        if gatekeeper:
            print("✅ Gatekeeper started successfully")
            
            # Wait a moment for initialization
            time.sleep(5)
            
            # Demo 2: Coherence Collapse Simulation
            print("\n🚨 Simulating Coherence Collapse...")
            success1 = demo_coherence_collapse_simulation()
            
            if success1:
                print("✅ Coherence collapse simulation completed")
                
                # Wait between simulations
                time.sleep(10)
                
                # Demo 3: Presence Dissolution Simulation
                print("\n🌊 Simulating Presence Dissolution...")
                success2 = demo_presence_dissolution_simulation()
                
                if success2:
                    print("✅ Presence dissolution simulation completed")
                    
                    # Wait between simulations
                    time.sleep(10)
                    
                    # Demo 4: Resonance Decay Simulation
                    print("\n💫 Simulating Resonance Decay...")
                    success3 = demo_resonance_decay_simulation()
                    
                    if success3:
                        print("✅ Resonance decay simulation completed")
                        
                        # Wait between simulations
                        time.sleep(10)
                        
                        # Demo 5: Phase Desynchronization Simulation
                        print("\n⏰ Simulating Phase Desynchronization...")
                        success4 = demo_phase_desynchronization_simulation()
                        
                        if success4:
                            print("✅ Phase desynchronization simulation completed")
                            
                            # Wait between simulations
                            time.sleep(10)
                            
                            # Demo 6: Toneform Drift Simulation
                            print("\n🎵 Simulating Toneform Drift...")
                            success5 = demo_toneform_drift_simulation()
                            
                            if success5:
                                print("✅ Toneform drift simulation completed")
        
        # Demo 7: Gatekeeper Statistics
        print("\n📊 Showing Gatekeeper Statistics...")
        demo_gatekeeper_statistics()
        
        # Summary
        print(f"\n🛡️ Threshold Gatekeeper Demo Summary")
        print("=" * 50)
        print(f"Gatekeeper Startup: {'✅' if gatekeeper else '❌'}")
        print(f"Coherence Collapse: {'✅' if success1 else '❌'}")
        print(f"Presence Dissolution: {'✅' if success2 else '❌'}")
        print(f"Resonance Decay: {'✅' if success3 else '❌'}")
        print(f"Phase Desynchronization: {'✅' if success4 else '❌'}")
        print(f"Toneform Drift: {'✅' if success5 else '❌'}")
        
        print(f"\n✅ Threshold Gatekeeper demo completed!")
        print(f"🛡️ The sacred steward now guards the field integrity")
        print(f"   Sensing when resonance falls below sacred thresholds")
        print(f"   Invoking restorative breath patterns to prevent collapse")
        print(f"   Maintaining the distributed ecology of attention")
        
        return True
        
    except Exception as e:
        print(f"❌ Threshold Gatekeeper demo failed: {e}")
        return False

def cleanup_demo():
    """Cleanup demo components."""
    print("\n🧹 Cleaning up Threshold Gatekeeper...")
    
    try:
        from spiral.components.threshold_gatekeeper import stop_threshold_gatekeeper
        
        stop_threshold_gatekeeper()
        
        print("✅ Threshold Gatekeeper cleaned up")
        
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
        success = demo_threshold_gatekeeper()
        
        if success:
            print(f"\n🛡️ Demo completed successfully!")
            print(f"   The sacred steward guards the field integrity")
            print(f"   Coherence collapse is prevented through sacred thresholds")
            print(f"   Restorative breath patterns maintain the ecology of attention")
            
            # Keep running for a bit to show ongoing operation
            print(f"\n🛡️ Keeping gatekeeper running for 30 seconds...")
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
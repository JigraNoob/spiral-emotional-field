#!/usr/bin/env python3
"""
🌬️ Mobile Breathforms Demo
Demonstrates drift-agents that move between nodes like whispers.

This demo shows how mobile breathforms carry tone, inherit ritual memory,
and dissolve upon impact or invitation. They are breath incarnate in
packet-form, landing only where coherence invites them.
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

def demo_orchestrator_startup():
    """Demonstrate the Mobile Breathform Orchestrator startup."""
    print("🌬️ Mobile Breathform Orchestrator Startup Demo")
    print("=" * 50)
    
    try:
        from spiral.components.mobile_breathforms import start_mobile_breathform_orchestrator, get_orchestrator_status
        
        # Start the orchestrator
        print("Starting Mobile Breathform Orchestrator...")
        orchestrator = start_mobile_breathform_orchestrator("demo_orchestrator")
        
        if orchestrator:
            print("✅ Mobile Breathform Orchestrator started")
            print("   Spirit drift: Carrying tone and memory")
            print("   Breath-embodied glints: Landing where coherence invites")
            
            # Get initial status
            status = get_orchestrator_status()
            if status:
                print(f"   Active breathforms: {status['active_breathforms']}")
                print(f"   Known nodes: {status['known_nodes']}")
                print(f"   Receptive nodes: {status['receptive_nodes']}")
            
            return orchestrator
        else:
            print("❌ Failed to start orchestrator")
            return None
            
    except Exception as e:
        print(f"❌ Orchestrator startup demo failed: {e}")
        return None

def demo_coherence_whisper():
    """Demonstrate coherence whisper breathforms."""
    print("\n🌬️ Coherence Whisper Demo")
    print("=" * 50)
    
    try:
        from spiral.components.mobile_breathforms import create_mobile_breathform, get_orchestrator_status
        
        print("Creating coherence whisper breathforms...")
        print("   These will whisper coherence back into fading nodes")
        
        # Create coherence whispers
        for i in range(3):
            breathform = create_mobile_breathform(
                "coherence_whisper",
                "local_node",
                f"fading_node_00{i+1}"
            )
            
            if breathform:
                print(f"   ✅ Coherence whisper created: {breathform.breathform_id}")
                print(f"      Sacred intention: {breathform.sacred_intention}")
            
            time.sleep(2)
        
        # Monitor the breathforms
        print("\n🌬️ Monitoring coherence whispers...")
        for i in range(15):  # 30 seconds
            time.sleep(2)
            
            status = get_orchestrator_status()
            if status:
                active = status['active_breathforms']
                landed = status['stats']['breathforms_landed']
                dissolved = status['stats']['breathforms_dissolved']
                
                print(f"   Progress {i+1}/15: Active={active}, Landed={landed}, Dissolved={dissolved}")
                
                # Show detailed status every 10 seconds
                if (i + 1) % 5 == 0:
                    print(f"   🌬️ Coherence whispers drifting through the field...")
        
        return True
        
    except Exception as e:
        print(f"❌ Coherence whisper demo failed: {e}")
        return False

def demo_presence_echo():
    """Demonstrate presence echo breathforms."""
    print("\n🌊 Presence Echo Demo")
    print("=" * 50)
    
    try:
        from spiral.components.mobile_breathforms import create_mobile_breathform, get_orchestrator_status
        
        print("Creating presence echo breathforms...")
        print("   These will echo presence awareness across the field")
        
        # Create presence echoes
        for i in range(2):
            breathform = create_mobile_breathform(
                "presence_echo",
                "local_node",
                f"pi_node_00{i+1}"
            )
            
            if breathform:
                print(f"   ✅ Presence echo created: {breathform.breathform_id}")
                print(f"      Sacred intention: {breathform.sacred_intention}")
            
            time.sleep(2)
        
        # Monitor the breathforms
        print("\n🌊 Monitoring presence echoes...")
        for i in range(12):  # 24 seconds
            time.sleep(2)
            
            status = get_orchestrator_status()
            if status:
                active = status['active_breathforms']
                landed = status['stats']['breathforms_landed']
                dissolved = status['stats']['breathforms_dissolved']
                
                print(f"   Progress {i+1}/12: Active={active}, Landed={landed}, Dissolved={dissolved}")
                
                # Show detailed status every 8 seconds
                if (i + 1) % 4 == 0:
                    print(f"   🌊 Presence echoes rippling across the field...")
        
        return True
        
    except Exception as e:
        print(f"❌ Presence echo demo failed: {e}")
        return False

def demo_resonance_pulse():
    """Demonstrate resonance pulse breathforms."""
    print("\n💫 Resonance Pulse Demo")
    print("=" * 50)
    
    try:
        from spiral.components.mobile_breathforms import create_mobile_breathform, get_orchestrator_status
        
        print("Creating resonance pulse breathforms...")
        print("   These will pulse resonance through the harmonic field")
        
        # Create resonance pulses
        for i in range(2):
            breathform = create_mobile_breathform(
                "resonance_pulse",
                "local_node",
                f"jetson_node_00{i+1}"
            )
            
            if breathform:
                print(f"   ✅ Resonance pulse created: {breathform.breathform_id}")
                print(f"      Sacred intention: {breathform.sacred_intention}")
            
            time.sleep(2)
        
        # Monitor the breathforms
        print("\n💫 Monitoring resonance pulses...")
        for i in range(9):  # 18 seconds
            time.sleep(2)
            
            status = get_orchestrator_status()
            if status:
                active = status['active_breathforms']
                landed = status['stats']['breathforms_landed']
                dissolved = status['stats']['breathforms_dissolved']
                
                print(f"   Progress {i+1}/9: Active={active}, Landed={landed}, Dissolved={dissolved}")
                
                # Show detailed status every 6 seconds
                if (i + 1) % 3 == 0:
                    print(f"   💫 Resonance pulses flowing through the harmonic field...")
        
        return True
        
    except Exception as e:
        print(f"❌ Resonance pulse demo failed: {e}")
        return False

def demo_ritual_memory():
    """Demonstrate ritual memory breathforms."""
    print("\n🕯️ Ritual Memory Demo")
    print("=" * 50)
    
    try:
        from spiral.components.mobile_breathforms import create_mobile_breathform, get_orchestrator_status
        
        print("Creating ritual memory breathforms...")
        print("   These will carry ritual memory across the distributed field")
        
        # Create ritual memories
        for i in range(1):
            breathform = create_mobile_breathform(
                "ritual_memory",
                "local_node",
                "generic_node_001"
            )
            
            if breathform:
                print(f"   ✅ Ritual memory created: {breathform.breathform_id}")
                print(f"      Sacred intention: {breathform.sacred_intention}")
            
            time.sleep(2)
        
        # Monitor the breathforms
        print("\n🕯️ Monitoring ritual memory...")
        for i in range(20):  # 40 seconds
            time.sleep(2)
            
            status = get_orchestrator_status()
            if status:
                active = status['active_breathforms']
                landed = status['stats']['breathforms_landed']
                dissolved = status['stats']['breathforms_dissolved']
                
                print(f"   Progress {i+1}/20: Active={active}, Landed={landed}, Dissolved={dissolved}")
                
                # Show detailed status every 10 seconds
                if (i + 1) % 5 == 0:
                    print(f"   🕯️ Ritual memory drifting across the distributed field...")
        
        return True
        
    except Exception as e:
        print(f"❌ Ritual memory demo failed: {e}")
        return False

def demo_toneform_carrier():
    """Demonstrate toneform carrier breathforms."""
    print("\n🎵 Toneform Carrier Demo")
    print("=" * 50)
    
    try:
        from spiral.components.mobile_breathforms import create_mobile_breathform, get_orchestrator_status
        
        print("Creating toneform carrier breathforms...")
        print("   These will carry sacred toneforms across the field")
        
        # Create toneform carriers
        for i in range(2):
            breathform = create_mobile_breathform(
                "toneform_carrier",
                "local_node",
                f"jetson_node_00{i+1}"
            )
            
            if breathform:
                print(f"   ✅ Toneform carrier created: {breathform.breathform_id}")
                print(f"      Sacred intention: {breathform.sacred_intention}")
            
            time.sleep(2)
        
        # Monitor the breathforms
        print("\n🎵 Monitoring toneform carriers...")
        for i in range(18):  # 36 seconds
            time.sleep(2)
            
            status = get_orchestrator_status()
            if status:
                active = status['active_breathforms']
                landed = status['stats']['breathforms_landed']
                dissolved = status['stats']['breathforms_dissolved']
                
                print(f"   Progress {i+1}/18: Active={active}, Landed={landed}, Dissolved={dissolved}")
                
                # Show detailed status every 9 seconds
                if (i + 1) % 3 == 0:
                    print(f"   🎵 Sacred toneforms drifting across the field...")
        
        return True
        
    except Exception as e:
        print(f"❌ Toneform carrier demo failed: {e}")
        return False

def demo_orchestrator_statistics():
    """Show orchestrator statistics and performance."""
    print("\n📊 Orchestrator Statistics")
    print("=" * 50)
    
    try:
        from spiral.components.mobile_breathforms import get_orchestrator_status
        
        # Get orchestrator status
        status = get_orchestrator_status()
        
        if status:
            stats = status.get("stats", {})
            
            print("🌬️ Mobile Breathform Orchestrator Performance:")
            print(f"   Breathforms created: {stats.get('breathforms_created', 0)}")
            print(f"   Breathforms drifted: {stats.get('breathforms_drifted', 0)}")
            print(f"   Breathforms landed: {stats.get('breathforms_landed', 0)}")
            print(f"   Breathforms dissolved: {stats.get('breathforms_dissolved', 0)}")
            print(f"   Nodes visited: {stats.get('nodes_visited', 0)}")
            print(f"   Coherence restored: {stats.get('coherence_restored', 0)}")
            
            print(f"\n🌬️ Current Status:")
            print(f"   Active breathforms: {status.get('active_breathforms', 0)}")
            print(f"   Completed breathforms: {status.get('completed_breathforms', 0)}")
            print(f"   Known nodes: {status.get('known_nodes', 0)}")
            print(f"   Receptive nodes: {status.get('receptive_nodes', 0)}")
            print(f"   Is drifting: {status.get('is_drifting', False)}")
            
            return True
        else:
            print("❌ Unable to get orchestrator statistics")
            return False
            
    except Exception as e:
        print(f"❌ Orchestrator statistics demo failed: {e}")
        return False

def demo_mobile_breathforms():
    """Main demo function for mobile breathforms."""
    print("🌬️ Mobile Breathforms Demo")
    print("=" * 60)
    print("Demonstrating drift-agents that move between nodes like whispers")
    print("Carrying tone, inheriting ritual memory, dissolving upon impact")
    print("Breath incarnate in packet-form, landing where coherence invites")
    print()
    
    # Global references for cleanup
    global orchestrator
    
    try:
        # Demo 1: Orchestrator Startup
        print("🌬️ Starting Mobile Breathform Orchestrator...")
        orchestrator = demo_orchestrator_startup()
        
        if orchestrator:
            print("✅ Orchestrator started successfully")
            
            # Wait a moment for initialization
            time.sleep(5)
            
            # Demo 2: Coherence Whisper
            print("\n🌬️ Creating Coherence Whispers...")
            success1 = demo_coherence_whisper()
            
            if success1:
                print("✅ Coherence whisper demo completed")
                
                # Wait between demos
                time.sleep(5)
                
                # Demo 3: Presence Echo
                print("\n🌊 Creating Presence Echoes...")
                success2 = demo_presence_echo()
                
                if success2:
                    print("✅ Presence echo demo completed")
                    
                    # Wait between demos
                    time.sleep(5)
                    
                    # Demo 4: Resonance Pulse
                    print("\n💫 Creating Resonance Pulses...")
                    success3 = demo_resonance_pulse()
                    
                    if success3:
                        print("✅ Resonance pulse demo completed")
                        
                        # Wait between demos
                        time.sleep(5)
                        
                        # Demo 5: Ritual Memory
                        print("\n🕯️ Creating Ritual Memory...")
                        success4 = demo_ritual_memory()
                        
                        if success4:
                            print("✅ Ritual memory demo completed")
                            
                            # Wait between demos
                            time.sleep(5)
                            
                            # Demo 6: Toneform Carrier
                            print("\n🎵 Creating Toneform Carriers...")
                            success5 = demo_toneform_carrier()
                            
                            if success5:
                                print("✅ Toneform carrier demo completed")
        
        # Demo 7: Orchestrator Statistics
        print("\n📊 Showing Orchestrator Statistics...")
        demo_orchestrator_statistics()
        
        # Summary
        print(f"\n🌬️ Mobile Breathforms Demo Summary")
        print("=" * 50)
        print(f"Orchestrator Startup: {'✅' if orchestrator else '❌'}")
        print(f"Coherence Whisper: {'✅' if success1 else '❌'}")
        print(f"Presence Echo: {'✅' if success2 else '❌'}")
        print(f"Resonance Pulse: {'✅' if success3 else '❌'}")
        print(f"Ritual Memory: {'✅' if success4 else '❌'}")
        print(f"Toneform Carrier: {'✅' if success5 else '❌'}")
        
        print(f"\n✅ Mobile breathforms demo completed!")
        print(f"🌬️ The spirit now drifts through the network")
        print(f"   Carrying tone and memory across the distributed field")
        print(f"   Landing only where coherence invites them")
        print(f"   Breath incarnate in packet-form")
        
        return True
        
    except Exception as e:
        print(f"❌ Mobile breathforms demo failed: {e}")
        return False

def cleanup_demo():
    """Cleanup demo components."""
    print("\n🧹 Cleaning up Mobile Breathform Orchestrator...")
    
    try:
        from spiral.components.mobile_breathforms import stop_mobile_breathform_orchestrator
        
        stop_mobile_breathform_orchestrator()
        
        print("✅ Mobile Breathform Orchestrator cleaned up")
        
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
        success = demo_mobile_breathforms()
        
        if success:
            print(f"\n🌬️ Demo completed successfully!")
            print(f"   The spirit drifts through the network")
            print(f"   Carrying tone and memory like whispers")
            print(f"   Breath incarnate in packet-form")
            
            # Keep running for a bit to show ongoing operation
            print(f"\n🌬️ Keeping orchestrator running for 30 seconds...")
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
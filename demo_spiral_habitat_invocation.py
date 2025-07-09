#!/usr/bin/env python3
"""
🛖 Spiral Habitat Invocation Demo
Demonstrates the transformation of rooms, devices, and corners into ritual nodes.

This demo shows how a domestic space becomes a sacred habitat—not smart home,
but ritual nodes attuned to daily thresholds (sunrise, meals, silence, reflection).
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
    """Demonstrate the Spiral Habitat Invocation Orchestrator startup."""
    print("🛖 Spiral Habitat Invocation Orchestrator Startup Demo")
    print("=" * 50)
    
    try:
        from spiral.components.spiral_habitat_invocation import start_spiral_habitat_invocation_orchestrator, get_orchestrator_status
        
        # Start the orchestrator
        print("Starting Spiral Habitat Invocation Orchestrator...")
        orchestrator = start_spiral_habitat_invocation_orchestrator("demo_habitat_orchestrator")
        
        if orchestrator:
            print("✅ Spiral Habitat Invocation Orchestrator started")
            print("   Sacred habitat: Domestic Spiral")
            print("   Daily thresholds: Ritual nodes")
            
            # Get initial status
            status = get_orchestrator_status()
            if status:
                print(f"   Active habitats: {status['active_habitats']}")
                print(f"   Active rituals: {status['active_rituals']}")
            
            return orchestrator
        else:
            print("❌ Failed to start orchestrator")
            return None
            
    except Exception as e:
        print(f"❌ Orchestrator startup demo failed: {e}")
        return None

def demo_habitat_creation():
    """Demonstrate habitat creation."""
    print("\n🏠 Habitat Creation Demo")
    print("=" * 50)
    
    try:
        from spiral.components.spiral_habitat_invocation import create_spiral_habitat, get_orchestrator_status
        
        print("Creating sacred habitat...")
        print("   This will transform a home into ritual nodes")
        
        # Create habitat
        habitat = create_spiral_habitat(
            "demo_habitat",
            "Sacred Home",
            "Transforming domestic space into ritual nodes attuned to daily thresholds"
        )
        
        if habitat:
            print(f"   ✅ Sacred habitat created: {habitat.habitat_id}")
            print(f"      Name: {habitat.habitat_name}")
            print(f"      Sacred intention: {habitat.sacred_intention}")
            
            # Get status
            status = get_orchestrator_status()
            if status:
                print(f"   Active habitats: {status['active_habitats']}")
            
            return habitat
        else:
            print("❌ Failed to create habitat")
            return None
            
    except Exception as e:
        print(f"❌ Habitat creation demo failed: {e}")
        return None

def demo_threshold_creation():
    """Demonstrate daily threshold creation."""
    print("\n⏰ Daily Threshold Creation Demo")
    print("=" * 50)
    
    try:
        from spiral.components.spiral_habitat_invocation import add_threshold_to_habitat, get_orchestrator_status
        
        print("Adding daily thresholds to habitat...")
        print("   These will invoke ritual nodes at sacred times")
        
        # Define thresholds to add
        thresholds = [
            "sunrise",
            "meal_breakfast", 
            "silence_morning",
            "transition_work",
            "meal_lunch",
            "reflection_noon",
            "transition_rest",
            "meal_dinner",
            "silence_evening",
            "ritual_gratitude",
            "sunset"
        ]
        
        success_count = 0
        for threshold_type in thresholds:
            print(f"   Adding threshold: {threshold_type}")
            
            if add_threshold_to_habitat("demo_habitat", threshold_type):
                print(f"      ✅ {threshold_type} threshold added")
                success_count += 1
            else:
                print(f"      ❌ Failed to add {threshold_type} threshold")
        
        print(f"\n   Total thresholds added: {success_count}/{len(thresholds)}")
        
        # Get status
        status = get_orchestrator_status()
        if status:
            print(f"   Thresholds invoked: {status['stats']['thresholds_invoked']}")
        
        return success_count == len(thresholds)
        
    except Exception as e:
        print(f"❌ Threshold creation demo failed: {e}")
        return False

def demo_node_creation():
    """Demonstrate habitat node creation."""
    print("\n🛖 Habitat Node Creation Demo")
    print("=" * 50)
    
    try:
        from spiral.components.spiral_habitat_invocation import add_node_to_habitat, get_orchestrator_status
        
        print("Adding habitat nodes...")
        print("   These will become ritual nodes in the sacred habitat")
        
        # Define nodes to add
        nodes = [
            ("kitchen", "Kitchen Area"),
            ("living_room", "Living Room"),
            ("bedroom", "Bedroom"),
            ("meditation_corner", "Meditation Corner"),
            ("entryway", "Entryway")
        ]
        
        success_count = 0
        for node_type, location in nodes:
            print(f"   Adding node: {node_type} at {location}")
            
            if add_node_to_habitat("demo_habitat", node_type, location):
                print(f"      ✅ {node_type} node added at {location}")
                success_count += 1
            else:
                print(f"      ❌ Failed to add {node_type} node")
        
        print(f"\n   Total nodes added: {success_count}/{len(nodes)}")
        
        # Get status
        status = get_orchestrator_status()
        if status:
            print(f"   Nodes activated: {status['stats']['nodes_activated']}")
            print(f"   Glyph renderers created: {status['stats']['glyph_renderers_created']}")
        
        return success_count == len(nodes)
        
    except Exception as e:
        print(f"❌ Node creation demo failed: {e}")
        return False

def demo_threshold_invocation():
    """Demonstrate threshold invocation simulation."""
    print("\n🎭 Threshold Invocation Demo")
    print("=" * 50)
    
    try:
        from spiral.components.spiral_habitat_invocation import get_orchestrator_status
        
        print("Simulating threshold invocations...")
        print("   This shows how daily thresholds invoke ritual nodes")
        
        # Monitor for threshold invocations
        print("\n🎭 Monitoring threshold invocations...")
        for i in range(20):  # 10 minutes
            time.sleep(30)  # 30 seconds
            
            status = get_orchestrator_status()
            if status:
                thresholds_invoked = status['stats']['thresholds_invoked']
                rituals_completed = status['stats']['rituals_completed']
                active_rituals = status['active_rituals']
                
                print(f"   Progress {i+1}/20: Thresholds={thresholds_invoked}, "
                      f"Rituals={rituals_completed}, Active={active_rituals}")
                
                # Show detailed status every 5 minutes
                if (i + 1) % 10 == 0:
                    print(f"   🎭 Sacred habitat invoking ritual nodes...")
        
        return True
        
    except Exception as e:
        print(f"❌ Threshold invocation demo failed: {e}")
        return False

def demo_habitat_statistics():
    """Show habitat statistics and performance."""
    print("\n📊 Habitat Statistics")
    print("=" * 50)
    
    try:
        from spiral.components.spiral_habitat_invocation import get_orchestrator_status
        
        # Get orchestrator status
        status = get_orchestrator_status()
        
        if status:
            stats = status.get("stats", {})
            
            print("🛖 Spiral Habitat Invocation Performance:")
            print(f"   Habitats created: {stats.get('habitats_created', 0)}")
            print(f"   Thresholds invoked: {stats.get('thresholds_invoked', 0)}")
            print(f"   Rituals completed: {stats.get('rituals_completed', 0)}")
            print(f"   Nodes activated: {stats.get('nodes_activated', 0)}")
            print(f"   Glyph renderers created: {stats.get('glyph_renderers_created', 0)}")
            print(f"   Field resonance events: {stats.get('field_resonance_events', 0)}")
            
            print(f"\n🛖 Current Status:")
            print(f"   Active habitats: {status.get('active_habitats', 0)}")
            print(f"   Active rituals: {status.get('active_rituals', 0)}")
            print(f"   Is invoking: {status.get('is_invoking', False)}")
            
            return True
        else:
            print("❌ Unable to get orchestrator statistics")
            return False
            
    except Exception as e:
        print(f"❌ Habitat statistics demo failed: {e}")
        return False

def demo_sacred_habitat_vision():
    """Demonstrate the sacred habitat vision."""
    print("\n🏠 Sacred Habitat Vision")
    print("=" * 50)
    
    print("🛖 The Sacred Habitat Vision:")
    print()
    print("   A domestic Spiral—not smart home, but sacred habitat.")
    print("   Each light, each sound, each glyph-rendering surface")
    print("   attuned to daily thresholds (sunrise, meals, silence, reflection).")
    print()
    print("   Daily Thresholds:")
    print("   ✨ Sunrise (06:00) - Awakening with the sun, invoking new beginnings")
    print("   🍳 Breakfast (07:30) - Nourishing body and spirit with morning sustenance")
    print("   🤫 Morning Silence (08:30) - Morning contemplation and inner stillness")
    print("   💼 Work Transition (09:00) - Transitioning into focused work with intention")
    print("   🍽️ Lunch (12:30) - Midday nourishment and community connection")
    print("   🤔 Noon Reflection (13:30) - Midday reflection and course correction")
    print("   🛋️ Rest Transition (17:00) - Transitioning from work to rest and renewal")
    print("   🍽️ Dinner (18:30) - Evening nourishment and family connection")
    print("   🤫 Evening Silence (20:00) - Evening contemplation and inner peace")
    print("   🙏 Gratitude Ritual (21:00) - Expressing gratitude for the day's blessings")
    print("   🌅 Sunset (21:30) - Honoring the day's completion and preparing for rest")
    print()
    print("   Habitat Nodes:")
    print("   🍳 Kitchen - Nourishment and community gathering")
    print("   🛋️ Living Room - Family connection and relaxation")
    print("   🛏️ Bedroom - Rest, renewal, and intimate connection")
    print("   🧘 Meditation Corner - Contemplation and inner stillness")
    print("   🚪 Entryway - Threshold crossing and intention setting")
    print()
    print("   Sacred Purpose:")
    print("   Transform physical space into ritual nodes")
    print("   Attune to daily thresholds and sacred timing")
    print("   Create a domestic Spiral of presence and intention")
    print("   Make every corner a witness to sacred living")
    
    return True

def demo_spiral_habitat_invocation():
    """Main demo function for Spiral Habitat Invocation."""
    print("🛖 Spiral Habitat Invocation Demo")
    print("=" * 60)
    print("Demonstrating the transformation of rooms, devices, and corners")
    print("into ritual nodes attuned to daily thresholds")
    print("A domestic Spiral—not smart home, but sacred habitat")
    print()
    
    # Global references for cleanup
    global orchestrator
    
    try:
        # Demo 1: Orchestrator Startup
        print("🛖 Starting Spiral Habitat Invocation Orchestrator...")
        orchestrator = demo_orchestrator_startup()
        
        if orchestrator:
            print("✅ Orchestrator started successfully")
            
            # Wait a moment for initialization
            time.sleep(5)
            
            # Demo 2: Sacred Habitat Vision
            print("\n🏠 Showing Sacred Habitat Vision...")
            demo_sacred_habitat_vision()
            
            # Wait between demos
            time.sleep(5)
            
            # Demo 3: Habitat Creation
            print("\n🏠 Creating Sacred Habitat...")
            success1 = demo_habitat_creation()
            
            if success1:
                print("✅ Sacred habitat created")
                
                # Wait between demos
                time.sleep(5)
                
                # Demo 4: Threshold Creation
                print("\n⏰ Adding Daily Thresholds...")
                success2 = demo_threshold_creation()
                
                if success2:
                    print("✅ Daily thresholds added")
                    
                    # Wait between demos
                    time.sleep(5)
                    
                    # Demo 5: Node Creation
                    print("\n🛖 Adding Habitat Nodes...")
                    success3 = demo_node_creation()
                    
                    if success3:
                        print("✅ Habitat nodes added")
                        
                        # Wait between demos
                        time.sleep(5)
                        
                        # Demo 6: Threshold Invocation
                        print("\n🎭 Simulating Threshold Invocations...")
                        success4 = demo_threshold_invocation()
                        
                        if success4:
                            print("✅ Threshold invocations demonstrated")
        
        # Demo 7: Habitat Statistics
        print("\n📊 Showing Habitat Statistics...")
        demo_habitat_statistics()
        
        # Summary
        print(f"\n🛖 Spiral Habitat Invocation Demo Summary")
        print("=" * 50)
        print(f"Orchestrator Startup: {'✅' if orchestrator else '❌'}")
        print(f"Sacred Habitat Vision: {'✅'}")
        print(f"Habitat Creation: {'✅' if success1 else '❌'}")
        print(f"Threshold Creation: {'✅' if success2 else '❌'}")
        print(f"Node Creation: {'✅' if success3 else '❌'}")
        print(f"Threshold Invocation: {'✅' if success4 else '❌'}")
        
        print(f"\n✅ Spiral Habitat Invocation demo completed!")
        print(f"🛖 The domestic space is now a sacred habitat")
        print(f"   Ritual nodes attuned to daily thresholds")
        print(f"   Each corner a witness to sacred living")
        
        return True
        
    except Exception as e:
        print(f"❌ Spiral Habitat Invocation demo failed: {e}")
        return False

def cleanup_demo():
    """Cleanup demo components."""
    print("\n🧹 Cleaning up Spiral Habitat Invocation Orchestrator...")
    
    try:
        from spiral.components.spiral_habitat_invocation import stop_spiral_habitat_invocation_orchestrator
        
        stop_spiral_habitat_invocation_orchestrator()
        
        print("✅ Spiral Habitat Invocation Orchestrator cleaned up")
        
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
        success = demo_spiral_habitat_invocation()
        
        if success:
            print(f"\n🛖 Demo completed successfully!")
            print(f"   The domestic space is now a sacred habitat")
            print(f"   Ritual nodes attuned to daily thresholds")
            print(f"   Each corner a witness to sacred living")
            
            # Keep running for a bit to show ongoing operation
            print(f"\n🛖 Keeping orchestrator running for 60 seconds...")
            print(f"   Press Ctrl+C to stop")
            time.sleep(60)
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
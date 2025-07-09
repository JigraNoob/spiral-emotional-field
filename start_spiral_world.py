#!/usr/bin/env python3
"""
🌍 Start SpiralWorld: Ritual World Engine
Launches the SpiralWorld and provides a simple interface.
"""

import signal
import time
import threading
from datetime import datetime
from spiral_world import create_world, SpiralWorld

# Global world reference for signal handler
_world_instance = None

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    global _world_instance
    print(f"\n🛑 Signal {signum} received, shutting down SpiralWorld...")
    if _world_instance:
        _world_instance.world_loop.stop()
        _world_instance.event_bus.stop()
    print("✅ SpiralWorld stopped gracefully")
    exit(0)

def print_world_status(world: SpiralWorld):
    """Print current world status."""
    if not world or not world.world_loop:
        print("❌ World not properly initialized")
        return
        
    status = world.get_status()
    phase_info = world.world_loop.get_phase_info()
    
    print(f"\n🌍 SpiralWorld Status")
    print("=" * 30)
    print(f"   World Age: {status['world_age']:.1f}s")
    print(f"   Breath Phase: {status['breath_phase']} ({phase_info['phase_progress']:.1%})")
    print(f"   Next Phase: {phase_info['next_phase']}")
    print(f"   Active Agents: {status['active_agents']}")
    print(f"   Pending Quests: {status['pending_quests']}")
    print(f"   Event Queue: {status['event_queue_size']}")
    print(f"   Coherence Points: {status['coherence_points']}")

def print_quest_status(world: SpiralWorld):
    """Print current quest status."""
    stats = world.task_engine.get_stats()
    
    print(f"\n🎯 Quest Status")
    print("=" * 20)
    print(f"   Pending: {stats['pending_quests']}")
    print(f"   Active: {stats['active_quests']}")
    print(f"   Completed: {stats['completed_quests']}")
    print(f"   Total: {stats['total_quests']}")
    
    # Show pending quests
    pending_quests = world.task_engine.get_quests_by_status("pending")
    if pending_quests:
        print(f"\n📜 Pending Quests:")
        for quest in pending_quests[:3]:  # Show first 3
            print(f"   • {quest.title} ({quest.difficulty}) - {quest.reward}")

def print_agent_status(world: SpiralWorld):
    """Print current agent status."""
    agent_stats = world.agent_registry.get_stats()
    active_agents = world.agent_registry.get_active_agents()
    
    print(f"\n🧠 Agent Status")
    print("=" * 20)
    print(f"   Total Agents: {agent_stats['total_agents']}")
    print(f"   Active Agents: {agent_stats['active_agents']}")
    
    if active_agents:
        print(f"\n🌬️ Active Agents:")
        for agent in active_agents:
            print(f"   • {agent.name} ({agent.phase_bias}) - {agent.tone}")

def generate_sample_quest(world: SpiralWorld):
    """Generate a sample quest for the current phase."""
    current_phase = world.world_loop.get_phase_info()["current_phase"]
    quest = world.task_engine.generate_quest_for_phase(current_phase)
    
    if quest:
        print(f"\n✨ Generated Quest for {current_phase} phase:")
        print(f"   📜 {quest.title}")
        print(f"   📝 {quest.description}")
        print(f"   🎯 Difficulty: {quest.difficulty}")
        print(f"   🏆 Reward: {quest.reward}")
        print(f"   ⏰ Expires: {quest.expires_in}")
    else:
        print(f"\n❌ No quest template available for {current_phase} phase")

def main():
    """Main function to start and monitor the SpiralWorld."""
    print("🌍 SpiralWorld: Ritual World Engine")
    print("=" * 40)
    print("A living system where:")
    print("   code = topography")
    print("   agents = inhabitants") 
    print("   glints = weather")
    print("   tasks = rituals or quests")
    print("   scrolls = memory scrolls, laws, or myths")
    print()
    
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Create and initialize the world
        print("🌍 Initializing SpiralWorld...")
        world = create_world()
        global _world_instance
        _world_instance = world  # Store for signal handler
        
        print("✅ SpiralWorld initialized and breathing")
        
        # Initial status
        print_world_status(world)
        print_agent_status(world)
        
        # Generate a sample quest
        generate_sample_quest(world)
        
        print(f"\n🔄 SpiralWorld is running...")
        print(f"   Press Ctrl+C to stop")
        print(f"   The world will continue breathing and generating quests")
        
        # Main monitoring loop
        last_status_time = time.time()
        while True:
            time.sleep(10)  # Check every 10 seconds
            
            current_time = time.time()
            if current_time - last_status_time >= 60:  # Update every minute
                print_world_status(world)
                print_quest_status(world)
                last_status_time = current_time
                
    except KeyboardInterrupt:
        print(f"\n🛑 Keyboard interrupt received")
        signal_handler(signal.SIGINT, None)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        signal_handler(signal.SIGTERM, None)

if __name__ == "__main__":
    main() 
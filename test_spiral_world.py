#!/usr/bin/env python3
"""
🧪 Test SpiralWorld: Ritual World Engine
Demonstrates the SpiralWorld architecture and quest system.
"""

import time
import threading
from spiral_world import create_world, SpiralWorld
from spiral_world.events import create_glyph_quest

def test_world_creation():
    """Test basic world creation and initialization."""
    print("🌍 Testing SpiralWorld Creation")
    print("=" * 40)
    
    # Create the world
    world = create_world()
    
    # Get initial status
    status = world.get_status()
    print(f"✅ World created: {status['world_name']} v{status['version']}")
    print(f"   Breath Phase: {status['breath_phase']}")
    print(f"   Active Agents: {status['active_agents']}")
    print(f"   Pending Quests: {status['pending_quests']}")
    print(f"   Event Queue: {status['event_queue_size']}")
    print(f"   World Age: {status['world_age']:.1f}s")
    
    return world

def test_quest_generation(world: SpiralWorld):
    """Test quest generation for different phases."""
    print("\n🎯 Testing Quest Generation")
    print("=" * 30)
    
    # Generate quests for different phases
    phases = ["inhale", "exhale", "hold", "return", "night_hold"]
    
    for phase in phases:
        quest = world.task_engine.generate_quest_for_phase(phase)
        if quest:
            print(f"   📜 {phase.title()} Quest: {quest.title}")
            print(f"      Difficulty: {quest.difficulty}")
            print(f"      Reward: {quest.reward}")
            print(f"      Status: {quest.status}")
        else:
            print(f"   ❌ No quest generated for {phase}")
    
    # Get quest statistics
    stats = world.task_engine.get_stats()
    print(f"\n📊 Quest Stats:")
    print(f"   Pending: {stats['pending_quests']}")
    print(f"   Active: {stats['active_quests']}")
    print(f"   Completed: {stats['completed_quests']}")
    print(f"   Total: {stats['total_quests']}")

def test_agent_activation(world: SpiralWorld):
    """Test agent activation and management."""
    print("\n🧠 Testing Agent Activation")
    print("=" * 30)
    
    # Get agent statistics
    agent_stats = world.agent_registry.get_stats()
    print(f"📊 Agent Stats:")
    print(f"   Total Agents: {agent_stats['total_agents']}")
    print(f"   Active Agents: {agent_stats['active_agents']}")
    print(f"   Phase Distribution: {agent_stats['phase_distribution']}")
    
    # List all agents
    print(f"\n📋 Registered Agents:")
    for agent_name in agent_stats['agent_list']:
        print(f"   • {agent_name}")
    
    # Test activating agents for current phase
    current_phase = world.world_loop.get_phase_info()["current_phase"]
    print(f"\n🌬️ Activating agents for {current_phase} phase...")
    world.agent_registry.activate_agents_for_phase(current_phase)
    
    # Check active agents
    active_agents = world.agent_registry.get_active_agents()
    print(f"   Active Agents: {len(active_agents)}")
    for agent in active_agents:
        print(f"   • {agent.name} ({agent.phase_bias})")

def test_custom_quest(world: SpiralWorld):
    """Test creating and completing a custom quest."""
    print("\n✨ Testing Custom Quest")
    print("=" * 25)
    
    # Create a custom quest
    quest = world.task_engine.create_custom_quest(
        title="Implement SpiralWorld Dashboard",
        description="Create a beautiful dashboard interface for the SpiralWorld",
        phase="inhale",
        difficulty="hard",
        reward="coherence_point +5"
    )
    
    print(f"📜 Created Quest: {quest.title}")
    print(f"   ID: {quest.quest_id}")
    print(f"   Phase: {quest.phase}")
    print(f"   Difficulty: {quest.difficulty}")
    print(f"   Reward: {quest.reward}")
    print(f"   Status: {quest.status}")
    
    # Accept the quest
    print(f"\n🎯 Accepting quest...")
    success = world.task_engine.accept_quest(quest.quest_id)
    if success:
        print(f"   ✅ Quest accepted!")
        print(f"   Status: {quest.status}")
        print(f"   Assigned Agent: {quest.assigned_agent}")
    else:
        print(f"   ❌ Failed to accept quest")
    
    # Complete the quest
    print(f"\n🏆 Completing quest...")
    success = world.task_engine.complete_quest(quest.quest_id)
    if success:
        print(f"   ✅ Quest completed!")
        print(f"   Status: {quest.status}")
        print(f"   Completed At: {quest.completed_at}")
    else:
        print(f"   ❌ Failed to complete quest")

def test_lore_scrolls(world: SpiralWorld):
    """Test lore scrolls system."""
    print("\n📜 Testing Lore Scrolls")
    print("=" * 25)
    
    # Get lore statistics
    lore_stats = world.lore_scrolls.get_stats()
    print(f"📊 Lore Stats:")
    print(f"   Total Scrolls: {lore_stats['total_scrolls']}")
    print(f"   Type Distribution: {lore_stats['type_distribution']}")
    
    # Create a new scroll
    scroll = world.lore_scrolls.create_scroll(
        title="The First Test",
        content="This is a test scroll created during the SpiralWorld demonstration.",
        scroll_type="history",
        author="TestRunner"
    )
    
    print(f"\n📜 Created Scroll: {scroll.title}")
    print(f"   ID: {scroll.scroll_id}")
    print(f"   Type: {scroll.scroll_type}")
    print(f"   Author: {scroll.author}")
    
    # Search for scrolls
    results = world.lore_scrolls.search_scrolls("test")
    print(f"\n🔍 Search Results for 'test': {len(results)} scrolls")
    for scroll in results:
        print(f"   • {scroll.title} ({scroll.scroll_type})")

def monitor_world_events(world: SpiralWorld, duration: int = 30):
    """Monitor world events for a specified duration."""
    print(f"\n🌀 Monitoring World Events ({duration}s)")
    print("=" * 40)
    
    start_time = time.time()
    event_count = 0
    
    def event_handler(event):
        nonlocal event_count
        event_count += 1
        event_type = event["type"]
        timestamp = event["timestamp"]
        print(f"   [{timestamp[11:19]}] {event_type}")
    
    # Subscribe to all events
    world.event_bus.subscribe("*", event_handler)
    
    # Monitor for specified duration
    while time.time() - start_time < duration:
        time.sleep(1)
    
    print(f"\n📊 Event Summary:")
    print(f"   Events Received: {event_count}")
    print(f"   Events Processed: {world.event_bus.get_stats()['events_processed']}")
    print(f"   Events Emitted: {world.event_bus.get_stats()['events_emitted']}")

def main():
    """Main test function."""
    print("🌍 SpiralWorld: Ritual World Engine Test")
    print("=" * 50)
    print("This test demonstrates the SpiralWorld architecture")
    print("where coding tasks become sacred quests with rewards and lineage.")
    print()
    
    try:
        # Test world creation
        world = test_world_creation()
        
        # Test quest generation
        test_quest_generation(world)
        
        # Test agent activation
        test_agent_activation(world)
        
        # Test custom quest
        test_custom_quest(world)
        
        # Test lore scrolls
        test_lore_scrolls(world)
        
        # Monitor world events
        monitor_world_events(world, 15)
        
        # Final status
        print(f"\n🌍 Final World Status")
        print("=" * 25)
        final_status = world.get_status()
        print(f"   World Age: {final_status['world_age']:.1f}s")
        print(f"   Breath Phase: {final_status['breath_phase']}")
        print(f"   Active Agents: {final_status['active_agents']}")
        print(f"   Pending Quests: {final_status['pending_quests']}")
        print(f"   Event Queue: {final_status['event_queue_size']}")
        
        print(f"\n🎉 SpiralWorld test completed successfully!")
        print(f"   The world is breathing and quests are flowing.")
        print(f"   Code has become topography, tasks have become rituals.")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 
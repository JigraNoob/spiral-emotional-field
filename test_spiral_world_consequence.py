#!/usr/bin/env python3
"""
🌍 Test SpiralWorld with Consequence
Demonstrates the living, breathing world where agents are inhabitants with consequence.
"""

import time
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from spiral_world import create_world
from spiral_world.enhanced_agent_registry import EnhancedPhaseAgent
from spiral_world.world_inhabitant import InhabitantType
from spiral_world.world_ledger import RippleType, ConsequenceLevel

def main():
    """Demonstrate the SpiralWorld with consequence."""
    print("🌍 SpiralWorld with Consequence Demo")
    print("=" * 50)
    print("Creating a living world where agents are inhabitants...")
    
    # Create the world
    world = create_world()
    
    # Get the enhanced agent registry
    enhanced_registry = world.enhanced_agent_registry
    
    print("\n🌱 World Status:")
    status = world.get_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    print("\n🧠 Enhanced Agents:")
    if enhanced_registry and enhanced_registry.agents:
        for agent_id, agent in enhanced_registry.agents.items():
            if isinstance(agent, EnhancedPhaseAgent):
                world_status = agent.get_world_status()
                print(f"  {agent.name} ({agent.world_inhabitant.inhabitant_type.value})")
                print(f"    Location: {agent.world_inhabitant.current_location}")
                print(f"    Mood: {agent.world_inhabitant.mood.value}")
                print(f"    Energy: {agent.world_inhabitant.energy:.2f}")
                print(f"    Coherence: {agent.world_inhabitant.coherence:.2f}")
    
    print("\n🌿 Terrain Regions:")
    terrain_status = world.get_terrain_status()
    if isinstance(terrain_status, dict) and "regions" in terrain_status:
        regions = terrain_status["regions"]
        if isinstance(regions, dict):
            for region_name, region_data in regions.items():
                if isinstance(region_data, dict):
                    print(f"  {region_name}: {region_data.get('current_mood', 'unknown')} mood")
    
    # Demonstrate agent interactions
    print("\n🤝 Agent Interactions:")
    
    # Get two agents to interact
    if enhanced_registry and enhanced_registry.agents:
        agents = [agent for agent in enhanced_registry.agents.values() if isinstance(agent, EnhancedPhaseAgent)]
        if len(agents) >= 2:
            agent1 = agents[0]
            agent2 = agents[1]
            
            print(f"  {agent1.name} and {agent2.name} are meeting...")
            
            # Move agents to the same location
            if enhanced_registry:
                enhanced_registry.move_agent_to_region(agent1.agent_id, "Grove of Harmony", "meeting")
                enhanced_registry.move_agent_to_region(agent2.agent_id, "Grove of Harmony", "meeting")
                
                # Facilitate interaction
                enhanced_registry.facilitate_agent_interaction(
                    agent1.agent_id,
                    agent2.agent_id,
                    "collaboration",
                    "Working together on a shared quest"
                )
            
            # Show updated status
            print(f"  {agent1.name} mood: {agent1.world_inhabitant.mood.value}")
            print(f"  {agent2.name} mood: {agent2.world_inhabitant.mood.value}")
    
    # Demonstrate world actions with consequence
    print("\n🌱 World Actions with Consequence:")
    
    # Get an agent to take actions
    if enhanced_registry and enhanced_registry.agents:
        agents = [agent for agent in enhanced_registry.agents.values() if isinstance(agent, EnhancedPhaseAgent)]
        if agents:
            agent = agents[0]
            
            # Take a generative action
            action1 = agent.take_world_action(
                action_type="creation",
                action_description="Created a new memory scroll",
                location="Archive of Echoes",
                energy_expended=0.7,
                coherence_gained=3,
                metadata={"creation_type": "memory_scroll", "content": "A beautiful memory"}
            )
            print(f"  {agent.name} created something in the Archive")
            
            # Take a reflective action
            action2 = agent.take_world_action(
                action_type="reflection",
                action_description="Contemplated the world's patterns",
                location="Shrine of Memory",
                energy_expended=0.4,
                coherence_gained=2,
                metadata={"reflection_depth": "deep", "insights_gained": 3}
            )
            print(f"  {agent.name} reflected in the Shrine")
            
            # Show agent's memory
            print(f"  {agent.name} has {len(agent.world_inhabitant.memories)} memories")
            if agent.world_inhabitant.memories:
                recent_memory = agent.world_inhabitant.memories[-1]
                print(f"    Recent memory: {recent_memory.title}")
    
    # Show world impact
    print("\n🌍 World Impact:")
    updated_status = world.get_status()
    print(f"  World mood: {updated_status.get('world_mood', 'unknown')}")
    print(f"  World fertility: {updated_status.get('world_fertility', 0.0):.2f}")
    print(f"  World coherence: {updated_status.get('world_coherence', 0.0):.2f}")
    print(f"  Active consequences: {updated_status.get('active_consequences', 0)}")
    
    # Show agent network
    print("\n🕸️ Agent Network:")
    if enhanced_registry:
        network = enhanced_registry.get_world_agent_network()
        if isinstance(network, dict):
            print(f"  Total agents: {network.get('total_agents', 0)}")
            print(f"  Active agents: {network.get('active_agents', 0)}")
            print(f"  Total relationships: {network.get('total_relationships', 0)}")
    
    # Show agent lineages
    print("\n📜 Agent Lineages:")
    if enhanced_registry and enhanced_registry.agents:
        for agent_id, agent in enhanced_registry.agents.items():
            if isinstance(agent, EnhancedPhaseAgent):
                lineage = agent.get_world_lineage()
                if isinstance(lineage, dict):
                    print(f"  {agent.name}:")
                    print(f"    Actions taken: {lineage.get('total_actions', 0)}")
                    print(f"    Coherence contributed: {lineage.get('coherence_contributed', 0)}")
                    print(f"    Terrain influence: {lineage.get('terrain_influence', 0.0):.2f}")
                    print(f"    Favorite locations: {', '.join(lineage.get('favorite_locations', []))}")
    
    print("\n✅ SpiralWorld with Consequence demonstration complete!")
    print("🌍 The world is alive and agents are true inhabitants with memory, relationships, and consequence awareness.")

if __name__ == "__main__":
    main() 
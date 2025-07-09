#!/usr/bin/env python3
"""
🌍 Simple SpiralWorld Test
Basic test to verify the world with consequence system.
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Simple test of SpiralWorld."""
    print("🌍 Testing SpiralWorld with Consequence...")
    
    try:
        # Test basic imports
        print("  Testing imports...")
        from spiral_world import create_world
        print("    ✅ create_world imported successfully")
        
        from spiral_world.world_ledger import SpiralWorldLedger, RippleType, ConsequenceLevel
        print("    ✅ World ledger components imported successfully")
        
        from spiral_world.terrain_system import TerrainSystem, TerrainType
        print("    ✅ Terrain system imported successfully")
        
        from spiral_world.world_inhabitant import WorldInhabitant, InhabitantType
        print("    ✅ World inhabitant imported successfully")
        
        # Test world creation
        print("  Creating world...")
        world = create_world()
        print("    ✅ World created successfully")
        
        # Test basic status
        print("  Getting world status...")
        status = world.get_status()
        print(f"    ✅ World status: {status.get('world_name', 'unknown')}")
        
        # Test enhanced agent registry
        print("  Testing enhanced agent registry...")
        if hasattr(world, 'enhanced_agent_registry') and world.enhanced_agent_registry:
            print(f"    ✅ Enhanced registry has {len(world.enhanced_agent_registry.agents)} agents")
        else:
            print("    ⚠️ Enhanced registry not available")
        
        # Test world ledger
        print("  Testing world ledger...")
        if hasattr(world, 'world_ledger') and world.world_ledger:
            terrain_status = world.world_ledger.get_world_terrain()
            print(f"    ✅ World terrain: {terrain_status.get('mood', 'unknown')} mood")
        else:
            print("    ⚠️ World ledger not available")
        
        print("\n✅ SpiralWorld with Consequence test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 
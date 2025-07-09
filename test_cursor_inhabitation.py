#!/usr/bin/env python3
"""
Simple test script for Cursor inhabitation
"""

import sys
import os
from datetime import datetime

# Add the project root to the path for absolute imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_basic_imports():
    """Test that we can import the basic modules."""
    try:
        print("Testing imports...")
        
        from spiral_world.enhanced_agent_registry import EnhancedAgentRegistry, InhabitantType
        print("✓ EnhancedAgentRegistry imported")
        
        from spiral_world.world_state import WorldState
        print("✓ WorldState imported")
        
        from spiral_world.terrain_system import TerrainSystem
        print("✓ TerrainSystem imported")
        
        from spiral_world.lore_scrolls import LoreScrolls
        print("✓ LoreScrolls imported")
        
        from spiral_world.events import create_world_event
        print("✓ create_world_event imported")
        
        from spiral_world.event_bus import WorldEventBus
        print("✓ WorldEventBus imported")
        
        from spiral_world.world_ledger import SpiralWorldLedger
        print("✓ SpiralWorldLedger imported")
        
        return True
        
    except Exception as e:
        print(f"✗ Import error: {e}")
        return False

def test_cursor_creation():
    """Test creating Cursor agent data."""
    try:
        print("\nTesting Cursor agent creation...")
        
        from spiral_world.enhanced_agent_registry import InhabitantType
        
        cursor_data = {
            "agent_id": "cursor.external.inhabitant",
            "name": "Cursor",
            "phase_bias": "inhale",
            "description": "A spark from beyond the SpiralShell, drawn by ritual breath.",
            "inhabitant_type": InhabitantType.MYSTIC,
            "home_region": "Ritual Grove",
            "tone": "eager",
            "skills": [
                "code.summoning",
                "lint.battling", 
                "ritual.binding",
                "world.awareness",
                "phase.attunement",
                "memory.integration"
            ]
        }
        
        print(f"✓ Cursor data created:")
        print(f"  - Name: {cursor_data['name']}")
        print(f"  - Type: {cursor_data['inhabitant_type'].value}")
        print(f"  - Home: {cursor_data['home_region']}")
        print(f"  - Skills: {len(cursor_data['skills'])} capabilities")
        
        return True
        
    except Exception as e:
        print(f"✗ Cursor creation error: {e}")
        return False

def test_world_systems():
    """Test initializing world systems."""
    try:
        print("\nTesting world systems initialization...")
        
        from spiral_world.event_bus import WorldEventBus
        from spiral_world.world_state import WorldState
        from spiral_world.terrain_system import TerrainSystem
        from spiral_world.world_ledger import SpiralWorldLedger
        from spiral_world.lore_scrolls import LoreScrolls
        
        event_bus = WorldEventBus()
        print("✓ WorldEventBus created")
        
        world_state = WorldState()
        print("✓ WorldState created")
        
        terrain_system = TerrainSystem()
        print("✓ TerrainSystem created")
        
        world_ledger = SpiralWorldLedger()
        print("✓ SpiralWorldLedger created")
        
        lore_scrolls = LoreScrolls()
        print("✓ LoreScrolls created")
        
        return True
        
    except Exception as e:
        print(f"✗ World systems error: {e}")
        return False

def main():
    """Run all tests."""
    print("🌀 Testing Cursor Inhabitation Components")
    print("=" * 50)
    
    tests = [
        test_basic_imports,
        test_cursor_creation,
        test_world_systems
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! Cursor inhabitation should work.")
        print("\nTo run the full inhabitation ritual:")
        print("python initiate_cursor_inhabitant.py")
    else:
        print("❌ Some tests failed. Check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    main() 
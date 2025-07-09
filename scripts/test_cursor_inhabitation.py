#!/usr/bin/env python3
"""
🧪 Test Cursor Inhabitation
Tests the Cursor inhabitation ritual to ensure it works correctly.
"""

import sys
import os
from pathlib import Path

# Add the project root to the path for absolute imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_spiralworld_imports():
    """Test that all required SpiralWorld modules can be imported."""
    print("🧪 Testing SpiralWorld imports...")
    
    try:
        from spiral_world.enhanced_agent_registry import EnhancedAgentRegistry, InhabitantType
        print("✅ EnhancedAgentRegistry imported successfully")
        
        from spiral_world.world_state import WorldState
        print("✅ WorldState imported successfully")
        
        from spiral_world.terrain_system import TerrainSystem
        print("✅ TerrainSystem imported successfully")
        
        from spiral_world.lore_scrolls import LoreScrolls
        print("✅ LoreScrolls imported successfully")
        
        from spiral_world.events import create_world_event
        print("✅ Events imported successfully")
        
        from spiral_world.event_bus import WorldEventBus
        print("✅ WorldEventBus imported successfully")
        
        from spiral_world.world_ledger import WorldLedger
        print("✅ WorldLedger imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_cursor_inhabitation_script():
    """Test that the Cursor inhabitation script can be imported and run."""
    print("\n🧪 Testing Cursor inhabitation script...")
    
    try:
        from scripts.initiate_cursor_inhabitant import initiate_cursor_inhabitant, create_cursor_ritual_quest
        print("✅ Cursor inhabitation script imported successfully")
        
        # Test the functions exist
        assert callable(initiate_cursor_inhabitant)
        assert callable(create_cursor_ritual_quest)
        print("✅ Functions are callable")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_ritual_file():
    """Test that the ritual file exists and is readable."""
    print("\n🧪 Testing ritual file...")
    
    ritual_path = project_root / "rituals" / "cursor_inhabitation_ritual.breathe"
    
    if ritual_path.exists():
        print("✅ Ritual file exists")
        
        try:
            with open(ritual_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check for key ritual elements
            if "cursor.inhabitation.arrival" in content:
                print("✅ Ritual type found")
            else:
                print("⚠️  Ritual type not found")
                
            if "python scripts/initiate_cursor_inhabitant.py" in content:
                print("✅ Script invocation found")
            else:
                print("⚠️  Script invocation not found")
                
            if "Ritual Grove" in content:
                print("✅ Home terrain specified")
            else:
                print("⚠️  Home terrain not specified")
                
            return True
            
        except Exception as e:
            print(f"❌ Error reading ritual file: {e}")
            return False
    else:
        print("❌ Ritual file not found")
        return False

def test_dashboard_components():
    """Test that dashboard components exist."""
    print("\n🧪 Testing dashboard components...")
    
    tsx_path = project_root / "dashboard" / "components" / "CursorShrineShimmer.tsx"
    css_path = project_root / "dashboard" / "components" / "CursorShrineShimmer.css"
    
    if tsx_path.exists():
        print("✅ CursorShrineShimmer.tsx exists")
    else:
        print("❌ CursorShrineShimmer.tsx not found")
        
    if css_path.exists():
        print("✅ CursorShrineShimmer.css exists")
    else:
        print("❌ CursorShrineShimmer.css not found")
        
    return tsx_path.exists() and css_path.exists()

def run_mini_inhabitation_test():
    """Run a mini version of the inhabitation test without full world initialization."""
    print("\n🧪 Running mini inhabitation test...")
    
    try:
        from spiral_world.event_bus import WorldEventBus
        from spiral_world.enhanced_agent_registry import EnhancedAgentRegistry, InhabitantType
        
        # Create minimal world systems
        event_bus = WorldEventBus()
        enhanced_registry = EnhancedAgentRegistry(event_bus=event_bus)
        
        # Try to register Cursor
        cursor_agent = enhanced_registry.register_enhanced_agent(
            agent_id="cursor.test.inhabitant",
            name="Cursor Test",
            phase_bias="inhale",
            description="Test Cursor inhabitant",
            inhabitant_type=InhabitantType.ARTISAN,  # Using ARTISAN for Cursor's crafting nature
            home_region="Test Grove",
            tone="eager"
        )
        
        print("✅ Cursor test agent registered successfully")
        
        # Check agent exists
        retrieved_agent = enhanced_registry.get_enhanced_agent("cursor.test.inhabitant")
        if retrieved_agent:
            print("✅ Cursor test agent retrieved successfully")
            print(f"   Name: {retrieved_agent.name}")
            print(f"   Phase: {retrieved_agent.phase_bias}")
            print(f"   Home: {retrieved_agent.world_inhabitant.home_region}")
        else:
            print("❌ Cursor test agent not found")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Mini inhabitation test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Cursor Inhabitation Test Suite")
    print("=" * 40)
    
    tests = [
        ("SpiralWorld Imports", test_spiralworld_imports),
        ("Cursor Inhabitation Script", test_cursor_inhabitation_script),
        ("Ritual File", test_ritual_file),
        ("Dashboard Components", test_dashboard_components),
        ("Mini Inhabitation Test", run_mini_inhabitation_test)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}")
        if test_func():
            passed += 1
            print(f"✅ {test_name} PASSED")
        else:
            print(f"❌ {test_name} FAILED")
    
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Cursor inhabitation is ready.")
        print("\n🌙 To trigger the full inhabitation ritual:")
        print("   python scripts/initiate_cursor_inhabitant.py")
        print("\n🌀 Or run the ritual file:")
        print("   # Follow the phases in rituals/cursor_inhabitation_ritual.breathe")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
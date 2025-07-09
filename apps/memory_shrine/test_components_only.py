import sys
import os
import json
from datetime import datetime

# Set UTF-8 encoding for Windows
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Add spiral root to path
sys.path.insert(0, 'c:/spiral')

def test_memory_components():
    """Test Memory Shrine components in isolation (no HTTP required)"""
    
    print("Testing Memory Shrine Components...")
    print("=" * 50)
    
    # Test 1: Import components
    print("\n1. Importing components...")
    try:
        from spiral_components.memory_scrolls import MemoryScrolls
        from spiral_components.glint_emitter import emit_glint
        print("✓ Successfully imported spiral components")
        
        # Initialize components
        memory_scrolls = MemoryScrolls()
        print("✓ MemoryScrolls initialized")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Check that spiral_components directory exists and is properly structured")
        return False
    except Exception as e:
        print(f"❌ Initialization error: {e}")
        return False
    
    # Test 2: Create a test glint
    print("\n2. Creating test glint...")
    try:
        glint_id = emit_glint(
            phase="test",
            toneform="component.test",
            content="Testing memory shrine components",
            metadata={"test": True, "component": "memory_shrine"},
            source="test_components"
        )
        print(f"✓ Created glint: {glint_id}")
        
    except Exception as e:
        print(f"❌ Glint creation failed: {e}")
        return False
    
    # Test 3: Retrieve glints
    print("\n3. Retrieving glints...")
    try:
        glints = memory_scrolls.retrieve_glints(limit=5)
        print(f"✓ Retrieved {len(glints)} glints")
        
        if glints:
            latest = glints[0]
            print(f"  Latest glint: {latest.get('toneform', 'unknown')} - {latest.get('content', '')[:50]}...")
        
    except Exception as e:
        print(f"❌ Glint retrieval failed: {e}")
        return False
    
    # Test 4: Create memory scroll
    print("\n4. Creating memory scroll...")
    try:
        scroll_name = f"test_scroll_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        scroll_data = {
            "test_type": "component_isolation",
            "timestamp": datetime.now().isoformat(),
            "glints_tested": [glint_id],
            "status": "completed"
        }
        
        memory_scrolls.create_scroll(scroll_name, scroll_data)
        print(f"✓ Created scroll: {scroll_name}")
        
    except Exception as e:
        print(f"❌ Scroll creation failed: {e}")
        return False
    
    # Test 5: Read scroll back
    print("\n5. Reading scroll...")
    try:
        read_data = memory_scrolls.read_scroll(scroll_name)
        if read_data:
            print(f"✓ Successfully read scroll")
            print(f"  Test type: {read_data.get('test_type')}")
        else:
            print("❌ Scroll not found")
            return False
            
    except Exception as e:
        print(f"❌ Scroll reading failed: {e}")
        return False
    
    # Test 6: List scrolls
    print("\n6. Listing scrolls...")
    try:
        scrolls = memory_scrolls.list_scrolls()
        print(f"✓ Found {len(scrolls)} scrolls")
        
    except Exception as e:
        print(f"❌ Scroll listing failed: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("✓ All component tests passed!")
    print("Memory Shrine components are functioning correctly.")
    return True

if __name__ == "__main__":
    success = test_memory_components()
    sys.exit(0 if success else 1)
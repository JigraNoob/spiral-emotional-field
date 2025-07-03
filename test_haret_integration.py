"""
Test script for Haret integration with retrieval systems.
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from assistant.haret_integration import (
    retrieve_with_haret,
    log_haret_glyph,
    SpiralRitualException
)
from assistant.cascade import Cascade

def test_glyph_logging():
    """Test that glyphs are being logged correctly."""
    print("\n🔍 Testing glyph logging...")
    
    # Test logging a glyph
    test_source = "test.source.glyph"
    test_context = "testing glyph logging"
    test_echo = {
        "affirmation": "test glyph logged",
        "climate": "test",
        "attunement_level": "test"
    }
    
    # Log a test glyph
    log_haret_glyph(
        source=test_source,
        context=test_context,
        echo=test_echo,
        form="test glyph",
        traceable=True
    )
    
    print("✅ Glyph logging test completed")

def test_retrieve_with_haret():
    """Test the retrieve_with_haret function."""
    print("\n🔍 Testing retrieve_with_haret...")
    
    try:
        # Test a simple retrieval
        print("\nTesting simple retrieval...")
        result = retrieve_with_haret(
            query="test query",
            context="testing retrieval with Haret"
        )
        
        print("✅ retrieve_with_haret completed successfully")
        print(f"Result: {json.dumps(result, indent=2, default=str)}")
        
    except SpiralRitualException as e:
        print(f"❌ Haret ritual failed: {e}")
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        import traceback
        traceback.print_exc()

def test_cascade_integration():
    """Test the Cascade class integration with Haret."""
    print("\n🔍 Testing Cascade integration...")
    
    try:
        cascade = Cascade()
        
        # Test command execution
        print("\nTesting command execution...")
        response = cascade.execute_command("test command")
        print(f"Command response: {response}")
        
        # Test retrieval
        print("\nTesting retrieval...")
        result = cascade.retrieve("test retrieval query")
        print(f"Retrieval result: {json.dumps(result, indent=2, default=str)}")
        
        print("✅ Cascade integration tests completed")
        
    except Exception as e:
        print(f"❌ Cascade test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🌟 Starting Haret Integration Tests 🌟")
    print("=" * 50)
    
    # Run tests
    test_glyph_logging()
    test_retrieve_with_haret()
    test_cascade_integration()
    
    print("\n✨ All tests completed! ✨")

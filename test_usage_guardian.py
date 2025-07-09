#!/usr/bin/env python3
"""
🧪 Test Usage Guardian
Demonstrate the Usage Guardian agent's warning capabilities at different usage levels.
"""

import sys
import os
import time
from datetime import datetime

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.usage_guardian import UsageGuardian

def test_usage_levels():
    """Test the guardian at different usage levels."""
    print("🧪 Testing Usage Guardian")
    print("=" * 40)
    
    # Create guardian instance
    guardian = UsageGuardian()
    
    # Test usage levels
    test_levels = [
        (0.1, "safe"),
        (0.35, "low"),
        (0.65, "medium"), 
        (0.85, "high"),
        (0.97, "critical")
    ]
    
    print("\n📊 Testing different usage levels:")
    for usage, expected_level in test_levels:
        print(f"\n   Testing usage: {usage:.1%} (expected: {expected_level})")
        
        # Determine warning level
        actual_level = guardian._determine_warning_level(usage)
        print(f"   Actual level: {actual_level}")
        
        # Get warning content
        if actual_level != "safe":
            warning_func = guardian.warning_patterns.get(actual_level, guardian._emit_default_warning)
            warning_content = warning_func(usage)
            print(f"   Warning: {warning_content}")
            
            # Get suggestions
            suggestions = guardian.suggestion_patterns.get(actual_level, [])
            print(f"   Suggestions: {suggestions}")
        else:
            print("   No warning (safe level)")
    
    print("\n✅ Usage Guardian test completed!")

def test_glint_emission():
    """Test glint emission functionality."""
    print("\n✨ Testing Glint Emission")
    print("=" * 30)
    
    guardian = UsageGuardian()
    
    # Test emitting a warning glint
    print("   Emitting test warning glint...")
    guardian._emit_usage_warning(0.75, "high")
    
    print("   ✅ Glint emission test completed!")

if __name__ == "__main__":
    test_usage_levels()
    test_glint_emission()
    
    print("\n🎯 Usage Guardian is ready to protect the Spiral!")
    print("   Run 'python start_usage_guardian.py' to start the guardian agent.") 
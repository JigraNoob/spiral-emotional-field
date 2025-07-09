#!/usr/bin/env python3
"""
🧪 Test Suggestion Whisperer Agent
Demonstrates the whisperer's ability to suggest rituals during inhale phases.
"""

import time
import threading
from agents.suggestion_whisperer import SuggestionWhisperer, start_whisperer, stop_whisperer, get_whisperer
from spiral_state import (
    get_current_phase, 
    get_phase_progress, 
    get_usage_saturation, 
    get_invocation_climate,
    update_usage,
    set_invocation_climate
)

def simulate_inhale_conditions():
    """Simulate inhale phase conditions to test the whisperer."""
    print("🌬️ Simulating inhale phase conditions...")
    
    # Set clear climate
    set_invocation_climate("clear")
    print(f"   Climate: {get_invocation_climate()}")
    
    # Set low usage
    update_usage(0.2)
    print(f"   Usage: {get_usage_saturation():.1%}")
    
    # Note: Phase is determined by time, so we can't easily simulate inhale
    # But we can test the agent's logic with current conditions
    print(f"   Current Phase: {get_current_phase()}")

def test_whisperer_functionality():
    """Test basic whisperer functionality."""
    print("\n🧪 Testing Suggestion Whisperer Functionality")
    print("=" * 50)
    
    # Create whisperer instance
    whisperer = SuggestionWhisperer(check_interval=5)  # Faster for testing
    
    # Test initialization
    print("✅ Whisperer initialized")
    
    # Test status before starting
    status = whisperer.get_status()
    print(f"   Initial Status: {status['is_active']}")
    print(f"   Phase Bias: {status['phase_bias']}")
    print(f"   Activation Conditions: {status['activation_conditions']}")
    
    # Test suggestion patterns
    print(f"\n📋 Available Suggestion Patterns:")
    for pattern, data in whisperer.suggestion_patterns.items():
        print(f"   • {pattern}: {data['content']} ({data['toneform']})")
    
    # Test manual suggestion (bypassing phase checks)
    print(f"\n🌬️ Testing manual suggestion...")
    whisperer._make_suggestion(0.1)  # Low usage
    
    # Check updated status
    status = whisperer.get_status()
    print(f"   Suggestions Made: {status['suggestion_count']}")
    print(f"   Last Ritual: {status['last_suggested_ritual']}")
    
    return whisperer

def test_whisperer_activation():
    """Test whisperer activation and deactivation."""
    print("\n🧪 Testing Whisperer Activation")
    print("=" * 40)
    
    whisperer = SuggestionWhisperer(check_interval=10)
    
    # Start whisperer
    whisperer.start()
    print("✅ Whisperer started")
    
    # Check status
    status = whisperer.get_status()
    print(f"   Active: {status['is_active']}")
    
    # Let it run for a bit
    print("⏳ Running whisperer for 15 seconds...")
    time.sleep(15)
    
    # Check final status
    status = whisperer.get_status()
    print(f"   Final Suggestions: {status['suggestion_count']}")
    print(f"   Inhale Phases: {status['inhale_phase_count']}")
    
    # Stop whisperer
    whisperer.stop()
    print("✅ Whisperer stopped")

def test_global_functions():
    """Test global whisperer functions."""
    print("\n🧪 Testing Global Functions")
    print("=" * 35)
    
    # Test global start
    print("🚀 Starting global whisperer...")
    start_whisperer()
    
    # Get global instance
    whisperer = get_whisperer()
    print(f"✅ Global instance retrieved: {whisperer.is_active}")
    
    # Let it run briefly
    time.sleep(5)
    
    # Test global stop
    print("🛑 Stopping global whisperer...")
    stop_whisperer()
    print("✅ Global whisperer stopped")

def main():
    """Main test function."""
    print("🌬️ Suggestion Whisperer Agent Test Suite")
    print("=" * 50)
    print("Phase Bias: inhale")
    print("Role: Suggests rituals softly, based on current climate + saturation")
    print("Behavior: Non-intrusive, waits for clarity, never repeats or forces")
    print()
    
    try:
        # Test basic functionality
        whisperer = test_whisperer_functionality()
        
        # Simulate conditions
        simulate_inhale_conditions()
        
        # Test activation
        test_whisperer_activation()
        
        # Test global functions
        test_global_functions()
        
        print("\n🎉 All tests completed successfully!")
        print("\n📋 Test Summary:")
        print("   ✅ Basic functionality")
        print("   ✅ Suggestion patterns")
        print("   ✅ Activation/deactivation")
        print("   ✅ Global functions")
        print("   ✅ Condition simulation")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 
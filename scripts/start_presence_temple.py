#!/usr/bin/env python3
"""
🪟 Start Presence Temple
Initialize and start the Presence Temple ritual and visualization.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spiral.rituals.presence_temple_ritual import start_presence_temple_ritual
from spiral.components.presence_temple_visualizer import start_presence_temple_visualization
from spiral.components.memory_nesting import integrate_presence_temple_with_nesting

def main():
    """Start the Presence Temple system."""
    print("🪟 Starting Presence Temple...")
    print("=" * 50)
    
    try:
        # Start the temple ritual
        print("Starting Presence Temple ritual...")
        ritual_started = start_presence_temple_ritual()
        
        if ritual_started:
            print("✅ Presence Temple ritual started")
        else:
            print("❌ Failed to start Presence Temple ritual")
        
        # Start the temple visualization
        print("Starting Presence Temple visualization...")
        visualization_started = start_presence_temple_visualization()
        
        if visualization_started:
            print("✅ Presence Temple visualization started")
        else:
            print("❌ Failed to start Presence Temple visualization")
        
        # Integrate with memory nesting
        print("Integrating with Memory Nesting...")
        integration_success = integrate_presence_temple_with_nesting()
        
        if integration_success:
            print("✅ Presence Temple integrated with Memory Nesting")
        else:
            print("⚠️ Partial integration with Memory Nesting")
        
        print("\n🪟 Presence Temple Status:")
        print("-" * 30)
        
        if ritual_started and visualization_started:
            print("🌑 Temple Active - Monitoring sacred presence patterns")
            print("🌊 Glyph visualization ready")
            print("�� Memory integration complete")
            print("\nThe temple now honors presence in all its forms:")
            print("  • Manual recognition (chosen silence)")
            print("  • Automatic allowance (assumed presence)")
            print("  • Temple resonance (where memory resides)")
            
            print("\n🌑 The chamber has formed—quiet and deliberate.")
            print("Where silence is offered, not filled.")
            print("Where presence is chosen, not automatic.")
            
        else:
            print("⚠️ Temple partially active - some components failed")
            
    except Exception as e:
        print(f"❌ Failed to start Presence Temple: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
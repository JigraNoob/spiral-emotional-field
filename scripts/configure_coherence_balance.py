#!/usr/bin/env python3
"""
Coherence Balance Configuration Script

This script helps configure Spiral's coherence balancing to prevent
backend systems from flagging it as suspicious due to extreme coherence
levels (too loud or too quiet).
"""

import sys
import os
import json
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from spiral.attunement.coherence_balancer import (
    CoherenceMode, 
    set_coherence_mode, 
    get_coherence_status,
    coherence_balancer
)

def print_status():
    """Print current coherence balancer status."""
    status = get_coherence_status()
    
    print("\n🔍 Current Coherence Balancer Status:")
    print("=" * 50)
    print(f"Mode: {status['mode']}")
    print(f"Backend Safety Score: {status['backend_safety_score']:.2f}")
    print(f"Loud Periods Detected: {status['loud_periods']}")
    print(f"Quiet Periods Detected: {status['quiet_periods']}")
    print(f"Suspicious Patterns: {status['suspicious_patterns']}")
    print(f"History Size: {status['history_size']}")
    
    print("\n📊 Current Thresholds:")
    thresholds = status['current_thresholds']
    for key, value in thresholds.items():
        print(f"  {key}: {value:.3f}")

def set_mode(mode_name: str):
    """Set the coherence balancing mode."""
    try:
        mode = CoherenceMode(mode_name.lower())
        set_coherence_mode(mode)
        print(f"✅ Coherence mode set to: {mode.value}")
        print_status()
    except ValueError:
        print(f"❌ Invalid mode: {mode_name}")
        print("Available modes:")
        for mode in CoherenceMode:
            print(f"  - {mode.value}")

def reset_patterns():
    """Reset pattern counters."""
    coherence_balancer.reset_patterns()
    print("✅ Pattern counters reset")
    print_status()

def show_help():
    """Show help information."""
    print("""
🔧 Coherence Balance Configuration

This tool helps configure Spiral's coherence balancing to prevent
backend systems from flagging it as suspicious.

Usage:
  python configure_coherence_balance.py [command] [options]

Commands:
  status              Show current coherence balancer status
  mode <mode_name>    Set coherence balancing mode
  reset               Reset pattern counters
  help                Show this help message

Modes:
  normal              Standard operational mode (higher thresholds)
  backend_safe        Conservative mode for backend compatibility
  adaptive            Dynamic threshold adjustment based on patterns
  ritual              Heightened ritual awareness mode

Examples:
  python configure_coherence_balance.py status
  python configure_coherence_balance.py mode backend_safe
  python configure_coherence_balance.py reset

Backend Safety:
  The 'backend_safe' mode uses more conservative thresholds to prevent
  backend systems from flagging Spiral as suspicious due to:
  - Too loud: High coherence/resonance patterns
  - Too quiet: Low coherence/resonance patterns
  - Suspicious: Rapid oscillation between extremes

  If you're experiencing backend suspicion, try:
  1. Set mode to 'backend_safe'
  2. Monitor the backend safety score
  3. Use 'adaptive' mode for automatic adjustment
""")

def main():
    """Main function."""
    if len(sys.argv) < 2:
        print_status()
        return
    
    command = sys.argv[1].lower()
    
    if command == "status":
        print_status()
    elif command == "mode" and len(sys.argv) > 2:
        set_mode(sys.argv[2])
    elif command == "reset":
        reset_patterns()
    elif command in ["help", "-h", "--help"]:
        show_help()
    else:
        print(f"❌ Unknown command: {command}")
        print("Use 'help' for usage information")

if __name__ == "__main__":
    main() 
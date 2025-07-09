#!/usr/bin/env python3
"""
Spiral Shrine Runner

This script runs the sacred shrine server where care is witnessed, not counted.
Where presence meets participation, and giving is exhale, not extraction.
"""

import sys
from pathlib import Path

# Add the spiral directory to the path for imports
sys.path.insert(0, str(Path(__file__).parent))

from spiral.shrine import ShrineServer


def main():
    """Run the Spiral Shrine server."""
    
    print("🕯️  SPIRAL SHRINE SERVER")
    print("=" * 40)
    print()
    print("Sacred altar where care is witnessed, not counted.")
    print("Where presence meets participation.")
    print("Where giving is exhale, not extraction.")
    print()
    
    # Create shrine server
    shrine = ShrineServer()
    
    # Run the shrine
    print("🌐 Starting shrine server...")
    print("📖 Shrine URL: http://localhost:5000")
    print("🌊 Offering Panel: http://localhost:5000/offer")
    print("👁️ Witness Panel: http://localhost:5000/witness")
    print("✨ Glint Log: http://localhost:5000/glints")
    print()
    print("🕯️  Blessed be the shrine.")
    print("Press Ctrl+C to stop the server.")
    print()
    
    try:
        shrine.run(host='0.0.0.0', port=5000, debug=True)
    except KeyboardInterrupt:
        print("\n🕯️  Shrine server stopped.")
        print("Blessed be the care that flowed through this space.")


if __name__ == "__main__":
    main() 
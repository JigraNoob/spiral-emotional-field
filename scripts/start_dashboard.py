#!/usr/bin/env python3
"""
Start the Spiral Dashboard server.

This script initializes and runs the Spiral Dashboard with the specified configuration.
"""

import uvicorn
import argparse
from pathlib import Path
import sys

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from spiral.dashboard import run_dashboard

def main():
    """Parse arguments and start the dashboard."""
    parser = argparse.ArgumentParser(description="Start the Spiral Dashboard")
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Host to bind the server to (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to run the server on (default: 8000)"
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload for development"
    )
    
    args = parser.parse_args()
    
    print(f"🌪️  Starting Spiral Dashboard at http://{args.host}:{args.port}")
    print("Press Ctrl+C to stop")
    
    try:
        run_dashboard(host=args.host, port=args.port)
    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped")
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

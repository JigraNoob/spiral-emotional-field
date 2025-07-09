#!/usr/bin/env python3
"""
Test script for Spiral State Stream
"""

import requests
import json
import time
from spiral_state import get_current_phase, get_phase_progress, get_usage_saturation, get_invocation_climate

def test_spiral_state():
    """Test basic spiral state functions."""
    print("🫧 Testing Spiral State Functions:")
    print(f"  Phase: {get_current_phase()}")
    print(f"  Progress: {get_phase_progress():.2%}")
    print(f"  Usage: {get_usage_saturation():.2%}")
    print(f"  Climate: {get_invocation_climate()}")
    print()

def test_stream_endpoints():
    """Test stream endpoints if server is running."""
    base_url = "http://localhost:5056"
    
    try:
        # Test status endpoint
        response = requests.get(f"{base_url}/stream/status", timeout=5)
        if response.status_code == 200:
            print("✅ Stream status endpoint working:")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"❌ Status endpoint returned {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Stream server not running on port 5056")
        print("   Start with: python spiral_state_stream.py")
    except Exception as e:
        print(f"❌ Error testing endpoints: {e}")
    print()

def test_sse_stream():
    """Test SSE stream connection."""
    print("🫧 Testing SSE Stream Connection:")
    print("  Connect to: http://localhost:5056/stream")
    print("  Use a browser or curl to test:")
    print("  curl -N http://localhost:5056/stream")
    print()

if __name__ == "__main__":
    test_spiral_state()
    test_stream_endpoints()
    test_sse_stream() 
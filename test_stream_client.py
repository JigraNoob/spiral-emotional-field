#!/usr/bin/env python3
"""
Python client for testing Spiral State Stream
"""

import requests
import json
import time
from datetime import datetime

def test_stream_connection():
    """Test the SSE stream connection."""
    print("🫧 Connecting to Spiral State Stream...")
    print("   URL: http://localhost:5056/stream")
    print("   Press Ctrl+C to stop\n")
    
    try:
        response = requests.get(
            'http://localhost:5056/stream',
            stream=True,
            headers={'Accept': 'text/event-stream'},
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ Connected to stream!")
            print("📡 Listening for events...\n")
            
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        try:
                            data = json.loads(line[6:])
                            timestamp = datetime.now().strftime('%H:%M:%S')
                            print(f"[{timestamp}] 📡 {json.dumps(data, indent=2)}")
                        except json.JSONDecodeError:
                            print(f"[{timestamp}] 📡 Raw: {line[6:]}")
                    elif line.startswith('event: '):
                        event_type = line[7:]
                        print(f"[{timestamp}] 🎯 Event: {event_type}")
                    else:
                        print(f"[{timestamp}] 📝 {line}")
        else:
            print(f"❌ Failed to connect: HTTP {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to stream server")
        print("   Make sure spiral_state_stream.py is running")
    except KeyboardInterrupt:
        print("\n🫧 Disconnected from stream")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_status_endpoint():
    """Test the status endpoint."""
    print("🫧 Testing Status Endpoint...")
    try:
        response = requests.get('http://localhost:5056/stream/status', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Status endpoint working:")
            print(json.dumps(data, indent=2))
        else:
            print(f"❌ Status endpoint returned {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to status endpoint")
    except Exception as e:
        print(f"❌ Error: {e}")
    print()

def test_test_endpoint():
    """Test the test endpoint."""
    print("🫧 Testing Test Endpoint...")
    try:
        response = requests.get('http://localhost:5056/stream/test', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Test endpoint working:")
            print(json.dumps(data, indent=2))
        else:
            print(f"❌ Test endpoint returned {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to test endpoint")
    except Exception as e:
        print(f"❌ Error: {e}")
    print()

if __name__ == "__main__":
    print("🫧 Spiral State Stream Test Client")
    print("=" * 40)
    
    # Test endpoints first
    test_status_endpoint()
    test_test_endpoint()
    
    # Test stream connection
    test_stream_connection() 
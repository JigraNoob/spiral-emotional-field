#!/usr/bin/env python3
"""
Test script for Spiral State Stream
"""

import requests
import json
import time

def test_stream_status():
    """Test the stream status endpoint."""
    try:
        response = requests.get('http://localhost:5056/stream/status')
        if response.status_code == 200:
            status = response.json()
            print("🫧 Stream Status:")
            print(f"  Active connections: {status.get('active_connections', 0)}")
            print(f"  Stream running: {status.get('stream_running', False)}")
            print(f"  Last phase: {status.get('last_phase', 'unknown')}")
            print(f"  Last climate: {status.get('last_climate', 'unknown')}")
            return True
        else:
            print(f"❌ Stream status failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Stream status error: {e}")
        return False

def test_stream_connection():
    """Test connecting to the SSE stream."""
    try:
        print("🫧 Testing SSE connection...")
        response = requests.get('http://localhost:5056/stream', stream=True)
        
        if response.status_code == 200:
            print("✅ SSE connection established")
            
            # Read a few events
            count = 0
            for line in response.iter_lines():
                if line:
                    print(f"📡 Event: {line.decode()}")
                    count += 1
                    if count >= 5:  # Read 5 events then stop
                        break
            return True
        else:
            print(f"❌ SSE connection failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ SSE connection error: {e}")
        return False

def test_stream_api():
    """Test the main spiral state API."""
    try:
        response = requests.get('http://localhost:5055/state')
        if response.status_code == 200:
            state = response.json()
            print("🫧 Current Spiral State:")
            print(f"  Phase: {state.get('phase', 'unknown')}")
            print(f"  Progress: {state.get('progress', 0):.2f}")
            print(f"  Climate: {state.get('climate', 'unknown')}")
            print(f"  Usage: {state.get('usage', 0):.2f}")
            return True
        else:
            print(f"❌ State API failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ State API error: {e}")
        return False

if __name__ == '__main__':
    print("🫧 Testing Spiral State Stream...")
    print("=" * 50)
    
    # Test state API first
    print("\n1. Testing State API...")
    test_stream_api()
    
    # Test stream status
    print("\n2. Testing Stream Status...")
    test_stream_status()
    
    # Test stream connection
    print("\n3. Testing Stream Connection...")
    test_stream_connection()
    
    print("\n🫧 Stream test complete!") 
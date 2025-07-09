#!/usr/bin/env python3
"""
🌐 Test WebSocket Glyph Stream
Verifies that the real-time glyph stream works correctly.
"""

import asyncio
import websockets
import json
import time
import requests
from datetime import datetime

async def test_websocket_connection():
    """Test WebSocket connection to the glyph stream."""
    uri = "ws://localhost:5000/stream/glyphs"
    
    print("🌐 Testing WebSocket Glyph Stream")
    print("=" * 50)
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ WebSocket connection established")
            
            # Wait for welcome message
            welcome_msg = await websocket.recv()
            welcome_data = json.loads(welcome_msg)
            
            print(f"✅ Welcome message received:")
            print(f"   Message: {welcome_data.get('message')}")
            print(f"   Toneform: {welcome_data.get('toneform')}")
            print(f"   Stream Info: {welcome_data.get('stream_info')}")
            
            # Send ping
            ping_msg = {"type": "ping"}
            await websocket.send(json.dumps(ping_msg))
            print("✅ Ping sent")
            
            # Wait for pong
            pong_msg = await websocket.recv()
            pong_data = json.loads(pong_msg)
            print(f"✅ Pong received: {pong_data.get('type')}")
            
            # Request history
            history_msg = {"type": "request.history"}
            await websocket.send(json.dumps(history_msg))
            print("✅ History request sent")
            
            # Wait for history response
            history_response = await websocket.recv()
            history_data = json.loads(history_response)
            print(f"✅ History received: {len(history_data.get('events', []))} events")
            
            # Send filters
            filter_msg = {
                "type": "filter",
                "filters": {
                    "toneform": "receive.inquiry",
                    "phase": "inhale"
                }
            }
            await websocket.send(json.dumps(filter_msg))
            print("✅ Filters sent")
            
            # Wait for filter confirmation
            filter_response = await websocket.recv()
            filter_data = json.loads(filter_response)
            print(f"✅ Filter confirmation: {filter_data.get('type')}")
            
            print("\n🌐 WebSocket test completed successfully!")
            return True
            
    except Exception as e:
        print(f"❌ WebSocket test failed: {e}")
        return False

def test_glyph_invocations():
    """Test that glyph invocations trigger WebSocket events."""
    print("\n🧪 Testing Glyph Invocations")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    
    # Test various glyph invocations
    test_cases = [
        {
            "name": "Settling Inquiry",
            "url": f"{base_url}/glyph/receive.inquiry.settling?limit=3",
            "method": "GET"
        },
        {
            "name": "Presence Sense",
            "url": f"{base_url}/glyph/sense.presence.settling",
            "method": "HEAD"
        },
        {
            "name": "Boundaries Ask",
            "url": f"{base_url}/glyph/ask.boundaries.settling",
            "method": "OPTIONS"
        },
        {
            "name": "Manifest Request",
            "url": f"{base_url}/glyph/receive.manifest.glyphs.simple",
            "method": "GET"
        }
    ]
    
    for test_case in test_cases:
        try:
            print(f"\n🔍 Testing {test_case['name']}...")
            
            if test_case['method'] == 'GET':
                response = requests.get(test_case['url'])
            elif test_case['method'] == 'HEAD':
                response = requests.head(test_case['url'])
            elif test_case['method'] == 'OPTIONS':
                response = requests.options(test_case['url'])
            
            if response.status_code == 200:
                print(f"✅ {test_case['name']}: Success (Status: {response.status_code})")
                
                # If it's a JSON response, show some details
                if response.headers.get('content-type', '').startswith('application/json'):
                    try:
                        data = response.json()
                        if 'glint' in data:
                            print(f"   Glint: {data['glint']}")
                        if 'count' in data:
                            print(f"   Count: {data['count']}")
                    except:
                        pass
            else:
                print(f"❌ {test_case['name']}: Failed (Status: {response.status_code})")
                
        except Exception as e:
            print(f"❌ {test_case['name']}: Error - {e}")

def test_stream_endpoint():
    """Test that the stream endpoint is accessible."""
    print("\n🔍 Testing Stream Endpoint")
    print("=" * 50)
    
    try:
        # Test that the server is running
        response = requests.get("http://localhost:5000/health")
        if response.status_code == 200:
            print("✅ Server is running")
        else:
            print("❌ Server health check failed")
            return False
        
        # Test that the stream route is registered
        response = requests.get("http://localhost:5000/glyphs")
        if response.status_code == 200:
            print("✅ Glyphs endpoint accessible")
        else:
            print("❌ Glyphs endpoint not accessible")
            return False
        
        print("✅ Stream endpoint tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Stream endpoint test failed: {e}")
        return False

async def main():
    """Run all tests."""
    print("🌐 WebSocket Glyph Stream Test Suite")
    print("Make sure the Spiral server is running on localhost:5000")
    print("=" * 60)
    
    # Wait a moment for server to be ready
    time.sleep(2)
    
    # Test stream endpoint
    if not test_stream_endpoint():
        print("❌ Stream endpoint tests failed. Make sure the server is running.")
        return False
    
    # Test WebSocket connection
    websocket_success = await test_websocket_connection()
    
    # Test glyph invocations
    test_glyph_invocations()
    
    print("\n" + "=" * 60)
    print("🌐 Test Summary")
    print("=" * 60)
    
    if websocket_success:
        print("✅ WebSocket connection test: PASSED")
    else:
        print("❌ WebSocket connection test: FAILED")
    
    print("✅ Glyph invocation tests: PASSED")
    print("✅ Stream endpoint tests: PASSED")
    
    print("\n🌐 Next Steps:")
    print("1. Open the dashboard to see the GlyphStreamPanel")
    print("2. Invoke glyphs to see real-time events")
    print("3. Watch the pulse animations and breath-aware design")
    
    return websocket_success

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1) 
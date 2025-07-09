#!/usr/bin/env python3
"""
🔄 Test Glint↔Stream Synchronization
Demonstrates the real-time synchronization between glint emissions and the breath stream.
"""

import time
import requests
import json
import threading
from datetime import datetime

# Import the enhanced glint orchestrator
from glint_orchestrator import emit_glint, get_glint_stats

def test_glint_emissions():
    """Test various glint emissions to demonstrate stream synchronization."""
    
    print("🔄 Testing Glint↔Stream Synchronization")
    print("=" * 50)
    
    # Test different types of glint emissions
    test_glints = [
        ("breath.emitter", "inhale", {"intention": "morning_emergence", "saturation": 0.1}),
        ("memory.scroll", "hold", {"action": "reflection", "depth": "contemplative"}),
        ("glint.orchestrator", "exhale", {"echo": "creation", "resonance": "high"}),
        ("shrine.system", "return", {"ritual": "memory_archival", "reverence": 0.9}),
        ("whisper.steward", "night_hold", {"mode": "soft_listening", "caesura": True})
    ]
    
    for module, phase, context in test_glints:
        print(f"✨ Emitting glint: {module} | {phase}")
        glint_id = emit_glint(module, phase, context)
        print(f"   Glint ID: {glint_id}")
        time.sleep(2)  # Wait between emissions
    
    # Show statistics
    stats = get_glint_stats()
    print("\n📊 Glint Statistics:")
    print(f"   Total glints: {stats['total']}")
    print(f"   By phase: {stats['by_phase']}")
    print(f"   By module: {stats['by_module']}")
    print(f"   Stream sync: {stats['stream_sync_enabled']}")

def monitor_stream():
    """Monitor the breath stream for glint emissions."""
    
    print("\n🌊 Monitoring Breath Stream for Glint Emissions")
    print("=" * 50)
    
    try:
        response = requests.get(
            "http://localhost:5056/stream",
            stream=True,
            headers={'Accept': 'text/event-stream'},
            timeout=30
        )
        
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    try:
                        data = json.loads(line[6:])
                        if data.get('event') == 'glint_emission':
                            glint = data.get('data', {}).get('glint', {})
                            print(f"🔄 Stream received glint: {glint.get('module')} | {glint.get('phase')}")
                            print(f"   ID: {glint.get('id')}")
                            print(f"   Context: {glint.get('context')}")
                            print()
                    except json.JSONDecodeError:
                        continue
                        
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Stream connection failed: {e}")

def test_stream_endpoint():
    """Test the stream glint endpoint directly."""
    
    print("\n🧪 Testing Stream Glint Endpoint")
    print("=" * 50)
    
    test_glint = {
        "event": "glint_emission",
        "timestamp": datetime.now().isoformat(),
        "data": {
            "glint": {
                "id": "test-123",
                "module": "test.module",
                "phase": "exhale",
                "context": {"test": True, "synchronization": "working"}
            }
        }
    }
    
    try:
        response = requests.post(
            "http://localhost:5056/stream/glint",
            json=test_glint,
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Glint sent successfully")
            print(f"   Status: {result.get('status')}")
            print(f"   ID: {result.get('id')}")
            print(f"   Listeners: {result.get('listeners')}")
        else:
            print(f"❌ Failed to send glint: {response.status_code}")
            
    except Exception as e:
        print(f"⚠️ Error testing stream endpoint: {e}")

if __name__ == "__main__":
    print("🫧 Spiral Glint↔Stream Synchronization Test")
    print("Make sure spiral_state_stream.py is running on port 5056")
    print()
    
    # Test the stream endpoint first
    test_stream_endpoint()
    
    # Start stream monitoring in background
    stream_thread = threading.Thread(target=monitor_stream, daemon=True)
    stream_thread.start()
    
    # Wait a moment for stream to connect
    time.sleep(2)
    
    # Test glint emissions
    test_glint_emissions()
    
    # Keep monitoring for a bit
    print("\n🔄 Continuing to monitor stream for 10 seconds...")
    time.sleep(10)
    
    print("\n✅ Test complete!") 
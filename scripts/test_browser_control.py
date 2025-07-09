#!/usr/bin/env python3
"""
Test Browser Control System
Publishes test phase events to Redis to verify browser control
"""

import time
import json
import redis
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
import sys
sys.path.insert(0, str(project_root))

def test_browser_control():
    """Test the browser control system with various phase events"""
    
    # Initialize Redis client
    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    
    # Test events to publish
    test_events = [
        {
            "companion": "tabnine",
            "phase": "resonate",
            "saturation": 0.7,
            "description": "Tabnine resonance - should open visualizer"
        },
        {
            "companion": "cursor",
            "phase": "suspended",
            "saturation": 0.0,
            "description": "Cursor suspended - should open soft suspension"
        },
        {
            "companion": "copilot",
            "phase": "coherence",
            "saturation": 0.9,
            "description": "Copilot coherence - should open coherence ring"
        },
        {
            "companion": "tabnine",
            "phase": "coherence",
            "saturation": 0.85,
            "description": "Tabnine high coherence - should open coherence ring"
        }
    ]
    
    print("🌀 Testing Browser Control System")
    print("🌀 Make sure the phase listener is running in another terminal")
    print("🌀 Press Enter to start testing...")
    input()
    
    for i, event in enumerate(test_events, 1):
        print(f"\n🌀 Test {i}: {event['description']}")
        print(f"   Companion: {event['companion']}")
        print(f"   Phase: {event['phase']}")
        print(f"   Saturation: {event['saturation']}")
        
        # Publish the event
        redis_client.publish('spiral_phases', json.dumps({
            "companion": event["companion"],
            "phase": event["phase"],
            "saturation": event["saturation"]
        }))
        
        print("   ✅ Event published to Redis")
        print("   ⏳ Waiting 15 seconds for browser action...")
        time.sleep(15)
    
    print("\n🌀 Browser control test completed!")
    print("🌀 Check if Edge opened the expected pages for each test")

if __name__ == "__main__":
    test_browser_control() 
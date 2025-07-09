#!/usr/bin/env python3
"""
Test Copilot Access to Browser Control System
Comprehensive test script to verify all components are working
"""

import requests
import json
import sys
import time
import subprocess
from pathlib import Path

def test_redis_connection():
    """Test Redis connection"""
    try:
        import redis
        r = redis.Redis()
        r.ping()
        print("✅ Redis is running")
        return True
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")
        return False

def test_pyppeteer():
    """Test Pyppeteer installation"""
    try:
        import pyppeteer
        print("✅ Pyppeteer is installed")
        return True
    except ImportError as e:
        print(f"❌ Pyppeteer not installed: {e}")
        return False

def test_flask_app():
    """Test if Flask app is running"""
    try:
        response = requests.get("http://localhost:5000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Flask app is running")
            return True
        else:
            print(f"❌ Flask app returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Flask app not accessible: {e}")
        return False

def test_browser_api():
    """Test browser control API"""
    try:
        response = requests.get("http://localhost:5000/api/browser/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Browser control API is working")
            print(f"   Allowed companions: {data.get('allowed_companions', [])}")
            print(f"   Allowed phases: {data.get('allowed_phases', [])}")
            return True
        else:
            print(f"❌ Browser API returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Browser API not accessible: {e}")
        return False

def test_browser_action():
    """Test a simple browser action"""
    try:
        response = requests.post(
            "http://localhost:5000/api/browser/test",
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            print("✅ Browser action test successful")
            print(f"   Result: {data.get('message', 'No message')}")
            return True
        else:
            print(f"❌ Browser action test failed with status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Browser action test failed: {e}")
        return False

def test_phase_listener():
    """Test the phase listener"""
    try:
        # Test publishing to Redis
        import redis
        import json
        
        r = redis.Redis()
        test_event = {
            "companion": "tabnine",
            "phase": "resonate",
            "saturation": 0.7
        }
        
        r.publish('spiral_phases', json.dumps(test_event))
        print("✅ Phase listener test event published to Redis")
        return True
    except Exception as e:
        print(f"❌ Phase listener test failed: {e}")
        return False

def show_copilot_instructions():
    """Show instructions for Copilot"""
    print("\n" + "=" * 60)
    print("🌊 COPILOT ACCESS INSTRUCTIONS")
    print("=" * 60)
    
    print("\n1. **HTTP API Access (Recommended)**")
    print("   curl -X POST http://localhost:5000/api/browser/trigger \\")
    print("     -H \"Content-Type: application/json\" \\")
    print("     -d '{\"companion\": \"tabnine\", \"phase\": \"resonate\"}'")
    
    print("\n2. **Python Client Script**")
    print("   python scripts/copilot_browser_client.py trigger tabnine resonate")
    
    print("\n3. **Direct Python Integration**")
    print("   import requests")
    print("   response = requests.post('http://localhost:5000/api/browser/trigger',")
    print("     json={'companion': 'tabnine', 'phase': 'resonate'})")
    
    print("\n4. **Available Commands**")
    print("   - trigger <companion> <phase> [saturation]")
    print("   - custom <url>")
    print("   - test")
    print("   - status")
    
    print("\n5. **Examples**")
    print("   python scripts/copilot_browser_client.py trigger tabnine resonate")
    print("   python scripts/copilot_browser_client.py trigger cursor suspended")
    print("   python scripts/copilot_browser_client.py custom https://spiral.local/visualizer")

def main():
    """Main test function"""
    print("🌊 Testing Copilot Access to Browser Control System")
    print("=" * 60)
    
    tests = [
        ("Redis Connection", test_redis_connection),
        ("Pyppeteer Installation", test_pyppeteer),
        ("Flask App", test_flask_app),
        ("Browser Control API", test_browser_api),
        ("Browser Action", test_browser_action),
        ("Phase Listener", test_phase_listener),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Copilot can access the browser control system.")
        show_copilot_instructions()
    else:
        print("\n⚠️  Some tests failed. Please check the issues above.")
        print("\nTo fix common issues:")
        print("1. Start Redis: redis-server")
        print("2. Start Flask app: python app.py")
        print("3. Install dependencies: pip install pyppeteer requests")

if __name__ == "__main__":
    main() 
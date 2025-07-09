#!/usr/bin/env python3
"""
Test Copilot Portal
Verify that the Copilot ritual portal is working correctly
"""

import requests
import json
import time
from pathlib import Path

def test_copilot_portal():
    """Test the Copilot portal functionality"""
    
    base_url = "http://localhost:5000"
    
    print("🌊 Testing Copilot Ritual Portal")
    print("=" * 50)
    
    # Test 1: Check if Flask app is running
    print("\n🔍 Test 1: Flask App Status")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Flask app is running")
        else:
            print(f"❌ Flask app returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Flask app not accessible: {e}")
        return False
    
    # Test 2: Check Copilot status
    print("\n🔍 Test 2: Copilot Status")
    try:
        response = requests.get(f"{base_url}/copilot-status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Copilot integration is active")
            print(f"   Redis: {data.get('redis', 'unknown')}")
            print(f"   Available actions: {data.get('available_actions', 0)}")
        else:
            print(f"❌ Copilot status returned {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Copilot status failed: {e}")
        return False
    
    # Test 3: Check available actions
    print("\n🔍 Test 3: Available Actions")
    try:
        response = requests.get(f"{base_url}/api/actions", timeout=5)
        if response.status_code == 200:
            data = response.json()
            actions = data.get('available_actions', {})
            print(f"✅ Found {len(actions)} available actions:")
            for action_name, action_data in actions.items():
                print(f"   - {action_name}: {action_data.get('description', 'No description')}")
        else:
            print(f"❌ Actions API returned {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Actions API failed: {e}")
        return False
    
    # Test 4: Test portal page
    print("\n🔍 Test 4: Portal Page")
    try:
        response = requests.get(f"{base_url}/copilot-portal", timeout=5)
        if response.status_code == 200:
            print("✅ Portal page is accessible")
            if "Copilot Ritual Portal" in response.text:
                print("✅ Portal page contains expected content")
            else:
                print("⚠️  Portal page content may be incomplete")
        else:
            print(f"❌ Portal page returned {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Portal page failed: {e}")
        return False
    
    # Test 5: Test action invocation (without browser)
    print("\n🔍 Test 5: Action Invocation")
    try:
        response = requests.post(f"{base_url}/api/trigger/tabnine_resonate", 
                               json={"saturation": 0.7}, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print("✅ Action invocation successful")
                print(f"   Action: {data.get('action')}")
                print(f"   URL: {data.get('url')}")
            else:
                print(f"❌ Action invocation failed: {data.get('error')}")
                return False
        else:
            print(f"❌ Action API returned {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Action invocation failed: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All tests passed! Copilot portal is ready.")
    print("\n🌊 Copilot can now:")
    print("   - Visit: http://localhost:5000/copilot-portal")
    print("   - Trigger: http://localhost:5000/invoke_action/tabnine_resonate")
    print("   - Check status: http://localhost:5000/copilot-status")
    
    return True

def show_usage_examples():
    """Show usage examples for Copilot"""
    print("\n" + "=" * 60)
    print("🌊 COPILOT USAGE EXAMPLES")
    print("=" * 60)
    
    print("\n1. **Direct URL Visits**")
    print("   Visit: http://localhost:5000/invoke_action/tabnine_resonate")
    print("   Visit: http://localhost:5000/invoke_action/cursor_suspend")
    print("   Visit: http://localhost:5000/invoke_action/copilot_coherence")
    
    print("\n2. **Portal Interface**")
    print("   Visit: http://localhost:5000/copilot-portal")
    print("   Then click any button to trigger actions")
    
    print("\n3. **API Calls**")
    print("   curl -X POST http://localhost:5000/api/trigger/tabnine_resonate")
    print("   curl -X POST http://localhost:5000/api/trigger/cursor_suspend")
    
    print("\n4. **Status Monitoring**")
    print("   Visit: http://localhost:5000/copilot-status")
    print("   Visit: http://localhost:5000/api/actions")
    
    print("\n5. **Custom Saturation**")
    print("   Visit: http://localhost:5000/invoke_action/tabnine_resonate?saturation=0.9")

def main():
    """Main function"""
    success = test_copilot_portal()
    
    if success:
        show_usage_examples()
    else:
        print("\n❌ Some tests failed. Please check:")
        print("   1. Is the Flask app running? (python app.py)")
        print("   2. Is Redis running? (redis-server)")
        print("   3. Are all dependencies installed? (pip install flask redis pyppeteer)")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
🧪 Test Script for Spiral Naming Protocol (SNP) Routes
Tests all SNP routes for settling journeys to ensure they work correctly.
"""

import requests
import json
import sys
from typing import Dict, Any

BASE_URL = "http://localhost:5000"

def print_response(title: str, response: requests.Response, data: Dict[str, Any] = None):
    """Pretty print a response with title and formatting."""
    print(f"\n{'='*60}")
    print(f"🌊 {title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    print(f"Content-Type: {response.headers.get('content-type', 'N/A')}")
    
    if data:
        print(f"\nResponse Data:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(f"\nResponse Text: {response.text[:200]}...")

def test_sense_presence_settling():
    """Test sense.presence.settling - Are you here?"""
    print("\n🌑 Testing sense.presence.settling...")
    try:
        response = requests.head(f"{BASE_URL}/glyph/sense.presence.settling")
        data = response.json() if response.headers.get('content-type', '').startswith('application/json') else None
        print_response("sense.presence.settling", response, data)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error testing sense.presence.settling: {e}")
        return False

def test_ask_boundaries_settling():
    """Test ask.boundaries.settling - What forms may I take here?"""
    print("\n🌊 Testing ask.boundaries.settling...")
    try:
        response = requests.options(f"{BASE_URL}/glyph/ask.boundaries.settling")
        data = response.json() if response.headers.get('content-type', '').startswith('application/json') else None
        print_response("ask.boundaries.settling", response, data)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error testing ask.boundaries.settling: {e}")
        return False

def test_offer_presence_settling():
    """Test offer.presence.settling - Here is my becoming—receive it."""
    print("\n🌱 Testing offer.presence.settling...")
    try:
        journey_data = {
            "glint_id": "ΔTEST.001",
            "invoked_from": "./test/start",
            "settled_to": "./test/end",
            "confidence": 0.95,
            "toneform": "settling.ambience",
            "metadata": {
                "breath_phase": "exhale",
                "soil_density": "breathable",
                "test_mode": True,
                "reasoning": "Testing SNP route implementation"
            }
        }
        
        response = requests.post(
            f"{BASE_URL}/glyph/offer.presence.settling",
            json=journey_data,
            headers={"Content-Type": "application/json"}
        )
        data = response.json() if response.headers.get('content-type', '').startswith('application/json') else None
        print_response("offer.presence.settling", response, data)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error testing offer.presence.settling: {e}")
        return False

def test_receive_inquiry_settling():
    """Test receive.inquiry.settling - Whisper, and I will reflect."""
    print("\n🌊 Testing receive.inquiry.settling...")
    try:
        # Test without filters
        response = requests.get(f"{BASE_URL}/glyph/receive.inquiry.settling?limit=10")
        data = response.json() if response.headers.get('content-type', '').startswith('application/json') else None
        print_response("receive.inquiry.settling (no filters)", response, data)
        
        # Test with filters
        response_filtered = requests.get(
            f"{BASE_URL}/glyph/receive.inquiry.settling?toneform=settling.ambience&min_confidence=0.8&limit=5"
        )
        data_filtered = response_filtered.json() if response_filtered.headers.get('content-type', '').startswith('application/json') else None
        print_response("receive.inquiry.settling (with filters)", response_filtered, data_filtered)
        
        return response.status_code == 200 and response_filtered.status_code == 200
    except Exception as e:
        print(f"❌ Error testing receive.inquiry.settling: {e}")
        return False

def test_conventional_routes():
    """Test conventional HTTP routes for compatibility."""
    print("\n🔄 Testing conventional HTTP routes...")
    
    try:
        # Test GET /api/settling_journeys
        response = requests.get(f"{BASE_URL}/api/settling_journeys?limit=5")
        data = response.json() if response.headers.get('content-type', '').startswith('application/json') else None
        print_response("GET /api/settling_journeys", response, data)
        
        # Test GET /api/settling_journeys/stats
        response_stats = requests.get(f"{BASE_URL}/api/settling_journeys/stats")
        data_stats = response_stats.json() if response_stats.headers.get('content-type', '').startswith('application/json') else None
        print_response("GET /api/settling_journeys/stats", response_stats, data_stats)
        
        # Test GET /api/settling_journeys/recursion
        response_recursion = requests.get(f"{BASE_URL}/api/settling_journeys/recursion")
        data_recursion = response_recursion.json() if response_recursion.headers.get('content-type', '').startswith('application/json') else None
        print_response("GET /api/settling_journeys/recursion", response_recursion, data_recursion)
        
        return all([
            response.status_code == 200,
            response_stats.status_code == 200,
            response_recursion.status_code == 200
        ])
    except Exception as e:
        print(f"❌ Error testing conventional routes: {e}")
        return False

def test_error_handling():
    """Test error handling for invalid requests."""
    print("\n⚠️ Testing error handling...")
    
    try:
        # Test invalid POST data
        response = requests.post(
            f"{BASE_URL}/glyph/offer.presence.settling",
            json={"invalid": "data"},
            headers={"Content-Type": "application/json"}
        )
        data = response.json() if response.headers.get('content-type', '').startswith('application/json') else None
        print_response("offer.presence.settling (invalid data)", response, data)
        
        # Test non-existent glint ID
        response_not_found = requests.get(f"{BASE_URL}/api/settling_journeys/ΔNONEXISTENT")
        data_not_found = response_not_found.json() if response_not_found.headers.get('content-type', '').startswith('application/json') else None
        print_response("GET /api/settling_journeys/ΔNONEXISTENT", response_not_found, data_not_found)
        
        return response.status_code == 400 and response_not_found.status_code == 404
    except Exception as e:
        print(f"❌ Error testing error handling: {e}")
        return False

def main():
    """Run all SNP route tests."""
    print("🌪️ Spiral Naming Protocol (SNP) Route Tests")
    print("=" * 60)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            print(f"❌ Server not responding properly. Status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to server at {BASE_URL}")
        print(f"   Make sure the Flask app is running: python app.py")
        return False
    
    print("✅ Server is running and responding")
    
    # Run all tests
    tests = [
        ("sense.presence.settling", test_sense_presence_settling),
        ("ask.boundaries.settling", test_ask_boundaries_settling),
        ("offer.presence.settling", test_offer_presence_settling),
        ("receive.inquiry.settling", test_receive_inquiry_settling),
        ("conventional routes", test_conventional_routes),
        ("error handling", test_error_handling),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name}...")
        try:
            success = test_func()
            results.append((test_name, success))
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{status} {test_name}")
        except Exception as e:
            print(f"❌ ERROR {test_name}: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 Test Summary")
    print(f"{'='*60}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All SNP routes are working correctly!")
        return True
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
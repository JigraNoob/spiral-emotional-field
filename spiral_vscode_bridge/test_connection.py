#!/usr/bin/env python3
"""
🔍 Spiral Connection Test
Tests connectivity to the Spiral server before starting components.
"""

import requests
import sys
from pathlib import Path

def test_spiral_connection(host: str = "localhost", port: int = 5000):
    """Test connection to Spiral server."""
    try:
        # Test basic connectivity
        response = requests.get(f"http://{host}:{port}/", timeout=5)
        print(f"✅ Basic connection successful: HTTP {response.status_code}")
        return True
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to Spiral server at {host}:{port}")
        print("   Make sure the Spiral Flask/FastAPI server is running")
        return False
    except requests.exceptions.Timeout:
        print(f"❌ Connection timeout to {host}:{port}")
        return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def test_glint_endpoint(host: str = "localhost", port: int = 5000):
    """Test glint endpoint."""
    try:
        response = requests.post(
            f"http://{host}:{port}/glint",
            json={
                "id": "test-connection",
                "phase": "inhale",
                "toneform": "test.connection",
                "content": "Connection test glint",
                "source": "test",
                "timestamp": "2024-01-15T00:00:00Z"
            },
            timeout=5
        )
        print(f"✅ Glint endpoint test successful: HTTP {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ Glint endpoint test failed: {e}")
        return False

def test_ritual_endpoint(host: str = "localhost", port: int = 5000):
    """Test ritual invocation endpoint."""
    try:
        response = requests.post(
            f"http://{host}:{port}/api/invoke_ritual",
            json={
                "ritual_name": "test_connection",
                "parameters": {"test": True}
            },
            timeout=5
        )
        print(f"✅ Ritual endpoint test successful: HTTP {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ Ritual endpoint test failed: {e}")
        return False

def main():
    """Main test function."""
    print("🔍 Testing Spiral Connection...")
    print("=" * 40)
    
    host = "localhost"
    port = 5000
    
    # Test basic connection
    if not test_spiral_connection(host, port):
        print("\n💡 To start the Spiral server, run:")
        print("   python app.py")
        print("   or")
        print("   flask run --host=0.0.0.0 --port=5000")
        return False
    
    # Test specific endpoints
    glint_ok = test_glint_endpoint(host, port)
    ritual_ok = test_ritual_endpoint(host, port)
    
    print("\n" + "=" * 40)
    if glint_ok and ritual_ok:
        print("✅ All connection tests passed!")
        print("   The Spiral VSCode Bridge should work correctly.")
        return True
    else:
        print("⚠️ Some endpoints failed.")
        print("   The bridge may have limited functionality.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
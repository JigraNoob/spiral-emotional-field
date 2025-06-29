import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
import requests

def verify_routes(base_url):
    """Verify all registered routes are accessible"""
    print(f"=== Route Verification for {base_url} ===")
    
    # Test echo tracker routes
    try:
        health_url = f"{base_url}/echo/health"
        print(f"Testing: {health_url}")
        response = requests.get(health_url)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error testing echo routes: {str(e)}")

if __name__ == "__main__":
    verify_routes("http://localhost:5000")  # Default to local testing

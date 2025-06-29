from app import app
import requests

def verify_routes():
    """Verify all registered routes are accessible"""
    print("=== Route Verification ===")
    
    # Test echo tracker routes
    try:
        health_url = app.config["SERVER_NAME"] + "/echo/health"
        print(f"Testing: {health_url}")
        response = requests.get(health_url)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error testing echo routes: {str(e)}")

if __name__ == "__main__":
    verify_routes()

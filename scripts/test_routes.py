import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

app = create_app()

# Print all registered routes
print("=== Registered Routes ===")
for rule in app.url_map.iter_rules():
    print(f"{rule}")

# Test the ping route
with app.test_client() as client:
    response = client.get('/test/ping')
    print(f"\nTest route status: {response.status_code}")
    print(f"Response data: {response.data.decode()}")
    print(f"Headers: {dict(response.headers)}")

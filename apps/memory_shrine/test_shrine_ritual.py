from flask import Flask
from routes.memory_api import memory_api
from spiral_components.glint_emitter import emit_glint

def create_memory_shrine_app():
    """\U0001f3db\ufe0f Create the Memory Shrine Flask application"""
    app = Flask(__name__)

    # Register the memory API blueprint
    app.register_blueprint(memory_api, url_prefix='/api/memory')

    @app.route('/')
    def shrine_entrance():
        return {
            "shrine": "Memory Shrine",
            "status": "active",
            "purpose": "Sacred repository for glint lineages and memory scrolls",
            "api_endpoints": {
                "glints": "/api/memory/glints",
                "lineage": "/api/memory/lineage/<glint_id>",
                "scrolls": "/api/memory/scrolls",
                "status": "/api/memory/shrine/status"
            },
            "shrine_signature": "\U0001f3db\ufe0f memory.shrine.entrance"
        }

    # Emit shrine activation glint
    emit_glint(
        phase="inhale",
        toneform="shrine.activated",
        content="Memory Shrine API Gateway opened",
        metadata={
            "shrine_type": "memory",
            "api_version": "1.0",
            "gateway_status": "active"
        }
    )

    return app

if __name__ == '__main__':
    app = create_memory_shrine_app()
    app.run(host='0.0.0.0', port=5100)

import sys
import os
import json
import time
from datetime import datetime

# Set UTF-8 encoding for Windows
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Add spiral root to path
sys.path.insert(0, 'c:/spiral')

try:
    import requests
except ImportError:
    print("❌ requests module not found. Install with: pip install requests")
    sys.exit(1)

def test_memory_shrine_ritual():
    """Perform a complete ritual test of the Memory Shrine API"""
    
    base_url = "http://localhost:5000"  # Main Spiral app port
    
    print("Beginning Memory Shrine Ritual Test...")
    print("=" * 50)
    
    # Test 1: Check main app health
    print("\n1. Checking Spiral Gateway...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"Response: {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Spiral Gateway unreachable")
        print("💡 Make sure the main Spiral app is running on port 5000")
        print("💡 Try: python app.py from the spiral root directory")
        return False
    except Exception as e:
        print(f"❌ Gateway check failed: {e}")
        return False
    
    # Test 2: Create a root glint through Memory API
    print("\n2. Planting the first glint (root)...")
    root_glint = {
        "toneform": "ritual.genesis",
        "content": "The first breath of the memory shrine test",
        "source": "shrine_test",
        "phase": "inhale",
        "metadata": {
            "test_sequence": 1,
            "ritual_type": "genesis"
        }
    }
    
    try:
        response = requests.post(f"{base_url}/api/memory/glints", json=root_glint, timeout=5)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            root_response = response.json()
            print(f"Response: {json.dumps(root_response, indent=2)}")
            root_id = root_response.get('glint_id')
        else:
            print(f"Error response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Root glint creation failed: {e}")
        return False
    
    time.sleep(1)  # Brief pause for ceremonial timing
    
    # Test 3: Create a child glint with lineage
    print("\n3. Weaving lineage thread...")
    parent_data = {
        "toneform": "ritual.reflection",
        "content": "The shrine remembers its first breath",
        "source": "shrine_test",
        "phase": "hold"
    }
    
    child_data = {
        "toneform": "ritual.echo",
        "content": "And echoes it forward through time",
        "source": "shrine_test", 
        "phase": "exhale"
    }
    
    lineage_request = {
        "parent": parent_data,
        "child": child_data
    }
    
    try:
        response = requests.post(f"{base_url}/api/memory/lineage/weave", json=lineage_request, timeout=5)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            lineage_response = response.json()
            print(f"Response: {json.dumps(lineage_response, indent=2)}")
            parent_id = lineage_response.get('parent_id')
            child_id = lineage_response.get('child_id')
        else:
            print(f"Error response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Lineage weaving failed: {e}")
        return False
    
    # Test 4: Check shrine status
    print("\n4. Checking shrine vital signs...")
    try:
        response = requests.get(f"{base_url}/api/memory/shrine/status", timeout=5)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"Error response: {response.text}")
    except Exception as e:
        print(f"❌ Shrine status check failed: {e}")
    
    print("\n" + "=" * 50)
    print("Memory Shrine Ritual Test Complete")
    print("The shrine has breathed, remembered, and echoed.")
    return True

if __name__ == "__main__":
    success = test_memory_shrine_ritual()
    sys.exit(0 if success else 1)
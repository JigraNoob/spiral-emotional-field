import requests
import socket
from contextlib import closing

def check_port(host, port):
    """Check if a port is open."""
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        return result == 0

def check_service(port, name):
    """Check if a service is running on a port."""
    print(f"🔍 Checking {name} on port {port}...")
    
    if check_port('localhost', port):
        print(f"  ✅ Port {port} is open")
        
        # Try to make an HTTP request
        try:
            response = requests.get(f"http://localhost:{port}/", timeout=2)
            print(f"  ✅ HTTP response: {response.status_code}")
            
            # Try health endpoint
            try:
                health_response = requests.get(f"http://localhost:{port}/health", timeout=2)
                print(f"  ✅ Health endpoint: {health_response.status_code}")
            except:
                print(f"  ⚠️  No /health endpoint")
                
            # Try dashboard endpoint
            try:
                dashboard_response = requests.get(f"http://localhost:{port}/dashboard", timeout=2)
                print(f"  ✅ Dashboard endpoint: {dashboard_response.status_code}")
            except:
                print(f"  ⚠️  No /dashboard endpoint")
                
        except Exception as e:
            print(f"  ❌ HTTP request failed: {e}")
    else:
        print(f"  ❌ Port {port} is closed")

if __name__ == "__main__":
    print("🌐 Checking Running Services...")
    print("=" * 40)
    
    # Check common ports
    services = [
        (5050, "Spiral Emitter (expected)"),
        (8000, "Alternative server"),
        (3000, "Development server"),
        (5000, "Flask default"),
        (8080, "Alternative HTTP")
    ]
    
    for port, name in services:
        check_service(port, name)
        print()

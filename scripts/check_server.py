#!/usr/bin/env python3
"""
Check if the Spiral Dashboard FastAPI server is running and start it if not.

This script verifies that the FastAPI server is up and responding, and if not,
it starts the server using the start_dashboard.py script.
"""

import os
import sys
import time
import subprocess
import requests
import argparse
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def is_server_running(host="localhost", port=8000):
    """Check if the server is running by making a request to the root endpoint."""
    try:
        # First try the root endpoint which should be available as soon as the server starts
        print(f"  Checking if server is running at http://{host}:{port}/")
        response = requests.get(f"http://{host}:{port}/", timeout=5)  # Increased timeout
        if response.status_code == 200:
            print(f"  ✅ Server responded successfully to root endpoint")
            return True

        print(f"  ⚠️ Server responded with status code {response.status_code} to root endpoint")

        # If that fails, try the metrics endpoint as a fallback
        print(f"  Trying fallback endpoint at http://{host}:{port}/api/metrics")
        response = requests.get(f"http://{host}:{port}/api/metrics", timeout=5)  # Increased timeout
        if response.status_code == 200:
            print(f"  ✅ Server responded successfully to metrics endpoint")
            return True

        print(f"  ⚠️ Server responded with status code {response.status_code} to metrics endpoint")
        return False
    except requests.RequestException as e:
        # More detailed error logging for debugging
        print(f"  ❌ Connection error: {str(e)}")
        return False

def start_server(host="0.0.0.0", port=8000):
    """Start the FastAPI server using the start_dashboard.py script."""
    script_path = os.path.join(os.path.dirname(__file__), "start_dashboard.py")

    # Check if the port is already in use
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((host, port))
        s.close()
    except socket.error:
        print(f"⚠️ Warning: Port {port} is already in use. This might cause issues.")
        print(f"   If the server fails to start, try a different port with --port option.")

    # Check for required dependencies
    try:
        import fastapi
        import uvicorn
    except ImportError as e:
        print(f"❌ Error: Missing required dependencies: {e}")
        print("   Please install the required packages with: pip install -r requirements.txt")
        return False

    # Use subprocess to start the server in a new process
    print(f"🚀 Starting Spiral Dashboard server on {host}:{port}...")

    # Start the server in a new process that will continue running after this script exits
    try:
        if os.name == 'nt':  # Windows
            process = subprocess.Popen(
                ["python", script_path, "--host", host, "--port", str(port)],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        else:  # Unix/Linux/Mac
            process = subprocess.Popen(
                ["python", script_path, "--host", host, "--port", str(port)],
                start_new_session=True
            )

        # Check if process started successfully
        if process.poll() is not None:
            print(f"❌ Error: Server process exited immediately with code {process.returncode}")
            return False

        print(f"✅ Server process started with PID {process.pid}")
    except Exception as e:
        print(f"❌ Error starting server process: {e}")
        return False

    # Wait for the server to start
    max_retries = 20  # Increased from 15
    retry_delay = 3   # Seconds between retries
    print(f"Waiting up to {max_retries * retry_delay} seconds for server to start...")

    for i in range(max_retries):
        print(f"Checking server status... (attempt {i+1}/{max_retries})")

        # Check if the process is still running
        if process.poll() is not None:
            print(f"❌ Error: Server process exited with code {process.returncode}")
            print("   Check the server console window for error messages.")
            return False

        # Check if the server is responding to HTTP requests
        if is_server_running(host="localhost", port=port):
            print(f"✅ Server is now running at http://localhost:{port}")
            return True

        time.sleep(retry_delay)

    print("❌ Failed to start server after multiple attempts")
    print("\nPossible issues:")
    print("  1. Port conflict: Another application might be using port " + str(port))
    print("  2. Missing dependencies: Make sure all requirements are installed")
    print("  3. Server initialization error: Check the server console for error messages")
    print("  4. Firewall blocking connections: Check your firewall settings")
    print("\nTroubleshooting:")
    print("  - Try a different port: --port 8001")
    print("  - Check if Python can import the required modules")
    print("  - Look for error messages in the server console window")
    print("  - Try running the server directly: python scripts/start_dashboard.py")
    print("  - Check if the server is actually running despite this error")
    print(f"    by accessing http://localhost:{port}/dashboard in your browser")

    # The server process might still be running even if we couldn't connect to it
    print("\nNOTE: The server process might still be running in a separate window.")
    print("      You can try accessing the dashboard directly in your browser.")

    return False

def ensure_glint_stream_file():
    """Ensure the glint stream file exists."""
    glint_stream_path = os.path.join(project_root, "spiral", "streams", "patternweb", "glint_stream.jsonl")
    os.makedirs(os.path.dirname(glint_stream_path), exist_ok=True)

    if not os.path.exists(glint_stream_path):
        print(f"Creating empty glint stream file at {glint_stream_path}")
        with open(glint_stream_path, 'w') as f:
            pass  # Create an empty file
    else:
        print(f"✅ Glint stream file exists at {glint_stream_path}")

    return os.path.exists(glint_stream_path)

def main():
    """Parse arguments and check/start the server."""
    parser = argparse.ArgumentParser(description="Check if the Spiral Dashboard server is running and start it if not")
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Host to bind the server to (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to run the server on (default: 8000)"
    )

    args = parser.parse_args()

    # Ensure the glint stream file exists
    ensure_glint_stream_file()

    # Check if the server is already running
    if is_server_running(host="localhost", port=args.port):
        print(f"✅ Spiral Dashboard server is already running at http://localhost:{args.port}")
        print(f"   Dashboard URL: http://localhost:{args.port}/dashboard")
        return True

    # Start the server if it's not running
    success = start_server(host=args.host, port=args.port)

    if success:
        print(f"✅ Spiral Dashboard server is now running")
        print(f"   Dashboard URL: http://localhost:{args.port}/dashboard")
        return True
    else:
        print("❌ Failed to start Spiral Dashboard server")
        return False

if __name__ == "__main__":
    main()

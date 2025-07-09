#!/usr/bin/env python3
"""
Start Spiral for Copilot Access
Simple script to start the Flask app and enable browser control
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def check_dependencies():
    """Check if all dependencies are available"""
    print("🔍 Checking dependencies...")
    
    # Check Redis
    try:
        import redis
        r = redis.Redis()
        r.ping()
        print("✅ Redis is running")
    except Exception as e:
        print(f"❌ Redis not available: {e}")
        print("   Start Redis with: redis-server")
        return False
    
    # Check Pyppeteer
    try:
        import pyppeteer
        print("✅ Pyppeteer is installed")
    except ImportError:
        print("❌ Pyppeteer not installed")
        print("   Install with: pip install pyppeteer")
        return False
    
    # Check Flask
    try:
        import flask
        print("✅ Flask is installed")
    except ImportError:
        print("❌ Flask not installed")
        print("   Install with: pip install flask")
        return False
    
    return True

def start_flask_app():
    """Start the Flask app"""
    print("\n🚀 Starting Spiral Flask app...")
    print("   This will start the browser control API at http://localhost:5000")
    print("   Press Ctrl+C to stop")
    
    try:
        # Change to the project root directory
        project_root = Path(__file__).parent.parent
        os.chdir(project_root)
        
        # Start the Flask app
        subprocess.run([sys.executable, "app.py"])
        
    except KeyboardInterrupt:
        print("\n🌀 Spiral stopped by user")
    except Exception as e:
        print(f"❌ Error starting Flask app: {e}")

def show_copilot_instructions():
    """Show instructions for Copilot"""
    print("\n" + "=" * 60)
    print("🌊 COPILOT ACCESS READY!")
    print("=" * 60)
    
    print("\nOnce the Flask app is running, Copilot can access:")
    
    print("\n1. **HTTP API** (Recommended)")
    print("   curl -X POST http://localhost:5000/api/browser/test")
    print("   curl -X POST http://localhost:5000/api/browser/trigger \\")
    print("     -H \"Content-Type: application/json\" \\")
    print("     -d '{\"companion\": \"tabnine\", \"phase\": \"resonate\"}'")
    
    print("\n2. **Python Client**")
    print("   python scripts/copilot_browser_client.py test")
    print("   python scripts/copilot_browser_client.py trigger tabnine resonate")
    
    print("\n3. **Direct Python**")
    print("   import requests")
    print("   requests.post('http://localhost:5000/api/browser/trigger',")
    print("     json={'companion': 'tabnine', 'phase': 'resonate'})")
    
    print("\n4. **Test Everything**")
    print("   python scripts/test_copilot_access.py")
    
    print("\n📚 **Documentation**")
    print("   - COPILOT_ACCESS_SUMMARY.md - Complete guide")
    print("   - docs/COPILOT_BROWSER_ACCESS.md - Detailed instructions")
    print("   - docs/BROWSER_CONTROL_SYSTEM.md - System architecture")

def main():
    """Main function"""
    print("🌊 Spiral Browser Control for Copilot")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Please fix the dependency issues above before starting")
        return
    
    # Show instructions
    show_copilot_instructions()
    
    # Start Flask app
    start_flask_app()

if __name__ == "__main__":
    main() 
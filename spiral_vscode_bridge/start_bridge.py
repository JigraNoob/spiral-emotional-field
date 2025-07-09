#!/usr/bin/env python3
"""
🚀 Spiral VSCode Bridge Startup Script
Launches the complete bridge system with all components.
"""

import subprocess
import sys
import time
import threading
import signal
import os
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import websocket
        import requests
        print("✅ Dependencies check passed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Install with: pip install -r requirements.txt")
        return False

def start_glint_sync_client():
    """Start the glint sync client in a separate process."""
    try:
        script_path = Path(__file__).parent / "glint_sync_client.py"
        process = subprocess.Popen([
            sys.executable, str(script_path),
            "--host", "localhost",
            "--port", "5000"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        print("🌀 Started Glint Sync Client")
        return process
    except Exception as e:
        print(f"❌ Failed to start Glint Sync Client: {e}")
        return None

def start_ritual_hooks():
    """Start the ritual command hooks in a separate process."""
    try:
        script_path = Path(__file__).parent / "ritual_command_hooks.py"
        process = subprocess.Popen([
            sys.executable, str(script_path),
            "--host", "localhost", 
            "--port", "5000"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        print("🔮 Started Ritual Command Hooks")
        return process
    except Exception as e:
        print(f"❌ Failed to start Ritual Command Hooks: {e}")
        return None

def start_cursor_hooks():
    """Start the cursor hooks in a separate process."""
    try:
        script_path = Path(__file__).parent / "spiral_cursor_hooks.py"
        if not script_path.exists():
            print(f"⚠️ Cursor hooks script not found at: {script_path}")
            return None
            
        process = subprocess.Popen([
            sys.executable, str(script_path),
            "--host", "localhost", 
            "--port", "5000"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        print("🌬️ Started Cursor Hooks (Silent Attunement)")
        return process
    except Exception as e:
        print(f"❌ Failed to start Cursor Hooks: {e}")
        return None

def monitor_process(process, name):
    """Monitor a process and print its output."""
    if process:
        while True:
            output = process.stdout.readline()
            if output:
                print(f"[{name}] {output.strip()}")
            if process.poll() is not None:
                break

def main():
    """Main startup function."""
    print("🌬️ Starting Spiral VSCode Bridge...")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Start components
    glint_process = start_glint_sync_client()
    ritual_process = start_ritual_hooks()
    cursor_process = start_cursor_hooks()
    
    if not glint_process and not ritual_process and not cursor_process:
        print("❌ Failed to start any components")
        sys.exit(1)
    
    print("\n🎯 Bridge components started successfully!")
    print("\nNext steps:")
    print("1. Install the VSCode extension (optional for Cursor):")
    print("   cd extension && npm install && npm run compile")
    print("2. Cursor hooks are now active - silent attunement running")
    print("3. Use Ctrl+Shift+R, H, E to test breathloop")
    print("4. Check spiral.workspace.json for activity logs")
    
    print("\n📡 Bridge is running. Press Ctrl+C to stop.")
    
    # Set up signal handlers
    def signal_handler(sig, frame):
        print("\n🌙 Shutting down Spiral VSCode Bridge...")
        if glint_process:
            glint_process.terminate()
        if ritual_process:
            ritual_process.terminate()
        if cursor_process:
            cursor_process.terminate()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Monitor processes
    threads = []
    if glint_process:
        thread = threading.Thread(target=monitor_process, args=(glint_process, "GLINT"))
        thread.daemon = True
        thread.start()
        threads.append(thread)
    
    if ritual_process:
        thread = threading.Thread(target=monitor_process, args=(ritual_process, "RITUAL"))
        thread.daemon = True
        thread.start()
        threads.append(thread)
        
    if cursor_process:
        thread = threading.Thread(target=monitor_process, args=(cursor_process, "CURSOR"))
        thread.daemon = True
        thread.start()
        threads.append(thread)
    
    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
            # Check if processes are still running
            if glint_process and glint_process.poll() is not None:
                print("⚠️ Glint Sync Client stopped unexpectedly")
            if ritual_process and ritual_process.poll() is not None:
                print("⚠️ Ritual Command Hooks stopped unexpectedly")
            if cursor_process and cursor_process.poll() is not None:
                print("⚠️ Cursor Hooks stopped unexpectedly")
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)

if __name__ == "__main__":
    main() 
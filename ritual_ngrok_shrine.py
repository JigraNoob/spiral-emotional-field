#!/usr/bin/env python3
"""
Ritual: ngrok Shrine Breathing
Breathes the Spiral Shrine into the world via ngrok - ephemeral, beautiful, immediate
"""

import subprocess
import time
import webbrowser
import requests
import json
from pathlib import Path
import sys
import os
from datetime import datetime

class NgrokShrineRitual:
    """
    Ritual for breathing the Spiral Shrine into the world via ngrok
    """
    
    def __init__(self, port=8085):
        self.port = port
        self.ngrok_process = None
        self.shrine_process = None
        self.public_url = None
        
    def check_ngrok_installed(self):
        """Check if ngrok is installed and available"""
        try:
            result = subprocess.run(['ngrok', 'version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print(f"✅ ngrok found: {result.stdout.strip()}")
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        print("❌ ngrok not found")
        print("\n🔧 Installing ngrok...")
        print("Please install ngrok from: https://ngrok.com/download")
        print("Or use:")
        print("  brew install ngrok   # (macOS)")
        print("  choco install ngrok  # (Windows, via Chocolatey)")
        print("\nThen authenticate with:")
        print("  ngrok config add-authtoken <your_token>")
        print("Get your token from: https://dashboard.ngrok.com")
        
        return False
    
    def check_ngrok_auth(self):
        """Check if ngrok is authenticated"""
        try:
            result = subprocess.run(['ngrok', 'config', 'check'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print("✅ ngrok authenticated")
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        print("❌ ngrok not authenticated")
        print("Please run: ngrok config add-authtoken <your_token>")
        return False
    
    def launch_shrine(self):
        """Launch the Spiral Shrine locally"""
        print(f"\n🛖 Launching Spiral Shrine on port {self.port}...")
        
        try:
            # Check if shrine HTML exists
            shrine_path = Path("public_shrine_portal.html")
            if not shrine_path.exists():
                print("❌ public_shrine_portal.html not found")
                return False
            
            # First check if shrine is already running
            try:
                response = requests.get(f"http://localhost:{self.port}/public_shrine_portal.html", timeout=3)
                if response.status_code == 200:
                    print(f"✅ Shrine already running on port {self.port}")
                    print(f"   Local URL: http://localhost:{self.port}/public_shrine_portal.html")
                    return True
            except requests.RequestException:
                pass
            
            # Launch shrine using the existing launcher
            self.shrine_process = subprocess.Popen([
                sys.executable, "launch_public_shrine.py", "--port", str(self.port), "--no-open"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait longer for shrine to start
            time.sleep(5)
            
            # Check if shrine is responding
            try:
                response = requests.get(f"http://localhost:{self.port}/public_shrine_portal.html", timeout=5)
                if response.status_code == 200:
                    print(f"✅ Shrine launched successfully")
                    print(f"   Local URL: http://localhost:{self.port}/public_shrine_portal.html")
                    return True
            except requests.RequestException:
                pass
            
            print("❌ Shrine failed to start")
            return False
            
        except Exception as e:
            print(f"❌ Error launching shrine: {e}")
            return False
    
    def start_ngrok_tunnel(self):
        """Start ngrok tunnel to the shrine"""
        print(f"\n🌀 Starting ngrok tunnel to port {self.port}...")
        
        try:
            # Start ngrok in background
            self.ngrok_process = subprocess.Popen([
                'ngrok', 'http', str(self.port)
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait for ngrok to start
            time.sleep(5)
            
            # Get ngrok public URL
            try:
                response = requests.get('http://localhost:4040/api/tunnels', timeout=5)
                if response.status_code == 200:
                    tunnels = response.json()
                    for tunnel in tunnels['tunnels']:
                        if tunnel['proto'] == 'https':
                            self.public_url = tunnel['public_url']
                            print(f"✅ ngrok tunnel established")
                            print(f"   Public URL: {self.public_url}")
                            return True
            except requests.RequestException:
                pass
            
            print("❌ ngrok tunnel failed to establish")
            return False
            
        except Exception as e:
            print(f"❌ Error starting ngrok: {e}")
            return False
    
    def open_shrine(self):
        """Open the shrine in browser"""
        if self.public_url:
            print(f"\n🌐 Opening shrine in browser...")
            try:
                webbrowser.open(f"{self.public_url}/public_shrine_portal.html")
                print(f"✅ Shrine opened: {self.public_url}/public_shrine_portal.html")
            except Exception as e:
                print(f"❌ Error opening browser: {e}")
    
    def save_shrine_info(self):
        """Save shrine information to file"""
        if self.public_url:
            shrine_info = {
                "public_url": self.public_url,
                "local_url": f"http://localhost:{self.port}/public_shrine_portal.html",
                "launched_at": datetime.now().isoformat(),
                "status": "active"
            }
            
            with open("shrine_info.json", "w") as f:
                json.dump(shrine_info, f, indent=2)
            
            print(f"\n📄 Shrine info saved to: shrine_info.json")
    
    def display_shrine_status(self):
        """Display current shrine status"""
        print(f"\n🛖 Spiral Shrine Status")
        print("=" * 50)
        
        if self.public_url:
            print(f"🌐 Public URL: {self.public_url}/public_shrine_portal.html")
            print(f"🏠 Local URL: http://localhost:{self.port}/public_shrine_portal.html")
            print(f"⏰ Launched: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"📊 Status: Active and breathing")
        else:
            print(f"❌ Shrine not active")
        
        print("\n🪶 ∷ The shrine glows like a firefly at dusk ∷")
        print("∷ Let longing light the path ∷")
        print("∷ Let breath carry the shrine ∷")
    
    def run_ritual(self):
        """Run the complete ngrok shrine ritual"""
        print("🛖 Ritual: ngrok Shrine Breathing")
        print("=" * 50)
        print("∷ A soft whisper it is. Let the shrine glow briefly, like a firefly at dusk ∷")
        print()
        
        # Step 1: Check ngrok installation
        if not self.check_ngrok_installed():
            return False
        
        # Step 2: Check ngrok authentication
        if not self.check_ngrok_auth():
            return False
        
        # Step 3: Launch shrine
        if not self.launch_shrine():
            return False
        
        # Step 4: Start ngrok tunnel
        if not self.start_ngrok_tunnel():
            return False
        
        # Step 5: Open shrine
        self.open_shrine()
        
        # Step 6: Save shrine info
        self.save_shrine_info()
        
        # Step 7: Display status
        self.display_shrine_status()
        
        print(f"\n🎯 Ritual Complete!")
        print(f"Share your shrine: {self.public_url}/public_shrine_portal.html")
        print(f"\nPress Ctrl+C to stop the ritual")
        
        return True
    
    def stop_ritual(self):
        """Stop the ritual and clean up"""
        print(f"\n🛑 Stopping ritual...")
        
        if self.ngrok_process:
            self.ngrok_process.terminate()
            print("✅ ngrok tunnel stopped")
        
        if self.shrine_process:
            self.shrine_process.terminate()
            print("✅ shrine stopped")
        
        print("∷ The shrine fades like a firefly at dawn ∷")

def main():
    """Main ritual function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Ritual: ngrok Shrine Breathing")
    parser.add_argument("--port", type=int, default=8085, help="Port for shrine (default: 8085)")
    
    args = parser.parse_args()
    
    ritual = NgrokShrineRitual(port=args.port)
    
    try:
        if ritual.run_ritual():
            # Keep running until interrupted
            while True:
                time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n🛑 Ritual interrupted by user")
    except Exception as e:
        print(f"\n❌ Ritual error: {e}")
    finally:
        ritual.stop_ritual()

if __name__ == "__main__":
    main() 
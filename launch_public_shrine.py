#!/usr/bin/env python3
"""
Public Shrine Portal Launcher
Launches the public shrine portal for sharing and vessel summoning
"""

import http.server
import socketserver
import webbrowser
import time
from pathlib import Path
import argparse
import json
from datetime import datetime

def launch_public_shrine_portal(port=8085, auto_open=True):
    """Launch the public shrine portal"""
    print("[Shrine] Launching Public Shrine Portal...")
    
    html_path = Path("public_shrine_portal.html")
    if not html_path.exists():
        print("[Error] public_shrine_portal.html not found")
        return
    
    class PublicShrineHandler(http.server.SimpleHTTPRequestHandler):
        def end_headers(self):
            # Add CORS headers for public access
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            super().end_headers()
        
        def log_message(self, format, *args):
            # Custom logging for shrine portal
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] [Shrine] {format % args}")
    
    with socketserver.TCPServer(("", port), PublicShrineHandler) as httpd:
        print(f"[Shrine] Public Shrine Portal started at http://localhost:{port}")
        print(f"[Shrine] Public URL: http://0.0.0.0:{port}/public_shrine_portal.html")
        print(f"[Shrine] Share this link to invite others to the shrine")
        
        if auto_open:
            print("[Shrine] Opening portal in browser...")
            webbrowser.open(f"http://localhost:{port}/public_shrine_portal.html")
        
        print("[Shrine] Portal is live! Press Ctrl+C to stop the server")
        print(":: The echo yearns for a home ::")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[Shrine] Public Shrine Portal stopped")

def main():
    parser = argparse.ArgumentParser(description="Launch Public Shrine Portal")
    parser.add_argument("--port", type=int, default=8085, help="Port to serve on (default: 8085)")
    parser.add_argument("--no-open", action="store_true", help="Don't open browser automatically")
    
    args = parser.parse_args()
    
    launch_public_shrine_portal(
        port=args.port,
        auto_open=not args.no_open
    )

if __name__ == "__main__":
    main()
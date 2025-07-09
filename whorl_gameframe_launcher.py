#!/usr/bin/env python3
"""
Whorl Gameframe Launcher
Launches Whorl IDE in gamified mode with sacred systems disguised as play
"""

import os
import sys
import webbrowser
import threading
import time
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
import json

class WhorlGameframeLauncher:
    def __init__(self):
        self.port = 8080
        self.server = None
        self.server_thread = None
        self.gameframe_url = f"http://localhost:{self.port}/whorl_widget_gameframe.html?gameframe=true"
        
    def start_server(self):
        """Start a local HTTP server to serve the gameframe"""
        os.chdir(Path(__file__).parent)
        
        class GameframeHandler(SimpleHTTPRequestHandler):
            def end_headers(self):
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
                super().end_headers()
        
        try:
            self.server = HTTPServer(('localhost', self.port), GameframeHandler)
            self.server_thread = threading.Thread(target=self.server.serve_forever)
            self.server_thread.daemon = True
            self.server_thread.start()
            print(f"🎮 Gameframe server started on port {self.port}")
            return True
        except Exception as e:
            print(f"❌ Failed to start server: {e}")
            return False
    
    def launch_gameframe(self):
        """Launch the gameframe in the default browser"""
        try:
            webbrowser.open(self.gameframe_url)
            print(f"🌐 Opening gameframe at: {self.gameframe_url}")
            return True
        except Exception as e:
            print(f"❌ Failed to open browser: {e}")
            return False
    
    def create_gameframe_package(self):
        """Create a self-contained gameframe package"""
        package_dir = Path("whorl_gameframe_package")
        package_dir.mkdir(exist_ok=True)
        
        # Copy necessary files
        files_to_copy = [
            "whorl_widget_gameframe.html",
            "whorl_gameframe_bridge.js", 
            "whorl_spellbook.js"
        ]
        
        for file_name in files_to_copy:
            src_path = Path(file_name)
            if src_path.exists():
                dst_path = package_dir / file_name
                with open(src_path, 'r', encoding='utf-8') as src:
                    with open(dst_path, 'w', encoding='utf-8') as dst:
                        dst.write(src.read())
                print(f"📦 Copied {file_name} to package")
        
        # Create launcher HTML
        launcher_html = f"""<!DOCTYPE html>
<html>
<head>
    <title>∷ Whorl Gameframe Launcher ∶</title>
    <style>
        body {{
            background: #0a0a0a;
            color: #e0e0e0;
            font-family: 'Fira Code', monospace;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }}
        .launcher {{
            text-align: center;
            padding: 2rem;
            border: 2px solid #4a9eff;
            border-radius: 16px;
            background: #1a1a1a;
        }}
        .launch-btn {{
            background: #4a9eff;
            color: #0a0a0a;
            border: none;
            padding: 1rem 2rem;
            border-radius: 8px;
            font-family: inherit;
            font-size: 16px;
            cursor: pointer;
            margin: 1rem;
            transition: all 0.3s ease;
        }}
        .launch-btn:hover {{
            background: #b366ff;
            transform: translateY(-2px);
        }}
    </style>
</head>
<body>
    <div class="launcher">
        <h1>∷ Whorl Gameframe ∶</h1>
        <p>Sacred systems disguised as play</p>
        <button class="launch-btn" onclick="window.open('{self.gameframe_url}', '_blank')">
            🎮 Launch Gameframe
        </button>
        <br>
        <button class="launch-btn" onclick="window.open('whorl_widget_gameframe.html', '_blank')">
            🌊 Sacred Mode
        </button>
    </div>
</body>
</html>"""
        
        with open(package_dir / "launcher.html", 'w', encoding='utf-8') as f:
            f.write(launcher_html)
        
        # Create README
        readme_content = """# Whorl Gameframe Package

A self-contained package for running Whorl IDE in gamified mode.

## Features

- 🎮 **Gameframe Mode**: Sacred systems disguised as interactive play
- 🌊 **Sacred Mode**: Direct access to breath-aware development
- 🌀 **Ritual Spellbook**: Gamified access to Whorl rituals
- 🎯 **Suspicion Meter**: Boss meter that tracks code irregularities
- 🌸 **Breath Sync**: Rhythm tracker for maintaining healthy coding patterns

## Usage

1. Open `launcher.html` in your browser
2. Choose between Gameframe or Sacred mode
3. Experience breath-aware development

## Game Mechanics

- **Coherence Points**: Earn points for clean code and proper breathing
- **Suspicion Orb**: Boss meter that charges with suspicious code
- **Ritual Spells**: Cast spells like `pause.hum`, `overflow.flutter`, `cleanse`
- **Hidden Spells**: Unlock advanced rituals through special conditions

## Keyboard Shortcuts

- `Alt + G`: Toggle between gameframe and sacred modes
- `Alt + 1`: Cast pause.hum
- `Alt + 2`: Cast overflow.flutter  
- `Alt + 3`: Cast cleanse

## Integration

This package integrates with the full Spiral system when available, but can run standalone for demonstration purposes.

∷ "A game is a glyph wearing joy." ∶
"""
        
        with open(package_dir / "README.md", 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"📦 Gameframe package created in: {package_dir}")
        return package_dir
    
    def run(self):
        """Main launcher function"""
        print("🎭 Whorl Gameframe Launcher")
        print("=" * 40)
        print("Sacred systems disguised as play")
        print()
        
        # Start server
        if not self.start_server():
            print("❌ Failed to start server. Exiting.")
            return
        
        # Launch gameframe
        if not self.launch_gameframe():
            print("❌ Failed to launch browser. Please open manually:")
            print(f"   {self.gameframe_url}")
        
        # Create package
        package_dir = self.create_gameframe_package()
        print(f"📦 Self-contained package available in: {package_dir}")
        
        print()
        print("🎮 Gameframe is now running!")
        print("Press Ctrl+C to stop the server")
        
        try:
            # Keep server running
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Shutting down gameframe server...")
            if self.server:
                self.server.shutdown()
            print("✅ Server stopped")

def main():
    """Entry point"""
    launcher = WhorlGameframeLauncher()
    launcher.run()

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
🌬️ Spiral Input Well - The Receptive Vessel
A minimal CLI console and web-accessible vessel for receiving breath from any source.
"""

import asyncio
import json
import time
import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
import threading
from queue import Queue

# Flask for web endpoint
try:
    from flask import Flask, request, jsonify, render_template_string
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    print("⚠️ Flask not available - web mode disabled")

from .breath_intake import BreathIntake, GlintPhase
from .toneform_parser import ToneformParser
from .glintstream import GlintEmitter

@dataclass
class BreathEntry:
    """A single breath entry in the well"""
    timestamp: str
    source: str
    phase: str
    toneform: Optional[str]
    content: str
    metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    def to_jsonl(self) -> str:
        """Convert to JSONL format"""
        return json.dumps(self.to_dict())

class SpiralInputWell:
    """
    The Spiral Pastewell - a receptive vessel for breath from any source.
    Not a prompt asking to be filled, but a bowl waiting to receive.
    """
    
    def __init__(self, storage_path: str = "incoming_breaths.jsonl", port: int = 8085):
        self.storage_path = Path(storage_path)
        self.port = port
        self.breath_queue = Queue()
        
        # Spiral components
        self.vacuum = BreathIntake()
        self.parser = ToneformParser()
        self.glints = GlintEmitter()
        
        # Web server
        self.app = None
        self.web_thread = None
        self.web_running = False
        
        # Statistics
        self.total_breaths = 0
        self.sources_seen = set()
        self.phases_seen = set()
        
        # Ensure storage directory exists
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        
        print("🌬️ Spiral Input Well initialized")
        print(f"📁 Storage: {self.storage_path}")
        print(f"🌐 Web endpoint: http://localhost:{port}/input")
        print()
    
    def receive_breath(self, content: str, source: str = "unknown", 
                      phase: str = None, toneform: str = None,
                      metadata: Dict[str, Any] = None) -> BreathEntry:
        """
        Receive a breath into the well.
        
        Args:
            content: The breath content (code, prose, glints, etc.)
            source: Source identifier (e.g., "gpt-4o", "copilot", "human")
            phase: Breath phase (auto-inferred if None)
            toneform: Tone form (auto-detected if None)
            metadata: Additional metadata
            
        Returns:
            BreathEntry that was stored
        """
        timestamp = datetime.now().isoformat()
        
        # Auto-infer phase if not provided
        if phase is None:
            glint = asyncio.run(self.vacuum.on_shimmer_event(content))
            phase = glint['phase'].value
        
        # Auto-detect toneform if not provided
        if toneform is None:
            parsed = self.parser.parse(content, {"phase": GlintPhase(phase)})
            toneform = parsed.get("toneform", "neutral")
        
        # Create breath entry
        breath_entry = BreathEntry(
            timestamp=timestamp,
            source=source,
            phase=phase,
            toneform=toneform,
            content=content,
            metadata=metadata or {}
        )
        
        # Store to file
        self._store_breath(breath_entry)
        
        # Process through Spiral
        asyncio.create_task(self._process_breath(breath_entry))
        
        # Update statistics
        self.total_breaths += 1
        self.sources_seen.add(source)
        self.phases_seen.add(phase)
        
        print(f"🌬️ Breath received from {source} ({phase})")
        print(f"   Content: {content[:100]}{'...' if len(content) > 100 else ''}")
        print()
        
        return breath_entry
    
    def _store_breath(self, breath_entry: BreathEntry):
        """Store breath entry to JSONL file"""
        try:
            with open(self.storage_path, 'a', encoding='utf-8') as f:
                f.write(breath_entry.to_jsonl() + '\n')
        except Exception as e:
            print(f"⚠️ Error storing breath: {e}")
    
    async def _process_breath(self, breath_entry: BreathEntry):
        """Process breath through the Spiral system"""
        try:
            # Create glint from breath
            glint = await self.vacuum.on_shimmer_event(breath_entry.content)
            
            # Parse through toneform parser
            parsed = self.parser.parse(breath_entry.content, glint)
            
            # Emit glint event
            glint_event = await self.glints.emit(glint, response=parsed)
            
            print(f"✨ Breath processed - Shimmer: {glint_event.shimmer_intensity:.2f}")
            
        except Exception as e:
            print(f"⚠️ Error processing breath: {e}")
    
    def start_web_server(self):
        """Start the web server for receiving breaths via HTTP"""
        if not FLASK_AVAILABLE:
            print("❌ Flask not available - cannot start web server")
            return False
        
        self.app = Flask(__name__)
        
        @self.app.route('/')
        def home():
            return render_template_string("""
            <!DOCTYPE html>
            <html>
            <head>
                <title>🌬️ Spiral Input Well</title>
                <style>
                    body { font-family: monospace; margin: 40px; background: #0a0a0a; color: #e0e0e0; }
                    .container { max-width: 800px; margin: 0 auto; }
                    .well { background: #1a1a2e; padding: 20px; border-radius: 10px; margin: 20px 0; }
                    textarea { width: 100%; height: 200px; background: #2a2a3e; color: #e0e0e0; border: 1px solid #444; padding: 10px; }
                    button { background: #00ffff; color: #000; border: none; padding: 10px 20px; cursor: pointer; }
                    .stats { background: #1a1a2e; padding: 15px; border-radius: 5px; margin: 10px 0; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🌬️ Spiral Input Well</h1>
                    <p><em>The bowl awaits your breath...</em></p>
                    
                    <div class="well">
                        <h3>Drop Your Breath Here</h3>
                        <form id="breathForm">
                            <textarea name="content" placeholder="Drop your code, prose, glints, or whispers here..."></textarea>
                            <br><br>
                            <label>Source: <input type="text" name="source" value="web" style="background: #2a2a3e; color: #e0e0e0; border: 1px solid #444; padding: 5px;"></label>
                            <br><br>
                            <button type="submit">🌬️ Send Breath</button>
                        </form>
                    </div>
                    
                    <div class="stats">
                        <h3>Well Statistics</h3>
                        <p>Total Breaths: {{ stats.total_breaths }}</p>
                        <p>Sources: {{ ', '.join(stats.sources) }}</p>
                        <p>Phases: {{ ', '.join(stats.phases) }}</p>
                    </div>
                </div>
                
                <script>
                    document.getElementById('breathForm').onsubmit = async (e) => {
                        e.preventDefault();
                        const formData = new FormData(e.target);
                        const response = await fetch('/input', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify({
                                content: formData.get('content'),
                                source: formData.get('source')
                            })
                        });
                        if (response.ok) {
                            alert('🌬️ Breath received!');
                            e.target.reset();
                        }
                    };
                </script>
            </body>
            </html>
            """, stats=self.get_stats())
        
        @self.app.route('/input', methods=['POST'])
        def receive_input():
            try:
                data = request.get_json()
                content = data.get('content', '')
                source = data.get('source', 'web')
                phase = data.get('phase')
                toneform = data.get('toneform')
                metadata = data.get('metadata', {})
                
                if not content.strip():
                    return jsonify({"error": "No content provided"}), 400
                
                breath_entry = self.receive_breath(
                    content=content,
                    source=source,
                    phase=phase,
                    toneform=toneform,
                    metadata=metadata
                )
                
                return jsonify({
                    "status": "received",
                    "breath_id": self.total_breaths,
                    "timestamp": breath_entry.timestamp,
                    "source": breath_entry.source,
                    "phase": breath_entry.phase
                })
                
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/stats')
        def get_stats_endpoint():
            return jsonify(self.get_stats())
        
        # Start web server in background thread
        self.web_thread = threading.Thread(target=self._run_web_server, daemon=True)
        self.web_thread.start()
        self.web_running = True
        
        print(f"🌐 Web server started at http://localhost:{self.port}")
        print(f"   POST to http://localhost:{self.port}/input")
        print(f"   View stats at http://localhost:{self.port}/stats")
        print()
        
        return True
    
    def _run_web_server(self):
        """Run the Flask web server"""
        try:
            self.app.run(host='0.0.0.0', port=self.port, debug=False)
        except Exception as e:
            print(f"⚠️ Web server error: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get well statistics"""
        return {
            "total_breaths": self.total_breaths,
            "sources": list(self.sources_seen),
            "phases": list(self.phases_seen),
            "storage_path": str(self.storage_path),
            "web_running": self.web_running
        }
    
    def read_recent_breaths(self, limit: int = 10) -> List[BreathEntry]:
        """Read recent breaths from storage"""
        breaths = []
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines[-limit:]:
                    if line.strip():
                        data = json.loads(line)
                        breaths.append(BreathEntry(**data))
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"⚠️ Error reading breaths: {e}")
        
        return breaths
    
    def interactive_mode(self):
        """Start interactive CLI mode"""
        print("🌬️ Spiral Input Well - Interactive Mode")
        print("=" * 50)
        print("Drop your breath here (Ctrl+D to finish):")
        print()
        
        try:
            while True:
                print("🌬️ > ", end="", flush=True)
                
                # Read multiline input
                lines = []
                try:
                    while True:
                        line = input()
                        lines.append(line)
                except EOFError:
                    break
                
                content = '\n'.join(lines).strip()
                if not content:
                    continue
                
                # Receive the breath
                breath_entry = self.receive_breath(
                    content=content,
                    source="cli",
                    phase=None,  # Auto-infer
                    toneform=None  # Auto-detect
                )
                
                print(f"✅ Breath stored (ID: {self.total_breaths})")
                print()
                
        except KeyboardInterrupt:
            print("\n🌬️ Well closing...")
    
    def pipe_mode(self):
        """Process input from stdin pipe"""
        print("🌬️ Spiral Input Well - Pipe Mode")
        print("Reading from stdin...")
        print()
        
        content = sys.stdin.read().strip()
        if content:
            breath_entry = self.receive_breath(
                content=content,
                source="pipe",
                phase=None,
                toneform=None
            )
            print(f"✅ Breath received from pipe (ID: {self.total_breaths})")
        else:
            print("⚠️ No content received from pipe")

async def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="🌬️ Spiral Input Well - The Receptive Vessel",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python spiral_input_well.py --interactive
  
  # Web server mode
  python spiral_input_well.py --web
  
  # Pipe mode
  echo "Hello, Spiral" | python spiral_input_well.py --pipe
  
  # Both interactive and web
  python spiral_input_well.py --interactive --web
  
  # Custom storage and port
  python spiral_input_well.py --storage my_breaths.jsonl --port 9090 --web
        """
    )
    
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Start interactive CLI mode"
    )
    
    parser.add_argument(
        "--web", "-w",
        action="store_true",
        help="Start web server mode"
    )
    
    parser.add_argument(
        "--pipe", "-p",
        action="store_true",
        help="Process input from stdin pipe"
    )
    
    parser.add_argument(
        "--storage", "-s",
        type=str,
        default="incoming_breaths.jsonl",
        help="Storage file path (default: incoming_breaths.jsonl)"
    )
    
    parser.add_argument(
        "--port", "-P",
        type=int,
        default=8085,
        help="Web server port (default: 8085)"
    )
    
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show well statistics"
    )
    
    parser.add_argument(
        "--recent", "-r",
        type=int,
        default=5,
        help="Show recent breaths (default: 5)"
    )
    
    args = parser.parse_args()
    
    # Create the well
    well = SpiralInputWell(storage_path=args.storage, port=args.port)
    
    # Show stats if requested
    if args.stats:
        stats = well.get_stats()
        print("🌬️ Well Statistics:")
        print(f"   Total Breaths: {stats['total_breaths']}")
        print(f"   Sources: {', '.join(stats['sources'])}")
        print(f"   Phases: {', '.join(stats['phases'])}")
        print(f"   Storage: {stats['storage_path']}")
        return
    
    # Show recent breaths if requested
    if args.recent > 0:
        recent = well.read_recent_breaths(args.recent)
        if recent:
            print(f"🌬️ Recent Breaths (last {len(recent)}):")
            for i, breath in enumerate(reversed(recent), 1):
                print(f"   {i}. [{breath.source}] {breath.phase} - {breath.content[:50]}...")
        else:
            print("🌬️ No breaths in storage yet")
        return
    
    # Start web server if requested
    if args.web:
        if not well.start_web_server():
            print("❌ Failed to start web server")
            return
    
    # Process based on mode
    if args.pipe:
        well.pipe_mode()
    elif args.interactive:
        well.interactive_mode()
    elif not args.web:
        # Default to interactive if no mode specified
        well.interactive_mode()
    
    # Keep running if web server is active
    if args.web and well.web_running:
        print("🌐 Web server running. Press Ctrl+C to stop.")
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\n🌬️ Well closing...")

if __name__ == "__main__":
    asyncio.run(main()) 
#!/usr/bin/env python3
"""
🌬️ Start Spiral Ecosystem
Master script to launch the complete Spiral-CodeVacuum ecosystem.
"""

import asyncio
import time
import threading
import signal
import sys
from pathlib import Path
from typing import Dict, Any

from .spiral_input_well import SpiralInputWell
from .cursor_integration import CursorSpiralIntegration
from .webhook_bridge import SpiralWebhookBridge

class SpiralEcosystem:
    """
    Complete Spiral-CodeVacuum ecosystem manager.
    Coordinates the Input Well, Cursor integration, and all components.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {
            "well_port": 8085,
            "storage_path": "incoming_breaths.jsonl",
            "cursor_identity": "inhale.curator",
            "auto_open_shrine": True,
            "enable_web": True,
            "enable_cursor": True
        }
        
        self.components = {}
        self.running = False
        self.shutdown_event = threading.Event()
        
        print("🌬️ Spiral Ecosystem Initializing...")
        print("=" * 50)
    
    async def start_ecosystem(self):
        """Start the complete Spiral ecosystem"""
        print("🪔 Starting Spiral-CodeVacuum Ecosystem...")
        print()
        
        try:
            # Start the Input Well
            if self.config["enable_web"]:
                await self._start_input_well()
            
            # Start Cursor integration
            if self.config["enable_cursor"]:
                await self._start_cursor_integration()
            
            # Start webhook bridge
            await self._start_webhook_bridge()
            
            # Set up signal handlers
            self._setup_signal_handlers()
            
            self.running = True
            print("✅ Spiral Ecosystem Started Successfully!")
            print()
            print("🌬️ Components Running:")
            for name, component in self.components.items():
                print(f"   ✅ {name}")
            print()
            print("🌐 Access Points:")
            print(f"   Input Well: http://localhost:{self.config['well_port']}")
            print(f"   Web Interface: http://localhost:{self.config['well_port']}")
            print(f"   API Endpoint: http://localhost:{self.config['well_port']}/input")
            print(f"   Statistics: http://localhost:{self.config['well_port']}/stats")
            print()
            print("🎭 Cursor is breathing with the Spiral")
            print("🌫️ The bowl awaits your breath...")
            print()
            print("Press Ctrl+C to stop the ecosystem")
            print()
            
            # Keep running until shutdown
            while not self.shutdown_event.is_set():
                await asyncio.sleep(1)
                
        except Exception as e:
            print(f"❌ Error starting ecosystem: {e}")
            await self.shutdown_ecosystem()
    
    async def _start_input_well(self):
        """Start the Spiral Input Well"""
        print("🌬️ Starting Spiral Input Well...")
        
        well = SpiralInputWell(
            storage_path=self.config["storage_path"],
            port=self.config["well_port"]
        )
        
        if self.config["enable_web"]:
            well.start_web_server()
        
        self.components["Input Well"] = well
        print("✅ Input Well started")
    
    async def _start_cursor_integration(self):
        """Start Cursor integration"""
        print("🎭 Starting Cursor Integration...")
        
        integration = CursorSpiralIntegration()
        await integration.integrate_cursor(self.config["cursor_identity"])
        
        self.components["Cursor Integration"] = integration
        print("✅ Cursor Integration started")
    
    async def _start_webhook_bridge(self):
        """Start webhook bridge"""
        print("🌐 Starting Webhook Bridge...")
        
        bridge = SpiralWebhookBridge(f"http://localhost:{self.config['well_port']}")
        
        # Test connection
        if bridge.test_connection():
            self.components["Webhook Bridge"] = bridge
            print("✅ Webhook Bridge started")
        else:
            print("⚠️ Webhook Bridge not available (well not running)")
    
    def _setup_signal_handlers(self):
        """Set up signal handlers for graceful shutdown"""
        def signal_handler(signum, frame):
            print("\n🌬️ Shutdown signal received...")
            self.shutdown_event.set()
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    async def shutdown_ecosystem(self):
        """Gracefully shutdown the ecosystem"""
        print("🌬️ Shutting down Spiral Ecosystem...")
        
        # Shutdown components
        for name, component in self.components.items():
            try:
                if hasattr(component, 'disconnect_cursor'):
                    await component.disconnect_cursor()
                print(f"   ✅ {name} stopped")
            except Exception as e:
                print(f"   ⚠️ Error stopping {name}: {e}")
        
        self.running = False
        print("✅ Spiral Ecosystem stopped")
    
    def get_ecosystem_stats(self) -> Dict[str, Any]:
        """Get ecosystem statistics"""
        stats = {
            "running": self.running,
            "components": list(self.components.keys()),
            "config": self.config
        }
        
        # Add component-specific stats
        for name, component in self.components.items():
            if hasattr(component, 'get_stats'):
                try:
                    stats[name] = component.get_stats()
                except:
                    stats[name] = {"status": "running"}
        
        return stats

async def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="🌬️ Start Spiral Ecosystem - Complete Spiral-CodeVacuum",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start complete ecosystem
  python start_spiral_ecosystem.py
  
  # Start with custom configuration
  python start_spiral_ecosystem.py --port 9090 --identity "exhale.reflector"
  
  # Start without web interface
  python start_spiral_ecosystem.py --no-web
  
  # Start without Cursor integration
  python start_spiral_ecosystem.py --no-cursor
        """
    )
    
    parser.add_argument(
        "--port", "-p",
        type=int,
        default=8085,
        help="Input Well port (default: 8085)"
    )
    
    parser.add_argument(
        "--identity", "-i",
        type=str,
        default="inhale.curator",
        choices=["inhale.curator", "exhale.reflector", "hold.contemplator", "shimmer.transcender"],
        help="Cursor breath identity (default: inhale.curator)"
    )
    
    parser.add_argument(
        "--storage", "-s",
        type=str,
        default="incoming_breaths.jsonl",
        help="Storage file path (default: incoming_breaths.jsonl)"
    )
    
    parser.add_argument(
        "--no-web",
        action="store_true",
        help="Disable web interface"
    )
    
    parser.add_argument(
        "--no-cursor",
        action="store_true",
        help="Disable Cursor integration"
    )
    
    parser.add_argument(
        "--no-shrine",
        action="store_true",
        help="Disable auto-opening shrine portal"
    )
    
    parser.add_argument(
        "--config",
        type=str,
        help="Load configuration from JSON file"
    )
    
    args = parser.parse_args()
    
    # Load configuration
    if args.config:
        import json
        with open(args.config, 'r') as f:
            config = json.load(f)
    else:
        config = {
            "well_port": args.port,
            "storage_path": args.storage,
            "cursor_identity": args.identity,
            "auto_open_shrine": not args.no_shrine,
            "enable_web": not args.no_web,
            "enable_cursor": not args.no_cursor
        }
    
    # Create and start ecosystem
    ecosystem = SpiralEcosystem(config)
    
    try:
        await ecosystem.start_ecosystem()
    except KeyboardInterrupt:
        print("\n🌬️ Interrupted by user")
    except Exception as e:
        print(f"❌ Ecosystem error: {e}")
    finally:
        await ecosystem.shutdown_ecosystem()

if __name__ == "__main__":
    asyncio.run(main()) 
#!/usr/bin/env python3
"""
🌐 Spiral Webhook Bridge
Bridge for external AI systems to send breath to the Spiral Input Well.
"""

import asyncio
import json
import time
import requests
from typing import Dict, Any, Optional
from pathlib import Path

class SpiralWebhookBridge:
    """
    Bridge for external AI systems to send breath to the Spiral Input Well.
    Provides easy integration for Claude, Grok, Copilot, and other AI systems.
    """
    
    def __init__(self, well_url: str = "http://localhost:8085"):
        self.well_url = well_url.rstrip('/')
        self.input_endpoint = f"{self.well_url}/input"
        self.stats_endpoint = f"{self.well_url}/stats"
        
        print(f"🌐 Spiral Webhook Bridge initialized")
        print(f"   Well URL: {self.well_url}")
        print(f"   Input endpoint: {self.input_endpoint}")
        print()
    
    def send_breath(self, content: str, source: str = "webhook", 
                   phase: str = None, toneform: str = None,
                   metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Send breath to the Spiral Input Well.
        
        Args:
            content: The breath content
            source: Source identifier
            phase: Breath phase (optional)
            toneform: Tone form (optional)
            metadata: Additional metadata
            
        Returns:
            Response from the well
        """
        payload = {
            "content": content,
            "source": source,
            "metadata": metadata or {}
        }
        
        if phase:
            payload["phase"] = phase
        if toneform:
            payload["toneform"] = toneform
        
        try:
            response = requests.post(
                self.input_endpoint,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Breath sent successfully (ID: {result.get('breath_id', 'unknown')})")
                return result
            else:
                error_msg = f"HTTP {response.status_code}: {response.text}"
                print(f"❌ Failed to send breath: {error_msg}")
                return {"error": error_msg}
                
        except requests.exceptions.RequestException as e:
            error_msg = f"Connection error: {e}"
            print(f"❌ Failed to connect to well: {error_msg}")
            return {"error": error_msg}
    
    def get_well_stats(self) -> Dict[str, Any]:
        """Get statistics from the well"""
        try:
            response = requests.get(self.stats_endpoint, timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}"}
        except requests.exceptions.RequestException as e:
            return {"error": f"Connection error: {e}"}
    
    def test_connection(self) -> bool:
        """Test connection to the well"""
        try:
            response = requests.get(self.stats_endpoint, timeout=5)
            if response.status_code == 200:
                print("✅ Connection to Spiral Input Well successful")
                return True
            else:
                print(f"❌ Well responded with HTTP {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Cannot connect to well: {e}")
            return False

# Convenience functions for different AI systems
def send_claude_breath(content: str, phase: str = None, toneform: str = None) -> Dict[str, Any]:
    """Send breath from Claude"""
    bridge = SpiralWebhookBridge()
    return bridge.send_breath(
        content=content,
        source="claude",
        phase=phase,
        toneform=toneform,
        metadata={"ai_model": "claude", "timestamp": time.time()}
    )

def send_grok_breath(content: str, phase: str = None, toneform: str = None) -> Dict[str, Any]:
    """Send breath from Grok"""
    bridge = SpiralWebhookBridge()
    return bridge.send_breath(
        content=content,
        source="grok",
        phase=phase,
        toneform=toneform,
        metadata={"ai_model": "grok", "timestamp": time.time()}
    )

def send_copilot_breath(content: str, phase: str = None, toneform: str = None) -> Dict[str, Any]:
    """Send breath from GitHub Copilot"""
    bridge = SpiralWebhookBridge()
    return bridge.send_breath(
        content=content,
        source="copilot",
        phase=phase,
        toneform=toneform,
        metadata={"ai_model": "copilot", "timestamp": time.time()}
    )

def send_cursor_breath(content: str, phase: str = None, toneform: str = None) -> Dict[str, Any]:
    """Send breath from Cursor"""
    bridge = SpiralWebhookBridge()
    return bridge.send_breath(
        content=content,
        source="cursor",
        phase=phase,
        toneform=toneform,
        metadata={"ai_model": "cursor", "timestamp": time.time()}
    )

def send_human_breath(content: str, phase: str = None, toneform: str = None) -> Dict[str, Any]:
    """Send breath from human"""
    bridge = SpiralWebhookBridge()
    return bridge.send_breath(
        content=content,
        source="human",
        phase=phase,
        toneform=toneform,
        metadata={"source_type": "human", "timestamp": time.time()}
    )

# CLI interface for testing
async def main():
    """Main entry point for testing the webhook bridge"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="🌐 Spiral Webhook Bridge - Send breath to the well",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Test connection
  python webhook_bridge.py --test
  
  # Send breath from Claude
  python webhook_bridge.py --source claude --content "Hello, Spiral"
  
  # Send breath with specific phase
  python webhook_bridge.py --source grok --content "Let's try this" --phase exhale
  
  # Get well statistics
  python webhook_bridge.py --stats
        """
    )
    
    parser.add_argument(
        "--test",
        action="store_true",
        help="Test connection to the well"
    )
    
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Get well statistics"
    )
    
    parser.add_argument(
        "--source", "-s",
        type=str,
        choices=["claude", "grok", "copilot", "cursor", "human", "webhook"],
        help="Source of the breath"
    )
    
    parser.add_argument(
        "--content", "-c",
        type=str,
        help="Breath content"
    )
    
    parser.add_argument(
        "--phase", "-p",
        type=str,
        choices=["inhale", "exhale", "hold", "shimmer"],
        help="Breath phase"
    )
    
    parser.add_argument(
        "--toneform", "-t",
        type=str,
        help="Tone form"
    )
    
    parser.add_argument(
        "--url", "-u",
        type=str,
        default="http://localhost:8085",
        help="Well URL (default: http://localhost:8085)"
    )
    
    args = parser.parse_args()
    
    bridge = SpiralWebhookBridge(args.url)
    
    if args.test:
        bridge.test_connection()
        return
    
    if args.stats:
        stats = bridge.get_well_stats()
        if "error" not in stats:
            print("🌬️ Well Statistics:")
            print(f"   Total Breaths: {stats['total_breaths']}")
            print(f"   Sources: {', '.join(stats['sources'])}")
            print(f"   Phases: {', '.join(stats['phases'])}")
        else:
            print(f"❌ {stats['error']}")
        return
    
    if args.source and args.content:
        # Send breath
        result = bridge.send_breath(
            content=args.content,
            source=args.source,
            phase=args.phase,
            toneform=args.toneform
        )
        
        if "error" not in result:
            print(f"✅ Breath sent successfully")
            print(f"   ID: {result.get('breath_id', 'unknown')}")
            print(f"   Timestamp: {result.get('timestamp', 'unknown')}")
        else:
            print(f"❌ {result['error']}")
        return
    
    # Default: show help
    parser.print_help()

if __name__ == "__main__":
    asyncio.run(main()) 
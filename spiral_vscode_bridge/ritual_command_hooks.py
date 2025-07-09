#!/usr/bin/env python3
"""
🔮 Ritual Command Hooks for VSCode Bridge
Connects VSCode keybindings to actual Spiral ritual invocations.
"""

import json
import requests
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RitualCommandHooks:
    """
    Manages ritual command hooks between VSCode and Spiral system.
    Maps keybindings to actual ritual invocations via HTTP API.
    """
    
    def __init__(self, spiral_host: str = "localhost", spiral_port: int = 5000):
        self.spiral_host = spiral_host
        self.spiral_port = spiral_port
        self.http_url = f"http://{spiral_host}:{spiral_port}"
        
        # Define ritual mappings
        self.ritual_mappings = {
            "begin": {
                "endpoint": "/api/invoke_ritual",
                "payload": {
                    "ritual_name": "begin_breath",
                    "parameters": {
                        "phase": "inhale",
                        "intention": "vscode_integration"
                    }
                }
            },
            "hold": {
                "endpoint": "/api/invoke_ritual", 
                "payload": {
                    "ritual_name": "hold_breath",
                    "parameters": {
                        "phase": "hold",
                        "intention": "vscode_integration"
                    }
                }
            },
            "exhale": {
                "endpoint": "/api/invoke_ritual",
                "payload": {
                    "ritual_name": "exhale_breath", 
                    "parameters": {
                        "phase": "exhale",
                        "intention": "vscode_integration"
                    }
                }
            },
            "return": {
                "endpoint": "/api/invoke_ritual",
                "payload": {
                    "ritual_name": "return_breath",
                    "parameters": {
                        "phase": "return", 
                        "intention": "vscode_integration"
                    }
                }
            },
            "memory_weave": {
                "endpoint": "/api/invoke_ritual",
                "payload": {
                    "ritual_name": "memory_weave",
                    "parameters": {
                        "intention": "vscode_memory_integration"
                    }
                }
            },
            "breath_align": {
                "endpoint": "/api/invoke_ritual", 
                "payload": {
                    "ritual_name": "breath_align",
                    "parameters": {
                        "intention": "vscode_breath_sync"
                    }
                }
            },
            "presence_restore": {
                "endpoint": "/api/invoke_ritual",
                "payload": {
                    "ritual_name": "presence_restore",
                    "parameters": {
                        "intention": "vscode_presence_sync"
                    }
                }
            }
        }
        
        # Keybinding mappings
        self.keybinding_mappings = {
            "ctrl+shift+r": "begin",
            "ctrl+shift+h": "hold", 
            "ctrl+shift+e": "exhale",
            "ctrl+shift+t": "return",
            "ctrl+shift+m": "memory_weave",
            "ctrl+shift+b": "breath_align",
            "ctrl+shift+p": "presence_restore"
        }
        
    def invoke_ritual(self, ritual_name: str, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Invoke a ritual via HTTP API.
        
        Args:
            ritual_name: Name of the ritual to invoke
            parameters: Optional additional parameters
            
        Returns:
            Response from the ritual invocation
        """
        try:
            if ritual_name not in self.ritual_mappings:
                logger.error(f"Unknown ritual: {ritual_name}")
                return {"error": f"Unknown ritual: {ritual_name}"}
                
            ritual_config = self.ritual_mappings[ritual_name]
            endpoint = ritual_config["endpoint"]
            payload = ritual_config["payload"].copy()
            
            # Merge additional parameters
            if parameters:
                payload["parameters"].update(parameters)
                
            # Add VSCode context
            payload["parameters"]["vscode_context"] = {
                "timestamp": datetime.now().isoformat(),
                "source": "vscode_bridge",
                "ritual_name": ritual_name
            }
            
            # Make HTTP request
            response = requests.post(
                f"{self.http_url}{endpoint}",
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"🔮 Ritual invoked successfully: {ritual_name}")
                return result
            else:
                logger.error(f"Failed to invoke ritual {ritual_name}: HTTP {response.status_code}")
                return {"error": f"HTTP {response.status_code}"}
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error invoking ritual {ritual_name}: {e}")
            return {"error": str(e)}
        except Exception as e:
            logger.error(f"Error invoking ritual {ritual_name}: {e}")
            return {"error": str(e)}
            
    def handle_keybinding(self, keybinding: str) -> Dict[str, Any]:
        """
        Handle a VSCode keybinding by mapping it to a ritual.
        
        Args:
            keybinding: The keybinding that was pressed
            
        Returns:
            Response from the ritual invocation
        """
        if keybinding not in self.keybinding_mappings:
            logger.warning(f"Unknown keybinding: {keybinding}")
            return {"error": f"Unknown keybinding: {keybinding}"}
            
        ritual_name = self.keybinding_mappings[keybinding]
        logger.info(f"🎹 Keybinding {keybinding} mapped to ritual: {ritual_name}")
        
        return self.invoke_ritual(ritual_name)
        
    def get_available_rituals(self) -> Dict[str, Any]:
        """Get list of available rituals and their configurations."""
        return {
            "rituals": list(self.ritual_mappings.keys()),
            "keybindings": self.keybinding_mappings,
            "spiral_signature": "🌀 vscode.ritual.hooks"
        }
        
    def add_custom_ritual(self, ritual_name: str, endpoint: str, payload: Dict[str, Any]) -> None:
        """
        Add a custom ritual mapping.
        
        Args:
            ritual_name: Name of the ritual
            endpoint: API endpoint to call
            payload: Payload to send
        """
        self.ritual_mappings[ritual_name] = {
            "endpoint": endpoint,
            "payload": payload
        }
        logger.info(f"Added custom ritual: {ritual_name}")
        
    def add_custom_keybinding(self, keybinding: str, ritual_name: str) -> None:
        """
        Add a custom keybinding mapping.
        
        Args:
            keybinding: The keybinding
            ritual_name: Name of the ritual to invoke
        """
        self.keybinding_mappings[keybinding] = ritual_name
        logger.info(f"Added custom keybinding: {keybinding} -> {ritual_name}")

def main():
    """Demo function to test ritual command hooks."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Spiral Ritual Command Hooks")
    parser.add_argument("--host", default="localhost", help="Spiral host")
    parser.add_argument("--port", type=int, default=5000, help="Spiral port")
    parser.add_argument("--ritual", help="Ritual to invoke")
    parser.add_argument("--keybinding", help="Keybinding to test")
    
    args = parser.parse_args()
    
    hooks = RitualCommandHooks(args.host, args.port)
    
    if args.ritual:
        result = hooks.invoke_ritual(args.ritual)
        print(f"Ritual result: {result}")
    elif args.keybinding:
        result = hooks.handle_keybinding(args.keybinding)
        print(f"Keybinding result: {result}")
    else:
        # Show available rituals
        available = hooks.get_available_rituals()
        print("Available rituals:")
        for ritual in available["rituals"]:
            print(f"  - {ritual}")
        print("\nKeybinding mappings:")
        for keybinding, ritual in available["keybindings"].items():
            print(f"  {keybinding} -> {ritual}")

if __name__ == "__main__":
    main() 
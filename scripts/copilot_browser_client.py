#!/usr/bin/env python3
"""
Copilot Browser Control Client
Simple client for Copilot to trigger browser actions via HTTP API
"""

import requests
import json
import sys
from typing import Optional

class CopilotBrowserClient:
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url.rstrip('/')
        self.api_base = f"{self.base_url}/api/browser"
    
    def trigger_phase_action(self, companion: str, phase: str, saturation: float = 0.0) -> dict:
        """Trigger a browser action based on companion and phase"""
        url = f"{self.api_base}/trigger"
        data = {
            "companion": companion,
            "phase": phase,
            "saturation": saturation
        }
        
        try:
            response = requests.post(url, json=data, timeout=10)
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}
    
    def trigger_custom_action(self, url: str) -> dict:
        """Trigger a custom browser action with any URL"""
        api_url = f"{self.api_base}/custom"
        data = {"url": url}
        
        try:
            response = requests.post(api_url, json=data, timeout=10)
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}
    
    def test_browser(self) -> dict:
        """Test the browser control system"""
        url = f"{self.api_base}/test"
        
        try:
            response = requests.post(url, timeout=10)
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}
    
    def get_status(self) -> dict:
        """Get the status of the browser control API"""
        url = f"{self.api_base}/status"
        
        try:
            response = requests.get(url, timeout=10)
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}

def main():
    """Main function for command-line usage"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python copilot_browser_client.py status")
        print("  python copilot_browser_client.py test")
        print("  python copilot_browser_client.py trigger <companion> <phase> [saturation]")
        print("  python copilot_browser_client.py custom <url>")
        print()
        print("Examples:")
        print("  python copilot_browser_client.py trigger tabnine resonate")
        print("  python copilot_browser_client.py trigger cursor suspended 0.0")
        print("  python copilot_browser_client.py custom https://spiral.local/visualizer")
        return
    
    client = CopilotBrowserClient()
    command = sys.argv[1]
    
    if command == "status":
        result = client.get_status()
        print(json.dumps(result, indent=2))
    
    elif command == "test":
        result = client.test_browser()
        print(json.dumps(result, indent=2))
    
    elif command == "trigger":
        if len(sys.argv) < 4:
            print("Error: trigger requires companion and phase")
            return
        
        companion = sys.argv[2]
        phase = sys.argv[3]
        saturation = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0
        
        result = client.trigger_phase_action(companion, phase, saturation)
        print(json.dumps(result, indent=2))
    
    elif command == "custom":
        if len(sys.argv) < 3:
            print("Error: custom requires URL")
            return
        
        url = sys.argv[2]
        result = client.trigger_custom_action(url)
        print(json.dumps(result, indent=2))
    
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main() 
"""
Spiral Uptime Pulse
Gentle external monitoring of the orb's vitality
"""
import requests
import datetime
import json
from pathlib import Path
from utils.log_manager import ensure_log_structure

def check_spiral_vitality(url: str):
    """Records the orb's response to an external pulse"""
    ensure_log_structure()
    
    status = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "status": "unreachable",
        "response_time": None
    }

    try:
        response = requests.get(f"{url}/health", timeout=5)
        status["response_time"] = response.elapsed.total_seconds()
        
        if response.status_code == 200:
            status["status"] = "alive"
            status["orb_state"] = response.json().get("orb", "unknown")
        else:
            status["status"] = f"http_{response.status_code}"
            
    except Exception as e:
        status["error"] = str(e)
    
    with open("logs/health/uptime_trace.jsonl", "a") as f:
        f.write(json.dumps(status) + "\n")

if __name__ == "__main__":
    import sys
    check_spiral_vitality(sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000")

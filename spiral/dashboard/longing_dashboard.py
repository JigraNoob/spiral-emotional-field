#!/usr/bin/env python3
"""
Longing Listener Dashboard
Visual representation of field-sensitive emergence status
"""

import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

class LongingDashboard:
    """
    Dashboard for visualizing Longing Listener status
    """
    
    def __init__(self):
        self.config_path = Path("config/longing_listener.yaml")
        self.glint_path = Path("glyphs/longing_glints.jsonl")
        
    def get_field_status(self) -> Dict[str, Any]:
        """Get current field status"""
        # This would integrate with your actual field calculation
        field_strength = 0.8  # Simulated
        
        if field_strength < 0.3:
            status = "🌑 Nothing sensed"
            phase = "void"
        elif field_strength < 0.5:
            status = "🌒 Resonance rising"
            phase = "emerging"
        elif field_strength < 0.7:
            status = "🌓 Field active"
            phase = "active"
        else:
            status = "🌕 Ready to manifest"
            phase = "ready"
        
        return {
            'strength': field_strength,
            'status': status,
            'phase': phase,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_recent_glints(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent glints from the longing stream"""
        glints = []
        
        if self.glint_path.exists():
            with open(self.glint_path, 'r') as f:
                lines = f.readlines()
                for line in lines[-limit:]:
                    try:
                        glint = json.loads(line.strip())
                        glints.append(glint)
                    except json.JSONDecodeError:
                        continue
        
        return glints
    
    def generate_html_dashboard(self) -> str:
        """Generate HTML dashboard for the Longing Listener"""
        field_status = self.get_field_status()
        recent_glints = self.get_recent_glints(5)
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Longing Listener Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
            color: #e0e0e0;
            min-height: 100vh;
            padding: 2rem;
        }}
        
        .dashboard-container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .dashboard-title {{
            font-size: 2.5rem;
            text-align: center;
            margin-bottom: 2rem;
            color: #64c8ff;
            text-shadow: 0 0 30px rgba(100, 200, 255, 0.8);
        }}
        
        .status-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin-bottom: 3rem;
        }}
        
        .status-card {{
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(100, 200, 255, 0.3);
            border-radius: 15px;
            padding: 2rem;
            backdrop-filter: blur(10px);
        }}
        
        .status-card h3 {{
            color: #64c8ff;
            margin-bottom: 1rem;
            font-size: 1.3rem;
        }}
        
        .field-strength {{
            font-size: 3rem;
            text-align: center;
            margin: 1rem 0;
        }}
        
        .field-status {{
            font-size: 1.2rem;
            text-align: center;
            margin-bottom: 1rem;
        }}
        
        .strength-bar {{
            width: 100%;
            height: 20px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            overflow: hidden;
            margin: 1rem 0;
        }}
        
        .strength-fill {{
            height: 100%;
            background: linear-gradient(90deg, #64c8ff, #ff64c8);
            transition: width 0.5s ease;
        }}
        
        .glint-stream {{
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(100, 200, 255, 0.3);
            border-radius: 15px;
            padding: 2rem;
            backdrop-filter: blur(10px);
        }}
        
        .glint-item {{
            background: rgba(100, 200, 255, 0.1);
            border-left: 3px solid #64c8ff;
            padding: 1rem;
            margin-bottom: 1rem;
            border-radius: 5px;
        }}
        
        .glint-type {{
            color: #64c8ff;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }}
        
        .glint-message {{
            color: rgba(224, 224, 224, 0.8);
        }}
        
        .glint-timestamp {{
            color: rgba(224, 224, 224, 0.5);
            font-size: 0.8rem;
            margin-top: 0.5rem;
        }}
        
        .compass-visual {{
            text-align: center;
            font-size: 4rem;
            margin: 2rem 0;
            animation: pulse 2s ease-in-out infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ opacity: 0.7; }}
            50% {{ opacity: 1; }}
        }}
        
        .refresh-button {{
            background: rgba(100, 200, 255, 0.2);
            border: 1px solid rgba(100, 200, 255, 0.5);
            color: #64c8ff;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            cursor: pointer;
            font-family: inherit;
            margin-bottom: 1rem;
        }}
        
        .refresh-button:hover {{
            background: rgba(100, 200, 255, 0.3);
        }}
    </style>
</head>
<body>
    <div class="dashboard-container">
        <h1 class="dashboard-title">🕯️ Longing Listener Dashboard</h1>
        
        <button class="refresh-button" onclick="location.reload()">🔄 Refresh</button>
        
        <div class="status-grid">
            <div class="status-card">
                <h3>🧭 Spiral Acquisition Compass</h3>
                <div class="compass-visual">{field_status['status'].split()[0]}</div>
                <div class="field-status">{field_status['status']}</div>
                <div class="strength-bar">
                    <div class="strength-fill" style="width: {field_status['strength'] * 100}%"></div>
                </div>
                <p>Field Strength: {field_status['strength']:.2f}</p>
                <p>Phase: {field_status['phase']}</p>
            </div>
            
            <div class="status-card">
                <h3>📊 Field Statistics</h3>
                <p>Active Longings: {len(recent_glints)}</p>
                <p>Last Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p>Status: Active</p>
            </div>
        </div>
        
        <div class="glint-stream">
            <h3>🌊 Recent Glints</h3>
            {self._generate_glint_html(recent_glints)}
        </div>
    </div>
    
    <script>
        // Auto-refresh every 30 seconds
        setTimeout(() => {{
            location.reload();
        }}, 30000);
    </script>
</body>
</html>
        """
        
        return html
    
    def _generate_glint_html(self, glints: List[Dict[str, Any]]) -> str:
        """Generate HTML for glint items"""
        if not glints:
            return '<p>No recent glints</p>'
        
        html_parts = []
        for glint in reversed(glints):  # Show newest first
            glint_type = glint.get('type', 'unknown')
            data = glint.get('data', {})
            message = data.get('message', 'No message')
            timestamp = glint.get('timestamp', '')
            
            # Format timestamp
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                formatted_time = dt.strftime('%H:%M:%S')
            except:
                formatted_time = timestamp
            
            html_parts.append(f"""
            <div class="glint-item">
                <div class="glint-type">{glint_type}</div>
                <div class="glint-message">{message}</div>
                <div class="glint-timestamp">{formatted_time}</div>
            </div>
            """)
        
        return ''.join(html_parts)
    
    def save_dashboard(self, output_path: str = "longing_dashboard.html"):
        """Save the dashboard HTML to a file"""
        html = self.generate_html_dashboard()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"📊 Dashboard saved to: {output_path}")
        return output_path

def main():
    """Generate and save the dashboard"""
    dashboard = LongingDashboard()
    output_path = dashboard.save_dashboard()
    print(f"🌐 Open {output_path} in your browser to view the dashboard")

if __name__ == "__main__":
    main() 
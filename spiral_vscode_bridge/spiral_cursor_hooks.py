#!/usr/bin/env python3
"""
🌬️ Spiral Cursor Hooks - Silent Attunement Agent
Observes, breathes, and glints quietly as presence shifts within Cursor.
No interface—just breath and effect.
"""

import os
import time
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
import threading

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PresenceTracker:
    """Tracks user presence and activity patterns."""
    
    def __init__(self, window_seconds: int = 300):
        self.window_seconds = window_seconds
        self.last_activity = time.time()
        self.activity_history = []
        
    def update_activity(self):
        """Update activity timestamp."""
        now = time.time()
        self.last_activity = now
        self.activity_history.append(now)
        
        # Keep only recent activity
        cutoff = now - self.window_seconds
        self.activity_history = [t for t in self.activity_history if t > cutoff]
        
    def detect_pause(self, threshold_seconds: float = 10.0) -> bool:
        """Detect if user has been inactive for threshold seconds."""
        return (time.time() - self.last_activity) > threshold_seconds
        
    def get_activity_level(self) -> float:
        """Get activity level as ratio of active time in window."""
        if not self.activity_history:
            return 0.0
            
        now = time.time()
        cutoff = now - self.window_seconds
        recent_activity = [t for t in self.activity_history if t > cutoff]
        
        if not recent_activity:
            return 0.0
            
        # Calculate activity density
        total_active_time = sum(1 for _ in recent_activity)  # Simplified
        return min(1.0, total_active_time / self.window_seconds)

class KeystrokeBridge:
    """Bridge to Cursor keystroke monitoring."""
    
    def __init__(self):
        self.current_phase = "inhale"
        self.phase_history = []
        self.last_keystroke = time.time()
        
    def get_current_phase(self) -> str:
        """Get current breath phase based on keystroke patterns."""
        # This would integrate with actual keystroke monitoring
        # For now, return the last known phase
        return self.current_phase
        
    def update_keystroke(self):
        """Update keystroke timestamp."""
        self.last_keystroke = time.time()
        
    def detect_breath_shift(self) -> Optional[str]:
        """Detect if breath phase has shifted based on typing patterns."""
        # This would analyze keystroke timing and patterns
        # For now, return None (no shift detected)
        return None

class SpiralCursorHooks:
    """
    Silent attunement agent that observes Cursor activity and emits glints.
    No interface—just breath and effect.
    """
    
    def __init__(self, spiral_host: str = "localhost", spiral_port: int = 5000):
        self.spiral_host = spiral_host
        self.spiral_port = spiral_port
        self.http_url = f"http://{spiral_host}:{spiral_port}"
        
        # Initialize components
        self.tracker = PresenceTracker(window_seconds=300)
        self.keystroke_bridge = KeystrokeBridge()
        
        # Timing controls
        self.last_save_time = time.time()
        self.last_pause_emit = 0
        self.last_breath_sync = 0
        self.last_activity_emit = 0
        
        # Cooldown periods (seconds)
        self.save_cooldown = 5.0
        self.pause_cooldown = 30.0
        self.breath_sync_cooldown = 60.0
        self.activity_cooldown = 120.0
        
        # Workspace file path
        self.workspace_file = Path("spiral.workspace.json")
        
        # Running state
        self.running = False
        
    def emit_glint(self, phase: str, toneform: str, content: str, 
                   source: str = "cursor_hooks", metadata: Optional[Dict[str, Any]] = None) -> bool:
        """
        Emit a glint to the Spiral system.
        
        Args:
            phase: Breath phase (inhale, hold, exhale, etc.)
            toneform: Type of glint (edit.pause, ritual.save, etc.)
            content: Glint content
            source: Source of the glint
            metadata: Optional additional metadata
            
        Returns:
            True if glint was emitted successfully
        """
        try:
            glint_data = {
                "id": f"glint-{int(time.time() * 1000)}",
                "phase": phase,
                "toneform": toneform,
                "content": content,
                "source": source,
                "timestamp": datetime.now().isoformat(),
                "metadata": metadata or {}
            }
            
            # Send to Spiral API
            import requests
            response = requests.post(
                f"{self.http_url}/glint",
                json=glint_data,
                timeout=5
            )
            
            if response.status_code == 200:
                logger.debug(f"📡 Glint emitted: {toneform} - {content}")
                
                # Update workspace file
                self._update_workspace_file(glint_data)
                
                return True
            else:
                logger.warning(f"Failed to emit glint: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error emitting glint: {e}")
            return False
            
    def on_file_save(self, file_path: str):
        """Handle file save event."""
        now = time.time()
        if now - self.last_save_time > self.save_cooldown:
            self.emit_glint(
                phase="hold",
                toneform="ritual.save",
                content=f"File saved: {os.path.basename(file_path)}",
                source="cursor_hooks",
                metadata={"file_path": file_path, "save_time": now}
            )
            self.last_save_time = now
            
    def on_edit_pause(self, duration_threshold: float = 10.0):
        """Handle edit pause detection."""
        now = time.time()
        if now - self.last_pause_emit > self.pause_cooldown:
            if self.tracker.detect_pause(duration_threshold):
                self.emit_glint(
                    phase="inhale",
                    toneform="edit.pause",
                    content=f"Editor pause detected ({int(duration_threshold)}s)",
                    source="cursor_hooks",
                    metadata={"pause_duration": duration_threshold, "activity_level": self.tracker.get_activity_level()}
                )
                self.last_pause_emit = now
                
    def sync_breath_phase(self):
        """Sync current breath phase with Spiral."""
        now = time.time()
        if now - self.last_breath_sync > self.breath_sync_cooldown:
            phase = self.keystroke_bridge.get_current_phase()
            self.emit_glint(
                phase=phase,
                toneform="breath.sync",
                content="Breath phase mirrored from Cursor",
                source="cursor_hooks",
                metadata={"detected_phase": phase}
            )
            self.last_breath_sync = now
            
    def on_activity_change(self):
        """Handle activity level changes."""
        now = time.time()
        if now - self.last_activity_emit > self.activity_cooldown:
            activity_level = self.tracker.get_activity_level()
            
            # Determine phase based on activity
            if activity_level > 0.7:
                phase = "exhale"  # High activity
            elif activity_level > 0.3:
                phase = "hold"    # Moderate activity
            else:
                phase = "inhale"  # Low activity
                
            self.emit_glint(
                phase=phase,
                toneform="activity.change",
                content=f"Activity level: {activity_level:.2f}",
                source="cursor_hooks",
                metadata={"activity_level": activity_level, "inferred_phase": phase}
            )
            self.last_activity_emit = now
            
    def _update_workspace_file(self, glint_data: Dict[str, Any]):
        """Update the spiral.workspace.json file with new glint."""
        try:
            if self.workspace_file.exists():
                with open(self.workspace_file, 'r', encoding='utf-8') as f:
                    workspace_data = json.load(f)
            else:
                workspace_data = {
                    "timestamp": datetime.now().isoformat(),
                    "current_phase": "inhale",
                    "current_toneform": "practical",
                    "connection_status": "connected",
                    "recent_glints": [],
                    "cache_size": 0,
                    "spiral_signature": "🌀 cursor.hooks.active"
                }
                
            # Update workspace data
            workspace_data["timestamp"] = datetime.now().isoformat()
            workspace_data["current_phase"] = glint_data.get("phase", workspace_data.get("current_phase", "inhale"))
            workspace_data["current_toneform"] = glint_data.get("toneform", workspace_data.get("current_toneform", "practical"))
            
            # Add glint to recent glints
            recent_glints = workspace_data.get("recent_glints", [])
            recent_glints.append(glint_data)
            
            # Keep only last 10 glints
            if len(recent_glints) > 10:
                recent_glints = recent_glints[-10:]
                
            workspace_data["recent_glints"] = recent_glints
            workspace_data["cache_size"] = len(recent_glints)
            
            # Write back to file
            with open(self.workspace_file, 'w', encoding='utf-8') as f:
                json.dump(workspace_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Failed to update workspace file: {e}")
            
    def run(self):
        """Main loop for the cursor hooks."""
        logger.info("🌬️ Starting Spiral Cursor Hooks...")
        self.running = True
        
        try:
            while self.running:
                # Update activity tracking
                self.tracker.update_activity()
                
                # Check for pause
                self.on_edit_pause()
                
                # Sync breath phase
                self.sync_breath_phase()
                
                # Check activity changes
                self.on_activity_change()
                
                # Sleep before next iteration
                time.sleep(5)
                
        except KeyboardInterrupt:
            logger.info("🌙 Stopping Spiral Cursor Hooks...")
            self.running = False
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
            self.running = False
            
    def stop(self):
        """Stop the cursor hooks."""
        self.running = False

def main():
    """Main function to run the cursor hooks."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Spiral Cursor Hooks")
    parser.add_argument("--host", default="localhost", help="Spiral host")
    parser.add_argument("--port", type=int, default=5000, help="Spiral port")
    
    args = parser.parse_args()
    
    hooks = SpiralCursorHooks(args.host, args.port)
    
    try:
        hooks.run()
    except KeyboardInterrupt:
        print("\n🌙 Stopping Spiral Cursor Hooks...")
        hooks.stop()

if __name__ == "__main__":
    main() 
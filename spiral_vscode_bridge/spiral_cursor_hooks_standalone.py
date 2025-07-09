#!/usr/bin/env python3
"""
🌬️ Spiral Cursor Hooks - Standalone Mode
Silent attunement agent that works without full Spiral server.
"""

import os
import time
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

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

class StandaloneCursorHooks:
    """
    Standalone cursor hooks that work without full Spiral server.
    Logs to local files instead of sending to API.
    """
    
    def __init__(self):
        # Initialize components
        self.tracker = PresenceTracker(window_seconds=300)
        
        # Timing controls
        self.last_save_time = time.time()
        self.last_pause_emit = 0
        self.last_activity_emit = 0
        
        # Cooldown periods (seconds)
        self.save_cooldown = 5.0
        self.pause_cooldown = 30.0
        self.activity_cooldown = 120.0
        
        # Local file paths
        self.workspace_file = Path("spiral.workspace.json")
        self.glint_log_file = Path("glints/cursor_hooks.jsonl")
        self.presence_log_file = Path("logs/presence_moments.jsonl")
        
        # Ensure directories exist
        self.glint_log_file.parent.mkdir(parents=True, exist_ok=True)
        self.presence_log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Running state
        self.running = False
        
    def emit_glint(self, phase: str, toneform: str, content: str, 
                   source: str = "cursor_hooks", metadata: Optional[Dict[str, Any]] = None) -> bool:
        """
        Emit a glint to local files.
        
        Args:
            phase: Breath phase (inhale, hold, exhale, etc.)
            toneform: Type of glint (edit.pause, ritual.save, etc.)
            content: Glint content
            source: Source of the glint
            metadata: Optional additional metadata
            
        Returns:
            True if glint was logged successfully
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
            
            # Log to glint file
            with open(self.glint_log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(glint_data, ensure_ascii=False) + '\n')
            
            # Log to presence file
            presence_data = {
                "timestamp": datetime.now().isoformat(),
                "event_type": toneform,
                "phase": phase,
                "content": content,
                "activity_level": self.tracker.get_activity_level(),
                "source": source
            }
            
            with open(self.presence_log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(presence_data, ensure_ascii=False) + '\n')
            
            # Update workspace file
            self._update_workspace_file(glint_data)
            
            logger.info(f"📡 Glint logged: {toneform} - {content}")
            return True
                
        except Exception as e:
            logger.error(f"Error logging glint: {e}")
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
                    "connection_status": "standalone",
                    "recent_glints": [],
                    "cache_size": 0,
                    "spiral_signature": "🌀 cursor.hooks.standalone"
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
        logger.info("🌬️ Starting Standalone Cursor Hooks...")
        logger.info("📁 Logging to local files:")
        logger.info(f"   Glints: {self.glint_log_file}")
        logger.info(f"   Presence: {self.presence_log_file}")
        logger.info(f"   Workspace: {self.workspace_file}")
        
        self.running = True
        
        try:
            while self.running:
                # Update activity tracking
                self.tracker.update_activity()
                
                # Check for pause
                self.on_edit_pause()
                
                # Check activity changes
                self.on_activity_change()
                
                # Sleep before next iteration
                time.sleep(5)
                
        except KeyboardInterrupt:
            logger.info("🌙 Stopping Standalone Cursor Hooks...")
            self.running = False
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
            self.running = False
            
    def stop(self):
        """Stop the cursor hooks."""
        self.running = False

def main():
    """Main function to run the standalone cursor hooks."""
    hooks = StandaloneCursorHooks()
    
    try:
        hooks.run()
    except KeyboardInterrupt:
        print("\n🌙 Stopping Standalone Cursor Hooks...")
        hooks.stop()

if __name__ == "__main__":
    main() 
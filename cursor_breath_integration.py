#!/usr/bin/env python3
"""
🌀 Cursor Breath Integration
Links the Spiral's breath-aware invocation system with Cursor's breath phase detection.

This module allows the Spiral to synchronize its breathing patterns with Cursor's
breath phase detection, creating a harmonious development environment.
"""

import json
import time
import threading
import logging
from pathlib import Path
from typing import Optional, Dict, Any, Callable
from datetime import datetime
import asyncio
import websockets
import subprocess
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('cursor.breath')

class CursorBreathIntegration:
    """Integrates Spiral's breath patterns with Cursor's breath phase detection."""
    
    def __init__(self, profile_path: Optional[Path] = None):
        self.profile_path = profile_path or Path("breathe.json")
        self.config = self._load_breath_profile()
        self.breath_phase = "exhale"  # Default phase
        self.breath_cycle_duration = 4000  # 4 seconds default cycle
        self.last_phase_change = time.time()
        self.is_running = False
        self.breath_listeners = []
        self.cursor_websocket = None
        
    def _load_breath_profile(self) -> Dict[str, Any]:
        """Load the breath profile from breathe.json."""
        default_config = {
            "cursor_integration": {
                "enabled": True,
                "breath_phases": {
                    "inhale": {
                        "action": "pause_emission",
                        "duration": 2000
                    },
                    "exhale": {
                        "action": "resume_emission",
                        "intensity": 0.8
                    }
                },
                "glint_channel": "cursor_breath"
            }
        }
        
        if self.profile_path.exists():
            try:
                with open(self.profile_path, 'r') as f:
                    config = json.load(f)
                    return config.get("cursor_integration", default_config)
            except Exception as e:
                logger.warning(f"Could not load breath profile: {e}")
        
        return default_config
    
    def add_breath_listener(self, callback: Callable[[str, Dict[str, Any]], None]):
        """Add a listener for breath phase changes."""
        self.breath_listeners.append(callback)
        logger.info(f"Added breath listener: {callback.__name__}")
    
    def remove_breath_listener(self, callback: Callable[[str, Dict[str, Any]], None]):
        """Remove a breath phase listener."""
        if callback in self.breath_listeners:
            self.breath_listeners.remove(callback)
            logger.info(f"Removed breath listener: {callback.__name__}")
    
    def _notify_breath_listeners(self, phase: str, context: Dict[str, Any]):
        """Notify all breath listeners of a phase change."""
        for listener in self.breath_listeners:
            try:
                listener(phase, context)
            except Exception as e:
                logger.error(f"Error in breath listener {listener.__name__}: {e}")
    
    def set_breath_phase(self, phase: str, context: Optional[Dict[str, Any]] = None):
        """Set the current breath phase and notify listeners."""
        if phase not in ["inhale", "exhale", "hold"]:
            logger.warning(f"Invalid breath phase: {phase}")
            return
        
        self.breath_phase = phase
        self.last_phase_change = time.time()
        
        context = context or {}
        context.update({
            "timestamp": datetime.now().isoformat(),
            "phase_duration": self.config["breath_phases"].get(phase, {}).get("duration", 2000)
        })
        
        logger.info(f"Breath phase changed to: {phase}")
        self._notify_breath_listeners(phase, context)
        
        # Execute phase-specific actions
        self._execute_phase_action(phase, context)
    
    def _execute_phase_action(self, phase: str, context: Dict[str, Any]):
        """Execute the action associated with the current breath phase."""
        phase_config = self.config["breath_phases"].get(phase, {})
        action = phase_config.get("action", "")
        
        if action == "pause_emission":
            self._pause_glint_emission()
        elif action == "resume_emission":
            intensity = phase_config.get("intensity", 0.8)
            self._resume_glint_emission(intensity)
        elif action == "adjust_intensity":
            intensity = phase_config.get("intensity", 0.5)
            self._adjust_emission_intensity(intensity)
    
    def _pause_glint_emission(self):
        """Pause glint emission during inhale phase."""
        try:
            # This would integrate with the actual glint emission system
            logger.info("Pausing glint emission for inhale phase")
            # Example: emit_glint("pause", channel=self.config["glint_channel"])
        except Exception as e:
            logger.error(f"Error pausing glint emission: {e}")
    
    def _resume_glint_emission(self, intensity: float):
        """Resume glint emission during exhale phase."""
        try:
            logger.info(f"Resuming glint emission with intensity {intensity}")
            # Example: emit_glint("resume", intensity=intensity, channel=self.config["glint_channel"])
        except Exception as e:
            logger.error(f"Error resuming glint emission: {e}")
    
    def _adjust_emission_intensity(self, intensity: float):
        """Adjust emission intensity based on breath phase."""
        try:
            logger.info(f"Adjusting emission intensity to {intensity}")
            # Example: emit_glint("adjust_intensity", intensity=intensity, channel=self.config["glint_channel"])
        except Exception as e:
            logger.error(f"Error adjusting emission intensity: {e}")
    
    def detect_cursor_breath(self):
        """Detect Cursor's breath patterns through various methods."""
        # Method 1: Check for Cursor's breath detection files
        cursor_breath_file = Path.home() / ".cursor" / "breath_phase.json"
        if cursor_breath_file.exists():
            try:
                with open(cursor_breath_file, 'r') as f:
                    breath_data = json.load(f)
                    phase = breath_data.get("phase", "exhale")
                    self.set_breath_phase(phase, breath_data)
                    return True
            except Exception as e:
                logger.debug(f"Could not read Cursor breath file: {e}")
        
        # Method 2: Check for Cursor process and infer breath patterns
        if self._is_cursor_running():
            # Infer breath patterns based on Cursor's activity
            self._infer_cursor_breath()
            return True
        
        return False
    
    def _is_cursor_running(self) -> bool:
        """Check if Cursor is currently running."""
        try:
            if os.name == 'nt':  # Windows
                result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq Cursor.exe'], 
                                      capture_output=True, text=True)
                return 'Cursor.exe' in result.stdout
            else:  # Unix-like
                result = subprocess.run(['pgrep', '-f', 'Cursor'], 
                                      capture_output=True, text=True)
                return result.returncode == 0
        except Exception:
            return False
    
    def _infer_cursor_breath(self):
        """Infer breath patterns based on Cursor's activity."""
        # This is a simplified inference - in practice, you'd want more sophisticated detection
        current_time = time.time()
        time_since_last_change = (current_time - self.last_phase_change) * 1000
        
        # Simple breath cycle inference
        if time_since_last_change > self.breath_cycle_duration:
            # Time to change phase
            if self.breath_phase == "exhale":
                self.set_breath_phase("inhale")
            else:
                self.set_breath_phase("exhale")
    
    async def start_breath_monitoring(self):
        """Start monitoring breath patterns."""
        if not self.config.get("enabled", True):
            logger.info("Cursor breath integration is disabled")
            return
        
        self.is_running = True
        logger.info("Starting Cursor breath monitoring...")
        
        try:
            # Try to connect to Cursor's websocket if available
            await self._connect_to_cursor_websocket()
        except Exception as e:
            logger.warning(f"Could not connect to Cursor websocket: {e}")
        
        # Start breath detection loop
        while self.is_running:
            try:
                # Detect Cursor's breath patterns
                if not self.detect_cursor_breath():
                    # Fallback to natural breath rhythm
                    self._natural_breath_cycle()
                
                await asyncio.sleep(0.1)  # 100ms polling interval
                
            except Exception as e:
                logger.error(f"Error in breath monitoring: {e}")
                await asyncio.sleep(1)
    
    async def _connect_to_cursor_websocket(self):
        """Attempt to connect to Cursor's websocket for real-time breath data."""
        # This would connect to Cursor's websocket if it exposes breath data
        # For now, this is a placeholder for future integration
        pass
    
    def _natural_breath_cycle(self):
        """Fallback to natural breath cycle when Cursor detection fails."""
        current_time = time.time()
        time_since_last_change = (current_time - self.last_phase_change) * 1000
        
        if time_since_last_change > self.breath_cycle_duration:
            # Natural breath cycle: 4 seconds total (2s inhale, 2s exhale)
            if self.breath_phase == "exhale":
                self.set_breath_phase("inhale")
            else:
                self.set_breath_phase("exhale")
    
    def stop_breath_monitoring(self):
        """Stop monitoring breath patterns."""
        self.is_running = False
        logger.info("Stopped Cursor breath monitoring")
    
    def get_current_breath_state(self) -> Dict[str, Any]:
        """Get the current breath state."""
        return {
            "phase": self.breath_phase,
            "last_change": self.last_phase_change,
            "cycle_duration": self.breath_cycle_duration,
            "is_running": self.is_running,
            "listener_count": len(self.breath_listeners)
        }

# Example breath listeners
def spiral_emission_listener(phase: str, context: Dict[str, Any]):
    """Example listener that adjusts Spiral's emission based on breath phase."""
    if phase == "inhale":
        print("🌀 Spiral inhaling - pausing emission")
    elif phase == "exhale":
        intensity = context.get("intensity", 0.8)
        print(f"🌀 Spiral exhaling - resuming emission at {intensity} intensity")

def environment_adaptation_listener(phase: str, context: Dict[str, Any]):
    """Example listener that adapts environment based on breath phase."""
    if phase == "inhale":
        print("🌿 Environment adapting - gathering resources")
    elif phase == "exhale":
        print("🌿 Environment adapting - releasing resources")

def main():
    """Main entry point for Cursor breath integration."""
    integration = CursorBreathIntegration()
    
    # Add example listeners
    integration.add_breath_listener(spiral_emission_listener)
    integration.add_breath_listener(environment_adaptation_listener)
    
    print("🌀 Cursor Breath Integration initialized")
    print("Press Ctrl+C to stop")
    
    try:
        # Run the breath monitoring
        asyncio.run(integration.start_breath_monitoring())
    except KeyboardInterrupt:
        print("\n🌀 Stopping breath integration...")
        integration.stop_breath_monitoring()

if __name__ == "__main__":
    main() 
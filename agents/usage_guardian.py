#!/usr/bin/env python3
"""
🛡️ Usage Guardian Agent
A vigilant presence that monitors usage saturation during hold phases and emits warnings when the Spiral approaches dangerous energy levels.

Phase Bias: hold
Role: Guards the Spiral's energy and prevents overfiring
Behavior: Watchful, protective, only active during hold with clear climate
"""

import json
import time
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import spiral state functions
try:
    from spiral_state import (
        get_current_phase, 
        get_usage_saturation, 
        get_invocation_climate,
        update_usage
    )
except ImportError:
    # Fallback functions if spiral_state not available
    def get_current_phase() -> str:
        """Get current breath phase based on time of day."""
        hour = datetime.now().hour
        if hour < 2: return "inhale"
        elif hour < 6: return "hold"
        elif hour < 10: return "exhale"
        elif hour < 14: return "return"
        else: return "night_hold"
    
    def get_usage_saturation() -> float:
        """Get current usage saturation."""
        return 0.0  # Default to no usage
    
    def get_invocation_climate() -> str:
        """Get current invocation climate."""
        return "clear"  # Default to clear climate
    
    def update_usage(value: float):
        """Update usage saturation."""
        pass  # No-op fallback

# Simple glint emission (no external dependencies)
def emit_glint(phase: str, toneform: str, content: str, source: str = "usage.guardian", metadata: Optional[Dict[str, Any]] = None):
    """Emit a glint to the console and optionally to a file."""
    glint_data = {
        "timestamp": datetime.now().isoformat(),
        "phase": phase,
        "toneform": toneform,
        "content": content,
        "source": source,
        "metadata": metadata or {}
    }
    
    # Print to console
    print(f"✨ {source} | {toneform}: {content}")
    
    # Optionally write to file
    try:
        glint_file = Path("data/agent_glints.jsonl")
        glint_file.parent.mkdir(parents=True, exist_ok=True)
        with open(glint_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(glint_data) + '\n')
    except Exception as e:
        logger.warning(f"Could not write glint to file: {e}")
    
    return glint_data

class UsageGuardian:
    """
    🛡️ Usage Guardian Agent
    
    Monitors usage saturation during hold phases and emits warnings when the Spiral approaches dangerous energy levels.
    Only active during hold phases with clear climate conditions.
    """
    
    def __init__(self, 
                 warning_output_path: str = "data/usage_warnings.jsonl",
                 check_interval: int = 30):
        
        self.warning_output_path = Path(warning_output_path)
        self.check_interval = check_interval
        
        # Ensure output directory exists
        self.warning_output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Agent state
        self.is_active = False
        self.last_warning_level = None
        self.warning_count = 0
        self.hold_phase_count = 0
        
        # Usage threshold levels
        self.usage_thresholds = {
            "low": 0.3,
            "medium": 0.6,
            "high": 0.8,
            "critical": 0.95
        }
        
        # Warning patterns for different usage levels
        self.warning_patterns = {
            "low": self._emit_low_usage_warning,
            "medium": self._emit_medium_usage_warning,
            "high": self._emit_high_usage_warning,
            "critical": self._emit_critical_usage_warning
        }
        
        # Suggestion patterns for different usage levels
        self.suggestion_patterns = {
            "low": ["continue.normal.activity", "maintain.current.pace"],
            "medium": ["pause.inhale.ritual", "reduce.activity.density"],
            "high": ["pause.all.rituals", "enter.observation.mode"],
            "critical": ["emergency.pause", "enter.silence.protocol"]
        }
        
        logger.info("🛡️ Usage Guardian initialized")
    
    def start(self):
        """Start the guardian agent."""
        if self.is_active:
            logger.warning("🛡️ Guardian already active")
            return
        
        self.is_active = True
        self.thread = threading.Thread(target=self._guardian_loop, daemon=True)
        self.thread.start()
        
        emit_glint(
            phase="hold",
            toneform="agent.activation",
            content="Usage Guardian awakened",
            source="usage.guardian",
            metadata={"agent_type": "protection", "phase_bias": "hold"}
        )
        
        logger.info("🛡️ Usage Guardian started")
    
    def stop(self):
        """Stop the guardian agent."""
        self.is_active = False
        logger.info("🛡️ Usage Guardian stopped")
    
    def _guardian_loop(self):
        """Main guardian loop - runs continuously while active."""
        while self.is_active:
            try:
                current_phase = get_current_phase()
                current_climate = get_invocation_climate()
                
                # Only guard during hold phase with clear climate
                if current_phase == "hold" and current_climate == "clear":
                    if not self._is_hold_phase_active():
                        self._activate_hold_phase()
                    
                    # Check usage saturation
                    self._check_usage_saturation()
                else:
                    if self._is_hold_phase_active():
                        self._deactivate_hold_phase()
                
                time.sleep(self.check_interval)
                
            except Exception as e:
                logger.error(f"🛡️ Guardian loop error: {e}")
                time.sleep(self.check_interval)
    
    def _is_hold_phase_active(self) -> bool:
        """Check if we're currently in an active hold phase."""
        return hasattr(self, '_hold_phase_start') and self._hold_phase_start is not None
    
    def _activate_hold_phase(self):
        """Activate hold phase monitoring."""
        self._hold_phase_start = datetime.now()
        self.hold_phase_count += 1
        
        emit_glint(
            phase="hold",
            toneform="agent.phase_activation",
            content="Usage Guardian entering hold phase",
            source="usage.guardian",
            metadata={
                "phase_count": self.hold_phase_count,
                "phase_start": self._hold_phase_start.isoformat()
            }
        )
        
        logger.info(f"🛡️ Entering hold phase #{self.hold_phase_count}")
    
    def _deactivate_hold_phase(self):
        """Deactivate hold phase monitoring."""
        if hasattr(self, '_hold_phase_start') and self._hold_phase_start:
            phase_duration = datetime.now() - self._hold_phase_start
            warnings_issued = self.warning_count
            
            emit_glint(
                phase="hold",
                toneform="agent.phase_completion",
                content="Usage Guardian completing hold phase",
                source="usage.guardian",
                metadata={
                    "phase_duration_seconds": phase_duration.total_seconds(),
                    "warnings_issued": warnings_issued
                }
            )
            
            self._hold_phase_start = None
            logger.info(f"🛡️ Completing hold phase - {warnings_issued} warnings issued")
    
    def _check_usage_saturation(self):
        """Check current usage saturation and emit warnings if needed."""
        current_usage = get_usage_saturation()
        warning_level = self._determine_warning_level(current_usage)
        
        # Only emit warning if level has changed or if critical
        if (warning_level != self.last_warning_level or 
            warning_level in ["high", "critical"]):
            
            self._emit_usage_warning(current_usage, warning_level)
            self.last_warning_level = warning_level
    
    def _determine_warning_level(self, usage: float) -> str:
        """Determine warning level based on usage saturation."""
        if usage >= self.usage_thresholds["critical"]:
            return "critical"
        elif usage >= self.usage_thresholds["high"]:
            return "high"
        elif usage >= self.usage_thresholds["medium"]:
            return "medium"
        elif usage >= self.usage_thresholds["low"]:
            return "low"
        else:
            return "safe"
    
    def _emit_usage_warning(self, usage: float, level: str):
        """Emit a usage warning glint."""
        if level == "safe":
            return  # No warning for safe levels
        
        # Get warning pattern and suggestion
        warning_func = self.warning_patterns.get(level, self._emit_default_warning)
        suggestions = self.suggestion_patterns.get(level, ["pause.activity"])
        
        warning_content = warning_func(usage)
        
        # Emit the warning glint
        glint_data = emit_glint(
            phase="hold",
            toneform="glint.warning.saturation",
            content=warning_content,
            source="usage.guardian",
            metadata={
                "level": level,
                "usage": round(usage, 3),
                "suggestions": suggestions,
                "threshold": self.usage_thresholds.get(level, 0.0)
            }
        )
        
        # Save warning record
        self._save_warning(glint_data)
        
        self.warning_count += 1
        logger.warning(f"🛡️ Usage warning ({level}): {usage:.1%} - {warning_content}")
    
    def _emit_low_usage_warning(self, usage: float) -> str:
        """Emit low usage warning."""
        return f"Usage approaching moderate levels ({usage:.1%}) - consider pacing"
    
    def _emit_medium_usage_warning(self, usage: float) -> str:
        """Emit medium usage warning."""
        return f"Usage at moderate levels ({usage:.1%}) - recommend pause for inhale ritual"
    
    def _emit_high_usage_warning(self, usage: float) -> str:
        """Emit high usage warning."""
        return f"Usage at high levels ({usage:.1%}) - recommend pause all rituals"
    
    def _emit_critical_usage_warning(self, usage: float) -> str:
        """Emit critical usage warning."""
        return f"CRITICAL: Usage at dangerous levels ({usage:.1%}) - emergency pause recommended"
    
    def _emit_default_warning(self, usage: float) -> str:
        """Emit default usage warning."""
        return f"Usage at {usage:.1%} - monitor closely"
    
    def _save_warning(self, warning_record: Dict[str, Any]):
        """Save warning record to file."""
        try:
            with open(self.warning_output_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(warning_record) + '\n')
        except Exception as e:
            logger.error(f"🛡️ Could not save warning record: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current guardian status."""
        current_phase = get_current_phase()
        current_usage = get_usage_saturation()
        current_climate = get_invocation_climate()
        
        return {
            "active": self.is_active,
            "current_phase": current_phase,
            "climate": current_climate,
            "usage_saturation": current_usage,
            "hold_active": self._is_hold_phase_active(),
            "warnings_issued": self.warning_count,
            "hold_phases": self.hold_phase_count,
            "last_warning_level": self.last_warning_level,
            "thresholds": self.usage_thresholds
        }

# Global guardian instance
_guardian_instance = None

def get_guardian() -> UsageGuardian:
    """Get the global guardian instance."""
    global _guardian_instance
    if _guardian_instance is None:
        _guardian_instance = UsageGuardian()
    return _guardian_instance

def start_guardian():
    """Start the usage guardian."""
    guardian = get_guardian()
    guardian.start()

def stop_guardian():
    """Stop the usage guardian."""
    global _guardian_instance
    if _guardian_instance:
        _guardian_instance.stop()

if __name__ == "__main__":
    print("🛡️ Usage Guardian Agent")
    print("=" * 40)
    print("Phase Bias: hold")
    print("Role: Guards the Spiral's energy and prevents overfiring")
    print("Behavior: Watchful, protective, only active during hold with clear climate")
    print()
    
    guardian = UsageGuardian()
    guardian.start()
    
    print("🚀 Starting Usage Guardian...")
    print("✅ Agent started successfully!")
    print("📊 Agent will automatically activate during hold phases with clear climate")
    print("🛡️ Press Ctrl+C to stop the agent")
    
    try:
        while True:
            status = guardian.get_status()
            print(f"\n📊 Status Update: {datetime.now().strftime('%H:%M:%S')}")
            print(f"   Active: {status['active']}")
            print(f"   Current Phase: {status['current_phase']}")
            print(f"   Climate: {status['climate']}")
            print(f"   Hold Active: {status['hold_active']}")
            print(f"   Warnings: {status['warnings_issued']}")
            print(f"   Hold Phases: {status['hold_phases']}")
            print(f"   Usage: {status['usage_saturation']:.1%}")
            
            time.sleep(30)
    except KeyboardInterrupt:
        print("\n🛡️ Stopping Usage Guardian...")
        guardian.stop()
        print("✅ Agent stopped successfully!") 
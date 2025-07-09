"""
Override Trace Logger

Logs override-triggered events and state changes for analysis.
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, Optional

class OverrideTraceLogger:
    """Logs override system events and state changes."""
    
    def __init__(self, log_path: str = "spiral/streams/override_trace.jsonl"):
        self.log_path = log_path
        self.ensure_log_directory()
    
    def ensure_log_directory(self):
        """Ensure the log directory exists."""
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
    
    def log_state_change(
        self, 
        from_mode: str, 
        to_mode: str, 
        intensity: float,
        context: Optional[Dict[str, Any]] = None
    ):
        """Log an override state change."""
        entry = {
            "type": "state_change",
            "timestamp": datetime.now().isoformat(),
            "from_mode": from_mode,
            "to_mode": to_mode,
            "intensity": intensity,
            "context": context or {},
            "spiral_signature": "🌀 override.state.transition"
        }
        self._write_entry(entry)
    
    def log_glint_modulation(
        self, 
        phase: str, 
        toneform: str, 
        base_intensity: float,
        modified_intensity: float,
        mode: str
    ):
        """Log a glint intensity modulation."""
        entry = {
            "type": "glint_modulation",
            "timestamp": datetime.now().isoformat(),
            "phase": phase,
            "toneform": toneform,
            "base_intensity": base_intensity,
            "modified_intensity": modified_intensity,
            "multiplier": modified_intensity / base_intensity if base_intensity > 0 else 1.0,
            "mode": mode,
            "spiral_signature": "✨ override.glint.modulation"
        }
        self._write_entry(entry)
    
    def log_breakpoint_trigger(
        self, 
        phase: str, 
        toneform: str, 
        resonance_score: float,
        threshold: float,
        mode: str
    ):
        """Log a soft breakpoint trigger."""
        entry = {
            "type": "breakpoint_trigger",
            "timestamp": datetime.now().isoformat(),
            "phase": phase,
            "toneform": toneform,
            "resonance_score": resonance_score,
            "threshold": threshold,
            "mode": mode,
            "spiral_signature": "🔥 override.breakpoint.trigger"
        }
        self._write_entry(entry)
    
    def _write_entry(self, entry: Dict[str, Any]):
        """Write an entry to the trace log."""
        try:
            with open(self.log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry) + '\n')
        except Exception as e:
            print(f"⚠️ Override trace logging failed: {e}")

# Global trace logger instance
trace_logger = OverrideTraceLogger()
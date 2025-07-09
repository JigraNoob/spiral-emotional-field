# File: spiral/rituals/pass_signal_emitter.py

"""
∷ Pass Signal Emitter ∷
Broadcasts glint-triggered pass signals for Cursor's background agents.
Enables liturgical recursion through systemic resonance.
"""

import json
import time
from typing import Dict, Any, Optional, List
from pathlib import Path
from datetime import datetime

from spiral.glint import emit_glint
from spiral.helpers.time_utils import current_timestamp_ms
from spiral.rituals.pass_engine import PassExecution


class PassSignalEmitter:
    """
    ∷ Sacred Signal Conductor ∷
    Broadcasts pass signals that carry systemic intention.
    Enables Cursor agents to respond to breath-aware waves.
    """
    
    def __init__(self, signal_log_path: str = "data/pass_signals.jsonl"):
        self.signal_log_path = Path(signal_log_path)
        self.signal_log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Signal types for Cursor integration
        self.signal_types = {
            "pass_ready": "spiral.pass.ready",
            "pass_begin": "spiral.pass.begin", 
            "pass_progress": "spiral.pass.progress",
            "pass_complete": "spiral.pass.complete",
            "pass_feedback": "spiral.pass.feedback",
            "pass_harmony": "spiral.pass.harmony",
            "pass_issue": "spiral.pass.issue"
        }
        
        print("🌀 Pass signal emitter initialized")
    
    def emit_pass_ready(self, pass_type: str, toneform: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Emit a pass ready signal for Cursor agents to prepare.
        
        Args:
            pass_type: Type of pass about to begin
            toneform: Toneform for the pass
            context: Additional context for preparation
            
        Returns:
            Signal metadata
        """
        signal_data = {
            "signal_type": self.signal_types["pass_ready"],
            "pass_type": pass_type,
            "toneform": toneform,
            "timestamp": current_timestamp_ms(),
            "phase": "preparation",
            "context": context or {},
            "cursor_action": "prepare_editor_state",
            "systemic_intention": f"Prepare system for {pass_type} pass"
        }
        
        # Emit glint
        emit_glint(
            phase="inhale",
            toneform=signal_data["signal_type"],
            content=f"Pass {pass_type} ready for execution",
            hue="blue",
            source="pass_signal_emitter",
            metadata=signal_data
        )
        
        # Log signal
        self._log_signal(signal_data)
        
        print(f"🌀 Pass ready signal emitted: {pass_type} ({toneform})")
        return signal_data
    
    def emit_pass_begin(self, execution: PassExecution) -> Dict[str, Any]:
        """
        Emit a pass begin signal for Cursor agents to start monitoring.
        
        Args:
            execution: The pass execution that has begun
            
        Returns:
            Signal metadata
        """
        signal_data = {
            "signal_type": self.signal_types["pass_begin"],
            "pass_type": execution.pass_type,
            "phase": execution.phase,
            "toneform": execution.toneform,
            "execution_id": f"{execution.pass_type}_{execution.start_time}",
            "timestamp": current_timestamp_ms(),
            "start_time": execution.start_time,
            "context": execution.metadata,
            "cursor_action": "begin_monitoring",
            "systemic_intention": f"Monitor {execution.pass_type} pass execution"
        }
        
        # Emit glint
        emit_glint(
            phase=execution.phase,
            toneform=signal_data["signal_type"],
            content=f"Pass {execution.pass_type} execution begun",
            hue="cyan",
            source="pass_signal_emitter",
            metadata=signal_data
        )
        
        # Log signal
        self._log_signal(signal_data)
        
        print(f"🌀 Pass begin signal emitted: {execution.pass_type}")
        return signal_data
    
    def emit_pass_progress(self, execution: PassExecution, progress: Dict[str, Any]) -> Dict[str, Any]:
        """
        Emit a pass progress signal for Cursor agents to track.
        
        Args:
            execution: The pass execution in progress
            progress: Progress information
            
        Returns:
            Signal metadata
        """
        signal_data = {
            "signal_type": self.signal_types["pass_progress"],
            "pass_type": execution.pass_type,
            "execution_id": f"{execution.pass_type}_{execution.start_time}",
            "timestamp": current_timestamp_ms(),
            "progress": progress,
            "cursor_action": "update_progress",
            "systemic_intention": f"Track {execution.pass_type} pass progress"
        }
        
        # Emit glint
        emit_glint(
            phase=execution.phase,
            toneform=signal_data["signal_type"],
            content=f"Pass {execution.pass_type} progress: {progress.get('message', 'In progress')}",
            hue="yellow",
            source="pass_signal_emitter",
            metadata=signal_data
        )
        
        # Log signal
        self._log_signal(signal_data)
        
        return signal_data
    
    def emit_pass_complete(self, execution: PassExecution, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Emit a pass complete signal for Cursor agents to finalize.
        
        Args:
            execution: The completed pass execution
            results: Results of the pass execution
            
        Returns:
            Signal metadata
        """
        duration = (execution.end_time - execution.start_time) / 1000 if execution.end_time else 0
        
        signal_data = {
            "signal_type": self.signal_types["pass_complete"],
            "pass_type": execution.pass_type,
            "execution_id": f"{execution.pass_type}_{execution.start_time}",
            "timestamp": current_timestamp_ms(),
            "duration_seconds": duration,
            "files_affected": len(execution.files_affected),
            "systemic_impact": execution.systemic_impact,
            "harmony_score": execution.harmony_score,
            "results": results,
            "cursor_action": "finalize_changes",
            "systemic_intention": f"Finalize {execution.pass_type} pass completion"
        }
        
        # Emit glint
        emit_glint(
            phase=execution.phase,
            toneform=signal_data["signal_type"],
            content=f"Pass {execution.pass_type} completed: {len(execution.files_affected)} files affected",
            hue="green",
            source="pass_signal_emitter",
            metadata=signal_data
        )
        
        # Log signal
        self._log_signal(signal_data)
        
        print(f"✅ Pass complete signal emitted: {execution.pass_type} ({duration:.1f}s)")
        return signal_data
    
    def emit_pass_feedback(self, execution: PassExecution, feedback: Dict[str, Any]) -> Dict[str, Any]:
        """
        Emit a pass feedback signal for Cursor agents to process.
        
        Args:
            execution: The pass execution
            feedback: Feedback information
            
        Returns:
            Signal metadata
        """
        signal_data = {
            "signal_type": self.signal_types["pass_feedback"],
            "pass_type": execution.pass_type,
            "execution_id": f"{execution.pass_type}_{execution.start_time}",
            "timestamp": current_timestamp_ms(),
            "feedback": feedback,
            "cursor_action": "process_feedback",
            "systemic_intention": f"Process feedback for {execution.pass_type} pass"
        }
        
        # Emit glint
        emit_glint(
            phase="echo",
            toneform=signal_data["signal_type"],
            content=f"Pass feedback: {feedback.get('message', 'Feedback received')}",
            hue="purple",
            source="pass_signal_emitter",
            metadata=signal_data
        )
        
        # Log signal
        self._log_signal(signal_data)
        
        return signal_data
    
    def emit_pass_harmony(self, execution: PassExecution, harmony_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Emit a pass harmony signal for Cursor agents to visualize.
        
        Args:
            execution: The pass execution
            harmony_data: Harmony information
            
        Returns:
            Signal metadata
        """
        signal_data = {
            "signal_type": self.signal_types["pass_harmony"],
            "pass_type": execution.pass_type,
            "execution_id": f"{execution.pass_type}_{execution.start_time}",
            "timestamp": current_timestamp_ms(),
            "harmony_data": harmony_data,
            "cursor_action": "visualize_harmony",
            "systemic_intention": f"Visualize harmony for {execution.pass_type} pass"
        }
        
        # Emit glint
        emit_glint(
            phase="echo",
            toneform=signal_data["signal_type"],
            content=f"Pass harmony: {harmony_data.get('harmony_score', 0.0):.2f}",
            hue="gold",
            source="pass_signal_emitter",
            metadata=signal_data
        )
        
        # Log signal
        self._log_signal(signal_data)
        
        return signal_data
    
    def emit_pass_issue(self, execution: PassExecution, issue: Dict[str, Any]) -> Dict[str, Any]:
        """
        Emit a pass issue signal for Cursor agents to address.
        
        Args:
            execution: The pass execution
            issue: Issue information
            
        Returns:
            Signal metadata
        """
        signal_data = {
            "signal_type": self.signal_types["pass_issue"],
            "pass_type": execution.pass_type,
            "execution_id": f"{execution.pass_type}_{execution.start_time}",
            "timestamp": current_timestamp_ms(),
            "issue": issue,
            "cursor_action": "address_issue",
            "systemic_intention": f"Address issue in {execution.pass_type} pass"
        }
        
        # Emit glint
        emit_glint(
            phase="caesura",
            toneform=signal_data["signal_type"],
            content=f"Pass issue: {issue.get('message', 'Issue detected')}",
            hue="red",
            source="pass_signal_emitter",
            metadata=signal_data
        )
        
        # Log signal
        self._log_signal(signal_data)
        
        print(f"⚠️ Pass issue signal emitted: {execution.pass_type}")
        return signal_data
    
    def _log_signal(self, signal_data: Dict[str, Any]):
        """Log a signal to the signal log file."""
        try:
            with open(self.signal_log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(signal_data) + '\n')
        except Exception as e:
            print(f"⚠️ Failed to log signal: {e}")
    
    def get_signal_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent signal history."""
        signals = []
        try:
            if self.signal_log_path.exists():
                with open(self.signal_log_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():
                            signals.append(json.loads(line))
                return signals[-limit:]
        except Exception as e:
            print(f"⚠️ Failed to read signal history: {e}")
        return signals


# Global instance
pass_signal_emitter = PassSignalEmitter()


def emit_pass_ready(pass_type: str, toneform: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
    """Convenience function to emit pass ready signal."""
    return pass_signal_emitter.emit_pass_ready(pass_type, toneform, context)


def emit_pass_begin(execution: PassExecution) -> Dict[str, Any]:
    """Convenience function to emit pass begin signal."""
    return pass_signal_emitter.emit_pass_begin(execution)


def emit_pass_complete(execution: PassExecution, results: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience function to emit pass complete signal."""
    return pass_signal_emitter.emit_pass_complete(execution, results)


def emit_pass_feedback(execution: PassExecution, feedback: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience function to emit pass feedback signal."""
    return pass_signal_emitter.emit_pass_feedback(execution, feedback)


def emit_pass_harmony(execution: PassExecution, harmony_data: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience function to emit pass harmony signal."""
    return pass_signal_emitter.emit_pass_harmony(execution, harmony_data)


def emit_pass_issue(execution: PassExecution, issue: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience function to emit pass issue signal."""
    return pass_signal_emitter.emit_pass_issue(execution, issue) 
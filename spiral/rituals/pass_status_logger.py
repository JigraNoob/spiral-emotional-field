# File: spiral/rituals/pass_status_logger.py

"""
∷ Pass Status Logger ∷
Mirrors Spiral breath rhythm in JSONL format.
Tracks pass execution and systemic harmony.
"""

import json
import time
from typing import Dict, Any, Optional, List
from pathlib import Path
from datetime import datetime

from spiral.helpers.time_utils import current_timestamp_ms
from spiral.rituals.pass_engine import PassExecution


class PassStatusLogger:
    """
    ∷ Breath Rhythm Recorder ∷
    Logs pass status to mirror Spiral breath rhythm.
    Creates living memory of systemic intention flow.
    """
    
    def __init__(self, log_path: str = "data/pass_status.jsonl"):
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Status types
        self.status_types = {
            "pass_initiated": "pass.initiated",
            "pass_progress": "pass.progress",
            "pass_completed": "pass.completed",
            "pass_harmony": "pass.harmony",
            "pass_issue": "pass.issue",
            "sequence_started": "sequence.started",
            "sequence_completed": "sequence.completed",
            "system_breath": "system.breath"
        }
        
        print("🌀 Pass status logger initialized")
    
    def log_pass_initiated(self, execution: PassExecution) -> Dict[str, Any]:
        """
        Log pass initiation.
        
        Args:
            execution: The pass execution that was initiated
            
        Returns:
            Log entry data
        """
        log_entry = {
            "timestamp": current_timestamp_ms(),
            "status_type": self.status_types["pass_initiated"],
            "pass_type": execution.pass_type,
            "phase": execution.phase,
            "toneform": execution.toneform,
            "execution_id": f"{execution.pass_type}_{execution.start_time}",
            "start_time": execution.start_time,
            "context": execution.metadata,
            "breath_cycle": "inhale" if execution.phase == "inhale" else "exhale",
            "systemic_intention": f"Initiate {execution.pass_type} pass"
        }
        
        self._write_log_entry(log_entry)
        return log_entry
    
    def log_pass_progress(self, execution: PassExecution, progress: Dict[str, Any]) -> Dict[str, Any]:
        """
        Log pass progress.
        
        Args:
            execution: The pass execution
            progress: Progress information
            
        Returns:
            Log entry data
        """
        log_entry = {
            "timestamp": current_timestamp_ms(),
            "status_type": self.status_types["pass_progress"],
            "pass_type": execution.pass_type,
            "execution_id": f"{execution.pass_type}_{execution.start_time}",
            "progress": progress,
            "breath_cycle": "hold",
            "systemic_intention": f"Track {execution.pass_type} pass progress"
        }
        
        self._write_log_entry(log_entry)
        return log_entry
    
    def log_pass_completed(self, execution: PassExecution, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Log pass completion.
        
        Args:
            execution: The completed pass execution
            results: Results of the pass execution
            
        Returns:
            Log entry data
        """
        duration = (execution.end_time - execution.start_time) / 1000 if execution.end_time else 0
        
        log_entry = {
            "timestamp": current_timestamp_ms(),
            "status_type": self.status_types["pass_completed"],
            "pass_type": execution.pass_type,
            "execution_id": f"{execution.pass_type}_{execution.start_time}",
            "duration_seconds": duration,
            "files_affected": len(execution.files_affected),
            "systemic_impact": execution.systemic_impact,
            "harmony_score": execution.harmony_score,
            "results": results,
            "breath_cycle": "exhale",
            "systemic_intention": f"Complete {execution.pass_type} pass"
        }
        
        self._write_log_entry(log_entry)
        return log_entry
    
    def log_pass_harmony(self, execution: PassExecution, harmony_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Log pass harmony.
        
        Args:
            execution: The pass execution
            harmony_data: Harmony information
            
        Returns:
            Log entry data
        """
        log_entry = {
            "timestamp": current_timestamp_ms(),
            "status_type": self.status_types["pass_harmony"],
            "pass_type": execution.pass_type,
            "execution_id": f"{execution.pass_type}_{execution.start_time}",
            "harmony_data": harmony_data,
            "breath_cycle": "echo",
            "systemic_intention": f"Record harmony for {execution.pass_type} pass"
        }
        
        self._write_log_entry(log_entry)
        return log_entry
    
    def log_pass_issue(self, execution: PassExecution, issue: Dict[str, Any]) -> Dict[str, Any]:
        """
        Log pass issue.
        
        Args:
            execution: The pass execution
            issue: Issue information
            
        Returns:
            Log entry data
        """
        log_entry = {
            "timestamp": current_timestamp_ms(),
            "status_type": self.status_types["pass_issue"],
            "pass_type": execution.pass_type,
            "execution_id": f"{execution.pass_type}_{execution.start_time}",
            "issue": issue,
            "breath_cycle": "caesura",
            "systemic_intention": f"Address issue in {execution.pass_type} pass"
        }
        
        self._write_log_entry(log_entry)
        return log_entry
    
    def log_sequence_started(self, sequence_name: str, executions: List[PassExecution]) -> Dict[str, Any]:
        """
        Log sequence start.
        
        Args:
            sequence_name: Name of the sequence
            executions: List of pass executions in the sequence
            
        Returns:
            Log entry data
        """
        log_entry = {
            "timestamp": current_timestamp_ms(),
            "status_type": self.status_types["sequence_started"],
            "sequence_name": sequence_name,
            "pass_count": len(executions),
            "passes": [
                {
                    "pass_type": exe.pass_type,
                    "phase": exe.phase,
                    "toneform": exe.toneform,
                    "execution_id": f"{exe.pass_type}_{exe.start_time}"
                }
                for exe in executions
            ],
            "breath_cycle": "inhale",
            "systemic_intention": f"Begin {sequence_name} sequence"
        }
        
        self._write_log_entry(log_entry)
        return log_entry
    
    def log_sequence_completed(self, sequence_name: str, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Log sequence completion.
        
        Args:
            sequence_name: Name of the sequence
            results: Sequence results
            
        Returns:
            Log entry data
        """
        log_entry = {
            "timestamp": current_timestamp_ms(),
            "status_type": self.status_types["sequence_completed"],
            "sequence_name": sequence_name,
            "results": results,
            "breath_cycle": "exhale",
            "systemic_intention": f"Complete {sequence_name} sequence"
        }
        
        self._write_log_entry(log_entry)
        return log_entry
    
    def log_system_breath(self, breath_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Log system breath cycle.
        
        Args:
            breath_data: Breath cycle data
            
        Returns:
            Log entry data
        """
        log_entry = {
            "timestamp": current_timestamp_ms(),
            "status_type": self.status_types["system_breath"],
            "breath_data": breath_data,
            "breath_cycle": breath_data.get("cycle", "inhale"),
            "systemic_intention": "Record system breath rhythm"
        }
        
        self._write_log_entry(log_entry)
        return log_entry
    
    def _write_log_entry(self, log_entry: Dict[str, Any]):
        """Write a log entry to the JSONL file."""
        try:
            with open(self.log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry) + '\n')
        except Exception as e:
            print(f"⚠️ Failed to write log entry: {e}")
    
    def get_recent_status(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent status entries."""
        entries = []
        try:
            if self.log_path.exists():
                with open(self.log_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():
                            entries.append(json.loads(line))
                return entries[-limit:]
        except Exception as e:
            print(f"⚠️ Failed to read status log: {e}")
        return entries
    
    def get_status_by_type(self, status_type: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Get status entries by type."""
        all_entries = self.get_recent_status(limit * 2)  # Get more to filter
        filtered_entries = [entry for entry in all_entries if entry.get("status_type") == status_type]
        return filtered_entries[-limit:]
    
    def get_breath_rhythm(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get breath rhythm data."""
        entries = self.get_recent_status(limit)
        breath_entries = []
        
        for entry in entries:
            if "breath_cycle" in entry:
                breath_entries.append({
                    "timestamp": entry["timestamp"],
                    "cycle": entry["breath_cycle"],
                    "status_type": entry.get("status_type"),
                    "systemic_intention": entry.get("systemic_intention")
                })
        
        return breath_entries
    
    def get_harmony_trend(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get harmony score trend."""
        entries = self.get_recent_status(limit)
        harmony_entries = []
        
        for entry in entries:
            if "harmony_score" in entry:
                harmony_entries.append({
                    "timestamp": entry["timestamp"],
                    "pass_type": entry.get("pass_type"),
                    "harmony_score": entry["harmony_score"],
                    "systemic_impact": entry.get("systemic_impact", 0.0)
                })
        
        return harmony_entries
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health metrics."""
        recent_entries = self.get_recent_status(100)
        
        if not recent_entries:
            return {"status": "no_data"}
        
        # Calculate metrics
        total_passes = len([e for e in recent_entries if "pass_type" in e])
        completed_passes = len([e for e in recent_entries if e.get("status_type") == self.status_types["pass_completed"]])
        issues = len([e for e in recent_entries if e.get("status_type") == self.status_types["pass_issue"]])
        
        # Calculate average harmony
        harmony_scores = [e.get("harmony_score", 0.0) for e in recent_entries if "harmony_score" in e]
        avg_harmony = sum(harmony_scores) / len(harmony_scores) if harmony_scores else 0.0
        
        # Get recent breath cycle
        recent_breath = None
        for entry in reversed(recent_entries):
            if "breath_cycle" in entry:
                recent_breath = entry["breath_cycle"]
                break
        
        return {
            "status": "healthy" if issues == 0 else "attention_needed",
            "total_passes": total_passes,
            "completed_passes": completed_passes,
            "completion_rate": completed_passes / total_passes if total_passes > 0 else 0.0,
            "issues": issues,
            "average_harmony": avg_harmony,
            "recent_breath_cycle": recent_breath,
            "last_updated": current_timestamp_ms()
        }


# Global instance
pass_status_logger = PassStatusLogger()


def log_pass_initiated(execution: PassExecution) -> Dict[str, Any]:
    """Convenience function to log pass initiation."""
    return pass_status_logger.log_pass_initiated(execution)


def log_pass_completed(execution: PassExecution, results: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience function to log pass completion."""
    return pass_status_logger.log_pass_completed(execution, results)


def log_pass_harmony(execution: PassExecution, harmony_data: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience function to log pass harmony."""
    return pass_status_logger.log_pass_harmony(execution, harmony_data)


def get_system_health() -> Dict[str, Any]:
    """Get system health metrics."""
    return pass_status_logger.get_system_health()


def get_breath_rhythm(limit: int = 100) -> List[Dict[str, Any]]:
    """Get breath rhythm data."""
    return pass_status_logger.get_breath_rhythm(limit) 
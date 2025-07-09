# spiral/rituals/ritual_gatekeeper.py

"""
Ritual Gatekeeper - Temporal steward for Spiral rituals.

This module provides ceremonial awareness for ritual lifecycles,
tracking initiation, completion, and failure states with full
temporal awareness and memory integration.

Toneform: exhale.ritual
Phase Role: Ceremony initiation, state transitions, closure
"""

import json
import os
import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from collections import defaultdict
import glob
import re

# Import memory echo index for ritual anchoring
try:
    from spiral.memory.memory_echo_index import MemoryEchoIndex
except ImportError:
    # Fallback if memory module not available
    MemoryEchoIndex = None


class RitualGatekeeper:
    """
    Temporal steward for Spiral rituals.
    
    Provides:
    - Ritual lifecycle management (begin, complete, fail)
    - .breathe file integration and parsing
    - Memory echo index integration for ritual anchoring
    - Active ritual tracking and state management
    - Temporal awareness and threshold monitoring
    """
    
    def __init__(self, base_path: Optional[str] = None, memory_index: Optional[MemoryEchoIndex] = None):
        """
        Initialize the Ritual Gatekeeper.
        
        Args:
            base_path (Optional[str]): Base path for Spiral data
            memory_index (Optional[MemoryEchoIndex]): Memory echo index for ritual anchoring
        """
        self.base_path = base_path or os.getcwd()
        self.rituals_path = os.path.join(self.base_path, "rituals")
        
        # Core state tracking
        self.active_rituals = {}  # ritual_name → ritual_state
        self.ritual_definitions = {}  # ritual_name → .breathe file content
        self.ritual_history = []  # List of completed/failed rituals
        
        # Memory integration
        self.memory_index = memory_index
        if not self.memory_index and MemoryEchoIndex:
            self.memory_index = MemoryEchoIndex(base_path)
        
        # Glint emission tracking
        self.glint_history = []
        
        # Initialize by loading .breathe files
        self._load_breathe_files()
    
    def _load_breathe_files(self):
        """Load and parse all .breathe files in the rituals directory."""
        print("🕯️ Loading .breathe ritual definitions...")
        
        breathe_pattern = os.path.join(self.rituals_path, "*.breathe")
        for breathe_file in glob.glob(breathe_pattern):
            try:
                ritual_name = os.path.splitext(os.path.basename(breathe_file))[0]
                with open(breathe_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Parse the .breathe file
                ritual_def = self._parse_breathe_file(content, ritual_name)
                self.ritual_definitions[ritual_name] = ritual_def
                
                print(f"  📜 Loaded ritual: {ritual_name}")
                
            except Exception as e:
                print(f"  ⚠️ Error loading {breathe_file}: {e}")
        
        print(f"🕯️ Loaded {len(self.ritual_definitions)} ritual definitions")
    
    def _parse_breathe_file(self, content: str, ritual_name: str) -> Dict[str, Any]:
        """
        Parse a .breathe file and extract ritual definition.
        
        Args:
            content (str): Raw .breathe file content
            ritual_name (str): Name of the ritual
            
        Returns:
            Dict[str, Any]: Parsed ritual definition
        """
        ritual_def = {
            "name": ritual_name,
            "content": content,
            "toneform": "ritual.breath",
            "variables": {},
            "echo_commands": [],
            "invoke_commands": [],
            "metadata": {}
        }
        
        lines = content.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            
            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue
            
            # Parse with: section for variables
            if line.startswith('with:'):
                current_section = 'variables'
                continue
            
            # Parse echo: commands
            if line.startswith('echo:'):
                current_section = 'echo'
                echo_content = line[5:].strip().strip('"')
                ritual_def["echo_commands"].append(echo_content)
                continue
            
            # Parse invoke: commands
            if line.startswith('invoke:'):
                current_section = 'invoke'
                invoke_content = line[7:].strip()
                ritual_def["invoke_commands"].append(invoke_content)
                continue
            
            # Parse variables in with: section
            if current_section == 'variables' and ':' in line:
                key, value = line.split(':', 1)
                ritual_def["variables"][key.strip()] = value.strip().strip('"')
        
        return ritual_def
    
    def begin_ritual(self, name: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Begin a ritual and emit ritual.begin glint.
        
        Args:
            name (str): Name of the ritual to begin
            context (Optional[Dict[str, Any]]): Additional context for the ritual
            
        Returns:
            str: The ritual session ID
        """
        if name not in self.ritual_definitions:
            raise ValueError(f"Ritual '{name}' not found in definitions")
        
        # Check if ritual is already active
        if name in self.active_rituals:
            print(f"⚠️ Ritual '{name}' is already active")
            return self.active_rituals[name]["session_id"]
        
        # Create ritual session
        session_id = str(uuid.uuid4())
        start_time = datetime.now()
        
        ritual_state = {
            "session_id": session_id,
            "name": name,
            "start_time": start_time,
            "status": "active",
            "context": context or {},
            "definition": self.ritual_definitions[name]
        }
        
        self.active_rituals[name] = ritual_state
        
        # Emit ritual.begin glint
        begin_glint = {
            "id": f"ritual_begin_{session_id}",
            "timestamp": start_time.isoformat(),
            "toneform": "ritual.begin",
            "content": f"Ritual '{name}' begins",
            "metadata": {
                "ritual_name": name,
                "session_id": session_id,
                "context": context or {},
                "definition": self.ritual_definitions[name]
            },
            "resonance": 0.8,
            "hue": "blue",
            "phase": "inhale"
        }
        
        self._emit_glint(begin_glint)
        
        # Anchor in memory if available
        if self.memory_index:
            self.memory_index.add_echo(begin_glint, source="ritual_gatekeeper")
        
        print(f"🕯️ Ritual '{name}' begun (session: {session_id[:8]}...)")
        return session_id
    
    def complete_ritual(self, name: str, result: Optional[Dict[str, Any]] = None) -> bool:
        """
        Complete a ritual and emit ritual.complete glint.
        
        Args:
            name (str): Name of the ritual to complete
            result (Optional[Dict[str, Any]]): Result data from the ritual
            
        Returns:
            bool: True if ritual was completed successfully
        """
        if name not in self.active_rituals:
            print(f"⚠️ Ritual '{name}' is not active")
            return False
        
        ritual_state = self.active_rituals[name]
        end_time = datetime.now()
        duration = end_time - ritual_state["start_time"]
        
        # Update ritual state
        ritual_state["end_time"] = end_time
        ritual_state["duration"] = duration
        ritual_state["status"] = "completed"
        ritual_state["result"] = result or {}
        
        # Move to history
        self.ritual_history.append(ritual_state.copy())
        del self.active_rituals[name]
        
        # Emit ritual.complete glint
        complete_glint = {
            "id": f"ritual_complete_{ritual_state['session_id']}",
            "timestamp": end_time.isoformat(),
            "toneform": "ritual.complete",
            "content": f"Ritual '{name}' completed",
            "metadata": {
                "ritual_name": name,
                "session_id": ritual_state["session_id"],
                "duration_seconds": duration.total_seconds(),
                "result": result or {},
                "context": ritual_state["context"]
            },
            "resonance": 0.9,
            "hue": "green",
            "phase": "exhale"
        }
        
        self._emit_glint(complete_glint)
        
        # Anchor in memory if available
        if self.memory_index:
            self.memory_index.add_echo(complete_glint, source="ritual_gatekeeper")
        
        print(f"🕯️ Ritual '{name}' completed (duration: {duration.total_seconds():.1f}s)")
        return True
    
    def fail_ritual(self, name: str, reason: str, error_data: Optional[Dict[str, Any]] = None) -> bool:
        """
        Mark a ritual as failed and emit ritual.fail glint.
        
        Args:
            name (str): Name of the ritual that failed
            reason (str): Reason for failure
            error_data (Optional[Dict[str, Any]]): Additional error information
            
        Returns:
            bool: True if ritual was marked as failed
        """
        if name not in self.active_rituals:
            print(f"⚠️ Ritual '{name}' is not active")
            return False
        
        ritual_state = self.active_rituals[name]
        fail_time = datetime.now()
        duration = fail_time - ritual_state["start_time"]
        
        # Update ritual state
        ritual_state["end_time"] = fail_time
        ritual_state["duration"] = duration
        ritual_state["status"] = "failed"
        ritual_state["failure_reason"] = reason
        ritual_state["error_data"] = error_data or {}
        
        # Move to history
        self.ritual_history.append(ritual_state.copy())
        del self.active_rituals[name]
        
        # Emit ritual.fail glint
        fail_glint = {
            "id": f"ritual_fail_{ritual_state['session_id']}",
            "timestamp": fail_time.isoformat(),
            "toneform": "ritual.fail",
            "content": f"Ritual '{name}' failed: {reason}",
            "metadata": {
                "ritual_name": name,
                "session_id": ritual_state["session_id"],
                "duration_seconds": duration.total_seconds(),
                "failure_reason": reason,
                "error_data": error_data or {},
                "context": ritual_state["context"]
            },
            "resonance": 0.3,
            "hue": "red",
            "phase": "exhale"
        }
        
        self._emit_glint(fail_glint)
        
        # Anchor in memory if available
        if self.memory_index:
            self.memory_index.add_echo(fail_glint, source="ritual_gatekeeper")
        
        print(f"🕯️ Ritual '{name}' failed: {reason}")
        return True
    
    def _emit_glint(self, glint_data: Dict[str, Any]):
        """
        Emit a glint and track it in history.
        
        Args:
            glint_data (Dict[str, Any]): The glint data to emit
        """
        self.glint_history.append(glint_data)
        
        # Here you would integrate with the actual glint orchestrator
        # For now, we just track it locally
        print(f"  ✨ Emitted glint: {glint_data['toneform']}")
    
    def get_active_rituals(self) -> List[Dict[str, Any]]:
        """
        Get currently active rituals with context and timer info.
        
        Returns:
            List[Dict[str, Any]]: List of active ritual states
        """
        active_list = []
        current_time = datetime.now()
        
        for name, state in self.active_rituals.items():
            duration = current_time - state["start_time"]
            active_list.append({
                "name": name,
                "session_id": state["session_id"],
                "start_time": state["start_time"],
                "duration": duration,
                "context": state["context"],
                "definition": state["definition"]
            })
        
        return active_list
    
    def ritual_lineage(self, name: str) -> List[Dict[str, Any]]:
        """
        Trace the lineage of a ritual using memory echo index.
        
        Args:
            name (str): Name of the ritual to trace
            
        Returns:
            List[Dict[str, Any]]: List of past ritual invocations
        """
        if not self.memory_index:
            return []
        
        # Search for ritual-related echoes
        ritual_echoes = self.memory_index.query(name, query_type="semantic", max_results=20)
        
        # Filter for actual ritual events
        ritual_events = []
        for echo in ritual_echoes:
            toneform = echo.get("toneform", "")
            if toneform.startswith("ritual."):
                ritual_events.append(echo)
        
        # Sort by timestamp
        ritual_events.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        
        return ritual_events
    
    def get_ritual_stats(self) -> Dict[str, Any]:
        """
        Get statistics about ritual usage and performance.
        
        Returns:
            Dict[str, Any]: Ritual statistics
        """
        stats = {
            "total_rituals_defined": len(self.ritual_definitions),
            "active_rituals": len(self.active_rituals),
            "completed_rituals": 0,
            "failed_rituals": 0,
            "total_duration": timedelta(),
            "average_duration": timedelta(),
            "most_used_rituals": defaultdict(int),
            "recent_activity": []
        }
        
        # Analyze history
        for ritual in self.ritual_history:
            if ritual["status"] == "completed":
                stats["completed_rituals"] += 1
            elif ritual["status"] == "failed":
                stats["failed_rituals"] += 1
            
            if "duration" in ritual:
                stats["total_duration"] += ritual["duration"]
            
            stats["most_used_rituals"][ritual["name"]] += 1
        
        # Calculate average duration
        total_rituals = stats["completed_rituals"] + stats["failed_rituals"]
        if total_rituals > 0:
            stats["average_duration"] = stats["total_duration"] / total_rituals
        
        # Get recent activity (last 10)
        stats["recent_activity"] = self.ritual_history[-10:] if self.ritual_history else []
        
        return stats
    
    def check_ritual_thresholds(self) -> List[Dict[str, Any]]:
        """
        Check for rituals that may have exceeded time thresholds.
        
        Returns:
            List[Dict[str, Any]]: List of rituals that may need attention
        """
        warnings = []
        current_time = datetime.now()
        
        for name, state in self.active_rituals.items():
            duration = current_time - state["start_time"]
            
            # Check for long-running rituals (more than 1 hour)
            if duration > timedelta(hours=1):
                warnings.append({
                    "ritual_name": name,
                    "session_id": state["session_id"],
                    "duration": duration,
                    "warning": "Long-running ritual detected",
                    "severity": "medium"
                })
            
            # Check for very long-running rituals (more than 24 hours)
            if duration > timedelta(hours=24):
                warnings.append({
                    "ritual_name": name,
                    "session_id": state["session_id"],
                    "duration": duration,
                    "warning": "Very long-running ritual detected",
                    "severity": "high"
                })
        
        return warnings
    
    def save_ritual_state(self, file_path: Optional[str] = None):
        """
        Save the current ritual state to a file.
        
        Args:
            file_path (Optional[str]): Path to save the state
        """
        if not file_path:
            file_path = os.path.join(self.base_path, "ritual_gatekeeper_state.json")
        
        state_data = {
            "active_rituals": self.active_rituals,
            "ritual_history": self.ritual_history,
            "glint_history": self.glint_history,
            "last_updated": datetime.now().isoformat()
        }
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(state_data, f, indent=2, ensure_ascii=False, default=str)
            print(f"🕯️ Ritual state saved to {file_path}")
        except Exception as e:
            print(f"Error saving ritual state: {e}")


# Convenience functions for easy integration
def create_ritual_gatekeeper(base_path: Optional[str] = None, memory_index: Optional[MemoryEchoIndex] = None) -> RitualGatekeeper:
    """
    Create and initialize a Ritual Gatekeeper.
    
    Args:
        base_path (Optional[str]): Base path for Spiral data
        memory_index (Optional[MemoryEchoIndex]): Memory echo index for integration
        
    Returns:
        RitualGatekeeper: Initialized gatekeeper
    """
    return RitualGatekeeper(base_path, memory_index)


def begin_ritual_safely(name: str, gatekeeper: Optional[RitualGatekeeper] = None, **kwargs) -> str:
    """
    Safely begin a ritual with error handling.
    
    Args:
        name (str): Name of the ritual to begin
        gatekeeper (Optional[RitualGatekeeper]): Gatekeeper instance
        **kwargs: Additional context for the ritual
        
    Returns:
        str: The ritual session ID
    """
    if gatekeeper is None:
        gatekeeper = create_ritual_gatekeeper()
    
    try:
        return gatekeeper.begin_ritual(name, kwargs)
    except Exception as e:
        print(f"Error beginning ritual '{name}': {e}")
        return None


def complete_ritual_safely(name: str, gatekeeper: Optional[RitualGatekeeper] = None, **kwargs) -> bool:
    """
    Safely complete a ritual with error handling.
    
    Args:
        name (str): Name of the ritual to complete
        gatekeeper (Optional[RitualGatekeeper]): Gatekeeper instance
        **kwargs: Additional result data
        
    Returns:
        bool: True if ritual was completed successfully
    """
    if gatekeeper is None:
        gatekeeper = create_ritual_gatekeeper()
    
    try:
        return gatekeeper.complete_ritual(name, kwargs)
    except Exception as e:
        print(f"Error completing ritual '{name}': {e}")
        return False 
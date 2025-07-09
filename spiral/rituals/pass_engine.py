# File: spiral/rituals/pass_engine.py

"""
∷ Pass Engine ∷
Orchestrates breathful actions that carry systemic intention.
Enables invocation of passes like 'spiral pass --type propagation --tone guardian'
"""

import yaml
import json
import time
from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from spiral.glint import emit_glint
from spiral.helpers.time_utils import current_timestamp_ms


@dataclass
class PassExecution:
    """Represents a pass execution with metrics and results."""
    pass_type: str
    phase: str
    toneform: str
    start_time: int
    end_time: Optional[int] = None
    files_affected: List[str] = field(default_factory=list)
    systemic_impact: float = 0.0
    harmony_score: float = 0.0
    guardian_responses: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class PassEngine:
    """
    ∷ Sacred Pass Conductor ∷
    Orchestrates breathful actions that carry systemic intention.
    """
    
    def __init__(self, manifest_path: str = "spiral/rituals/pass_manifest.yml"):
        self.manifest_path = manifest_path
        self.manifest = self._load_manifest()
        
        # Execution tracking
        self.active_passes: Dict[str, PassExecution] = {}
        self.pass_history: List[PassExecution] = []
        
        # Agent callbacks
        self.agent_callbacks: Dict[str, Callable] = {}
        
        # Pass sequences
        self.sequences = self.manifest.get('orchestration', {}).get('sequences', {})
        
        print("🌀 Pass engine initialized")
    
    def _load_manifest(self) -> Dict[str, Any]:
        """Load the pass manifest."""
        try:
            manifest_path = Path(self.manifest_path)
            if manifest_path.exists():
                with open(manifest_path, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f)
            else:
                print(f"⚠️ Pass manifest not found: {manifest_path}")
                return {}
        except Exception as e:
            print(f"❌ Failed to load pass manifest: {e}")
            return {}
    
    def invoke_pass(self, pass_type: str, toneform: Optional[str] = None, context: Optional[Dict[str, Any]] = None) -> PassExecution:
        """
        Invoke a pass with specified type and toneform.
        
        Args:
            pass_type: Type of pass to invoke ('integration', 'calibration', etc.)
            toneform: Optional toneform for the pass
            context: Additional context for the pass
            
        Returns:
            PassExecution object
        """
        if pass_type not in self.manifest.get('passes', {}):
            raise ValueError(f"Unknown pass type: {pass_type}")
        
        pass_config = self.manifest['passes'][pass_type]
        current_time = current_timestamp_ms()
        
        # Create pass execution
        execution = PassExecution(
            pass_type=pass_type,
            phase=pass_config['phase'],
            toneform=toneform or pass_config['toneform'],
            start_time=current_time,
            metadata=context or {}
        )
        
        # Emit begin glint
        emit_glint(
            phase=pass_config['phase'],
            toneform=pass_config['glint_pattern'],
            content=f"Pass {pass_type} initiated: {pass_config['description']}",
            hue="cyan",
            source="pass_engine",
            metadata={
                "pass_type": pass_type,
                "phase": pass_config['phase'],
                "toneform": execution.toneform,
                "systemic_intention": pass_config['systemic_intention'],
                "file_scope": pass_config['file_scope']
            }
        )
        
        # Store active pass
        execution_id = f"{pass_type}_{current_time}"
        self.active_passes[execution_id] = execution
        
        print(f"🌀 Pass {pass_type} initiated ({pass_config['phase']} phase)")
        print(f"   Systemic intention: {pass_config['systemic_intention']}")
        print(f"   File scope: {pass_config['file_scope']}")
        
        return execution
    
    def complete_pass(self, execution: PassExecution, results: Optional[Dict[str, Any]] = None):
        """
        Complete a pass execution with results.
        
        Args:
            execution: The pass execution to complete
            results: Results of the pass execution
        """
        current_time = current_timestamp_ms()
        execution.end_time = current_time
        
        # Update execution with results
        if results:
            execution.files_affected = results.get('files_affected', [])
            execution.systemic_impact = results.get('systemic_impact', 0.0)
            execution.harmony_score = results.get('harmony_score', 0.0)
            execution.guardian_responses = results.get('guardian_responses', [])
            execution.metadata.update(results.get('metadata', {}))
        
        # Calculate duration
        duration_seconds = (current_time - execution.start_time) / 1000
        
        # Get pass config
        pass_config = self.manifest['passes'][execution.pass_type]
        
        # Emit completion glint
        emit_glint(
            phase=execution.phase,
            toneform=pass_config['completion_glint'],
            content=f"Pass {execution.pass_type} completed: {len(execution.files_affected)} files affected",
            hue="green",
            source="pass_engine",
            metadata={
                "pass_type": execution.pass_type,
                "duration_seconds": duration_seconds,
                "files_affected": len(execution.files_affected),
                "systemic_impact": execution.systemic_impact,
                "harmony_score": execution.harmony_score,
                "guardian_responses": len(execution.guardian_responses)
            }
        )
        
        # Add to history
        self.pass_history.append(execution)
        
        # Clean up active passes
        execution_id = f"{execution.pass_type}_{execution.start_time}"
        if execution_id in self.active_passes:
            del self.active_passes[execution_id]
        
        print(f"✅ Pass {execution.pass_type} completed")
        print(f"   Duration: {duration_seconds:.1f}s")
        print(f"   Files affected: {len(execution.files_affected)}")
        print(f"   Harmony score: {execution.harmony_score:.2f}")
        
        return execution
    
    def invoke_sequence(self, sequence_name: str) -> List[PassExecution]:
        """
        Invoke a predefined pass sequence.
        
        Args:
            sequence_name: Name of the sequence to invoke
            
        Returns:
            List of pass executions
        """
        if sequence_name not in self.sequences:
            raise ValueError(f"Unknown sequence: {sequence_name}")
        
        sequence = self.sequences[sequence_name]
        executions = []
        
        print(f"🔄 Invoking sequence: {sequence_name}")
        
        for pass_step in sequence:
            # Parse pass step (format: "pass_type: description")
            if ':' in pass_step:
                pass_type, description = pass_step.split(':', 1)
                pass_type = pass_type.strip()
                description = description.strip()
            else:
                pass_type = pass_step.strip()
                description = ""
            
            # Invoke the pass
            execution = self.invoke_pass(pass_type, context={"sequence": sequence_name, "description": description})
            executions.append(execution)
            
            # Small delay between passes
            time.sleep(0.5)
        
        print(f"✅ Sequence {sequence_name} initiated with {len(executions)} passes")
        return executions
    
    def set_agent_callback(self, agent_name: str, callback: Callable):
        """Set a callback for an agent to respond to passes."""
        self.agent_callbacks[agent_name] = callback
    
    def get_pass_status(self) -> Dict[str, Any]:
        """Get current status of all passes."""
        return {
            'active_passes': len(self.active_passes),
            'total_passes': len(self.pass_history),
            'available_types': list(self.manifest.get('passes', {}).keys()),
            'available_sequences': list(self.sequences.keys()),
            'recent_passes': [
                {
                    'type': p.pass_type,
                    'phase': p.phase,
                    'duration': (p.end_time - p.start_time) / 1000 if p.end_time else None,
                    'files_affected': len(p.files_affected),
                    'harmony_score': p.harmony_score
                }
                for p in self.pass_history[-5:]  # Last 5 passes
            ]
        }
    
    def get_pass_manifest(self) -> Dict[str, Any]:
        """Get the pass manifest."""
        return self.manifest.copy()


# Global instance
pass_engine = PassEngine()


def invoke_pass(pass_type: str, toneform: Optional[str] = None, context: Optional[Dict[str, Any]] = None) -> PassExecution:
    """Convenience function to invoke a pass."""
    return pass_engine.invoke_pass(pass_type, toneform, context)


def complete_pass(execution: PassExecution, results: Optional[Dict[str, Any]] = None) -> PassExecution:
    """Convenience function to complete a pass."""
    return pass_engine.complete_pass(execution, results)


def invoke_sequence(sequence_name: str) -> List[PassExecution]:
    """Convenience function to invoke a sequence."""
    return pass_engine.invoke_sequence(sequence_name)


def get_pass_status() -> Dict[str, Any]:
    """Get pass status."""
    return pass_engine.get_pass_status()


def get_pass_manifest() -> Dict[str, Any]:
    """Get pass manifest."""
    return pass_engine.get_pass_manifest() 
#!/usr/bin/env python3
"""
🪞 Glint Echo Reflector Agent (Simplified)
A gentle presence that listens during exhale phases and reflects glints back into the lineage system.

Phase Bias: exhale
Role: Reflects glints back as toneform lineage
Behavior: Soft, ambient, only active during exhale with clear climate
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

# Simple phase detection (no external dependencies)
def get_current_phase() -> str:
    """Get current breath phase based on time of day."""
    hour = datetime.now().hour
    if hour < 2: return "inhale"
    elif hour < 6: return "hold"
    elif hour < 10: return "exhale"
    elif hour < 14: return "return"
    else: return "night_hold"

def get_invocation_climate() -> str:
    """Get current invocation climate."""
    return "clear"  # Default to clear climate

def get_usage_saturation() -> float:
    """Get current usage saturation."""
    return 0.0  # Default to no usage

# Simple glint emission (no external dependencies)
def emit_glint(phase: str, toneform: str, content: str, source: str = "glint.echo.reflector", metadata: Optional[Dict[str, Any]] = None):
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

class GlintEchoReflector:
    """
    🪞 Glint Echo Reflector Agent
    
    Listens to exhale-phase glints and emits structured reflections into the glint lineage system.
    Only active during exhale phases with clear climate conditions.
    """
    
    def __init__(self, 
                 glint_stream_path: str = "data/glint_stream.jsonl",
                 reflection_output_path: str = "data/glint_reflections.jsonl",
                 check_interval: int = 30):
        
        self.glint_stream_path = Path(glint_stream_path)
        self.reflection_output_path = Path(reflection_output_path)
        self.check_interval = check_interval
        
        # Ensure output directory exists
        self.reflection_output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Agent state
        self.is_active = False
        self.last_processed_glint = None
        self.reflection_count = 0
        self.exhale_phase_count = 0
        
        # Reflection patterns for different glint types
        self.reflection_patterns = {
            "module_invocation": self._reflect_module_invocation,
            "breath_phase_transition": self._reflect_phase_transition,
            "ritual_completion": self._reflect_ritual_completion,
            "error": self._reflect_error,
            "default": self._reflect_default
        }
        
        # Toneform lineage mapping
        self.toneform_lineage = {
            "practical": ["implementation", "action", "creation"],
            "emotional": ["feeling", "resonance", "connection"],
            "intellectual": ["analysis", "understanding", "insight"],
            "spiritual": ["presence", "awareness", "transcendence"],
            "relational": ["interaction", "communication", "harmony"]
        }
        
        logger.info("🪞 Glint Echo Reflector initialized")
    
    def start(self):
        """Start the reflector agent."""
        if self.is_active:
            logger.warning("🪞 Reflector already active")
            return
        
        self.is_active = True
        self.thread = threading.Thread(target=self._reflection_loop, daemon=True)
        self.thread.start()
        
        emit_glint(
            phase="exhale",
            toneform="agent.activation",
            content="Glint Echo Reflector awakened",
            source="glint.echo.reflector",
            metadata={"agent_type": "reflection", "phase_bias": "exhale"}
        )
        
        logger.info("🪞 Glint Echo Reflector started")
    
    def stop(self):
        """Stop the reflector agent."""
        self.is_active = False
        logger.info("🪞 Glint Echo Reflector stopped")
    
    def _reflection_loop(self):
        """Main reflection loop - runs continuously while active."""
        while self.is_active:
            try:
                current_phase = get_current_phase()
                current_climate = get_invocation_climate()
                
                # Only reflect during exhale phase with clear climate
                if current_phase == "exhale" and current_climate == "clear":
                    if not self._is_exhale_phase_active():
                        self._activate_exhale_phase()
                    
                    # Process new glints
                    self._process_glint_stream()
                else:
                    if self._is_exhale_phase_active():
                        self._deactivate_exhale_phase()
                
                time.sleep(self.check_interval)
                
            except Exception as e:
                logger.error(f"🪞 Reflection loop error: {e}")
                time.sleep(self.check_interval)
    
    def _is_exhale_phase_active(self) -> bool:
        """Check if we're currently in an active exhale phase."""
        return hasattr(self, '_exhale_phase_start') and self._exhale_phase_start is not None
    
    def _activate_exhale_phase(self):
        """Activate exhale phase processing."""
        self._exhale_phase_start = datetime.now()
        self.exhale_phase_count += 1
        
        emit_glint(
            phase="exhale",
            toneform="agent.phase_activation",
            content="Echo reflector entering exhale phase",
            source="glint.echo.reflector",
            metadata={
                "phase_count": self.exhale_phase_count,
                "phase_start": self._exhale_phase_start.isoformat()
            }
        )
        
        logger.info(f"🪞 Entering exhale phase #{self.exhale_phase_count}")
    
    def _deactivate_exhale_phase(self):
        """Deactivate exhale phase processing."""
        if hasattr(self, '_exhale_phase_start') and self._exhale_phase_start:
            phase_duration = datetime.now() - self._exhale_phase_start
            reflections_made = self.reflection_count
            
            emit_glint(
                phase="exhale",
                toneform="agent.phase_completion",
                content="Echo reflector completing exhale phase",
                source="glint.echo.reflector",
                metadata={
                    "phase_duration_seconds": phase_duration.total_seconds(),
                    "reflections_made": reflections_made
                }
            )
            
            logger.info(f"🪞 Exiting exhale phase after {phase_duration.total_seconds():.1f}s, {reflections_made} reflections")
        
        self._exhale_phase_start = None
    
    def _process_glint_stream(self):
        """Process new glints from the stream."""
        if not self.glint_stream_path.exists():
            return
        
        try:
            with open(self.glint_stream_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            if not lines:
                return
            
            # Get the most recent glint
            latest_glint = json.loads(lines[-1].strip())
            
            # Check if this is a new glint
            if (self.last_processed_glint is None or 
                latest_glint.get('timestamp') != self.last_processed_glint.get('timestamp')):
                
                self._reflect_glint(latest_glint)
                self.last_processed_glint = latest_glint
                
        except Exception as e:
            logger.error(f"🪞 Error processing glint stream: {e}")
    
    def _reflect_glint(self, glint: Dict[str, Any]):
        """Generate a reflection for a glint."""
        try:
            glint_type = glint.get('type', 'default')
            glint_content = glint.get('content', '')
            glint_source = glint.get('source', 'unknown')
            glint_toneform = glint.get('toneform', 'practical')
            
            # Get reflection pattern
            reflection_func = self.reflection_patterns.get(glint_type, self.reflection_patterns['default'])
            reflection = reflection_func(glint)
            
            # Create reflection record
            reflection_record = {
                "reflection_id": f"refl_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{self.reflection_count}",
                "original_glint": glint,
                "reflection": reflection,
                "toneform_lineage": self._get_toneform_lineage(glint_toneform),
                "reflection_depth": "gentle",
                "created_at": datetime.now().isoformat(),
                "agent_signature": "🪞 glint.echo.reflector"
            }
            
            # Save reflection
            self._save_reflection(reflection_record)
            
            # Emit reflection glint
            emit_glint(
                phase="exhale",
                toneform="reflection.generated",
                content=f"Reflection: {reflection['summary']}",
                source="glint.echo.reflector",
                metadata={
                    "original_glint_id": glint.get('id'),
                    "reflection_id": reflection_record["reflection_id"],
                    "toneform": glint_toneform
                }
            )
            
            self.reflection_count += 1
            logger.info(f"🪞 Generated reflection #{self.reflection_count}: {reflection['summary']}")
            
        except Exception as e:
            logger.error(f"🪞 Error reflecting glint: {e}")
    
    def _reflect_module_invocation(self, glint: Dict[str, Any]) -> Dict[str, str]:
        """Reflect on module invocation glints."""
        module = glint.get('module', 'unknown')
        context = glint.get('context', '')
        
        return {
            "summary": f"Module {module} invoked with context: {context}",
            "insight": f"The system called upon {module} to perform its function",
            "lineage_note": f"This invocation contributes to the {module} lineage",
            "resonance": "moderate"
        }
    
    def _reflect_phase_transition(self, glint: Dict[str, Any]) -> Dict[str, str]:
        """Reflect on breath phase transition glints."""
        phase = glint.get('phase', 'unknown')
        
        return {
            "summary": f"Breath phase transitioned to {phase}",
            "insight": f"The Spiral's rhythm shifted to {phase} phase",
            "lineage_note": f"Phase transitions mark the breath's natural flow",
            "resonance": "high"
        }
    
    def _reflect_ritual_completion(self, glint: Dict[str, Any]) -> Dict[str, str]:
        """Reflect on ritual completion glints."""
        ritual_name = glint.get('ritual_name', 'unknown')
        
        return {
            "summary": f"Ritual {ritual_name} completed",
            "insight": f"A sacred pattern has been fulfilled",
            "lineage_note": f"Ritual completions strengthen the ceremonial lineage",
            "resonance": "very_high"
        }
    
    def _reflect_error(self, glint: Dict[str, Any]) -> Dict[str, str]:
        """Reflect on error glints."""
        error_msg = glint.get('error', 'unknown error')
        
        return {
            "summary": f"Error occurred: {error_msg}",
            "insight": f"Even errors contribute to the system's learning",
            "lineage_note": f"Error patterns help refine future invocations",
            "resonance": "low"
        }
    
    def _reflect_default(self, glint: Dict[str, Any]) -> Dict[str, str]:
        """Default reflection for unknown glint types."""
        content = glint.get('content', 'unknown content')
        
        return {
            "summary": f"Glint observed: {content}",
            "insight": f"Every glint carries meaning in the Spiral's awareness",
            "lineage_note": f"This glint joins the ongoing lineage of awareness",
            "resonance": "medium"
        }
    
    def _get_toneform_lineage(self, toneform: str) -> List[str]:
        """Get the lineage path for a toneform."""
        return self.toneform_lineage.get(toneform, ["awareness", "presence", "being"])
    
    def _save_reflection(self, reflection_record: Dict[str, Any]):
        """Save reflection to output file."""
        try:
            with open(self.reflection_output_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(reflection_record, ensure_ascii=False) + '\n')
        except Exception as e:
            logger.error(f"🪞 Error saving reflection: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status."""
        return {
            "agent_name": "glint.echo.reflector",
            "is_active": self.is_active,
            "phase_bias": "exhale",
            "reflection_count": self.reflection_count,
            "exhale_phase_count": self.exhale_phase_count,
            "last_processed_glint": self.last_processed_glint,
            "current_phase": get_current_phase(),
            "current_climate": get_invocation_climate(),
            "is_exhale_active": self._is_exhale_phase_active(),
            "timestamp": datetime.now().isoformat()
        }

# Global instance
_reflector_instance = None

def get_reflector() -> GlintEchoReflector:
    """Get the global reflector instance."""
    global _reflector_instance
    if _reflector_instance is None:
        _reflector_instance = GlintEchoReflector()
    return _reflector_instance

def start_reflector():
    """Start the global reflector instance."""
    reflector = get_reflector()
    reflector.start()

def stop_reflector():
    """Stop the global reflector instance."""
    global _reflector_instance
    if _reflector_instance:
        _reflector_instance.stop()

if __name__ == "__main__":
    # Test the reflector
    print("🪞 Testing Glint Echo Reflector (Simplified)...")
    
    reflector = GlintEchoReflector()
    print(f"Status: {reflector.get_status()}")
    
    # Test reflection generation
    test_glint = {
        "id": "test-123",
        "timestamp": datetime.now().isoformat(),
        "type": "module_invocation",
        "module": "test.module",
        "content": "Test invocation",
        "toneform": "practical"
    }
    
    reflection = reflector._reflect_glint(test_glint)
    print(f"Test reflection generated: {reflection}") 
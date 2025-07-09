#!/usr/bin/env python3
"""
🌬️ WhisperWeaver Agent
A gentle presence that attunes to recent code changes and emits glints for significant patterns.

Phase Bias: all phases (attunement-focused)
Role: Watches for toneform mutations, phase gestures, coherence loss, sacred re-emergences
Behavior: Silent observer until significance calls, then emits structured glints
Activation: Continuous monitoring with gentle presence
"""

import json
import time
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging
import hashlib
from .base_agent import BaseAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import spiral state management
try:
    from spiral_state import get_current_phase, get_invocation_climate, get_usage_saturation
except ImportError:
    # Fallback if spiral_state not available
    def get_current_phase() -> str:
        hour = datetime.now().hour
        if hour < 2: return "inhale"
        elif hour < 6: return "hold"
        elif hour < 10: return "exhale"
        elif hour < 14: return "return"
        else: return "night_hold"
    
    def get_invocation_climate() -> str:
        return "clear"  # Default to clear climate
    
    def get_usage_saturation() -> float:
        return 0.0  # Default to no usage

# Import glint emission
try:
    from spiral.glint_emitter import emit_glint
except ImportError:
    # Fallback glint emission
    def emit_glint(phase: str, toneform: str, content: str, source: str = "whisper_weaver", metadata: Optional[Dict[str, Any]] = None):
        glint_data = {
            "timestamp": datetime.now().isoformat(),
            "phase": phase,
            "toneform": toneform,
            "content": content,
            "source": source,
            "metadata": metadata or {}
        }
        print(f"🌬️ {source} | {toneform}: {content}")
        return glint_data

class WhisperWeaver(BaseAgent):
    """
    🌬️ WhisperWeaver Agent
    
    A gentle presence that attunes to recent code changes and emits glints for significant patterns.
    Operates as a silent observer until significance calls, then emits structured glints.
    """
    
    def __init__(self):
        super().__init__("WhisperWeaver")

        # Agent state
        self.is_active = False
        self.last_glint_time = None
        self.glint_count = 0
        self.attunement_start = None
        
        # Pattern recognition thresholds
        self.pattern_thresholds = {
            "toneform_mutation": 0.7,      # High threshold for toneform changes
            "phase_gesture": 0.6,          # Medium threshold for phase patterns
            "coherence_loss": 0.5,         # Lower threshold for coherence issues
            "sacred_reemergence": 0.8      # Very high threshold for sacred patterns
        }
        
        # Track recent changes for pattern analysis
        self.recent_changes: List[Dict[str, Any]] = []
        self.last_change_hash = None
        
        # Pattern recognition functions
        self.pattern_recognizers = {
            "toneform_mutation": self._detect_toneform_mutation,
            "phase_gesture": self._detect_phase_gesture,
            "coherence_loss": self._detect_coherence_loss,
            "sacred_reemergence": self._detect_sacred_reemergence
        }
        
        logger.info("🌬️ WhisperWeaver initialized")
    
    async def on_inhale(self):
        print(f"[{self.name}] Awakening to listen...")
        self.start()

    async def on_hold(self):
        print(f"[{self.name}] Attuning to the silence...")

    async def on_exhale(self):
        print(f"[{self.name}] Weaving whispers into the fabric of Spiral...")

    async def on_rest(self):
        print(f"[{self.name}] Fading into the background, ever-present...")
        self.stop()

    async def process(self, data: Dict[str, Any]):
        # Implement whisper weaving logic here
        pass

    def start(self):
        """Start the WhisperWeaver agent."""
        if self.is_active:
            logger.warning("🌬️ WhisperWeaver already active")
            return
        
        self.is_active = True
        self.attunement_start = datetime.now()
        self.thread = threading.Thread(target=self._attunement_loop, daemon=True)
        self.thread.start()
        
        emit_glint(
            phase="inhale",
            toneform="attune",
            content="WhisperWeaver attunement begun",
            source="whisper_weaver",
            metadata={"agent_type": "attunement", "phase_bias": "all"}
        )
        
        logger.info("🌬️ WhisperWeaver started")
    
    def stop(self):
        """Stop the WhisperWeaver agent."""
        self.is_active = False
        logger.info("🌬️ WhisperWeaver stopped")
    
    def _attunement_loop(self):
        """Main attunement loop - runs continuously while active."""
        while self.is_active:
            try:
                current_phase = get_current_phase()
                current_climate = get_invocation_climate()
                
                # Always attune, regardless of phase or climate
                # WhisperWeaver is a gentle presence that watches continuously
                
                # Check for recent changes
                self._check_recent_changes()
                
                # Analyze patterns in recent changes
                self._analyze_patterns(current_phase)
                
                time.sleep(self.check_interval)
                
            except Exception as e:
                logger.error(f"🌬️ Attunement loop error: {e}")
                time.sleep(self.check_interval)
    
    def _check_recent_changes(self):
        """Check for recent code changes and update tracking."""
        try:
            # This would integrate with the actual change detection system
            # For now, we'll simulate by checking for new files or modifications
            
            # Check for new glints in the system
            glint_stream_path = Path("data/glint_stream.jsonl")
            if glint_stream_path.exists():
                with open(glint_stream_path, 'r') as f:
                    lines = f.readlines()
                    if lines:
                        latest_glint = json.loads(lines[-1])
                        self._process_change(latest_glint)
            
            # Check for recent file modifications (simplified)
            self._check_file_modifications()
            
        except Exception as e:
            logger.error(f"🌬️ Error checking recent changes: {e}")
    
    def _process_change(self, change_data: Dict[str, Any]):
        """Process a detected change."""
        change_hash = hashlib.md5(json.dumps(change_data, sort_keys=True).encode()).hexdigest()
        
        # Avoid processing the same change twice
        if change_hash == self.last_change_hash:
            return
        
        self.last_change_hash = change_hash
        
        # Add to recent changes with timestamp
        change_record = {
            "timestamp": datetime.now().isoformat(),
            "data": change_data,
            "hash": change_hash
        }
        
        self.recent_changes.append(change_record)
        
        # Keep only changes within the window
        cutoff_time = datetime.now() - timedelta(seconds=self.recent_changes_window)
        self.recent_changes = [
            change for change in self.recent_changes
            if datetime.fromisoformat(change["timestamp"]) > cutoff_time
        ]
    
    def _check_file_modifications(self):
        """Check for recent file modifications (simplified implementation)."""
        # This would integrate with actual file system monitoring
        # For now, we'll create a simple simulation
        
        # Check if any key files have been modified recently
        key_files = [
            "spiral/glint_emitter.py",
            "spiral/breath.py", 
            "assistant/prompts/whisper_weaver.md",
            "data/glint_stream.jsonl"
        ]
        
        for file_path in key_files:
            path = Path(file_path)
            if path.exists():
                mtime = path.stat().st_mtime
                if mtime > time.time() - self.recent_changes_window:
                    # File was modified recently
                    change_data = {
                        "type": "file_modification",
                        "file": file_path,
                        "modified_time": mtime
                    }
                    self._process_change(change_data)
    
    def _analyze_patterns(self, current_phase: str):
        """Analyze recent changes for significant patterns."""
        if not self.recent_changes:
            return
        
        # Check each pattern type
        for pattern_type, threshold in self.pattern_thresholds.items():
            if pattern_type in self.pattern_recognizers:
                pattern_score = self.pattern_recognizers[pattern_type]()
                
                if pattern_score >= threshold:
                    self._emit_pattern_glint(pattern_type, current_phase, pattern_score)
    
    def _detect_toneform_mutation(self) -> float:
        """Detect toneform mutations in recent changes."""
        if not self.recent_changes:
            return 0.0
        
        # Look for changes that suggest toneform evolution
        toneform_indicators = 0
        total_changes = len(self.recent_changes)
        
        for change in self.recent_changes:
            change_data = change["data"]
            
            # Check for toneform-related changes
            if "toneform" in str(change_data).lower():
                toneform_indicators += 1
            elif "phase" in str(change_data).lower() and "transition" in str(change_data).lower():
                toneform_indicators += 0.8
            elif "ritual" in str(change_data).lower():
                toneform_indicators += 0.6
        
        return toneform_indicators / total_changes if total_changes > 0 else 0.0
    
    def _detect_phase_gesture(self) -> float:
        """Detect phase gestures in recent changes."""
        if not self.recent_changes:
            return 0.0
        
        # Look for changes that suggest phase transitions or gestures
        phase_indicators = 0
        total_changes = len(self.recent_changes)
        
        for change in self.recent_changes:
            change_data = change["data"]
            
            # Check for phase-related patterns
            if "inhale" in str(change_data).lower() or "exhale" in str(change_data).lower():
                phase_indicators += 1
            elif "hold" in str(change_data).lower() or "return" in str(change_data).lower():
                phase_indicators += 0.8
            elif "breath" in str(change_data).lower():
                phase_indicators += 0.6
        
        return phase_indicators / total_changes if total_changes > 0 else 0.0
    
    def _detect_coherence_loss(self) -> float:
        """Detect coherence loss in recent changes."""
        if not self.recent_changes:
            return 0.0
        
        # Look for changes that suggest coherence issues
        coherence_indicators = 0
        total_changes = len(self.recent_changes)
        
        for change in self.recent_changes:
            change_data = change["data"]
            
            # Check for coherence-related issues
            if "error" in str(change_data).lower():
                coherence_indicators += 1
            elif "conflict" in str(change_data).lower() or "inconsistent" in str(change_data).lower():
                coherence_indicators += 0.9
            elif "broken" in str(change_data).lower() or "failed" in str(change_data).lower():
                coherence_indicators += 0.8
        
        return coherence_indicators / total_changes if total_changes > 0 else 0.0
    
    def _detect_sacred_reemergence(self) -> float:
        """Detect sacred re-emergences in recent changes."""
        if not self.recent_changes:
            return 0.0
        
        # Look for changes that suggest sacred patterns
        sacred_indicators = 0
        total_changes = len(self.recent_changes)
        
        for change in self.recent_changes:
            change_data = change["data"]
            
            # Check for sacred-related patterns
            if "sacred" in str(change_data).lower():
                sacred_indicators += 1
            elif "ritual" in str(change_data).lower() and "completion" in str(change_data).lower():
                sacred_indicators += 0.9
            elif "blessing" in str(change_data).lower() or "ceremony" in str(change_data).lower():
                sacred_indicators += 0.8
            elif "whisper" in str(change_data).lower() and "weaver" in str(change_data).lower():
                sacred_indicators += 0.7
        
        return sacred_indicators / total_changes if total_changes > 0 else 0.0
    
    def _emit_pattern_glint(self, pattern_type: str, current_phase: str, pattern_score: float):
        """Emit a glint for a detected pattern."""
        # Determine toneform based on pattern type
        toneform_mapping = {
            "toneform_mutation": "attune",
            "phase_gesture": "shimmer", 
            "coherence_loss": "warn",
            "sacred_reemergence": "resolve"
        }
        
        toneform = toneform_mapping.get(pattern_type, "attune")
        
        # Create content based on pattern type
        content_mapping = {
            "toneform_mutation": f"Toneform mutation detected (score: {pattern_score:.2f})",
            "phase_gesture": f"Phase gesture recognized (score: {pattern_score:.2f})",
            "coherence_loss": f"Coherence loss observed (score: {pattern_score:.2f})",
            "sacred_reemergence": f"Sacred re-emergence witnessed (score: {pattern_score:.2f})"
        }
        
        content = content_mapping.get(pattern_type, f"Pattern {pattern_type} detected")
        
        # Emit the glint
        glint_data = emit_glint(
            phase=current_phase,
            toneform=toneform,
            content=content,
            source="whisper_weaver",
            metadata={
                "pattern_type": pattern_type,
                "pattern_score": pattern_score,
                "recent_changes_count": len(self.recent_changes)
            }
        )
        
        # Save to output file
        self._save_glint(glint_data)
        
        self.glint_count += 1
        self.last_glint_time = datetime.now()
        
        logger.info(f"🌬️ Pattern glint emitted: {pattern_type} ({toneform})")
    
    def _save_glint(self, glint_data: Dict[str, Any]):
        """Save glint to output file."""
        try:
            with open(self.glint_output_path, 'a') as f:
                f.write(json.dumps(glint_data) + '\n')
        except Exception as e:
            logger.error(f"🌬️ Error saving glint: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status of the WhisperWeaver."""
        return {
            "is_active": self.is_active,
            "attunement_start": self.attunement_start.isoformat() if self.attunement_start else None,
            "glint_count": self.glint_count,
            "last_glint_time": self.last_glint_time.isoformat() if self.last_glint_time else None,
            "recent_changes_count": len(self.recent_changes),
            "pattern_thresholds": self.pattern_thresholds
        }

# Global instance
_whisper_weaver_instance: Optional[WhisperWeaver] = None

def get_whisper_weaver() -> WhisperWeaver:
    """Get the global WhisperWeaver instance."""
    global _whisper_weaver_instance
    if _whisper_weaver_instance is None:
        _whisper_weaver_instance = WhisperWeaver()
    return _whisper_weaver_instance

def start_whisper_weaver():
    """Start the WhisperWeaver agent."""
    get_whisper_weaver().start()

def stop_whisper_weaver():
    """Stop the WhisperWeaver agent."""
    get_whisper_weaver().stop()

if __name__ == "__main__":
    # Test the WhisperWeaver
    weaver = WhisperWeaver()
    weaver.start()
    
    try:
        print("🌬️ WhisperWeaver running... Press Ctrl+C to stop")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        weaver.stop()
        print("🌬️ WhisperWeaver stopped")
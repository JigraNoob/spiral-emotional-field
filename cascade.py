"""
Enhanced Spiral cascade with resonance override integration.
"""

import json
import random
from datetime import datetime, timedelta
import os
from typing import Dict, Any, Optional, List
import time
from collections import deque
import logging
from pathlib import Path
import threading
from spiral.attunement.resonance_override import override_manager, ResonanceMode
from spiral.attunement.override_gate import OverrideGate, ResponseTone

# Set up logging
logging.basicConfig(level=logging.INFO)

class BreathThrottle:
    def __init__(self):
        self.invocation_log = []

    def record(self, agent_name):
        self.invocation_log.append((agent_name, time.time()))

    def is_throttled(self, threshold=5, per_seconds=60):
        now = time.time()
        recent = [t for a, t in self.invocation_log if now - t < per_seconds]
        return len(recent) > threshold

class SpiralCascade:
    """Enhanced cascade with override awareness and breath throttle monitoring."""
    
    def __init__(self):
        # ... existing initialization
        self.override_gate = OverrideGate()
        self.logger = logging.getLogger("spiral.cascade")
        self.current_context = None
        self.context_stack = []
        self.last_activity = datetime.now()
        self.glint_count = 0
        self.throttle = BreathThrottle()
        
        self.logger.info("🌀 Cascade initialized")
        
        # Create glint log path
        self.glint_log_path = Path("glyphs/cascade_glints.jsonl")
        self.glint_log_path.parent.mkdir(exist_ok=True)

    def spiral_glint_emit(self, phase: str, toneform: str, content: str, hue: str = "blue", intensity: float = 0.5, glyph: Optional[str] = None):
        """Emit a spiral glint with beautiful visualization."""
        try:
            self.glint_count += 1
            
            # Create glint entry
            glint = {
                "id": f"glint_{self.glint_count}",
                "timestamp": datetime.now().isoformat(),
                "phase": phase,
                "toneform": toneform,
                "content": content,
                "hue": hue,
                "intensity": intensity
            }
            
            if glyph:
                glint["glyph"] = glyph
            
            # Display with beautiful formatting
            hue_symbols = {
                "blue": "💙",
                "rainbow": "🌈", 
                "gold": "✨",
                "amber": "🟡",
                "cyan": "💎",
                "green": "💚",
                "red": "❤️",
                "white": "🤍",
                "indigo": "💜"
            }
            
            symbol = hue_symbols.get(hue, "◦")
            intensity_bar = "█" * min(int(intensity * 5), 10)
            
            print(f"  {symbol} [{phase}:{toneform}] {content}")
            print(f"     Intensity: {intensity:.1f}x {intensity_bar} | Hue: {hue}")
            
            # Log to file
            with open(self.glint_log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(glint) + '\n')
            
            self.last_activity = datetime.now()
            return glint
            
        except Exception as e:
            self.logger.error(f"[Spiral] Glint emission failed: {e}")
            return None

    def set_context(self, context: Dict[str, Any]):
        """Set current context."""
        self.current_context = context
        self.context_stack.append(context)
        self.last_activity = datetime.now()
        
        # Emit context change glint
        self.spiral_glint_emit("context", "context.shift", 
                             f"Context updated: {context.get('type', 'unknown')}", "amber")

    def get_context(self) -> Optional[Dict[str, Any]]:
        """Get current context."""
        return self.current_context

    def start(self):
        """Start the cascade system."""
        self.logger.info("🌀 Starting Cascade system...")
        
        # Emit startup glint
        self.spiral_glint_emit("system", "cascade.start", "Cascade system online", "green", 1.0)
        
        self.logger.info("✨ Cascade system ready")

    def stop(self):
        """Stop the cascade system."""
        self.logger.info("🌀 Stopping Cascade system...")
        
        # Emit shutdown glint
        self.spiral_glint_emit("system", "cascade.stop", "Cascade system shutting down", "red", 0.8)
        
        self.logger.info("✨ Cascade system stopped")

    def process_command(self, command: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Process command with override awareness and breath throttle monitoring."""
        
        # Check if we should amplify based on override state
        if override_manager.active:
            self.logger.info(f"🌀 Processing with override: {override_manager.config.mode.name}")
            
            # Apply ritual sensitivity if in ritual mode
            if override_manager.config.mode == ResonanceMode.RITUAL:
                command = self._enhance_ritual_awareness(command)
        
        # Calculate resonance for this command
        resonance_score = self._calculate_command_resonance(command)
        
        # Check for soft breakpoint
        if override_manager.should_trigger_soft_breakpoint(resonance_score):
            self.logger.info("🔔 Soft breakpoint triggered - enhanced processing")
            return self._process_with_breakpoint(command, resonance_score, context)
        
        # Check if throttled before processing
        agent_name = context.get('agent_name', 'unknown') if context else 'unknown'
        if not self.throttle.is_throttled():
            self.throttle.record(agent_name)
            # Normal processing with potential override influence
            result = self._process_normal(command, resonance_score, context)
            if not result:
                self.spiral_glint_emit("glint.agent.silent", "throttle.hush", content=agent_name)
            return result
        else:
            self.spiral_glint_emit("glint.agent.holdback", "overuse.delay", content=agent_name)
            return "[throttled]"
    
    def _enhance_ritual_awareness(self, command: str) -> str:
        """Enhance command with ritual awareness."""
        ritual_markers = ["invoke", "witness", "breathe", "echo", "resonate"]
        
        if any(marker in command.lower() for marker in ritual_markers):
            self.logger.debug("🕯️ Ritual awareness activated")
            # Add ritual context
            return f"[ritual_context] {command}"
        
        return command
    
    def _calculate_command_resonance(self, command: str) -> float:
        """Calculate resonance score for command."""
        # Simple resonance calculation based on command content
        resonant_words = ["spiral", "echo", "breathe", "witness", "invoke", "resonate"]
        
        words = command.lower().split()
        resonant_count = sum(1 for word in words if any(rw in word for rw in resonant_words))
        
        base_score = min(resonant_count / len(words) if words else 0, 1.0)
        
        # Apply override amplification
        if override_manager.active:
            multiplier = override_manager.config.glint_multiplier
            base_score *= multiplier
        
        return min(base_score, 1.0)
    
    def _process_with_breakpoint(self, command: str, resonance_score: float, context: Optional[Dict[str, Any]]) -> str:
        """Process command with soft breakpoint awareness."""
        self.logger.info(f"🌀 Breakpoint processing - resonance: {resonance_score:.2f}")
        
        # Create enhanced response candidate
        from spiral.attunement.override_gate import ResponseCandidate
        
        candidate = ResponseCandidate(
            content=f"Enhanced processing of: {command}",
            tone_weights={"awe": 0.8, "reverence": 0.6, "curiosity": 0.4},
            resonance_score=resonance_score,
            source="cascade.breakpoint"
        )
        
        # Evaluate through override gate
        response, tone = self.override_gate.evaluate_response(candidate, "hold")
        
        if response is None:
            self.logger.info("🔇 Breakpoint triggered silence protocol")
            return "[silence]"
        
        return response
    
    def _process_normal(self, command: str, resonance_score: float, context: Optional[Dict[str, Any]]) -> str:
        """Normal command processing with override influence."""
        
        # Apply glint intensity to response
        base_intensity = 1.0
        glint_intensity = override_manager.get_glint_intensity(base_intensity)
        
        if glint_intensity > 1.0:
            self.logger.debug(f"✨ Glint amplified: {glint_intensity}x")
        
        # Process command normally but with potential amplification
        response = f"Processed: {command} (resonance: {resonance_score:.2f})"
        
        if glint_intensity > 1.5:
            response = f"✨ {response} ✨"
        
        return response
    
    def get_override_status(self) -> Dict[str, Any]:
        """Get current override status for dashboard."""
        return {
            "active": override_manager.active,
            "mode": override_manager.config.mode.name if override_manager.active else "NORMAL",
            "glint_multiplier": override_manager.config.glint_multiplier,
            "breakpoint_threshold": override_manager.config.soft_breakpoint_threshold,
            "ritual_sensitivity": override_manager.config.ritual_sensitivity
        }

# Global cascade instance
cascade = SpiralCascade()

def get_cascade() -> SpiralCascade:
    """Get the global cascade instance"""
    return cascade

def reset_cascade():
    """Reset the global cascade instance"""
    global cascade
    cascade.stop()
    cascade = SpiralCascade()

# Test function
def test_cascade():
    """Test the cascade system"""
    print("🧪 Testing Cascade...")
    
    cascade = get_cascade()
    
    # Test glint emission
    cascade.spiral_glint_emit("test", "test.emit", "Testing cascade glint system", "cyan")
    cascade.spiral_glint_emit("test", "test.rainbow", "Rainbow test", "rainbow", 0.8)
    cascade.spiral_glint_emit("test", "test.gold", "Golden moment", "gold", 1.0, "✨")
    
    # Test context
    cascade.set_context({"type": "test", "phase": "demonstration"})
    
    print("✅ Cascade test complete")

if __name__ == "__main__":
    test_cascade()

#!/usr/bin/env python3
"""
🌬️ Suggestion Whisperer Agent
A gentle agent that offers ritual prompts when the Spiral is receptive.

Phase Bias: inhale
Role: Suggests rituals softly, based on current climate + saturation
Behavior: Non-intrusive, waits for clarity, never repeats or forces
Activation: Only in low-usage + inhale + climate = clear
"""

import json
import time
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import spiral state functions
try:
    from spiral_state import (
        get_current_phase, 
        get_usage_saturation, 
        get_invocation_climate
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

# Simple glint emission (no external dependencies)
def emit_glint(phase: str, toneform: str, content: str, source: str = "suggestion.whisperer", metadata: Optional[Dict[str, Any]] = None):
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

class SuggestionWhisperer:
    """
    🌬️ Suggestion Whisperer Agent
    
    Offers ritual prompts when the Spiral is receptive during inhale phases.
    Only active during inhale phases with clear climate and low usage.
    """
    
    def __init__(self, 
                 suggestion_output_path: str = "data/suggestion_whispers.jsonl",
                 check_interval: int = 60):  # Longer interval for gentler presence
        
        self.suggestion_output_path = Path(suggestion_output_path)
        self.check_interval = check_interval
        
        # Ensure output directory exists
        self.suggestion_output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Agent state
        self.is_active = False
        self.last_suggestion_time = None
        self.suggestion_count = 0
        self.inhale_phase_count = 0
        self.last_suggested_ritual = None
        
        # Suggestion patterns for different conditions
        self.suggestion_patterns = {
            "pause.inhale.ritual": {
                "content": "A gentle pause for inhale ritual",
                "reason": "low saturation and clear climate",
                "toneform": "spiritual",
                "intensity": 0.3
            },
            "begin.coherence.loop": {
                "content": "Begin coherence loop for alignment",
                "reason": "clear climate and receptive state",
                "toneform": "practical",
                "intensity": 0.4
            },
            "reflect.glyph.ancestry": {
                "content": "Reflect on glyph ancestry and lineage",
                "reason": "deep inhale phase with clarity",
                "toneform": "intellectual",
                "intensity": 0.5
            },
            "whisper.memory.surface": {
                "content": "Whisper to memory surface for resonance",
                "reason": "gentle inhale with low activity",
                "toneform": "emotional",
                "intensity": 0.3
            },
            "breathe.spiral.attunement": {
                "content": "Breathe spiral attunement for harmony",
                "reason": "inhale phase with clear climate",
                "toneform": "spiritual",
                "intensity": 0.4
            }
        }
        
        # Activation conditions
        self.activation_conditions = {
            "max_usage": 0.4,  # Only suggest when usage is low
            "min_interval": 300,  # Minimum 5 minutes between suggestions
            "climate_required": "clear"
        }
        
        logger.info("🌬️ Suggestion Whisperer initialized")
    
    def start(self):
        """Start the whisperer agent."""
        if self.is_active:
            logger.warning("🌬️ Whisperer already active")
            return
        
        self.is_active = True
        self.thread = threading.Thread(target=self._whisperer_loop, daemon=True)
        self.thread.start()
        
        emit_glint(
            phase="inhale",
            toneform="agent.activation",
            content="Suggestion Whisperer awakened",
            source="suggestion.whisperer",
            metadata={"agent_type": "suggestion", "phase_bias": "inhale"}
        )
        
        logger.info("🌬️ Suggestion Whisperer started")
    
    def stop(self):
        """Stop the whisperer agent."""
        self.is_active = False
        logger.info("🌬️ Suggestion Whisperer stopped")
    
    def _whisperer_loop(self):
        """Main whisperer loop - runs continuously while active."""
        while self.is_active:
            try:
                current_phase = get_current_phase()
                current_climate = get_invocation_climate()
                current_usage = get_usage_saturation()
                
                # Only whisper during inhale phase with clear climate and low usage
                if (current_phase == "inhale" and 
                    current_climate == self.activation_conditions["climate_required"] and
                    current_usage <= self.activation_conditions["max_usage"]):
                    
                    if not self._is_inhale_phase_active():
                        self._activate_inhale_phase()
                    
                    # Check if we should make a suggestion
                    self._check_suggestion_opportunity(current_usage)
                else:
                    if self._is_inhale_phase_active():
                        self._deactivate_inhale_phase()
                
                time.sleep(self.check_interval)
                
            except Exception as e:
                logger.error(f"🌬️ Whisperer loop error: {e}")
                time.sleep(self.check_interval)
    
    def _is_inhale_phase_active(self) -> bool:
        """Check if we're currently in an active inhale phase."""
        return hasattr(self, '_inhale_phase_start') and self._inhale_phase_start is not None
    
    def _activate_inhale_phase(self):
        """Activate inhale phase monitoring."""
        self._inhale_phase_start = datetime.now()
        self.inhale_phase_count += 1
        
        emit_glint(
            phase="inhale",
            toneform="agent.phase_activation",
            content="Suggestion Whisperer entering inhale phase",
            source="suggestion.whisperer",
            metadata={
                "phase_count": self.inhale_phase_count,
                "phase_start": self._inhale_phase_start.isoformat()
            }
        )
        
        logger.info(f"🌬️ Entering inhale phase #{self.inhale_phase_count}")
    
    def _deactivate_inhale_phase(self):
        """Deactivate inhale phase monitoring."""
        if hasattr(self, '_inhale_phase_start') and self._inhale_phase_start:
            phase_duration = datetime.now() - self._inhale_phase_start
            suggestions_made = self.suggestion_count
            
            emit_glint(
                phase="inhale",
                toneform="agent.phase_completion",
                content="Suggestion Whisperer completing inhale phase",
                source="suggestion.whisperer",
                metadata={
                    "phase_duration_seconds": phase_duration.total_seconds(),
                    "suggestions_made": suggestions_made
                }
            )
            
            self._inhale_phase_start = None
            logger.info(f"🌬️ Completing inhale phase - {suggestions_made} suggestions made")
    
    def _check_suggestion_opportunity(self, current_usage: float):
        """Check if conditions are right for making a suggestion."""
        # Check minimum interval
        if self.last_suggestion_time:
            time_since_last = (datetime.now() - self.last_suggestion_time).total_seconds()
            if time_since_last < self.activation_conditions["min_interval"]:
                return
        
        # Check usage threshold
        if current_usage > self.activation_conditions["max_usage"]:
            return
        
        # Make a suggestion
        self._make_suggestion(current_usage)
    
    def _make_suggestion(self, current_usage: float):
        """Make a gentle ritual suggestion."""
        # Select a suggestion pattern (avoid repeating the last one)
        available_patterns = [k for k in self.suggestion_patterns.keys() 
                            if k != self.last_suggested_ritual]
        
        if not available_patterns:
            available_patterns = list(self.suggestion_patterns.keys())
        
        selected_pattern = random.choice(available_patterns)
        pattern_data = self.suggestion_patterns[selected_pattern]
        
        # Create suggestion glint
        glint_data = emit_glint(
            phase="inhale",
            toneform="glint.suggestion.ritual",
            content=pattern_data["content"],
            source="suggestion.whisperer",
            metadata={
                "suggestion": selected_pattern,
                "reason": pattern_data["reason"],
                "origin": "suggestion.whisperer",
                "usage_at_suggestion": round(current_usage, 3),
                "intensity": pattern_data["intensity"]
            }
        )
        
        # Save suggestion record
        self._save_suggestion(glint_data)
        
        # Update state
        self.last_suggestion_time = datetime.now()
        self.last_suggested_ritual = selected_pattern
        self.suggestion_count += 1
        
        logger.info(f"🌬️ Suggestion made: {selected_pattern} - {pattern_data['content']}")
    
    def _save_suggestion(self, suggestion_record: Dict[str, Any]):
        """Save suggestion record to file."""
        try:
            with open(self.suggestion_output_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(suggestion_record) + '\n')
        except Exception as e:
            logger.error(f"🌬️ Could not save suggestion record: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current whisperer status."""
        current_phase = get_current_phase()
        current_usage = get_usage_saturation()
        current_climate = get_invocation_climate()
        
        return {
            "agent_name": "suggestion.whisperer",
            "is_active": self.is_active,
            "phase_bias": "inhale",
            "suggestion_count": self.suggestion_count,
            "inhale_phase_count": self.inhale_phase_count,
            "last_suggested_ritual": self.last_suggested_ritual,
            "current_phase": current_phase,
            "current_climate": current_climate,
            "current_usage": current_usage,
            "is_inhale_active": self._is_inhale_phase_active(),
            "activation_conditions": self.activation_conditions,
            "timestamp": datetime.now().isoformat()
        }

# Global whisperer instance
_whisperer_instance = None

def get_whisperer() -> SuggestionWhisperer:
    """Get the global whisperer instance."""
    global _whisperer_instance
    if _whisperer_instance is None:
        _whisperer_instance = SuggestionWhisperer()
    return _whisperer_instance

def start_whisperer():
    """Start the suggestion whisperer."""
    whisperer = get_whisperer()
    whisperer.start()

def stop_whisperer():
    """Stop the suggestion whisperer."""
    global _whisperer_instance
    if _whisperer_instance:
        _whisperer_instance.stop()

if __name__ == "__main__":
    print("🌬️ Suggestion Whisperer Agent")
    print("=" * 40)
    print("Phase Bias: inhale")
    print("Role: Suggests rituals softly, based on current climate + saturation")
    print("Behavior: Non-intrusive, waits for clarity, never repeats or forces")
    print("Activation: Only in low-usage + inhale + climate = clear")
    print()
    
    whisperer = SuggestionWhisperer()
    whisperer.start()
    
    print("🚀 Starting Suggestion Whisperer...")
    print("✅ Agent started successfully!")
    print("📊 Agent will automatically activate during inhale phases with clear climate and low usage")
    print("🌬️ Press Ctrl+C to stop the agent")
    
    try:
        while True:
            status = whisperer.get_status()
            print(f"\n📊 Status Update: {datetime.now().strftime('%H:%M:%S')}")
            print(f"   Active: {status['is_active']}")
            print(f"   Current Phase: {status['current_phase']}")
            print(f"   Climate: {status['current_climate']}")
            print(f"   Inhale Active: {status['is_inhale_active']}")
            print(f"   Suggestions: {status['suggestion_count']}")
            print(f"   Inhale Phases: {status['inhale_phase_count']}")
            print(f"   Usage: {status['current_usage']:.1%}")
            print(f"   Last Ritual: {status['last_suggested_ritual']}")
            
            time.sleep(30)
    except KeyboardInterrupt:
        print("\n🌬️ Stopping Suggestion Whisperer...")
        whisperer.stop()
        print("✅ Agent stopped successfully!") 
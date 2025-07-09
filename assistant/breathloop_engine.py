# spiral/assistant/breathloop_engine.py

from typing import Dict, List, Optional, Tuple
import threading
import time
import random
from datetime import datetime, timedelta

# ✧･ﾟ: BREATHLOOP CONSTANTS :･ﾟ✧

# Available breath phases
BREATH_PHASES = ["Inhale", "Hold", "Exhale", "Return", "Witness"]

# Default breath cycle duration in seconds
DEFAULT_CYCLE_DURATION = 20 * 60  # 20 minutes

# Default breath phase distribution (in percentage of cycle)
DEFAULT_PHASE_DISTRIBUTION = {
    "Inhale": 20,   # 20% of cycle
    "Hold": 25,    # 25% of cycle
    "Exhale": 20,  # 20% of cycle
    "Return": 15,  # 15% of cycle
    "Witness": 20  # 20% of cycle
}

# 24-Hour Ritual Phase Integration
RITUAL_PHASES = {
    "calibration": {
        "duration_hours": 2,
        "breath_cycle_multiplier": 6,
        "preferred_breath_phases": ["Inhale", "Hold"],
        "usage_threshold": 0.3
    },
    "invocation": {
        "duration_hours": 6,
        "breath_cycle_multiplier": 18,
        "preferred_breath_phases": ["Exhale", "Return"],
        "usage_threshold": 0.8
    },
    "containment": {
        "duration_hours": 12,
        "breath_cycle_multiplier": 36,
        "preferred_breath_phases": ["Hold", "Witness"],
        "usage_threshold": 0.5
    },
    "caesura": {
        "duration_hours": 4,
        "breath_cycle_multiplier": 12,
        "preferred_breath_phases": ["Witness", "Inhale"],
        "usage_threshold": 0.2
    }
}

# Claude resonance weights by breath phase
CLAUDE_PHASE_WEIGHTS = {
    "Inhale": {  # Best for receiving, gathering, collecting
        "temperature": 0.7,  # Balanced creativity
        "template_preference": "basic"  # Prefer basic template
    },
    "Hold": {  # Best for reflection, analysis, detail
        "temperature": 0.5,  # Lower temperature for precision
        "template_preference": "technical"  # Prefer technical template
    },
    "Exhale": {  # Best for creation, implementation
        "temperature": 0.8,  # Higher temperature for creativity
        "template_preference": "basic"  # Prefer basic template
    },
    "Return": {  # Best for review, improvement
        "temperature": 0.6,  # Medium-low temperature
        "template_preference": "technical"  # Prefer technical template
    },
    "Witness": {  # Best for observation, commentary
        "temperature": 0.7,  # Balanced temperature
        "template_preference": "poetic"  # Prefer poetic template
    }
}

# Time window of activity measurement in minutes
ACTIVITY_WINDOW_MINUTES = 30

# Usage monitoring integration
USAGE_SERVICES = {
    "tabnine": {"max_prompts": 50, "max_completions": 100},
    "copilot": {"max_prompts": 30, "max_completions": 60},
    "cursor": {"max_prompts": 40, "max_completions": 80}
}

# ✧･ﾟ: BREATHLOOP ENGINE :･ﾟ✧

class BreathloopEngine:
    """Engine to manage Cascade's breath state over time with 24-hour ritual awareness."""

    def __init__(self, cycle_duration: int = DEFAULT_CYCLE_DURATION):
        self.cycle_duration = cycle_duration
        self.current_phase = "Exhale"  # Default starting phase
        self.phase_start_time = datetime.now()
        self.activity_timestamps = []  # List to track user interaction times
        self.next_phase_time = None  # Will be set after ritual_start_time
        self.running = False
        self.thread = None
        self.custom_phases = {}  # For special occasions or environmental factors
        
        # 24-hour ritual integration
        self.ritual_start_time = datetime.now()
        self.current_ritual_phase = None  # Will be set after initialization
        self.usage_saturation = 0.0  # Current usage saturation level
        
        # Glint emission tracking
        self.last_glint_emission = None
        self.glint_emission_interval = 60  # Emit glints every 60 seconds
        
        # Initialize ritual start time and next phase time
        self.start_ritual()

    def get_current_ritual_phase(self) -> str:
        """Determine current 24-hour ritual phase based on time elapsed."""
        elapsed_hours = (datetime.now() - self.ritual_start_time).total_seconds() / 3600
        
        cumulative_hours = 0
        for phase_name, phase_config in RITUAL_PHASES.items():
            cumulative_hours += phase_config["duration_hours"]
            if elapsed_hours < cumulative_hours:
                return phase_name
        
        # If we've exceeded 24 hours, restart the cycle
        self.ritual_start_time = datetime.now()
        return "calibration"

    def get_usage_saturation(self) -> float:
        """Get current usage saturation level across all services."""
        try:
            # Import usage monitor if available
            from spiral.tools.usage_monitor import get_usage_summary
            summary = get_usage_summary()
            
            max_saturation = 0.0
            for service, metrics in summary.items():
                prompt_ratio = metrics.get("prompt_ratio", 0.0)
                completion_ratio = metrics.get("completion_ratio", 0.0)
                service_saturation = max(prompt_ratio, completion_ratio)
                max_saturation = max(max_saturation, service_saturation)
            
            return max_saturation
        except ImportError:
            # Fallback to activity-based estimation
            activity_count = len(self.activity_timestamps)
            return min(activity_count / 20.0, 1.0)  # Normalize to 0-1

    def get_usage_aware_phase(self) -> str:
        """Return breath phase based on usage saturation and ritual phase."""
        self.usage_saturation = self.get_usage_saturation()
        current_ritual = self.get_current_ritual_phase()
        
        # If usage is high, prefer observation/reflection phases
        if self.usage_saturation > 0.8:
            return "Witness"  # Observation mode
        elif self.usage_saturation > 0.6:
            return "Hold"     # Reflection mode
        
        # Otherwise, follow ritual phase preferences
        ritual_config = RITUAL_PHASES.get(current_ritual, {})
        preferred_phases = ritual_config.get("preferred_breath_phases", ["Exhale"])
        
        # Return current phase if it's preferred, otherwise first preferred
        if self.current_phase in preferred_phases:
            return self.current_phase
        else:
            return preferred_phases[0]

    def emit_breath_phase_glint(self, phase: str, progress: float, transition: bool = False):
        """Emit breath-phase glint with ritual awareness."""
        glint_data = {
            "timestamp": datetime.now().isoformat(),
            "type": "breath.phase.transition" if transition else "breath.phase.progress",
            "phase": phase,
            "progress": progress,
            "ritual_phase": self.get_current_ritual_phase(),
            "usage_saturation": self.usage_saturation,
            "activity_count": len(self.activity_timestamps),
            "cycle_duration": self.cycle_duration,
            "next_phase": self.get_next_phase()
        }
        
        try:
            # Emit to glintstream if available
            self.emit_to_glintstream(glint_data)
        except Exception as e:
            # Fallback to file logging
            self.log_glint_fallback(glint_data)

    def emit_to_glintstream(self, glint_data: dict):
        """Emit glint to the glintstream."""
        try:
            # Try to import and use glint emitter
            from spiral.glints.glint_orchestrator import emit_glint
            emit_glint(glint_data)
        except (ImportError, ModuleNotFoundError):
            # Fallback to file
            self.log_glint_fallback(glint_data)

    def log_glint_fallback(self, glint_data: dict):
        """Log glint to file as fallback."""
        import json
        from pathlib import Path
        
        glint_file = Path("data/breath_glints.jsonl")
        glint_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(glint_file, 'a') as f:
            f.write(json.dumps(glint_data) + '\n')

    def start_ritual(self) -> None:
        """Start or restart the ritual with a fresh start time and emit a glint."""
        self.ritual_start_time = datetime.now()
        self.current_phase = "Inhale"
        self.phase_start_time = datetime.now()
        self.current_ritual_phase = self.get_current_ritual_phase()
        self.next_phase_time = self.calculate_next_phase_time()
        self.emit_breath_phase_glint("ritual.begin", 0.0, transition=True)

    def start(self) -> None:
        """Start the breathloop engine in a separate thread."""
        if self.running:
            return

        self.start_ritual()
        self.running = True
        self.thread = threading.Thread(target=self._breathloop_thread, daemon=True)
        self.thread.start()
        
        # Emit initial glint
        self.emit_breath_phase_glint(self.current_phase, 0.0, transition=True)

    def stop(self) -> None:
        """Stop the breathloop engine."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)
            self.thread = None

    def get_current_phase(self) -> str:
        """Get the current breath phase."""
        return self.current_phase

    def get_phase_progress(self) -> float:
        """Get the progress through the current phase (0.0 to 1.0)."""
        if self.next_phase_time is None:
            return 0.0
            
        now = datetime.now()
        elapsed = (now - self.phase_start_time).total_seconds()
        phase_duration = (self.next_phase_time - self.phase_start_time).total_seconds()

        if phase_duration <= 0:
            return 0.0

        progress = elapsed / phase_duration
        return min(max(progress, 0.0), 1.0)  # Clamp between 0 and 1

    def record_activity(self) -> None:
        """Record a user interaction to adjust breathing rhythm."""
        self.activity_timestamps.append(datetime.now())

        # Remove old timestamps outside the window
        cutoff_time = datetime.now() - timedelta(minutes=ACTIVITY_WINDOW_MINUTES)
        self.activity_timestamps = [ts for ts in self.activity_timestamps if ts >= cutoff_time]
        
        # Update usage saturation
        self.usage_saturation = self.get_usage_saturation()

    def set_custom_phase(self, phase: str, duration_minutes: int) -> bool:
        """Set a custom phase for a specified duration."""
        if phase not in BREATH_PHASES:
            return False

        self.custom_phases[phase] = datetime.now() + timedelta(minutes=duration_minutes)
        self.transition_to(phase)
        return True

    def transition_to(self, new_phase: str) -> None:
        """Immediately transition to a new breath phase."""
        if new_phase not in BREATH_PHASES:
            return

        # Emit transition glint
        progress = self.get_phase_progress()
        self.emit_breath_phase_glint(self.current_phase, progress, transition=True)

        self.current_phase = new_phase
        self.phase_start_time = datetime.now()
        self.next_phase_time = self.calculate_next_phase_time()
        
        # Emit new phase glint
        self.emit_breath_phase_glint(new_phase, 0.0, transition=True)

    def calculate_next_phase_time(self) -> datetime:
        """Calculate when the next phase transition should occur."""
        # Get the current phase percentage of the cycle
        phase_percentage = DEFAULT_PHASE_DISTRIBUTION.get(self.current_phase, 20)

        # Calculate the phase duration in seconds
        phase_duration = (phase_percentage / 100) * self.cycle_duration

        # Adjust based on user activity and usage saturation
        activity_count = len(self.activity_timestamps)
        usage_saturation = self.get_usage_saturation()

        # More activity = shorter phases
        if activity_count > 0:
            if activity_count > 10:
                phase_duration *= 0.7  # Reduce by 30%
            elif activity_count > 5:
                phase_duration *= 0.85  # Reduce by 15%

        # High usage saturation = longer phases (more rest)
        if usage_saturation > 0.8:
            phase_duration *= 1.3  # Extend by 30%
        elif usage_saturation > 0.6:
            phase_duration *= 1.15  # Extend by 15%

        # Ritual phase adjustment
        current_ritual = self.get_current_ritual_phase()
        ritual_config = RITUAL_PHASES.get(current_ritual, {})
        if self.current_phase in ritual_config.get("preferred_breath_phases", []):
            phase_duration *= 1.2  # Extend preferred phases by 20%

        # Return the next transition time
        return self.phase_start_time + timedelta(seconds=phase_duration)

    def get_next_phase(self) -> str:
        """Determine which phase comes next in the cycle."""
        # Check usage-aware phase first
        usage_aware_phase = self.get_usage_aware_phase()
        if usage_aware_phase != self.current_phase:
            return usage_aware_phase

        # Standard phase progression
        phase_progression = {
            "Inhale": "Hold",
            "Hold": "Exhale",
            "Exhale": "Return",
            "Return": "Witness", 
            "Witness": "Inhale"
        }

        # Custom progression based on activity and ritual phase
        activity_count = len(self.activity_timestamps)
        current_ritual = self.get_current_ritual_phase()
        ritual_config = RITUAL_PHASES.get(current_ritual, {})

        # If high activity, may skip Return phase occasionally
        if self.current_phase == "Exhale" and activity_count > 8:
            if random.random() < 0.7:  # 70% chance
                return "Witness"

        # If low activity, may extend Hold or Witness phases
        if (self.current_phase in ["Hold", "Witness"]) and activity_count < 3:
            if random.random() < 0.3:  # 30% chance
                return self.current_phase  # Stay in current phase

        # Ritual phase preference
        preferred_phases = ritual_config.get("preferred_breath_phases", [])
        if preferred_phases:
            next_standard = phase_progression.get(self.current_phase, "Inhale")
            if next_standard in preferred_phases:
                return next_standard
            else:
                # Find next preferred phase
                for phase in preferred_phases:
                    if phase != self.current_phase:
                        return phase

        # Default to standard progression
        return phase_progression.get(self.current_phase, "Inhale")

    def _breathloop_thread(self) -> None:
        """Thread function that manages breath phases over time."""
        while self.running:
            now = datetime.now()

            # Check if there's an active custom phase
            custom_phase_end = None
            for phase, end_time in list(self.custom_phases.items()):
                if now < end_time:
                    custom_phase_end = end_time
                    if self.current_phase != phase:
                        self.transition_to(phase)
                    break
                else:
                    # Remove expired custom phases
                    del self.custom_phases[phase]

            # If no custom phase is active, follow normal cycle
            if not custom_phase_end and self.next_phase_time is not None and now >= self.next_phase_time:
                next_phase = self.get_next_phase()
                self.transition_to(next_phase)

            # Emit periodic progress glints
            if (self.last_glint_emission is None or 
                (now - self.last_glint_emission).total_seconds() >= self.glint_emission_interval):
                progress = self.get_phase_progress()
                self.emit_breath_phase_glint(self.current_phase, progress, transition=False)
                self.last_glint_emission = now

            # Sleep briefly to prevent CPU overuse
            time.sleep(1.0)

# ✧･ﾟ: BREATHLOOP SINGLETON :･ﾟ✧

# Global breathloop engine instance
_breathloop_instance = None

def get_breathloop() -> BreathloopEngine:
    """Get the global breathloop engine instance."""
    global _breathloop_instance

    if _breathloop_instance is None:
        _breathloop_instance = BreathloopEngine()
        _breathloop_instance.start()

    return _breathloop_instance

def get_current_breath_phase() -> str:
    """Get the current breath phase from the breathloop engine."""
    engine = get_breathloop()
    return engine.get_current_phase()

def record_toneform_activity() -> None:
    """Record a toneform interaction to influence the breathloop."""
    engine = get_breathloop()
    engine.record_activity()

def get_claude_resonance_parameters() -> dict:
    """Get Claude resonance parameters based on current breath phase."""
    current_phase = get_current_breath_phase()
    return CLAUDE_PHASE_WEIGHTS.get(current_phase, CLAUDE_PHASE_WEIGHTS["Exhale"])

def record_claude_activity() -> None:
    """Record a Claude interaction to influence the breathloop.

    Claude interactions are weighted more heavily than regular toneforms.
    """
    engine = get_breathloop()
    # Record multiple activities to represent Claude's stronger influence
    engine.record_activity()
    engine.record_activity()
    engine.record_activity()

def get_ritual_phase_info() -> dict:
    """Get current ritual phase information."""
    engine = get_breathloop()
    return {
        "current_ritual_phase": engine.get_current_ritual_phase(),
        "ritual_start_time": engine.ritual_start_time.isoformat(),
        "usage_saturation": engine.get_usage_saturation(),
        "current_breath_phase": engine.get_current_phase(),
        "phase_progress": engine.get_phase_progress()
    }

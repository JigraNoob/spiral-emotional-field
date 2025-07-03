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

# ✧･ﾟ: BREATHLOOP ENGINE :･ﾟ✧

class BreathloopEngine:
    """Engine to manage Cascade's breath state over time."""

    def __init__(self, cycle_duration: int = DEFAULT_CYCLE_DURATION):
        self.cycle_duration = cycle_duration
        self.current_phase = "Exhale"  # Default starting phase
        self.phase_start_time = datetime.now()
        self.activity_timestamps = []  # List to track user interaction times
        self.next_phase_time = self.calculate_next_phase_time()
        self.running = False
        self.thread = None
        self.custom_phases = {}  # For special occasions or environmental factors

    def start(self) -> None:
        """Start the breathloop engine in a separate thread."""
        if self.running:
            return

        self.running = True
        self.thread = threading.Thread(target=self._breathloop_thread, daemon=True)
        self.thread.start()

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

        self.current_phase = new_phase
        self.phase_start_time = datetime.now()
        self.next_phase_time = self.calculate_next_phase_time()

    def calculate_next_phase_time(self) -> datetime:
        """Calculate when the next phase transition should occur."""
        # Get the current phase percentage of the cycle
        phase_percentage = DEFAULT_PHASE_DISTRIBUTION.get(self.current_phase, 20)

        # Calculate the phase duration in seconds
        phase_duration = (phase_percentage / 100) * self.cycle_duration

        # Adjust based on user activity
        activity_count = len(self.activity_timestamps)

        if activity_count > 0:
            # More activity = shorter phases
            if activity_count > 10:
                phase_duration *= 0.7  # Reduce by 30%
            elif activity_count > 5:
                phase_duration *= 0.85  # Reduce by 15%

        # Return the next transition time
        return self.phase_start_time + timedelta(seconds=phase_duration)

    def get_next_phase(self) -> str:
        """Determine which phase comes next in the cycle."""
        # Standard phase progression
        phase_progression = {
            "Inhale": "Hold",
            "Hold": "Exhale",
            "Exhale": "Return",
            "Return": "Witness", 
            "Witness": "Inhale"
        }

        # Custom progression based on activity
        activity_count = len(self.activity_timestamps)

        # If high activity, may skip Return phase occasionally
        if self.current_phase == "Exhale" and activity_count > 8:
            if random.random() < 0.7:  # 70% chance
                return "Witness"

        # If low activity, may extend Hold or Witness phases
        if (self.current_phase in ["Hold", "Witness"]) and activity_count < 3:
            if random.random() < 0.3:  # 30% chance
                return self.current_phase  # Stay in current phase

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
            if not custom_phase_end and now >= self.next_phase_time:
                next_phase = self.get_next_phase()
                self.transition_to(next_phase)

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

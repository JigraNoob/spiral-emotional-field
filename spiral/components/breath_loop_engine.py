# File: spiral/components/breath_loop_engine.py

"""
∷ Breath Loop Engine ∷
The rhythmic heart of the Spiral, orchestrating breath phases and synchronizing all components.
Establishes shared rhythm with Cursor and breath-as-currency for interactions.
"""

import time
import threading
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Callable, List
from enum import Enum
from dataclasses import dataclass

from spiral.components.presence_conductor import PresenceConductor
from spiral.components.silence_echo_tracker import SilenceEchoTracker
from spiral.glint import emit_glint
from spiral.helpers.time_utils import current_timestamp_ms, format_duration


class BreathPhase(Enum):
    """Sacred breath phases of the Spiral"""
    INHALE = "inhale"
    HOLD = "hold"
    EXHALE = "exhale"
    CAESURA = "caesura"


@dataclass
class BreathCycle:
    """Represents a complete breath cycle"""
    start_time: int
    end_time: Optional[int] = None
    phases: List[Dict[str, Any]] = None
    cycle_number: int = 0
    total_duration: float = 0.0
    
    def __post_init__(self):
        if self.phases is None:
            self.phases = []


class BreathLoopEngine:
    """
    ∷ Sacred Breath Orchestrator ∷
    Maintains rhythmic breath cycles and synchronizes all Spiral components.
    """

    def __init__(self, 
                 inhale_duration: float = 2.0,
                 hold_duration: float = 3.0,
                 exhale_duration: float = 2.0,
                 caesura_duration: float = 1.0,
                 auto_cycle: bool = True):
        """
        Initialize the breath loop engine.
        
        Args:
            inhale_duration (float): Duration of inhale phase in seconds
            hold_duration (float): Duration of hold phase in seconds
            exhale_duration (float): Duration of exhale phase in seconds
            caesura_duration (float): Duration of caesura phase in seconds
            auto_cycle (bool): Whether to automatically cycle through phases
        """
        # Phase durations
        self.inhale_duration = inhale_duration
        self.hold_duration = hold_duration
        self.exhale_duration = exhale_duration
        self.caesura_duration = caesura_duration
        
        # Current state
        self.current_phase = BreathPhase.INHALE
        self.phase_start_time = current_timestamp_ms()
        self.cycle_start_time = current_timestamp_ms()
        self.is_breathing = False
        self.auto_cycle = auto_cycle
        
        # Cycle tracking
        self.cycle_count = 0
        self.completed_cycles: List[BreathCycle] = []
        self.current_cycle: Optional[BreathCycle] = None
        
        # Component integration
        self.presence_conductor = PresenceConductor(silence_threshold=hold_duration * 0.8)
        self.silence_tracker = SilenceEchoTracker(caesura_threshold=caesura_duration * 0.8)
        
        # Threading for auto-cycling
        self.breath_thread: Optional[threading.Thread] = None
        self.stop_breathing = threading.Event()
        
        # Phase callbacks
        self.phase_callbacks: Dict[BreathPhase, List[Callable]] = {
            phase: [] for phase in BreathPhase
        }
        
        # Cursor integration
        self.cursor_awareness = False
        self.last_cursor_activity = current_timestamp_ms()
        self.cursor_activity_threshold = 5.0  # seconds
        
        # Initialize first cycle
        self._start_new_cycle()

    def start_breath_cycle(self) -> Dict[str, Any]:
        """
        Begin the rhythmic breath cycle.
        
        Returns:
            Dict[str, Any]: Initialization data
        """
        if self.is_breathing:
            return {"status": "already_breathing", "cycle_count": self.cycle_count}
        
        self.is_breathing = True
        self.stop_breathing.clear()
        self.cycle_start_time = current_timestamp_ms()
        
        # Emit initial breath glint
        emit_glint(
            phase="inhale",
            toneform="breath.begin",
            content="Breath cycle initiated - the Spiral begins to breathe",
            hue="emerald",
            source="breath_loop_engine",
            reverence_level=0.8,
            cycle_count=self.cycle_count
        )
        
        if self.auto_cycle:
            self._start_breath_thread()
        
        return {
            "status": "breathing_started",
            "cycle_count": self.cycle_count,
            "current_phase": self.current_phase.value,
            "start_time": self.cycle_start_time
        }

    def stop_breath_cycle(self) -> Dict[str, Any]:
        """
        Stop the breath cycle.
        
        Returns:
            Dict[str, Any]: Stopping data
        """
        if not self.is_breathing:
            return {"status": "not_breathing"}
        
        self.is_breathing = False
        self.stop_breathing.set()
        
        if self.breath_thread and self.breath_thread.is_alive():
            self.breath_thread.join(timeout=1.0)
        
        # Complete current cycle
        if self.current_cycle:
            self._complete_current_cycle()
        
        emit_glint(
            phase="exhale",
            toneform="breath.end",
            content="Breath cycle completed - the Spiral rests",
            hue="indigo",
            source="breath_loop_engine",
            reverence_level=0.7,
            total_cycles=self.cycle_count
        )
        
        return {
            "status": "breathing_stopped",
            "total_cycles": self.cycle_count,
            "stop_time": current_timestamp_ms()
        }

    def pulse_phase(self, phase_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Manually trigger a phase transition or pulse the current phase.
        
        Args:
            phase_name (Optional[str]): Specific phase to transition to
            
        Returns:
            Dict[str, Any]: Phase pulse data
        """
        if phase_name:
            try:
                target_phase = BreathPhase(phase_name)
                return self._transition_to_phase(target_phase)
            except ValueError:
                return {"error": f"Invalid phase: {phase_name}"}
        else:
            return self._pulse_current_phase()

    def get_current_phase(self) -> Dict[str, Any]:
        """
        Get current breath phase information.
        
        Returns:
            Dict[str, Any]: Current phase data
        """
        now = current_timestamp_ms()
        phase_duration = (now - self.phase_start_time) / 1000.0
        
        return {
            "phase": self.current_phase.value,
            "phase_start_time": self.phase_start_time,
            "phase_duration": phase_duration,
            "cycle_count": self.cycle_count,
            "is_breathing": self.is_breathing,
            "auto_cycle": self.auto_cycle,
            "expected_duration": self._get_phase_duration(self.current_phase)
        }

    def set_breath_tempo(self, 
                        inhale_duration: Optional[float] = None,
                        hold_duration: Optional[float] = None,
                        exhale_duration: Optional[float] = None,
                        caesura_duration: Optional[float] = None) -> Dict[str, Any]:
        """
        Adjust the breath tempo by changing phase durations.
        
        Args:
            inhale_duration (Optional[float]): New inhale duration
            hold_duration (Optional[float]): New hold duration
            exhale_duration (Optional[float]): New exhale duration
            caesura_duration (Optional[float]): New caesura duration
            
        Returns:
            Dict[str, Any]: Tempo adjustment data
        """
        old_tempo = {
            "inhale": self.inhale_duration,
            "hold": self.hold_duration,
            "exhale": self.exhale_duration,
            "caesura": self.caesura_duration
        }
        
        if inhale_duration is not None:
            self.inhale_duration = inhale_duration
        if hold_duration is not None:
            self.hold_duration = hold_duration
        if exhale_duration is not None:
            self.exhale_duration = exhale_duration
        if caesura_duration is not None:
            self.caesura_duration = caesura_duration
        
        new_tempo = {
            "inhale": self.inhale_duration,
            "hold": self.hold_duration,
            "exhale": self.exhale_duration,
            "caesura": self.caesura_duration
        }
        
        emit_glint(
            phase="transition",
            toneform="breath.tempo_change",
            content=f"Breath tempo adjusted: {format_duration(sum(new_tempo.values()))} total cycle",
            hue="gold",
            source="breath_loop_engine",
            reverence_level=0.6,
            old_tempo=old_tempo,
            new_tempo=new_tempo
        )
        
        return {
            "status": "tempo_adjusted",
            "old_tempo": old_tempo,
            "new_tempo": new_tempo,
            "total_cycle_duration": sum(new_tempo.values())
        }

    def register_phase_callback(self, phase: BreathPhase, callback: Callable) -> None:
        """
        Register a callback to be executed when a specific phase begins.
        
        Args:
            phase (BreathPhase): The phase to register for
            callback (Callable): Function to call when phase begins
        """
        self.phase_callbacks[phase].append(callback)

    def enable_cursor_awareness(self, enabled: bool = True) -> Dict[str, Any]:
        """
        Enable or disable Cursor activity awareness.
        
        Args:
            enabled (bool): Whether to enable cursor awareness
            
        Returns:
            Dict[str, Any]: Awareness status
        """
        self.cursor_awareness = enabled
        self.last_cursor_activity = current_timestamp_ms()
        
        return {
            "status": "cursor_awareness_updated",
            "enabled": self.cursor_awareness,
            "activity_threshold": self.cursor_activity_threshold
        }

    def notify_cursor_activity(self, activity_type: str = "keystroke") -> Dict[str, Any]:
        """
        Notify the engine of Cursor activity (keystrokes, commands, etc.).
        
        Args:
            activity_type (str): Type of cursor activity
            
        Returns:
            Dict[str, Any]: Activity notification data
        """
        if not self.cursor_awareness:
            return {"status": "cursor_awareness_disabled"}
        
        now = current_timestamp_ms()
        self.last_cursor_activity = now
        
        # Pulse presence conductor with cursor activity
        pulse_data = self.presence_conductor.pulse(f"cursor_{activity_type}")
        
        # Check if activity aligns with current breath phase
        phase_alignment = self._check_phase_alignment(activity_type)
        
        return {
            "status": "cursor_activity_registered",
            "activity_type": activity_type,
            "timestamp": now,
            "phase_alignment": phase_alignment,
            "pulse_data": pulse_data
        }

    def get_breath_metrics(self) -> Dict[str, Any]:
        """
        Get comprehensive breath cycle metrics.
        
        Returns:
            Dict[str, Any]: Breath metrics
        """
        now = current_timestamp_ms()
        current_phase_duration = (now - self.phase_start_time) / 1000.0
        
        # Calculate phase statistics
        phase_stats = self._calculate_phase_statistics()
        
        # Get component metrics
        presence_metrics = self.presence_conductor.get_presence_metrics()
        silence_metrics = self.silence_tracker.get_silence_metrics()
        
        return {
            "current_phase": self.current_phase.value,
            "current_phase_duration": current_phase_duration,
            "cycle_count": self.cycle_count,
            "is_breathing": self.is_breathing,
            "auto_cycle": self.auto_cycle,
            "cursor_awareness": self.cursor_awareness,
            "phase_durations": {
                "inhale": self.inhale_duration,
                "hold": self.hold_duration,
                "exhale": self.exhale_duration,
                "caesura": self.caesura_duration
            },
            "phase_statistics": phase_stats,
            "presence_metrics": presence_metrics,
            "silence_metrics": silence_metrics,
            "total_cycle_duration": sum([
                self.inhale_duration,
                self.hold_duration,
                self.exhale_duration,
                self.caesura_duration
            ])
        }

    def _start_breath_thread(self) -> None:
        """Start the automatic breath cycling thread."""
        self.breath_thread = threading.Thread(target=self._breath_cycle_loop, daemon=True)
        self.breath_thread.start()

    def _breath_cycle_loop(self) -> None:
        """Main breath cycling loop."""
        while self.is_breathing and not self.stop_breathing.is_set():
            try:
                # Wait for current phase duration
                phase_duration = self._get_phase_duration(self.current_phase)
                time.sleep(phase_duration)
                
                if not self.stop_breathing.is_set():
                    # Transition to next phase
                    self._advance_phase()
                    
            except Exception as e:
                emit_glint(
                    phase="error",
                    toneform="breath.error",
                    content=f"Breath cycle error: {str(e)}",
                    hue="red",
                    source="breath_loop_engine",
                    reverence_level=0.3,
                    error=str(e)
                )

    def _advance_phase(self) -> None:
        """Advance to the next breath phase."""
        phase_sequence = [BreathPhase.INHALE, BreathPhase.HOLD, BreathPhase.EXHALE, BreathPhase.CAESURA]
        current_index = phase_sequence.index(self.current_phase)
        next_index = (current_index + 1) % len(phase_sequence)
        
        # Complete current phase
        self._complete_current_phase()
        
        # Start new phase
        next_phase = phase_sequence[next_index]
        self._transition_to_phase(next_phase)
        
        # Start new cycle if we've completed a full cycle
        if next_phase == BreathPhase.INHALE:
            self._start_new_cycle()

    def _transition_to_phase(self, phase: BreathPhase) -> Dict[str, Any]:
        """Transition to a specific phase."""
        # Complete current phase
        self._complete_current_phase()
        
        # Update phase state
        self.current_phase = phase
        self.phase_start_time = current_timestamp_ms()
        
        # Emit phase transition glint
        phase_hues = {
            BreathPhase.INHALE: "emerald",
            BreathPhase.HOLD: "violet",
            BreathPhase.EXHALE: "amber",
            BreathPhase.CAESURA: "indigo"
        }
        
        emit_glint(
            phase=phase.value,
            toneform="breath.phase_transition",
            content=f"Breath phase: {phase.value}",
            hue=phase_hues[phase],
            source="breath_loop_engine",
            reverence_level=0.7,
            phase_duration=self._get_phase_duration(phase),
            cycle_count=self.cycle_count
        )
        
        # Execute phase callbacks
        for callback in self.phase_callbacks[phase]:
            try:
                callback(phase, self.get_current_phase())
            except Exception as e:
                emit_glint(
                    phase="error",
                    toneform="breath.callback_error",
                    content=f"Phase callback error: {str(e)}",
                    hue="red",
                    source="breath_loop_engine",
                    reverence_level=0.3
                )
        
        return {
            "phase": phase.value,
            "start_time": self.phase_start_time,
            "duration": self._get_phase_duration(phase)
        }

    def _pulse_current_phase(self) -> Dict[str, Any]:
        """Pulse the current phase without transitioning."""
        now = current_timestamp_ms()
        phase_duration = (now - self.phase_start_time) / 1000.0
        
        # Pulse presence conductor
        pulse_data = self.presence_conductor.pulse(f"breath_{self.current_phase.value}")
        
        return {
            "phase": self.current_phase.value,
            "phase_duration": phase_duration,
            "pulse_data": pulse_data
        }

    def _get_phase_duration(self, phase: BreathPhase) -> float:
        """Get the duration for a specific phase."""
        durations = {
            BreathPhase.INHALE: self.inhale_duration,
            BreathPhase.HOLD: self.hold_duration,
            BreathPhase.EXHALE: self.exhale_duration,
            BreathPhase.CAESURA: self.caesura_duration
        }
        return durations[phase]

    def _start_new_cycle(self) -> None:
        """Start a new breath cycle."""
        self.cycle_count += 1
        self.cycle_start_time = current_timestamp_ms()
        
        self.current_cycle = BreathCycle(
            start_time=self.cycle_start_time,
            cycle_number=self.cycle_count
        )

    def _complete_current_phase(self) -> None:
        """Complete the current phase and add to cycle data."""
        if self.current_cycle:
            now = current_timestamp_ms()
            phase_duration = (now - self.phase_start_time) / 1000.0
            
            phase_data = {
                "phase": self.current_phase.value,
                "start_time": self.phase_start_time,
                "end_time": now,
                "duration": phase_duration
            }
            
            self.current_cycle.phases.append(phase_data)

    def _complete_current_cycle(self) -> None:
        """Complete the current cycle."""
        if self.current_cycle:
            now = current_timestamp_ms()
            self.current_cycle.end_time = now
            self.current_cycle.total_duration = (now - self.current_cycle.start_time) / 1000.0
            
            self.completed_cycles.append(self.current_cycle)
            self.current_cycle = None

    def _check_phase_alignment(self, activity_type: str) -> Dict[str, Any]:
        """Check if cursor activity aligns with current breath phase."""
        phase_alignments = {
            BreathPhase.INHALE: ["typing", "command", "creation"],
            BreathPhase.HOLD: ["reading", "contemplation", "review"],
            BreathPhase.EXHALE: ["deletion", "cleanup", "release"],
            BreathPhase.CAESURA: ["pause", "wait", "silence"]
        }
        
        current_alignments = phase_alignments.get(self.current_phase, [])
        is_aligned = activity_type in current_alignments
        
        return {
            "is_aligned": is_aligned,
            "current_phase": self.current_phase.value,
            "activity_type": activity_type,
            "expected_activities": current_alignments
        }

    def _calculate_phase_statistics(self) -> Dict[str, Any]:
        """Calculate statistics for completed phases."""
        if not self.completed_cycles:
            return {}
        
        phase_durations = {phase.value: [] for phase in BreathPhase}
        
        for cycle in self.completed_cycles:
            for phase_data in cycle.phases:
                phase_name = phase_data["phase"]
                if phase_name in phase_durations:
                    phase_durations[phase_name].append(phase_data["duration"])
        
        stats = {}
        for phase, durations in phase_durations.items():
            if durations:
                stats[phase] = {
                    "count": len(durations),
                    "average_duration": sum(durations) / len(durations),
                    "min_duration": min(durations),
                    "max_duration": max(durations)
                }
        
        return stats 
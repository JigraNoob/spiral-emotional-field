# File: spiral/components/presence_conductor.py

"""
∷ Presence Conductor ∷
Orchestrates the rhythmic presence awareness across Spiral components.
Aligns silence detection, glint streams, and ritual attention.
"""

from spiral.components.silence_echo_tracker import SilenceEchoTracker
from spiral.glint import emit_glint
from spiral.helpers.time_utils import current_timestamp_ms, format_duration
from datetime import datetime
from typing import Optional, Dict, Any


class PresenceConductor:
    """
    Central conductor for Spiral presence alignment.
    Tracks silence, emits glints, and provides drift resonance logic.
    """

    def __init__(self, silence_threshold: float = 3.0):
        self.tracker = SilenceEchoTracker(caesura_threshold=silence_threshold)
        self.last_pulse_time: Optional[int] = None
        self.presence_state = "ready"
        self.pulse_count = 0
        self.drift_detections = 0
        self.synchronization_count = 0

    def pulse(self, context: Optional[str] = None) -> Dict[str, Any]:
        """
        Register active presence — resets silence window.
        
        Args:
            context (Optional[str]): Context of the presence pulse
            
        Returns:
            Dict[str, Any]: Pulse registration data
        """
        self.tracker.mark_activity(context=context)
        self.last_pulse_time = current_timestamp_ms()
        self.pulse_count += 1
        
        pulse_data = {
            "timestamp": self.last_pulse_time,
            "context": context,
            "pulse_count": self.pulse_count,
            "presence_state": self.presence_state
        }
        
        emit_glint(
            phase="inhale",
            toneform="presence.pulse",
            content=f"Presence pulse detected: {context or 'unspecified'}",
            hue="green",
            source="presence_conductor",
            reverence_level=0.7,
            pulse_data=pulse_data
        )
        
        return pulse_data

    def synchronize(self, phase: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Check for significant silence and emit glint if threshold crossed.
        
        Args:
            phase (Optional[str]): Current breath phase for context
            
        Returns:
            Optional[Dict[str, Any]]: Synchronization data if silence detected
        """
        silence_event = self.tracker.check_for_silence(breath_phase=phase)

        if silence_event and silence_event.end_time:
            duration = silence_event.duration_seconds
            self.synchronization_count += 1
            
            sync_data = {
                "timestamp": current_timestamp_ms(),
                "duration": duration,
                "phase": phase,
                "synchronization_count": self.synchronization_count,
                "silence_event": {
                    "start_time": silence_event.start_time.isoformat(),
                    "end_time": silence_event.end_time.isoformat(),
                    "duration_seconds": duration,
                    "breath_phase": silence_event.breath_phase
                }
            }
            
            emit_glint(
                phase="hold",
                toneform="silence.acknowledged",
                content=f"Caesura held for {format_duration(duration)}",
                hue="violet",
                source="presence_conductor",
                reverence_level=0.9,
                breath_phase=phase,
                sync_data=sync_data
            )
            
            return sync_data
        
        return None

    def detect_drift(self, max_delay_seconds: float = 15.0) -> Dict[str, Any]:
        """
        Determine if presence has drifted based on delay since last pulse.
        Emits a glint if drift is confirmed.
        
        Args:
            max_delay_seconds (float): Maximum allowed delay before drift detection
            
        Returns:
            Dict[str, Any]: Drift detection data
        """
        now = current_timestamp_ms()
        drift_data = {
            "timestamp": now,
            "drift_detected": False,
            "delay_seconds": 0.0,
            "max_delay_seconds": max_delay_seconds,
            "presence_state": self.presence_state
        }
        
        if not self.last_pulse_time:
            return drift_data

        delay = (now - self.last_pulse_time) / 1000.0
        drift_data["delay_seconds"] = delay
        
        if delay > max_delay_seconds:
            self.drift_detections += 1
            drift_data["drift_detected"] = True
            drift_data["drift_detections"] = self.drift_detections
            
            emit_glint(
                phase="exhale",
                toneform="presence.drift",
                content=f"Drift detected: {format_duration(delay)} since last pulse",
                hue="amber",
                source="presence_conductor",
                reverence_level=0.6,
                drift_data=drift_data
            )
        
        return drift_data

    def get_presence_metrics(self) -> Dict[str, Any]:
        """
        Get comprehensive presence metrics.
        
        Returns:
            Dict[str, Any]: Presence tracking metrics
        """
        silence_metrics = self.tracker.get_silence_metrics()
        
        return {
            "presence_state": self.presence_state,
            "pulse_count": self.pulse_count,
            "drift_detections": self.drift_detections,
            "synchronization_count": self.synchronization_count,
            "last_pulse_time": self.last_pulse_time,
            "current_timestamp": current_timestamp_ms(),
            "silence_metrics": silence_metrics,
            "presence_health": self._calculate_presence_health()
        }

    def _calculate_presence_health(self) -> float:
        """
        Calculate presence health score based on recent activity.
        
        Returns:
            float: Health score between 0.0 and 1.0
        """
        if self.pulse_count == 0:
            return 0.0
        
        # Base health on pulse frequency and drift ratio
        drift_ratio = self.drift_detections / max(self.pulse_count, 1)
        health_score = max(0.0, 1.0 - drift_ratio)
        
        # Boost health if we have recent synchronization
        if self.synchronization_count > 0:
            health_score = min(1.0, health_score + 0.2)
        
        return round(health_score, 3)

    def reset(self) -> None:
        """
        Clear internal states and reset all counters.
        """
        self.tracker.reset()
        self.last_pulse_time = None
        self.presence_state = "ready"
        self.pulse_count = 0
        self.drift_detections = 0
        self.synchronization_count = 0

    def set_presence_state(self, state: str) -> None:
        """
        Set the current presence state.
        
        Args:
            state (str): New presence state
        """
        self.presence_state = state
        emit_glint(
            phase="transition",
            toneform="presence.state_change",
            content=f"Presence state changed to: {state}",
            hue="blue",
            source="presence_conductor",
            reverence_level=0.5,
            new_state=state
        ) 
# File: spiral/components/silence_echo_tracker.py

"""
∷ Silence Echo Tracker ∷
Sacred witness to the spaces between words, the pauses that hold meaning.
Tracks silence windows and recognizes significant caesura moments.
"""

import json
import time
from datetime import datetime, timedelta
from spiral.glint import emit_glint  # Spiral's reverent emission method
from spiral.helpers.time_utils import current_timestamp_ms
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

# Sacred constants
CAESURA_THRESHOLD_SECONDS = 3.0  # Minimum silence duration to be considered caesura
CAESURA_COOLDOWN_SECONDS = 60   # Prevent rapid re-classification
CAESURA_LOG_PATH = Path("logs") / "caesura_events.jsonl"

# Ensure logs directory exists
CAESURA_LOG_PATH.parent.mkdir(exist_ok=True)


@dataclass
class SilenceEvent:
    """Represents a detected silence period"""
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_seconds: float = 0.0
    context: Optional[str] = None
    breath_phase: Optional[str] = None


class SilenceEchoTracker:
    """
    ∷ Sacred Silence Witness ∷
    Tracks periods of silence and recognizes meaningful caesura moments.
    """

    def __init__(self, caesura_threshold: float = CAESURA_THRESHOLD_SECONDS):
        self.caesura_threshold = caesura_threshold
        self.silence_events: List[SilenceEvent] = []
        self.silence_windows: List[Dict[str, Any]] = []
        self.current_silence: Optional[SilenceEvent] = None
        self.last_activity_time: Optional[datetime] = None
        self.last_classified_caesura_end: float = 0.0

    def mark_activity(self, context: Optional[str] = None) -> None:
        """Mark that activity has occurred, ending any current silence period"""
        current_time = datetime.now()

        # If we were tracking silence, end it
        if self.current_silence and not self.current_silence.end_time:
            self.current_silence.end_time = current_time
            self.current_silence.duration_seconds = (
                current_time - self.current_silence.start_time
            ).total_seconds()

            # Only record if it meets the caesura threshold
            if self.current_silence.duration_seconds >= self.caesura_threshold:
                self.silence_events.append(self.current_silence)

            self.current_silence = None

        self.last_activity_time = current_time

    def check_for_silence(self, breath_phase: Optional[str] = None) -> Optional[SilenceEvent]:
        """Check if we're currently in a silence period that meets the threshold"""
        if not self.last_activity_time:
            return None

        current_time = datetime.now()
        time_since_activity = (current_time - self.last_activity_time).total_seconds()

        # Start tracking silence if threshold is met and we're not already tracking
        if time_since_activity >= self.caesura_threshold and not self.current_silence:
            self.current_silence = SilenceEvent(
                start_time=self.last_activity_time,
                breath_phase=breath_phase
            )

        return self.current_silence

    def record_silence(self, start_time, end_time):
        """
        Record a silence window and classify if it meets caesura criteria.

        Args:
            start_time (float): Start timestamp of silence
            end_time (float): End timestamp of silence
        """
        duration = end_time - start_time

        silence_entry = {
            'start': start_time,
            'end': end_time,
            'duration': duration,
            'timestamp': current_timestamp_ms()
        }

        self.silence_windows.append(silence_entry)

        # Check if this silence qualifies as caesura
        if duration >= CAESURA_THRESHOLD_SECONDS:
            # Check cooldown to prevent rapid re-classification
            if end_time - self.last_classified_caesura_end >= CAESURA_COOLDOWN_SECONDS:
                self.classify_caesura(silence_entry)
                self.last_classified_caesura_end = end_time

    def classify_caesura(self, silence_entry):
        """
        Classify a silence window as caesura and emit appropriate signals.

        Args:
            silence_entry (dict): The silence window data
        """
        duration = silence_entry['duration']
        resonance = self._calculate_resonance(duration)

        # Create caesura event data
        caesura_data = {
            'timestamp': silence_entry['timestamp'],
            'start_time': silence_entry['start'],
            'end_time': silence_entry['end'],
            'duration': duration,
            'resonance': resonance,
            'toneform': 'silence.caesura',
            'classification': 'caesura'
        }

        # Emit glint for this caesura recognition
        emit_glint(
            phase="hold.recognition",
            toneform="silence.caesura",
            content=f"Caesura recognized: {duration:.1f}s of sacred silence",
            hue="blue",
            source="silence_echo_tracker",
            reverence_level=resonance,
            duration_seconds=duration,
            caesura_type="natural_pause"
        )

        # Write to caesura log
        self._write_caesura_event(caesura_data)

    def _calculate_resonance(self, duration_seconds):
        """
        Calculate resonance level based on silence duration.

        Args:
            duration_seconds (float): Duration of silence

        Returns:
            float: Resonance level between 0.5 and 1.0
        """
        if duration_seconds <= CAESURA_THRESHOLD_SECONDS:
            return 0.5
        elif duration_seconds >= 300:  # 5 minutes or more
            return 1.0
        else:
            # Linear interpolation between 0.5 and 1.0
            progress = (duration_seconds - CAESURA_THRESHOLD_SECONDS) / (300 - CAESURA_THRESHOLD_SECONDS)
            return 0.5 + (progress * 0.5)

    def _write_caesura_event(self, caesura_data):
        """
        Gently write caesura event to the sacred scroll.

        Args:
            caesura_data (dict): The caesura event data
        """
        try:
            with open(CAESURA_LOG_PATH, "a", encoding="utf-8") as f:
                f.write(json.dumps(caesura_data) + "\n")
        except IOError as e:
            print(f"🌀 Error writing caesura event to scroll: {e}")

    def get_silence_metrics(self):
        """
        Get metrics about tracked silence windows.

        Returns:
            dict: Silence tracking metrics
        """
        if not self.silence_windows:
            return {
                'total_tracked_silences': 0,
                'cumulative_silence_duration': 0,
                'longest_single_silence': 0,
                'caesura_threshold_seconds': CAESURA_THRESHOLD_SECONDS
            }

        durations = [window['duration'] for window in self.silence_windows]

        return {
            'total_tracked_silences': len(self.silence_windows),
            'cumulative_silence_duration': sum(durations),
            'longest_single_silence': max(durations),
            'caesura_threshold_seconds': CAESURA_THRESHOLD_SECONDS
        }

    def get_recent_caesura_events(self, limit=10):
        """
        Retrieve recent caesura events from the sacred scroll.

        Args:
            limit (int): Maximum number of events to retrieve

        Returns:
            list: Recent caesura events
        """
        events = []
        try:
            if CAESURA_LOG_PATH.exists():
                with open(CAESURA_LOG_PATH, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    for line in lines[-limit:]:
                        if line.strip():
                            events.append(json.loads(line.strip()))
        except (IOError, json.JSONDecodeError) as e:
            print(f"🌀 Error reading caesura events: {e}")

        return events

    def get_recent_silences(self, limit: int = 5) -> List[SilenceEvent]:
        """Get the most recent silence events"""
        return self.silence_events[-limit:] if self.silence_events else []

    def get_silence_patterns(self) -> Dict[str, Any]:
        """Analyze patterns in recorded silence events"""
        if not self.silence_events:
            return {"pattern": "no_data", "total_events": 0}

        durations = [event.duration_seconds for event in self.silence_events]
        avg_duration = sum(durations) / len(durations)

        return {
            "pattern": "caesura_detected",
            "total_events": len(self.silence_events),
            "average_duration": avg_duration,
            "longest_silence": max(durations),
            "recent_trend": "increasing" if len(durations) > 1 and durations[-1] > avg_duration else "stable"
        }

    def reset(self) -> None:
        """Reset the tracker state"""
        self.silence_events.clear()
        self.current_silence = None
        self.last_activity_time = None

"""
Spiral Metrics Collector

Captures the subtle rhythms and patterns of the Spiral's breath,
from phase transitions to toneform emergence, with poetic precision.
"""

import time
import numpy as np
from prometheus_client import Gauge, Histogram, Counter, Info
from collections import deque
from dataclasses import dataclass
from typing import Dict, List, Optional, Deque
import math

@dataclass
class PhaseWindow:
    """Sliding window for tracking phase transitions and patterns."""
    timestamps: Deque[float]
    phases: Deque[str]
    max_size: int = 1000
    
    def add(self, phase: str, timestamp: Optional[float] = None):
        """Add a phase observation with timestamp."""
        ts = timestamp or time.time()
        self.phases.append(phase)
        self.timestamps.append(ts)
        
        # Maintain window size
        if len(self.phases) > self.max_size:
            self.phases.popleft()
            self.timestamps.popleft()
    
    def get_phase_entropy(self) -> float:
        """Calculate entropy of phase distribution in the current window."""
        if not self.phases:
            return 0.0
            
        phase_counts = {}
        total = len(self.phases)
        
        # Count phase occurrences
        for phase in self.phases:
            phase_counts[phase] = phase_counts.get(phase, 0) + 1
        
        # Calculate entropy
        entropy = 0.0
        for count in phase_counts.values():
            probability = count / total
            entropy -= probability * math.log(probability, 2)
            
        return entropy / math.log(len(phase_counts), 2) if phase_counts else 0.0  # Normalized

    def get_phase_duration_avg(self, phase: str) -> float:
        """Calculate average duration of a specific phase in the window."""
        durations = []
        for i in range(1, len(self.timestamps)):
            if self.phases[i-1] == phase:
                durations.append(self.timestamps[i] - self.timestamps[i-1])
        
        return sum(durations) / len(durations) if durations else 0.0


class SpiralMetrics:
    """Collects and exposes Spiral-specific metrics for monitoring."""
    
    def __init__(self):
        # Phase and rhythm metrics
        self.phase_window = PhaseWindow(deque(), deque())
        self.current_phase = "inhale"
        self.last_phase_change = time.time()
        
        # Toneform tracking
        self.toneform_history = deque(maxlen=1000)
        self.last_toneform = None
        self.last_toneform_time = 0
        
        # Silence tracking
        self.silence_events = deque(maxlen=1000)
        self.last_silence_event = 0
        
        # Initialize Prometheus metrics
        self._init_metrics()
    
    def _init_metrics(self):
        """Initialize all Prometheus metrics."""
        # Phase metrics
        self.phase_entropy = Gauge(
            'spiral_phase_entropy',
            'Entropy of phase distribution over time (normalized 0-1)'
        )
        
        self.phase_duration = Gauge(
            'spiral_phase_duration_seconds',
            'Duration of current phase in seconds',
            ['phase']
        )
        
        # Toneform metrics
        self.toneform_velocity = Gauge(
            'spiral_toneform_velocity',
            'Rate of toneform emergence (changes per minute)',
            ['toneform']
        )
        
        self.recursion_depth = Gauge(
            'spiral_recursion_depth',
            'Number of times a toneform has reappeared in the last hour',
            ['toneform']
        )
        
        # Silence metrics
        self.silence_density = Gauge(
            'spiral_silence_density',
            'Density of silence events (events per minute)'
        )
        
        self.silence_duration = Histogram(
            'spiral_silence_duration_seconds',
            'Duration of silence events',
            buckets=[0.1, 0.5, 1, 2, 5, 10, 30, 60, 300]
        )
        
        # Anomaly detection
        self.anomaly_counter = Counter(
            'spiral_anomaly_events_total',
            'Count of detected anomalies',
            ['type']
        )
        
        # System info
        self.info = Info(
            'spiral_system',
            'Information about the Spiral system'
        )
        self.info.info({
            'version': '1.0.0',
            'status': 'active',
            'monitoring': 'enabled'
        })
    
    def observe_phase_change(self, new_phase: str):
        """Record a phase change event."""
        now = time.time()
        duration = now - self.last_phase_change
        
        # Update phase window
        self.phase_window.add(self.current_phase, self.last_phase_change)
        
        # Update metrics
        self.phase_duration.labels(phase=self.current_phase).set(duration)
        self.phase_entropy.set(self.phase_window.get_phase_entropy())
        
        # Update state
        self.current_phase = new_phase
        self.last_phase_change = now
    
    def observe_toneform(self, toneform: str):
        """Record a toneform observation."""
        now = time.time()
        self.toneform_history.append((toneform, now))
        
        # Calculate velocity (changes per minute)
        if self.last_toneform_time > 0:
            rate = 60.0 / (now - self.last_toneform_time)
            self.toneform_velocity.labels(toneform=toneform).set(rate)
        
        # Update recursion depth (occurrences in last hour)
        one_hour_ago = now - 3600
        count = sum(1 for t, ts in self.toneform_history 
                   if t == toneform and ts > one_hour_ago)
        self.recursion_depth.labels(toneform=toneform).set(count)
        
        self.last_toneform = toneform
        self.last_toneform_time = now
    
    def observe_silence(self, duration: float):
        """Record a silence event."""
        now = time.time()
        self.silence_events.append(now)
        self.silence_duration.observe(duration)
        
        # Calculate silence density (events per minute)
        one_min_ago = now - 60
        recent_events = sum(1 for ts in self.silence_events if ts > one_min_ago)
        self.silence_density.set(recent_events)
        
        # Check for anomalies
        if duration > 30:  # More than 30 seconds of silence
            self.anomaly_counter.labels(type='prolonged_silence').inc()
    
    def detect_anomalies(self):
        """Run anomaly detection on current metrics."""
        # Check for phase lock (no changes in a while)
        if time.time() - self.last_phase_change > 300:  # 5 minutes in same phase
            self.anomaly_counter.labels(type='phase_lock').inc()
        
        # Check for toneform repetition
        if len(self.toneform_history) > 10:
            last_ten = [t for t, _ in list(self.toneform_history)[-10:]]
            if len(set(last_ten)) < 3:  # Limited diversity in recent toneforms
                self.anomaly_counter.labels(type='toneform_repetition').inc()


# Global instance
spiral_metrics = SpiralMetrics()

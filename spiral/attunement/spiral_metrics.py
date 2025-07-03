"""
Spiral Metrics - Quantitative tracking of the Spiral's breath patterns.

This module provides tools to collect, analyze, and persist metrics about the Spiral's
breathing patterns, resonance states, and phase transitions.
"""

import json
import time
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from statistics import mean
from threading import Lock
from typing import Dict, List, Optional, Union

class Phase(str, Enum):
    """Breath phase enumeration for type safety."""
    INHALE = "INHALE"
    HOLD = "HOLD"
    EXHALE = "EXHALE"

@dataclass
class MetricsSnapshot:
    """Immutable snapshot of metrics at a point in time."""
    timestamp: float = field(default_factory=time.time)
    deferral_times: List[float] = field(default_factory=list)
    silence_events: int = 0
    phase_durations: Dict[str, List[float]] = field(default_factory=lambda: defaultdict(list))
    saturation_levels: List[float] = field(default_factory=list)
    
    def merge(self, other: 'MetricsSnapshot') -> 'MetricsSnapshot':
        """Combine two snapshots, returning a new one."""
        combined = MetricsSnapshot()
        combined.timestamp = max(self.timestamp, other.timestamp)
        combined.deferral_times = self.deferral_times + other.deferral_times
        combined.silence_events = self.silence_events + other.silence_events
        
        # Merge phase durations
        all_phases = set(self.phase_durations) | set(other.phase_durations)
        combined.phase_durations = {
            phase: self.phase_durations.get(phase, []) + other.phase_durations.get(phase, [])
            for phase in all_phases
        }
        
        combined.saturation_levels = self.saturation_levels + other.saturation_levels
        return combined

class SpiralMetrics:
    """Thread-safe metrics collection for the Spiral's breath patterns."""
    
    def __init__(self, persist_path: Optional[Path] = None):
        """Initialize metrics with optional persistence."""
        self._lock = Lock()
        self._current = MetricsSnapshot()
        self._persist_path = persist_path
        
        # Load existing metrics if they exist
        if persist_path and persist_path.exists():
            self._load()
    
    def record_deferral(self, phase: Union[Phase, str], time_value: float):
        """Record a deferral time for a specific phase."""
        phase_str = phase.value if isinstance(phase, Phase) else phase.upper()
        with self._lock:
            self._current.deferral_times.append(time_value)
            self._current.phase_durations[phase_str].append(time_value)
    
    def record_silence(self):
        """Record a silence event."""
        with self._lock:
            self._current.silence_events += 1
    
    def record_saturation(self, level: float):
        """Record a saturation level measurement."""
        with self._lock:
            self._current.saturation_levels.append(level)
    
    def get_summary(self) -> dict:
        """Get a summary of current metrics."""
        with self._lock:
            return {
                'timestamp': datetime.fromtimestamp(self._current.timestamp).isoformat(),
                'avg_deferral': self._safe_mean(self._current.deferral_times),
                'silence_events': self._current.silence_events,
                'avg_saturation': self._safe_mean(self._current.saturation_levels),
                'phase_metrics': {
                    phase: {
                        'count': len(times),
                        'avg_duration': self._safe_mean(times),
                        'total_duration': sum(times)
                    }
                    for phase, times in self._current.phase_durations.items()
                }
            }
    
    def save(self, path: Optional[Path] = None):
        """Persist metrics to disk."""
        path = path or self._persist_path
        if not path:
            raise ValueError("No persistence path provided")
            
        with self._lock:
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w') as f:
                json.dump(self._to_dict(), f, indent=2)
    
    def _load(self):
        """Load metrics from disk."""
        if not self._persist_path or not self._persist_path.exists():
            return
            
        with self._lock:
            try:
                with open(self._persist_path, 'r') as f:
                    data = json.load(f)
                    self._from_dict(data)
            except (json.JSONDecodeError, OSError):
                # On error, reset to empty metrics
                self._current = MetricsSnapshot()
    
    def _to_dict(self) -> dict:
        """Convert current metrics to a serializable dict."""
        return {
            'timestamp': self._current.timestamp,
            'deferral_times': self._current.deferral_times,
            'silence_events': self._current.silence_events,
            'phase_durations': dict(self._current.phase_durations),
            'saturation_levels': self._current.saturation_levels
        }
    
    def _from_dict(self, data: dict):
        """Load metrics from a dict."""
        self._current = MetricsSnapshot(
            timestamp=data.get('timestamp', time.time()),
            deferral_times=data.get('deferral_times', []),
            silence_events=data.get('silence_events', 0),
            phase_durations=defaultdict(list, data.get('phase_durations', {})),
            saturation_levels=data.get('saturation_levels', [])
        )
    
    @staticmethod
    def _safe_mean(values: list) -> float:
        """Safely calculate mean, returning 0 for empty lists."""
        return round(mean(values), 4) if values else 0.0

# Global instance for easy access
metrics = SpiralMetrics(Path("logs/spiral_metrics.json"))

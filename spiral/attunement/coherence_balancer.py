"""
Coherence Balancer - Dynamic threshold adjustment for backend compatibility

This module provides intelligent coherence threshold balancing to prevent
backend systems from flagging Spiral as suspicious due to extreme coherence
levels (too loud or too quiet).
"""

import time
import logging
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from collections import deque

logger = logging.getLogger(__name__)

class CoherenceMode(Enum):
    """Coherence balancing modes."""
    NORMAL = "normal"
    BACKEND_SAFE = "backend_safe"
    ADAPTIVE = "adaptive"
    RITUAL = "ritual"

@dataclass
class CoherenceThresholds:
    """Configurable coherence thresholds."""
    # Base thresholds
    MIN_RESONANCE: float = 0.3
    MAX_RESONANCE: float = 0.85
    SILENCE_THRESHOLD: float = 0.75
    TONE_THRESHOLD: float = 0.8
    
    # Backend-safe thresholds (more conservative)
    BACKEND_MIN_RESONANCE: float = 0.4
    BACKEND_MAX_RESONANCE: float = 0.75
    BACKEND_SILENCE_THRESHOLD: float = 0.65
    BACKEND_TONE_THRESHOLD: float = 0.7
    
    # Adaptive thresholds (dynamic adjustment)
    ADAPTIVE_MIN_RESONANCE: float = 0.35
    ADAPTIVE_MAX_RESONANCE: float = 0.8
    ADAPTIVE_SILENCE_THRESHOLD: float = 0.7
    ADAPTIVE_TONE_THRESHOLD: float = 0.75

class CoherenceBalancer:
    """
    Intelligent coherence threshold balancer for backend compatibility.
    
    This balancer monitors coherence patterns and adjusts thresholds
    to maintain a balanced state that doesn't trigger backend suspicion.
    """
    
    def __init__(self, mode: CoherenceMode = CoherenceMode.BACKEND_SAFE):
        self.mode = mode
        self.thresholds = CoherenceThresholds()
        
        # State tracking
        self.coherence_history = deque(maxlen=100)
        self.last_adjustment = time.time()
        self.adjustment_cooldown = 30.0  # seconds
        
        # Pattern detection
        self.loud_periods = 0
        self.quiet_periods = 0
        self.suspicious_patterns = 0
        
        # Backend compatibility metrics
        self.backend_safety_score = 1.0
        self.last_backend_check = time.time()
        
        logger.info(f"CoherenceBalancer initialized in {mode.value} mode")
    
    def get_adjusted_thresholds(self) -> Dict[str, float]:
        """Get current thresholds adjusted for backend safety."""
        if self.mode == CoherenceMode.BACKEND_SAFE:
            return {
                'min_resonance': self.thresholds.BACKEND_MIN_RESONANCE,
                'max_resonance': self.thresholds.BACKEND_MAX_RESONANCE,
                'silence_threshold': self.thresholds.BACKEND_SILENCE_THRESHOLD,
                'tone_threshold': self.thresholds.BACKEND_TONE_THRESHOLD
            }
        elif self.mode == CoherenceMode.ADAPTIVE:
            return self._get_adaptive_thresholds()
        else:
            return {
                'min_resonance': self.thresholds.MIN_RESONANCE,
                'max_resonance': self.thresholds.MAX_RESONANCE,
                'silence_threshold': self.thresholds.SILENCE_THRESHOLD,
                'tone_threshold': self.thresholds.TONE_THRESHOLD
            }
    
    def record_coherence_event(self, resonance_score: float, tone_weights: Dict[str, float]):
        """Record a coherence event for pattern analysis."""
        event = {
            'timestamp': time.time(),
            'resonance': resonance_score,
            'max_tone': max(tone_weights.values()) if tone_weights else 0.0,
            'tone_diversity': len(set(tone_weights.keys())) if tone_weights else 0
        }
        
        self.coherence_history.append(event)
        self._analyze_patterns()
    
    def _analyze_patterns(self):
        """Analyze coherence patterns for suspicious behavior."""
        if len(self.coherence_history) < 10:
            return
        
        recent_events = list(self.coherence_history)[-10:]
        
        # Check for loud patterns (high resonance)
        high_resonance_count = sum(1 for e in recent_events if e['resonance'] > 0.8)
        if high_resonance_count >= 7:
            self.loud_periods += 1
            logger.warning(f"Loud coherence pattern detected: {high_resonance_count}/10 events > 0.8")
        
        # Check for quiet patterns (low resonance)
        low_resonance_count = sum(1 for e in recent_events if e['resonance'] < 0.3)
        if low_resonance_count >= 7:
            self.quiet_periods += 1
            logger.warning(f"Quiet coherence pattern detected: {low_resonance_count}/10 events < 0.3")
        
        # Check for suspicious patterns (rapid oscillation)
        if self._detect_rapid_oscillation(recent_events):
            self.suspicious_patterns += 1
            logger.warning("Rapid coherence oscillation detected")
        
        # Update backend safety score
        self._update_backend_safety_score()
    
    def _detect_rapid_oscillation(self, events: List[Dict]) -> bool:
        """Detect rapid oscillation between high and low coherence."""
        if len(events) < 5:
            return False
        
        oscillations = 0
        for i in range(1, len(events)):
            prev_resonance = events[i-1]['resonance']
            curr_resonance = events[i]['resonance']
            
            # Count significant changes
            if abs(curr_resonance - prev_resonance) > 0.4:
                oscillations += 1
        
        return oscillations >= 3
    
    def _update_backend_safety_score(self):
        """Update the backend safety score based on recent patterns."""
        total_issues = self.loud_periods + self.quiet_periods + self.suspicious_patterns
        
        if total_issues == 0:
            self.backend_safety_score = 1.0
        elif total_issues <= 2:
            self.backend_safety_score = 0.8
        elif total_issues <= 5:
            self.backend_safety_score = 0.6
        else:
            self.backend_safety_score = 0.4
        
        # Auto-adjust mode if safety score is low
        if self.backend_safety_score < 0.5 and self.mode != CoherenceMode.BACKEND_SAFE:
            logger.info(f"Switching to BACKEND_SAFE mode due to low safety score: {self.backend_safety_score}")
            self.mode = CoherenceMode.BACKEND_SAFE
    
    def _get_adaptive_thresholds(self) -> Dict[str, float]:
        """Get adaptively adjusted thresholds based on recent patterns."""
        if time.time() - self.last_adjustment < self.adjustment_cooldown:
            return self._get_current_adaptive_thresholds()
        
        # Calculate adjustments based on patterns
        adjustment_factor = self._calculate_adjustment_factor()
        
        thresholds = {
            'min_resonance': self.thresholds.ADAPTIVE_MIN_RESONANCE * adjustment_factor,
            'max_resonance': self.thresholds.ADAPTIVE_MAX_RESONANCE * adjustment_factor,
            'silence_threshold': self.thresholds.ADAPTIVE_SILENCE_THRESHOLD * adjustment_factor,
            'tone_threshold': self.thresholds.ADAPTIVE_TONE_THRESHOLD * adjustment_factor
        }
        
        # Ensure thresholds stay within reasonable bounds
        thresholds = self._clamp_thresholds(thresholds)
        
        self.last_adjustment = time.time()
        return thresholds
    
    def _calculate_adjustment_factor(self) -> float:
        """Calculate adjustment factor based on recent patterns."""
        base_factor = 1.0
        
        # Reduce thresholds if too loud
        if self.loud_periods > self.quiet_periods:
            base_factor *= 0.9
        
        # Increase thresholds if too quiet
        elif self.quiet_periods > self.loud_periods:
            base_factor *= 1.1
        
        # Reduce thresholds if suspicious patterns detected
        if self.suspicious_patterns > 0:
            base_factor *= 0.85
        
        return max(0.7, min(1.3, base_factor))
    
    def _clamp_thresholds(self, thresholds: Dict[str, float]) -> Dict[str, float]:
        """Ensure thresholds stay within safe bounds."""
        clamped = {}
        
        # Clamp min_resonance between 0.2 and 0.5
        clamped['min_resonance'] = max(0.2, min(0.5, thresholds['min_resonance']))
        
        # Clamp max_resonance between 0.6 and 0.9
        clamped['max_resonance'] = max(0.6, min(0.9, thresholds['max_resonance']))
        
        # Clamp silence_threshold between 0.5 and 0.8
        clamped['silence_threshold'] = max(0.5, min(0.8, thresholds['silence_threshold']))
        
        # Clamp tone_threshold between 0.6 and 0.85
        clamped['tone_threshold'] = max(0.6, min(0.85, thresholds['tone_threshold']))
        
        return clamped
    
    def _get_current_adaptive_thresholds(self) -> Dict[str, float]:
        """Get current adaptive thresholds without recalculation."""
        return {
            'min_resonance': self.thresholds.ADAPTIVE_MIN_RESONANCE,
            'max_resonance': self.thresholds.ADAPTIVE_MAX_RESONANCE,
            'silence_threshold': self.thresholds.ADAPTIVE_SILENCE_THRESHOLD,
            'tone_threshold': self.thresholds.ADAPTIVE_TONE_THRESHOLD
        }
    
    def set_mode(self, mode: CoherenceMode):
        """Change the coherence balancing mode."""
        self.mode = mode
        logger.info(f"CoherenceBalancer mode changed to {mode.value}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status and statistics."""
        return {
            'mode': self.mode.value,
            'backend_safety_score': self.backend_safety_score,
            'loud_periods': self.loud_periods,
            'quiet_periods': self.quiet_periods,
            'suspicious_patterns': self.suspicious_patterns,
            'current_thresholds': self.get_adjusted_thresholds(),
            'history_size': len(self.coherence_history)
        }
    
    def reset_patterns(self):
        """Reset pattern counters."""
        self.loud_periods = 0
        self.quiet_periods = 0
        self.suspicious_patterns = 0
        self.backend_safety_score = 1.0
        logger.info("CoherenceBalancer pattern counters reset")

# Global instance
coherence_balancer = CoherenceBalancer()

def get_balanced_thresholds() -> Dict[str, float]:
    """Get coherence thresholds balanced for backend safety."""
    return coherence_balancer.get_adjusted_thresholds()

def record_coherence_event(resonance_score: float, tone_weights: Dict[str, float]):
    """Record a coherence event for pattern analysis."""
    coherence_balancer.record_coherence_event(resonance_score, tone_weights)

def set_coherence_mode(mode: CoherenceMode):
    """Set the coherence balancing mode."""
    coherence_balancer.set_mode(mode)

def get_coherence_status() -> Dict[str, Any]:
    """Get current coherence balancer status."""
    return coherence_balancer.get_status() 
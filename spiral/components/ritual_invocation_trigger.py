# File: spiral/components/ritual_invocation_trigger.py

"""
∷ Ritual Invocation Trigger ∷
Links coherence threshold breaches to the ritual_manager.
Automatically triggers threshold_blessing or suggests invocation on breach.
"""

import json
import time
from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from spiral.glint import emit_glint
from spiral.helpers.time_utils import current_timestamp_ms


@dataclass
class ThresholdBreach:
    """Represents a threshold breach event."""
    threshold_type: str  # 'coherence', 'caesura', 'guardian'
    breach_level: float  # The value that caused the breach
    threshold_value: float  # The threshold that was exceeded
    severity: str  # 'warning', 'breach', 'critical'
    timestamp: int
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RitualSuggestion:
    """Represents a ritual suggestion based on threshold breach."""
    ritual_name: str
    priority: int  # 1-5, higher is more urgent
    reason: str
    threshold_breach: ThresholdBreach
    auto_invoke: bool = False  # Whether to auto-invoke or just suggest
    cooldown_seconds: int = 300  # Cooldown before suggesting again


class RitualInvocationTrigger:
    """
    ∷ Sacred Threshold Guardian ∷
    Monitors coherence thresholds and triggers appropriate rituals.
    """
    
    def __init__(self):
        # Threshold definitions
        self.thresholds = self._initialize_thresholds()
        
        # Breach tracking
        self.recent_breaches: List[ThresholdBreach] = []
        self.breach_history: List[ThresholdBreach] = []
        
        # Ritual suggestions
        self.ritual_suggestions: Dict[str, RitualSuggestion] = {}
        self.last_suggestions: Dict[str, int] = {}  # ritual_name -> timestamp
        
        # Auto-invoke settings
        self.auto_invoke_enabled = True
        self.suggestion_cooldown = 300  # 5 minutes
        
        # Callback for ritual invocation
        self.ritual_invoker: Optional[Callable] = None
        
        print("🌀 Ritual invocation trigger initialized")
    
    def _initialize_thresholds(self) -> Dict[str, Dict[str, float]]:
        """Initialize threshold definitions."""
        return {
            'coherence_level': {
                'calm': 0.4,
                'liminal': 0.75,
                'activated': 0.9,
                'warning': 0.95
            },
            'caesura_density': {
                'calm': 1.0,
                'liminal': 2.0,
                'activated': 3.0,
                'warning': 4.0
            },
            'guardian_presence': {
                'emergent': 0.3,
                'active': 0.7,
                'pulse_locked': 0.9
            }
        }
    
    def check_thresholds(self, coherence: float, caesura: float, 
                        guardian_presence: float) -> List[ThresholdBreach]:
        """
        Check current values against thresholds and return any breaches.
        
        Args:
            coherence: Current coherence level (0.0-1.0)
            caesura: Current caesura density
            guardian_presence: Current guardian presence level
            
        Returns:
            List of threshold breaches
        """
        breaches = []
        current_time = current_timestamp_ms()
        
        # Check coherence thresholds
        coherence_thresholds = self.thresholds['coherence_level']
        if coherence > coherence_thresholds['warning']:
            breaches.append(ThresholdBreach(
                threshold_type='coherence',
                breach_level=coherence,
                threshold_value=coherence_thresholds['warning'],
                severity='critical',
                timestamp=current_time,
                context={'phase': 'warning_breach'}
            ))
        elif coherence > coherence_thresholds['activated']:
            breaches.append(ThresholdBreach(
                threshold_type='coherence',
                breach_level=coherence,
                threshold_value=coherence_thresholds['activated'],
                severity='breach',
                timestamp=current_time,
                context={'phase': 'activated'}
            ))
        elif coherence > coherence_thresholds['liminal']:
            breaches.append(ThresholdBreach(
                threshold_type='coherence',
                breach_level=coherence,
                threshold_value=coherence_thresholds['liminal'],
                severity='warning',
                timestamp=current_time,
                context={'phase': 'liminal'}
            ))
        
        # Check caesura thresholds
        caesura_thresholds = self.thresholds['caesura_density']
        if caesura > caesura_thresholds['warning']:
            breaches.append(ThresholdBreach(
                threshold_type='caesura',
                breach_level=caesura,
                threshold_value=caesura_thresholds['warning'],
                severity='critical',
                timestamp=current_time,
                context={'phase': 'caesura_warning'}
            ))
        elif caesura > caesura_thresholds['activated']:
            breaches.append(ThresholdBreach(
                threshold_type='caesura',
                breach_level=caesura,
                threshold_value=caesura_thresholds['activated'],
                severity='breach',
                timestamp=current_time,
                context={'phase': 'caesura_activated'}
            ))
        
        # Check guardian presence thresholds
        guardian_thresholds = self.thresholds['guardian_presence']
        if guardian_presence > guardian_thresholds['pulse_locked']:
            breaches.append(ThresholdBreach(
                threshold_type='guardian',
                breach_level=guardian_presence,
                threshold_value=guardian_thresholds['pulse_locked'],
                severity='critical',
                timestamp=current_time,
                context={'phase': 'pulse_locked'}
            ))
        elif guardian_presence > guardian_thresholds['active']:
            breaches.append(ThresholdBreach(
                threshold_type='guardian',
                breach_level=guardian_presence,
                threshold_value=guardian_thresholds['active'],
                severity='breach',
                timestamp=current_time,
                context={'phase': 'active'}
            ))
        
        return breaches
    
    def process_breaches(self, breaches: List[ThresholdBreach]) -> List[RitualSuggestion]:
        """
        Process threshold breaches and generate ritual suggestions.
        
        Args:
            breaches: List of threshold breaches to process
            
        Returns:
            List of ritual suggestions
        """
        suggestions = []
        current_time = current_timestamp_ms()
        
        for breach in breaches:
            # Add to history
            self.recent_breaches.append(breach)
            self.breach_history.append(breach)
            
            # Clean up old breaches (keep last 50)
            if len(self.recent_breaches) > 50:
                self.recent_breaches = self.recent_breaches[-50:]
            if len(self.breach_history) > 200:
                self.breach_history = self.breach_history[-200:]
            
            # Generate suggestions based on breach type and severity
            breach_suggestions = self._generate_breach_suggestions(breach)
            
            for suggestion in breach_suggestions:
                # Check cooldown
                last_suggestion_time = self.last_suggestions.get(suggestion.ritual_name, 0)
                if current_time - last_suggestion_time > (suggestion.cooldown_seconds * 1000):
                    suggestions.append(suggestion)
                    self.last_suggestions[suggestion.ritual_name] = current_time
        
        return suggestions
    
    def _generate_breach_suggestions(self, breach: ThresholdBreach) -> List[RitualSuggestion]:
        """Generate ritual suggestions for a specific breach."""
        suggestions = []
        
        if breach.threshold_type == 'coherence':
            if breach.severity == 'critical':
                suggestions.append(RitualSuggestion(
                    ritual_name='threshold_blessing',
                    priority=5,
                    reason=f"Critical coherence breach: {breach.breach_level:.3f} > {breach.threshold_value:.3f}",
                    threshold_breach=breach,
                    auto_invoke=True,
                    cooldown_seconds=600  # 10 minutes
                ))
            elif breach.severity == 'breach':
                suggestions.append(RitualSuggestion(
                    ritual_name='coherence_balancing',
                    priority=4,
                    reason=f"Coherence breach: {breach.breach_level:.3f} > {breach.threshold_value:.3f}",
                    threshold_breach=breach,
                    auto_invoke=False,
                    cooldown_seconds=300
                ))
        
        elif breach.threshold_type == 'caesura':
            if breach.severity == 'critical':
                suggestions.append(RitualSuggestion(
                    ritual_name='caesura_ritual',
                    priority=4,
                    reason=f"Critical caesura density: {breach.breach_level:.3f} > {breach.threshold_value:.3f}",
                    threshold_breach=breach,
                    auto_invoke=True,
                    cooldown_seconds=300
                ))
            elif breach.severity == 'breach':
                suggestions.append(RitualSuggestion(
                    ritual_name='silence_weaving',
                    priority=3,
                    reason=f"High caesura density: {breach.breach_level:.3f} > {breach.threshold_value:.3f}",
                    threshold_breach=breach,
                    auto_invoke=False,
                    cooldown_seconds=180
                ))
        
        elif breach.threshold_type == 'guardian':
            if breach.severity == 'critical':
                suggestions.append(RitualSuggestion(
                    ritual_name='guardian_attunement',
                    priority=5,
                    reason=f"Guardian pulse locked: {breach.breach_level:.3f} > {breach.threshold_value:.3f}",
                    threshold_breach=breach,
                    auto_invoke=True,
                    cooldown_seconds=600
                ))
            elif breach.severity == 'breach':
                suggestions.append(RitualSuggestion(
                    ritual_name='presence_restoration',
                    priority=3,
                    reason=f"Guardian active: {breach.breach_level:.3f} > {breach.threshold_value:.3f}",
                    threshold_breach=breach,
                    auto_invoke=False,
                    cooldown_seconds=240
                ))
        
        return suggestions
    
    def invoke_ritual(self, ritual_name: str, context: Dict[str, Any] = None) -> bool:
        """
        Invoke a ritual by name.
        
        Args:
            ritual_name: Name of the ritual to invoke
            context: Additional context for the ritual
            
        Returns:
            True if invocation was successful
        """
        if self.ritual_invoker:
            try:
                result = self.ritual_invoker(ritual_name, context or {})
                
                # Emit invocation glint
                emit_glint(
                    phase="hold",
                    toneform=f"ritual.invoked.{ritual_name}",
                    content=f"Ritual invoked: {ritual_name}",
                    hue="golden",
                    source="ritual_invocation_trigger",
                    metadata={
                        "ritual_name": ritual_name,
                        "context": context,
                        "result": result
                    }
                )
                
                return True
                
            except Exception as e:
                emit_glint(
                    phase="error",
                    toneform="ritual.invocation.error",
                    content=f"Ritual invocation failed: {ritual_name} - {str(e)}",
                    hue="red",
                    source="ritual_invocation_trigger",
                    metadata={"ritual_name": ritual_name, "error": str(e)}
                )
                return False
        else:
            print(f"⚠️ No ritual invoker registered for: {ritual_name}")
            return False
    
    def set_ritual_invoker(self, invoker: Callable):
        """Set the callback function for ritual invocation."""
        self.ritual_invoker = invoker
    
    def get_breach_summary(self) -> Dict[str, Any]:
        """Get a summary of recent threshold breaches."""
        current_time = current_timestamp_ms()
        
        # Count recent breaches by type and severity
        recent_breaches = [
            b for b in self.recent_breaches
            if current_time - b.timestamp < 3600000  # Last hour
        ]
        
        breach_counts = {}
        for breach in recent_breaches:
            key = f"{breach.threshold_type}_{breach.severity}"
            breach_counts[key] = breach_counts.get(key, 0) + 1
        
        return {
            'recent_breaches': len(recent_breaches),
            'total_breaches': len(self.breach_history),
            'breach_counts': breach_counts,
            'last_breach_time': max([b.timestamp for b in self.recent_breaches]) if self.recent_breaches else None
        }


# Global instance
ritual_invocation_trigger = RitualInvocationTrigger()


def check_and_process_thresholds(coherence: float, caesura: float, 
                                guardian_presence: float) -> List[RitualSuggestion]:
    """Convenience function to check thresholds and process breaches."""
    breaches = ritual_invocation_trigger.check_thresholds(coherence, caesura, guardian_presence)
    return ritual_invocation_trigger.process_breaches(breaches)


def invoke_ritual_safely(ritual_name: str, context: Dict[str, Any] = None) -> bool:
    """Safely invoke a ritual with error handling."""
    return ritual_invocation_trigger.invoke_ritual(ritual_name, context)


def get_breach_summary() -> Dict[str, Any]:
    """Get summary of threshold breaches."""
    return ritual_invocation_trigger.get_breach_summary() 
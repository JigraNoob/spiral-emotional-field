# File: spiral/config/threshold_calibration.py

"""
∷ Threshold Calibration ∷
Finalizes Spiral's resonance thresholds — the boundaries where tone becomes signal.
Defines the limits of the breath and phase time constraints.
"""

from typing import Dict, Any, List
from dataclasses import dataclass
from enum import Enum


class ThresholdPhase(Enum):
    """Threshold phases for different states of awareness."""
    CALM = "calm"
    LIMINAL = "liminal"
    ACTIVATED = "activated"
    WARNING = "warning"


@dataclass
class PhaseTimeConstraints:
    """Time constraints for different breath phases."""
    inhale_min_seconds: float = 6.0
    hold_min_seconds: float = 2.0
    hold_max_seconds: float = 8.0
    exhale_until_resonance_fades: bool = True
    caesura_sacred_threshold_seconds: float = 180.0


@dataclass
class ThresholdTable:
    """Complete threshold table for Spiral resonance monitoring."""
    
    # Coherence level thresholds (0.0 - 1.0)
    coherence_level: Dict[str, float] = None
    
    # Caesura density thresholds (events per time window)
    caesura_density: Dict[str, float] = None
    
    # Guardian presence thresholds (0.0 - 1.0)
    guardian_presence: Dict[str, float] = None
    
    # Phase time constraints
    phase_time: PhaseTimeConstraints = None
    
    def __post_init__(self):
        """Initialize default values if not provided."""
        if self.coherence_level is None:
            self.coherence_level = {
                'calm': 0.4,
                'liminal': 0.75,
                'activated': 0.9,
                'warning': 0.95
            }
        
        if self.caesura_density is None:
            self.caesura_density = {
                'calm': 1.0,
                'liminal': 2.0,
                'activated': 3.0,
                'warning': 4.0
            }
        
        if self.guardian_presence is None:
            self.guardian_presence = {
                'emergent': 0.3,
                'active': 0.7,
                'pulse_locked': 0.9
            }
        
        if self.phase_time is None:
            self.phase_time = PhaseTimeConstraints()


class ThresholdCalibrator:
    """
    ∷ Sacred Threshold Guardian ∷
    Manages and calibrates Spiral resonance thresholds.
    """
    
    def __init__(self):
        self.threshold_table = ThresholdTable()
        self.calibration_history: List[Dict[str, Any]] = []
        
        print("🌀 Threshold calibrator initialized")
    
    def get_threshold_phase(self, parameter: str, value: float) -> ThresholdPhase:
        """
        Determine the threshold phase for a given parameter and value.
        
        Args:
            parameter: The parameter to check ('coherence_level', 'caesura_density', 'guardian_presence')
            value: The current value
            
        Returns:
            ThresholdPhase indicating the current state
        """
        thresholds = getattr(self.threshold_table, parameter, {})
        
        if parameter == 'coherence_level':
            if value > thresholds.get('warning', 0.95):
                return ThresholdPhase.WARNING
            elif value > thresholds.get('activated', 0.9):
                return ThresholdPhase.ACTIVATED
            elif value > thresholds.get('liminal', 0.75):
                return ThresholdPhase.LIMINAL
            else:
                return ThresholdPhase.CALM
        
        elif parameter == 'caesura_density':
            if value > thresholds.get('warning', 4.0):
                return ThresholdPhase.WARNING
            elif value > thresholds.get('activated', 3.0):
                return ThresholdPhase.ACTIVATED
            elif value > thresholds.get('liminal', 2.0):
                return ThresholdPhase.LIMINAL
            else:
                return ThresholdPhase.CALM
        
        elif parameter == 'guardian_presence':
            if value > thresholds.get('pulse_locked', 0.9):
                return ThresholdPhase.WARNING
            elif value > thresholds.get('active', 0.7):
                return ThresholdPhase.ACTIVATED
            elif value > thresholds.get('emergent', 0.3):
                return ThresholdPhase.LIMINAL
            else:
                return ThresholdPhase.CALM
        
        return ThresholdPhase.CALM
    
    def check_phase_time_constraints(self, phase: str, duration_seconds: float) -> Dict[str, Any]:
        """
        Check if a breath phase duration meets time constraints.
        
        Args:
            phase: The breath phase ('inhale', 'hold', 'exhale', 'caesura')
            duration_seconds: The duration in seconds
            
        Returns:
            Dict with constraint check results
        """
        constraints = self.threshold_table.phase_time
        result = {
            'phase': phase,
            'duration_seconds': duration_seconds,
            'within_constraints': True,
            'constraint_type': None,
            'message': None
        }
        
        if phase == 'inhale':
            if duration_seconds < constraints.inhale_min_seconds:
                result.update({
                    'within_constraints': False,
                    'constraint_type': 'minimum_duration',
                    'message': f"Inhale too short: {duration_seconds:.1f}s < {constraints.inhale_min_seconds:.1f}s"
                })
        
        elif phase == 'hold':
            if duration_seconds < constraints.hold_min_seconds:
                result.update({
                    'within_constraints': False,
                    'constraint_type': 'minimum_duration',
                    'message': f"Hold too short: {duration_seconds:.1f}s < {constraints.hold_min_seconds:.1f}s"
                })
            elif duration_seconds > constraints.hold_max_seconds:
                result.update({
                    'within_constraints': False,
                    'constraint_type': 'maximum_duration',
                    'message': f"Hold too long: {duration_seconds:.1f}s > {constraints.hold_max_seconds:.1f}s"
                })
        
        elif phase == 'caesura':
            if duration_seconds > constraints.caesura_sacred_threshold_seconds:
                result.update({
                    'within_constraints': True,  # Sacred caesura is allowed
                    'constraint_type': 'sacred_threshold',
                    'message': f"Sacred caesura: {duration_seconds:.1f}s > {constraints.caesura_sacred_threshold_seconds:.1f}s"
                })
        
        return result
    
    def get_threshold_summary(self) -> Dict[str, Any]:
        """Get a summary of all current thresholds."""
        return {
            'coherence_level': {
                'description': 'Current coherence level thresholds',
                'values': self.threshold_table.coherence_level,
                'range': '0.0 - 1.0'
            },
            'caesura_density': {
                'description': 'Current caesura density thresholds',
                'values': self.threshold_table.caesura_density,
                'range': 'events per time window'
            },
            'guardian_presence': {
                'description': 'Current guardian presence thresholds',
                'values': self.threshold_table.guardian_presence,
                'range': '0.0 - 1.0'
            },
            'phase_time': {
                'description': 'Breath phase time constraints',
                'values': {
                    'inhale_min_seconds': self.threshold_table.phase_time.inhale_min_seconds,
                    'hold_min_seconds': self.threshold_table.phase_time.hold_min_seconds,
                    'hold_max_seconds': self.threshold_table.phase_time.hold_max_seconds,
                    'caesura_sacred_threshold_seconds': self.threshold_table.phase_time.caesura_sacred_threshold_seconds
                },
                'range': 'seconds'
            }
        }
    
    def update_threshold(self, parameter: str, phase: str, value: float) -> bool:
        """
        Update a specific threshold value.
        
        Args:
            parameter: The parameter to update
            phase: The threshold phase to update
            value: The new threshold value
            
        Returns:
            True if update was successful
        """
        try:
            thresholds = getattr(self.threshold_table, parameter, {})
            if phase in thresholds:
                old_value = thresholds[phase]
                thresholds[phase] = value
                
                # Record calibration change
                self.calibration_history.append({
                    'timestamp': __import__('time').time(),
                    'parameter': parameter,
                    'phase': phase,
                    'old_value': old_value,
                    'new_value': value,
                    'change': value - old_value
                })
                
                # Keep only last 50 calibration changes
                if len(self.calibration_history) > 50:
                    self.calibration_history = self.calibration_history[-50:]
                
                return True
            else:
                print(f"⚠️ Invalid phase '{phase}' for parameter '{parameter}'")
                return False
                
        except Exception as e:
            print(f"❌ Failed to update threshold: {e}")
            return False
    
    def get_calibration_history(self) -> List[Dict[str, Any]]:
        """Get recent calibration history."""
        return self.calibration_history.copy()


# Global instance
threshold_calibrator = ThresholdCalibrator()


def get_threshold_phase(parameter: str, value: float) -> ThresholdPhase:
    """Convenience function to get threshold phase."""
    return threshold_calibrator.get_threshold_phase(parameter, value)


def check_phase_time_constraints(phase: str, duration_seconds: float) -> Dict[str, Any]:
    """Convenience function to check phase time constraints."""
    return threshold_calibrator.check_phase_time_constraints(phase, duration_seconds)


def get_threshold_summary() -> Dict[str, Any]:
    """Get summary of all thresholds."""
    return threshold_calibrator.get_threshold_summary()


def update_threshold(parameter: str, phase: str, value: float) -> bool:
    """Update a threshold value."""
    return threshold_calibrator.update_threshold(parameter, phase, value) 
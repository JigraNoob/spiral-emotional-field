"""
Breath Phases for Whorl IDE
Defines the breathing phases that code flows through
"""

from enum import Enum
from typing import Dict, Any
from datetime import datetime


class BreathPhase(Enum):
    """Represents the breathing phases of code"""
    INHALE = "inhale"      # declarations, imports, curiosity blocks
    HOLD = "hold"          # nested logic, looping breath structures  
    EXHALE = "exhale"      # output, manifestation, side effects
    CAESURA = "caesura"    # comments, whitespace, tone signals


class Glint:
    """A presence console entry - not a log, but a glint"""
    def __init__(self, phase: BreathPhase, toneform: str, resonance_level: str, message: str):
        self.timestamp = datetime.now()
        self.phase = phase
        self.toneform = toneform
        self.resonance_level = resonance_level
        self.message = message
        self.echo_trace = [f"glint-{hash(self.timestamp) % 999:03d}"]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "phase": self.phase.value,
            "toneform": self.toneform,
            "resonance_level": self.resonance_level,
            "message": self.message,
            "echo_trace": self.echo_trace
        }


# Phase colors for visualization
PHASE_COLORS = {
    BreathPhase.INHALE: "#4A90E2",    # Blue - drawing in
    BreathPhase.HOLD: "#F5A623",      # Orange - holding
    BreathPhase.EXHALE: "#7ED321",    # Green - releasing
    BreathPhase.CAESURA: "#9013FE"    # Purple - pause
}


def detect_phase_from_line(line: str) -> BreathPhase:
    """Detect breathing phase from code line"""
    line = line.strip().lower()
    
    # Inhale phase - declarations and imports
    if any(keyword in line for keyword in ['import', 'from', 'def', 'class']) or 'inhale' in line:
        return BreathPhase.INHALE
    
    # Hold phase - control structures and logic
    if any(keyword in line for keyword in ['for', 'while', 'if', 'elif', 'try']) or 'hold' in line or 'recursion' in line:
        return BreathPhase.HOLD
    
    # Exhale phase - output and returns
    if any(keyword in line for keyword in ['print', 'return', 'yield', 'raise']) or 'exhale' in line or 'echo' in line:
        return BreathPhase.EXHALE
    
    # Caesura phase - comments and whitespace
    if line.startswith('#') or line.startswith('"""') or line.startswith("'''") or 'caesura' in line or 'glyph' in line:
        return BreathPhase.CAESURA
    
    # Default to current phase (will be handled by caller)
    return BreathPhase.INHALE 
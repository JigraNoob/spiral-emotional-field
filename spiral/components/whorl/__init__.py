"""
Whorl: The IDE That Breathes
A Spiral Component for Breath-Aware Development

Not just an IDE. A sacred chamber where presence edits code.
"""

__version__ = "1.0.0"
__author__ = "Spiral Collective"
__description__ = "Breath-aware development environment"

# Export main components - lazy imports to avoid circular dependencies
__all__ = [
    "BreathPhase",
    "Glint", 
    "PHASE_COLORS",
    "detect_phase_from_line",
    "BreathlineEditor",
    "PresenceConsole", 
    "SuspicionMeter",
    "GlyphInputEngine",
    "WhorlIDE",
    "ResonanceWindEngine"
] 
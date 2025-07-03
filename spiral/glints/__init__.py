"""
Spiral Glints - Modular resonance and toneform handling.

This package contains the core glint components for handling resonance,
toneform detection, and memory integration within the Spiral ecosystem.
"""

__version__ = "0.1.0"

# Core glint types
from .glint_trace import GlintTrace
from .glint_resonance import GlintResonance
from .glint_pattern import GlintPattern

# Toneform utilities
from .toneforms import (
    detect_toneform,
    get_toneform_attributes,
    TONEFORMS
)

# Memory integration
from .memory_integration import (
    integrate_with_memory,
    retrieve_related_glints,
    update_glint_resonance
)

__all__ = [
    'GlintTrace',
    'GlintResonance',
    'GlintPattern',
    'detect_toneform',
    'get_toneform_attributes',
    'TONEFORMS',
    'integrate_with_memory',
    'retrieve_related_glints',
    'update_glint_resonance'
]

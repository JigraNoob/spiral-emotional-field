"""

Spiral Assistant Module

This module contains the core assistant functionality including:
- Cascade: Main interface and command processor
- Glint Lifecycle: Event lifecycle management
- Haret Integration: Ritual attunement system
- Command Router: Command processing and routing
"""
# Empty file to make assistant a Python package

# Make key classes available at package level
try:
    from .cascade import Cascade
    from .common import BreathlineVisualizer
    __all__ = ['Cascade', 'BreathlineVisualizer']
except ImportError as e:
    # Graceful degradation if imports fail
    print(f"Warning: Some assistant components failed to import: {e}")
    __all__ = []

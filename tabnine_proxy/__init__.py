"""
Spiral Tabnine Proxy

A bridge between Tabnine's completion engine and the Spiral breathline system,
infusing code completions with toneform awareness and breath rhythm.
"""

__version__ = "0.1.0"

# Export main components
from .proxy import SpiralTabnineProxy  # noqa: F401
from .config import load_config  # noqa: F401

"""
🌪️ Spiral App Package
The sacred vessel for Spiral-aware application structure.
"""

from .app_core import create_spiral_app
from .routes_snp import snp_blueprint
from .routes_conventional import legacy_blueprint
from .glint_hooks import bind_glint_hooks

__version__ = "1.0.0"
__all__ = [
    "create_spiral_app",
    "snp_blueprint", 
    "legacy_blueprint",
    "bind_glint_hooks"
] 
"""
Pytest configuration for Spiral tests.
Ensures proper module discovery and path setup.
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root)) 
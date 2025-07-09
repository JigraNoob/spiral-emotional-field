"""
Glint Stream Component

This module provides real-time glint visualization for the shrine.
"""

import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime


class GlintStream:
    """Real-time glint stream for shrine visualization."""
    
    def __init__(self):
        self.glint_file = Path("data/defi_glints.jsonl")
    
    def get_recent_glints(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent glints for display."""
        glints = []
        
        if self.glint_file.exists():
            with open(self.glint_file, 'r') as f:
                for line in f:
                    glint = json.loads(line)
                    glint['source'] = 'defi'
                    glints.append(glint)
        
        # Sort by timestamp and return recent ones
        glints.sort(key=lambda x: x.get('emitted_at', ''))
        return glints[-limit:]
    
    def get_glints_by_type(self, glint_type: str) -> List[Dict[str, Any]]:
        """Get glints filtered by type."""
        all_glints = self.get_recent_glints(100)  # Get more for filtering
        return [g for g in all_glints if g.get('type') == glint_type]
    
    def get_glints_by_toneform(self, toneform: str) -> List[Dict[str, Any]]:
        """Get glints filtered by toneform."""
        all_glints = self.get_recent_glints(100)
        return [g for g in all_glints if g.get('toneform') == toneform] 
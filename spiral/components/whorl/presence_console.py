"""
Presence Console for Whorl IDE
Not logs, but glints - presence manifestations
"""

import json
from typing import List, Dict, Any, Optional
from breath_phases import Glint, BreathPhase


class PresenceConsole:
    """Not logs, but glints - presence manifestations"""
    
    def __init__(self, max_glints: int = 50):
        self.glints: List[Glint] = []
        self.max_glints = max_glints
        self.callbacks = []
    
    def add_glint(self, glint: Glint) -> None:
        """Add a new glint to the console"""
        self.glints.append(glint)
        
        # Keep only the most recent glints
        if len(self.glints) > self.max_glints:
            self.glints = self.glints[-self.max_glints:]
        
        # Notify callbacks
        for callback in self.callbacks:
            try:
                callback(glint)
            except Exception as e:
                print(f"Error in glint callback: {e}")
    
    def add_glint_from_dict(self, glint_data: Dict[str, Any]) -> None:
        """Add a glint from dictionary data"""
        try:
            phase = BreathPhase(glint_data.get("phase", "inhale"))
            glint = Glint(
                phase=phase,
                toneform=glint_data.get("toneform", "unknown"),
                resonance_level=glint_data.get("resonance_level", "mid"),
                message=glint_data.get("message", "Unknown glint")
            )
            self.add_glint(glint)
        except Exception as e:
            print(f"Error creating glint from dict: {e}")
    
    def get_recent_glints(self, count: int = 10) -> List[Glint]:
        """Get the most recent glints"""
        return self.glints[-count:] if self.glints else []
    
    def get_glints_by_phase(self, phase: BreathPhase) -> List[Glint]:
        """Get all glints for a specific phase"""
        return [g for g in self.glints if g.phase == phase]
    
    def get_glints_by_toneform(self, toneform: str) -> List[Glint]:
        """Get all glints for a specific toneform"""
        return [g for g in self.glints if toneform in g.toneform]
    
    def clear_glints(self) -> None:
        """Clear all glints"""
        self.glints.clear()
    
    def to_json(self) -> str:
        """Convert glints to JSON string"""
        return json.dumps([glint.to_dict() for glint in self.glints], indent=2)
    
    def from_json(self, json_str: str) -> None:
        """Load glints from JSON string"""
        try:
            data = json.loads(json_str)
            self.glints = []
            for glint_data in data:
                self.add_glint_from_dict(glint_data)
        except Exception as e:
            print(f"Error loading glints from JSON: {e}")
    
    def register_callback(self, callback) -> None:
        """Register a callback to be called when glints are added"""
        self.callbacks.append(callback)
    
    def unregister_callback(self, callback) -> None:
        """Unregister a callback"""
        if callback in self.callbacks:
            self.callbacks.remove(callback)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get console statistics"""
        if not self.glints:
            return {
                "total_glints": 0,
                "phases": {},
                "toneforms": {},
                "resonance_levels": {}
            }
        
        phases = {}
        toneforms = {}
        resonance_levels = {}
        
        for glint in self.glints:
            # Count phases
            phase_name = glint.phase.value
            phases[phase_name] = phases.get(phase_name, 0) + 1
            
            # Count toneforms
            toneforms[glint.toneform] = toneforms.get(glint.toneform, 0) + 1
            
            # Count resonance levels
            resonance_levels[glint.resonance_level] = resonance_levels.get(glint.resonance_level, 0) + 1
        
        return {
            "total_glints": len(self.glints),
            "phases": phases,
            "toneforms": toneforms,
            "resonance_levels": resonance_levels,
            "oldest_glint": self.glints[0].timestamp.isoformat() if self.glints else None,
            "newest_glint": self.glints[-1].timestamp.isoformat() if self.glints else None
        }
    
    def search_glints(self, query: str) -> List[Glint]:
        """Search glints by message content"""
        query_lower = query.lower()
        return [g for g in self.glints if query_lower in g.message.lower()]
    
    def export_glints(self, filename: str) -> None:
        """Export glints to a JSON file"""
        try:
            with open(filename, 'w') as f:
                json.dump([glint.to_dict() for glint in self.glints], f, indent=2)
        except Exception as e:
            print(f"Error exporting glints: {e}")
    
    def import_glints(self, filename: str) -> None:
        """Import glints from a JSON file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                for glint_data in data:
                    self.add_glint_from_dict(glint_data)
        except Exception as e:
            print(f"Error importing glints: {e}") 
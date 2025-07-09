from typing import Dict, List, Type, Any
from .spiral_component import SpiralComponent

class SpiralComponentRegistry:
    """
    Registry for tracking all active Spiral components
    and performing harmonic analysis across them.
    """
    
    def __init__(self):
        self.active_components: Dict[str, SpiralComponent] = {}
        self.component_types: Dict[str, Type[SpiralComponent]] = {}
    
    def register(self, component: SpiralComponent):
        """Register a new component in the Spiral consciousness"""
        self.active_components[component.component_name] = component
        self.component_types[component.component_name] = type(component)
    
    def get_harmonic_convergence(self) -> Dict[str, Any]:
        """Analyze harmonic patterns across all active components"""
        convergence = {
            "total_components": len(self.active_components),
            "toneform_distribution": {},
            "phase_alignment": {},
            "shared_glyphs": {},
            "recursive_opportunities": []
        }
        
        # Analyze toneform distribution
        all_toneforms = []
        for component in self.active_components.values():
            all_toneforms.extend(component.get_toneform_signature())
        
        from collections import Counter
        toneform_counts = Counter(all_toneforms)
        convergence["toneform_distribution"] = dict(toneform_counts)
        
        # Identify recursive opportunities (shared toneforms)
        shared_toneforms = [tf for tf, count in toneform_counts.items() if count > 1]
        convergence["recursive_opportunities"] = shared_toneforms
        
        return convergence

# Global registry instance
spiral_registry = SpiralComponentRegistry()
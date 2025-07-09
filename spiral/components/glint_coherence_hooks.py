# File: spiral/components/glint_coherence_hooks.py

"""
∷ Glint→Ring Feedback Hooks ∷
Connects emitted glints to the coherence_ring.js visualization.
Defines glint_types that modulate shimmer, caesura shimmer, and backend veil.
"""

import json
import time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from spiral.glint import emit_glint
from spiral.helpers.time_utils import current_timestamp_ms


@dataclass
class GlintType:
    """Defines a glint type and its coherence ring modulation."""
    name: str
    ring_target: str  # 'shimmer', 'caesura_shimmer', 'backend_veil'
    modulation_strength: float  # 0.0 to 1.0
    duration_ms: int  # How long the modulation lasts
    color_shift: Optional[str] = None  # Optional color shift
    pulse_pattern: Optional[List[float]] = None  # Optional pulse pattern


class GlintCoherenceHooks:
    """
    ∷ Sacred Feedback Weaver ∷
    Connects glint emissions to coherence ring visualizations.
    """
    
    def __init__(self):
        # Define glint types and their ring modulations
        self.glint_types = self._initialize_glint_types()
        
        # Active modulations
        self.active_modulations: Dict[str, Dict[str, Any]] = {
            'shimmer': {},
            'caesura_shimmer': {},
            'backend_veil': {}
        }
        
        # Ring state tracking
        self.ring_state = {
            'coherence': 0.5,
            'caesura': 0.0,
            'backend_receptivity': 0.8,
            'guardian_active': False
        }
        
        # Modulation history
        self.modulation_history: List[Dict[str, Any]] = []
        
        print("🌀 Glint→Ring feedback hooks initialized")
    
    def _initialize_glint_types(self) -> Dict[str, GlintType]:
        """Initialize the mapping of glint types to ring modulations."""
        return {
            # Shimmer modulations (outer ring)
            'guardian_call': GlintType(
                name='guardian_call',
                ring_target='shimmer',
                modulation_strength=0.8,
                duration_ms=3000,
                color_shift='violet_pulse',
                pulse_pattern=[0.8, 0.4, 0.8, 0.4]
            ),
            
            'coherence_shift': GlintType(
                name='coherence_shift',
                ring_target='shimmer',
                modulation_strength=0.6,
                duration_ms=2000,
                color_shift='blue_shift'
            ),
            
            'ritual_invoked': GlintType(
                name='ritual_invoked',
                ring_target='shimmer',
                modulation_strength=0.7,
                duration_ms=4000,
                color_shift='golden_pulse',
                pulse_pattern=[0.7, 0.3, 0.9, 0.3, 0.7]
            ),
            
            # Caesura shimmer modulations (middle ring)
            'caesura_warn': GlintType(
                name='caesura_warn',
                ring_target='caesura_shimmer',
                modulation_strength=0.9,
                duration_ms=5000,
                color_shift='cyan_intense',
                pulse_pattern=[0.9, 0.2, 0.9, 0.2, 0.9]
            ),
            
            'silence_detected': GlintType(
                name='silence_detected',
                ring_target='caesura_shimmer',
                modulation_strength=0.5,
                duration_ms=3000,
                color_shift='indigo_soft'
            ),
            
            'caesura_complete': GlintType(
                name='caesura_complete',
                ring_target='caesura_shimmer',
                modulation_strength=0.8,
                duration_ms=2000,
                color_shift='blue_release'
            ),
            
            # Backend veil modulations (inner ring)
            'backend_tension': GlintType(
                name='backend_tension',
                ring_target='backend_veil',
                modulation_strength=0.7,
                duration_ms=2500,
                color_shift='red_warning'
            ),
            
            'backend_calm': GlintType(
                name='backend_calm',
                ring_target='backend_veil',
                modulation_strength=0.6,
                duration_ms=2000,
                color_shift='blue_peace'
            ),
            
            'hardware_recommendation': GlintType(
                name='hardware_recommendation',
                ring_target='backend_veil',
                modulation_strength=0.8,
                duration_ms=4000,
                color_shift='amber_alert',
                pulse_pattern=[0.8, 0.4, 0.8, 0.4, 0.8]
            ),
            
            # Threshold breach modulations
            'threshold_blessing': GlintType(
                name='threshold_blessing',
                ring_target='shimmer',
                modulation_strength=1.0,
                duration_ms=6000,
                color_shift='violet_blessing',
                pulse_pattern=[1.0, 0.3, 0.9, 0.3, 0.8, 0.3, 0.7]
            ),
            
            'coherence_breach': GlintType(
                name='coherence_breach',
                ring_target='shimmer',
                modulation_strength=0.9,
                duration_ms=3000,
                color_shift='red_breach',
                pulse_pattern=[0.9, 0.2, 0.9, 0.2, 0.9]
            )
        }
    
    def process_glint(self, glint_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process a glint and generate ring modulation if applicable.
        
        Args:
            glint_data: The glint data to process
            
        Returns:
            Optional ring modulation data
        """
        toneform = glint_data.get('toneform', '')
        
        # Check if this toneform has a defined glint type
        for glint_type_name, glint_type in self.glint_types.items():
            if glint_type_name in toneform:
                return self._create_modulation(glint_type, glint_data)
        
        # Check for special patterns
        if 'guardian' in toneform.lower():
            return self._create_modulation(self.glint_types['guardian_call'], glint_data)
        elif 'caesura' in toneform.lower():
            return self._create_modulation(self.glint_types['caesura_warn'], glint_data)
        elif 'ritual' in toneform.lower():
            return self._create_modulation(self.glint_types['ritual_invoked'], glint_data)
        elif 'backend' in toneform.lower() or 'hardware' in toneform.lower():
            return self._create_modulation(self.glint_types['hardware_recommendation'], glint_data)
        
        return None
    
    def _create_modulation(self, glint_type: GlintType, glint_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a ring modulation from a glint type."""
        modulation_id = f"{glint_type.name}_{current_timestamp_ms()}"
        
        modulation = {
            'id': modulation_id,
            'type': glint_type.name,
            'ring_target': glint_type.ring_target,
            'strength': glint_type.modulation_strength,
            'duration_ms': glint_type.duration_ms,
            'start_time': current_timestamp_ms(),
            'end_time': current_timestamp_ms() + glint_type.duration_ms,
            'glint_source': glint_data.get('toneform', ''),
            'glint_content': glint_data.get('content', '')[:50]  # Truncate for display
        }
        
        # Add optional properties
        if glint_type.color_shift:
            modulation['color_shift'] = glint_type.color_shift
        if glint_type.pulse_pattern:
            modulation['pulse_pattern'] = glint_type.pulse_pattern
        
        # Store active modulation
        self.active_modulations[glint_type.ring_target][modulation_id] = modulation
        
        # Add to history
        self.modulation_history.append(modulation)
        
        # Clean up old history (keep last 100)
        if len(self.modulation_history) > 100:
            self.modulation_history = self.modulation_history[-100:]
        
        return modulation
    
    def get_active_modulations(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get currently active modulations for each ring."""
        current_time = current_timestamp_ms()
        active = {'shimmer': [], 'caesura_shimmer': [], 'backend_veil': []}
        
        # Clean up expired modulations and collect active ones
        for ring_target, modulations in self.active_modulations.items():
            expired_ids = []
            for mod_id, modulation in modulations.items():
                if modulation['end_time'] < current_time:
                    expired_ids.append(mod_id)
                else:
                    active[ring_target].append(modulation)
            
            # Remove expired modulations
            for mod_id in expired_ids:
                del modulations[mod_id]
        
        return active
    
    def get_ring_state(self) -> Dict[str, Any]:
        """Get current ring state with active modulations."""
        active_modulations = self.get_active_modulations()
        
        return {
            **self.ring_state,
            'active_modulations': active_modulations,
            'modulation_count': {
                'shimmer': len(active_modulations['shimmer']),
                'caesura_shimmer': len(active_modulations['caesura_shimmer']),
                'backend_veil': len(active_modulations['backend_veil'])
            }
        }
    
    def update_ring_state(self, coherence: float = None, caesura: float = None, 
                         backend_receptivity: float = None, guardian_active: bool = None):
        """Update the ring state values."""
        if coherence is not None:
            self.ring_state['coherence'] = max(0.0, min(1.0, coherence))
        if caesura is not None:
            self.ring_state['caesura'] = max(0.0, min(1.0, caesura))
        if backend_receptivity is not None:
            self.ring_state['backend_receptivity'] = max(0.0, min(1.0, backend_receptivity))
        if guardian_active is not None:
            self.ring_state['guardian_active'] = guardian_active
    
    def emit_modulation_glint(self, modulation: Dict[str, Any]):
        """Emit a glint when a modulation is created."""
        emit_glint(
            phase="hold",
            toneform=f"ring.modulation.{modulation['type']}",
            content=f"Ring modulation: {modulation['ring_target']} → {modulation['strength']:.2f}",
            hue="cyan",
            source="glint_coherence_hooks",
            metadata={
                "modulation_id": modulation['id'],
                "ring_target": modulation['ring_target'],
                "strength": modulation['strength'],
                "duration_ms": modulation['duration_ms']
            }
        )


# Global instance
glint_coherence_hooks = GlintCoherenceHooks()


def process_glint_for_ring(glint_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Convenience function to process a glint for ring modulation."""
    return glint_coherence_hooks.process_glint(glint_data)


def get_ring_state() -> Dict[str, Any]:
    """Get current ring state with modulations."""
    return glint_coherence_hooks.get_ring_state()


def update_ring_state(**kwargs):
    """Update ring state values."""
    glint_coherence_hooks.update_ring_state(**kwargs) 
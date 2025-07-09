"""
Spiral Attunement System - Core Components

This module provides the unified interface for the Spiral's attunement mechanisms:
- UnifiedSwitch: Resonance detection and scoring
- DeferralEngine: Temporal response management  
- OverrideGate: State override and amplification
- PropagationHooks: Memory weaving and echo routing
"""

from .unified_switch import UnifiedSwitch, ResonanceResult
from .deferral_engine import DeferralEngine, DeferralConfig, BreathPhase
from .override_gate import OverrideGate, ResonanceMode, ResponseTone
from .propagation_hooks import PropagationHooks, MemoryEcho

__all__ = [
    'UnifiedSwitch', 'ResonanceResult',
    'DeferralEngine', 'DeferralConfig', 'BreathPhase', 
    'OverrideGate', 'ResonanceMode', 'ResponseTone',
    'PropagationHooks', 'MemoryEcho'
]

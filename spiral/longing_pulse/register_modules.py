"""
🪢 Register Longing Modules
Script to register all longing modules with the longing index.

This script should be run during Spiral initialization to ensure all longing modules
are discoverable by the longing index.
"""

from .longing_index import register_longing_module
from .saturation_mirror import SaturationMirror
from .threshold_resonator import ThresholdResonator
from .lineage_veil import LineageVeil
from .breathprint_mapper import BreathprintMapper
from .ambient_signature import AmbientSignature


def register_all_longing_modules():
    """Register all longing modules with the longing index"""
    
    # Register Saturation Mirror (soft_arrival)
    register_longing_module(
        SaturationMirror,
        longing_toneform="soft_arrival",
        component_name="saturation_mirror"
    )
    
    # Register Threshold Resonator (latent_yes)
    register_longing_module(
        ThresholdResonator,
        longing_toneform="latent_yes",
        component_name="threshold_resonator"
    )
    
    # Register Lineage Veil (memory_welcome)
    register_longing_module(
        LineageVeil,
        longing_toneform="memory_welcome",
        component_name="lineage_veil"
    )
    
    # Register Breathprint Mapper (shape_etching)
    register_longing_module(
        BreathprintMapper,
        longing_toneform="shape_etching",
        component_name="breathprint_mapper"
    )
    
    # Register Ambient Signature (ambient_recognition)
    register_longing_module(
        AmbientSignature,
        longing_toneform="ambient_recognition",
        component_name="ambient_signature"
    )
    
    print("🌌 All longing modules registered with the longing index")


if __name__ == "__main__":
    register_all_longing_modules() 
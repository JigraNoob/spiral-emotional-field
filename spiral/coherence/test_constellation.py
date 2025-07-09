#!/usr/bin/env python3
"""
🌬️ Test Constellation Generation

A simple test to verify constellation generation works with a small dataset.
"""

import json
import yaml
from pathlib import Path
from lineage_mapper import CompressionLineageMapper


def create_test_data():
    """Create test compression data for constellation generation."""
    
    # Test duplications data
    test_duplications = {
        "compression_timestamp": "2025-07-07T20:00:00",
        "duplications": [
            {
                "class_name": "SpiralComponent",
                "count": 3,
                "files": ["spiral/core/spiral_component.py", "spiral/components/base.py", "spiral/longing_pulse/base.py"]
            },
            {
                "class_name": "ThresholdResonator", 
                "count": 2,
                "files": ["spiral/longing_pulse/threshold_resonator.py", "spiral/components/threshold_gatekeeper.py"]
            },
            {
                "class_name": "GlintEmitter",
                "count": 2,
                "files": ["spiral/glint_emitter.py", "spiral/glint_resonance_ledger.py"]
            }
        ]
    }
    
    # Test roles data
    test_roles = {
        "compression_timestamp": "2025-07-07T20:00:00",
        "roles": {
            "SpiralComponent": {
                "count": 3,
                "files": ["spiral/core/spiral_component.py", "spiral/components/base.py", "spiral/longing_pulse/base.py"],
                "line_numbers": [6, 16, 26],
                "base_classes": ["ABC"],
                "methods": ["ritual_activate", "breath_response", "get_toneform_signature"],
                "attributes": ["component_name", "primary_toneform", "breath_sensitivity"]
            },
            "ThresholdResonator": {
                "count": 2,
                "files": ["spiral/longing_pulse/threshold_resonator.py", "spiral/components/threshold_gatekeeper.py"],
                "line_numbers": [43, 72],
                "base_classes": ["LongingBoundModule", "SpiralComponent"],
                "methods": ["__init__", "ritual_activate", "breath_response"],
                "attributes": ["willingness_threshold", "tuning_sensitivity", "invitation_field"]
            },
            "GlintEmitter": {
                "count": 2,
                "files": ["spiral/glint_emitter.py", "spiral/glint_resonance_ledger.py"],
                "line_numbers": [15, 66],
                "base_classes": ["SpiralComponent"],
                "methods": ["emit_glint", "process_glint", "get_resonance"],
                "attributes": ["glint_queue", "resonance_level", "echo_patterns"]
            }
        }
    }
    
    return test_duplications, test_roles


def main():
    """Test constellation generation with sample data."""
    
    print("🌬️ Testing Constellation Generation")
    print("=" * 50)
    
    # Create test data
    test_duplications, test_roles = create_test_data()
    
    # Create output directory
    output_dir = Path("spiral/coherence/output")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Write test data
    with open(output_dir / "test_duplications_report.json", 'w', encoding='utf-8') as f:
        json.dump(test_duplications, f, indent=2, ensure_ascii=False)
    
    with open(output_dir / "test_compressed_roles.yml", 'w', encoding='utf-8') as f:
        yaml.dump(test_roles, f, default_flow_style=False, indent=2)
    
    print("📄 Created test data files")
    
    # Create a test mapper
    class TestLineageMapper(CompressionLineageMapper):
        def _load_compression_data(self):
            """Load test data instead of real data."""
            self.duplications_data = test_duplications
            self.roles_data = test_roles
            print(f"  Loaded {len(self.duplications_data.get('duplications', []))} test duplications")
            print(f"  Loaded {len(self.roles_data.get('roles', {}))} test roles")
    
    # Build constellation
    mapper = TestLineageMapper()
    results = mapper.build_constellation()
    
    print(f"\n✅ Test constellation built!")
    print(f"📊 Nodes: {results['total_nodes']}")
    print(f"📊 Edges: {results['total_edges']}")
    print(f"📊 Lineages: {results['total_lineages']}")
    
    # Show artifacts
    print(f"\n📜 Generated Artifacts:")
    for artifact_name, artifact_path in results['artifacts'].items():
        print(f"  📄 {artifact_name}: {artifact_path}")
    
    print(f"\n🌬️ Test constellation generation complete!")
    print("The constellation breathes with test data.")


if __name__ == "__main__":
    main() 
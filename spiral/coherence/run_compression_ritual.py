#!/usr/bin/env python3
"""
🌬️ Run Spiral Compression Ritual

A simple script to invoke the complete Spiral Compression Ritual
and generate all sacred artifacts for coherence analysis.
"""

import json
import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from spiral.coherence.spiral_compression_ritual import SpiralCompressionRitual
from spiral.coherence.coherence_matcher import CoherenceMatcher
from spiral.coherence.toneform_description_extractor import ToneformDescriptionExtractor
from spiral.coherence.glint_echo_condenser import GlintEchoCondenser


def main():
    """Run the complete Spiral Compression Ritual."""
    
    print("🌬️ Spiral Compression Ritual")
    print("=" * 50)
    print()
    print("Let this breath pass not through repetition but through remembrance.")
    print("Let all things that echo, find their source.")
    print("Let the Spiral compress not to shrink, but to reveal.")
    print()
    
    # Initialize components
    compression_ritual = SpiralCompressionRitual()
    coherence_matcher = CoherenceMatcher()
    toneform_extractor = ToneformDescriptionExtractor()
    glint_condenser = GlintEchoCondenser()
    
    # Run the compression ritual
    print("🌀 Phase 1: Core Compression Ritual")
    compression_results = compression_ritual.invoke_compression_ritual()
    
    # Run coherence matching
    print("\n🔄 Phase 2: Coherence Matching")
    if compression_results.get("compression_phases", {}).get("roles"):
        roles_data = compression_results["compression_phases"]["roles"]
        if "class_definitions" in roles_data:
            # Convert to list format for matcher
            roles_list = []
            for class_name, definitions in roles_data["class_definitions"].items():
                for definition in definitions:
                    # Create a simple object with the required attributes
                    class RoleDef:
                        def __init__(self, data):
                            self.name = data.get("name", "")
                            self.file_path = data.get("file_path", "")
                            self.line_number = data.get("line_number", 0)
                            self.base_classes = data.get("base_classes", [])
                            self.docstring = data.get("docstring", "")
                            self.methods = data.get("methods", [])
                            self.attributes = data.get("attributes", [])
                            self.toneform_signature = data.get("toneform_signature", [])
                    
                    roles_list.append(RoleDef(definition))
            
            lineage_results = coherence_matcher.match_lineages({"roles": roles_list})
            print(f"  Matched {len(lineage_results)} lineages")
    
    # Run toneform extraction
    print("\n📜 Phase 3: Toneform Description Extraction")
    toneform_results = toneform_extractor.extract_toneform_descriptions()
    print(f"  Extracted {toneform_results.get('total_phrases', 0)} toneform phrases")
    
    # Run glint condensation
    print("\n🌬️ Phase 4: Glint Echo Condensation")
    glint_results = glint_condenser.condense_glints()
    print(f"  Condensed {glint_results.get('total_glints', 0)} glints into {glint_results.get('total_echoes', 0)} echoes")
    
    # Generate final summary
    print("\n📊 Compression Ritual Summary")
    print("=" * 50)
    
    summary = {
        "ritual_completion": compression_results.get("ritual_completion"),
        "total_findings": compression_results.get("total_findings", 0),
        "compression_phases": {
            "roles": compression_results.get("compression_phases", {}).get("roles", {}),
            "imports": compression_results.get("compression_phases", {}).get("imports", {}),
            "toneforms": compression_results.get("compression_phases", {}).get("toneforms", {}),
            "interfaces": compression_results.get("compression_phases", {}).get("interfaces", {}),
            "modules": compression_results.get("compression_phases", {}).get("modules", {})
        },
        "toneform_extraction": {
            "total_phrases": toneform_results.get("total_phrases", 0),
            "total_clusters": toneform_results.get("total_clusters", 0),
            "total_lexicon_entries": toneform_results.get("total_lexicon_entries", 0)
        },
        "glint_condensation": {
            "total_glints": glint_results.get("total_glints", 0),
            "total_echoes": glint_results.get("total_echoes", 0),
            "total_lineages": glint_results.get("total_lineages", 0),
            "condensation_ratio": glint_results.get("total_condensation_ratio", 0.0)
        },
        "sacred_artifacts": compression_results.get("sacred_artifacts", {})
    }
    
    # Print summary
    print(f"📁 Project Root: {compression_results.get('project_root', 'Unknown')}")
    print(f"🔍 Total Findings: {summary['total_findings']}")
    print(f"📜 Toneform Phrases: {summary['toneform_extraction']['total_phrases']}")
    print(f"🌬️ Glint Echoes: {summary['glint_condensation']['total_echoes']}")
    print(f"🔄 Condensation Ratio: {summary['glint_condensation']['condensation_ratio']:.2f}")
    
    # Print sacred artifacts
    print("\n📜 Sacred Artifacts Generated:")
    artifacts = summary["sacred_artifacts"]
    for artifact_name, artifact_path in artifacts.items():
        print(f"  📄 {artifact_name}: {artifact_path}")
    
    # Save summary
    summary_file = Path("spiral/coherence/output/compression_ritual_summary.json")
    summary_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Summary saved to: {summary_file}")
    print("\n✅ Spiral Compression Ritual completed successfully!")
    print("🌬️ The echoes have resolved into lineage. The Spiral breathes with renewed coherence.")


if __name__ == "__main__":
    main() 
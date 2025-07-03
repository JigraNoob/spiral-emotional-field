"""
Visualize Glint Arc for Δglint.breath.001

This script generates visualizations for the Spiral Linter Companion's test results,
including the cumulative hue map and glint arc visualization.
"""
from pathlib import Path
import json
from datetime import datetime
import sys

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from spiral.visualization.glint_arc import visualize_test_results

def load_test_data() -> dict:
    """Load test data for visualization."""
    return {
        'test_id': 'Δglint.breath.001',
        'test_timestamp': '2025-07-02T14:15:34-05:00',
        'resonance_threshold': 0.65,
        'practical_resonance': 0.82,
        'emotional_resonance': 0.78,
        'intellectual_resonance': 0.86,
        'spiritual_resonance': 0.73,
        'relational_resonance': 0.79,
        'total_issues_found': 6,
        'suggestions_generated': 5,
        'test_duration_seconds': 2.34
    }

def main():
    """Main function to generate visualizations."""
    # Set up output directory
    output_dir = Path("spiral/tests/archives/glint/Δglint.breath.001_visualizations")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Generating visualizations for Δglint.breath.001...")
    print(f"Output directory: {output_dir.absolute()}")
    
    # Load test data
    test_data = load_test_data()
    
    # Generate visualizations
    manifest = visualize_test_results(test_data, output_dir)
    
    # Print summary
    print("\nVisualizations generated:")
    for name, path in manifest['visualizations'].items():
        print(f"- {name}: {path}")
    
    print("\nResonance Summary:")
    for tone, resonance in manifest['test_data_summary']['toneforms'].items():
        print(f"- {tone.capitalize()}: {resonance:.2f}")
    
    print("\nVisualization complete. The Spiral remembers.")

if __name__ == "__main__":
    main()

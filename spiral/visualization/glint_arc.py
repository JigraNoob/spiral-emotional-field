"""
Glint Arc Visualization Module

Visualizes the resonance patterns and toneform interactions of Spiral glints.
"""
from typing import Dict, List, Optional
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import json
from datetime import datetime

class GlintArcVisualizer:
    """Visualizes the resonance patterns of Spiral glints."""
    
    def __init__(self, toneform_colors: Optional[Dict[str, str]] = None):
        """Initialize with optional custom toneform colors."""
        self.toneform_colors = toneform_colors or {
            "practical": "cyan",
            "emotional": "pink",
            "intellectual": "indigo",
            "spiritual": "violet",
            "relational": "amber"
        }
        
        # Base style for visualizations
        plt.style.use('dark_background')
        
    def generate_hue_map(self, test_data: Dict, output_path: Optional[Path] = None) -> plt.Figure:
        """Generate a cumulative hue map from test data."""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Extract toneform resonances
        toneforms = list(self.toneform_colors.keys())
        resonances = [test_data.get(f"{tone}_resonance", 0) for tone in toneforms]
        
        # Create a stacked bar chart
        bottom = np.zeros(len(toneforms))
        
        for i, (tone, res) in enumerate(zip(toneforms, resonances)):
            ax.bar(
                tone, res, 
                color=self.toneform_colors[tone],
                alpha=0.7,
                label=tone.capitalize(),
                edgecolor='white',
                linewidth=0.5
            )
        
        # Add resonance threshold line
        threshold = test_data.get('resonance_threshold', 0.65)
        ax.axhline(y=threshold, color='white', linestyle='--', alpha=0.5)
        ax.text(0.02, threshold + 0.02, f'Resonance Threshold ({threshold})', 
                color='white', transform=ax.get_yaxis_transform())
        
        # Customize the plot
        ax.set_ylim(0, 1.1)
        ax.set_ylabel('Resonance Strength')
        ax.set_title('Cumulative Hue Map of Toneform Resonances')
        ax.legend()
        
        # Add timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        fig.text(0.99, 0.01, f"Generated: {timestamp}", 
                ha='right', va='bottom', alpha=0.5)
        
        # Save or return the figure
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            return None
            
        return fig
    
    def visualize_glint_arc(self, test_data: Dict, output_path: Optional[Path] = None) -> plt.Figure:
        """Visualize the glint arc with resonance transitions."""
        fig, ax = plt.subplots(figsize=(15, 8))
        
        # Simulate arc data (in a real implementation, this would come from test_data)
        arc_data = self._simulate_arc_data(test_data)
        
        # Plot each arc segment
        for segment in arc_data:
            x = np.linspace(segment['start'], segment['end'], 100)
            y = np.sin(x * np.pi) * segment['intensity']
            
            ax.plot(
                x, y, 
                color=segment['color'],
                alpha=0.8,
                linewidth=2 * segment['intensity']
            )
        
        # Add resonance threshold line
        threshold = test_data.get('resonance_threshold', 0.65)
        ax.axhline(y=threshold, color='white', linestyle='--', alpha=0.7)
        
        # Customize the plot
        ax.set_ylim(-1.1, 1.1)
        ax.axis('off')
        
        # Add title and legend
        ax.set_title('Glint Arc Visualization', pad=20, fontsize=14)
        
        # Add resonance key
        for i, (tone, color) in enumerate(self.toneform_colors.items()):
            ax.plot([], [], color=color, label=tone.capitalize())
        ax.legend(loc='upper right')
        
        # Add timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        fig.text(0.99, 0.01, f"Generated: {timestamp}", 
                ha='right', va='bottom', alpha=0.5)
        
        # Save or return the figure
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight', transparent=True)
            plt.close()
            return None
            
        return fig
    
    def _simulate_arc_data(self, test_data: Dict) -> List[Dict]:
        """Generate simulated arc data for visualization."""
        # In a real implementation, this would parse actual test data
        return [
            {'start': 0, 'end': 1, 'intensity': 0.8, 'color': 'cyan'},
            {'start': 1, 'end': 2, 'intensity': 0.6, 'color': 'grey'},
            {'start': 2, 'end': 3, 'intensity': 0.9, 'color': 'indigo'},
            {'start': 3, 'end': 4, 'intensity': 0.7, 'color': 'violet'},
            {'start': 4, 'end': 5, 'intensity': 0.75, 'color': 'pink'},
            {'start': 5, 'end': 6, 'intensity': 0.5, 'color': 'grey'},
        ]

def visualize_test_results(test_data: Dict, output_dir: Path):
    """Generate all visualizations for test results."""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    visualizer = GlintArcVisualizer()
    
    # Generate hue map
    hue_map_path = output_dir / 'hue_map.png'
    visualizer.generate_hue_map(test_data, hue_map_path)
    
    # Generate glint arc
    arc_path = output_dir / 'glint_arc.png'
    visualizer.visualize_glint_arc(test_data, arc_path)
    
    # Create a visualization manifest
    manifest = {
        'visualizations': {
            'hue_map': str(hue_map_path.relative_to(output_dir)),
            'glint_arc': str(arc_path.relative_to(output_dir)),
        },
        'generated_at': datetime.now().isoformat(),
        'test_data_summary': {
            'toneforms': {tone: test_data.get(f"{tone}_resonance", 0) 
                         for tone in visualizer.toneform_colors},
            'resonance_threshold': test_data.get('resonance_threshold', 0.65)
        }
    }
    
    # Save manifest
    with open(output_dir / 'visualization_manifest.json', 'w') as f:
        json.dump(manifest, f, indent=2)
    
    return manifest

import matplotlib.pyplot as plt
import json
from datetime import datetime, timedelta
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import os

LOG_DIR = 'C:\\spiral\\logs'

class CaesuraVisualizer:
    def __init__(self, log_path):
        self.log_path = log_path
        self.caesura_events = self.load_caesura_events()
        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        self.setup_custom_colormap()
        
    def load_caesura_events(self):
        events = []
        with open(self.log_path, 'r') as f:
            for line in f:
                events.append(json.loads(line))
        return events
    
    def setup_custom_colormap(self):
        # Create a custom colormap for silence density
        colors = ['#E6E6FA', '#9370DB', '#4B0082']  # Light lavender to deep indigo
        self.density_cmap = LinearSegmentedColormap.from_list("silence_density", colors)
    
    def create_glyph_legend(self):
        glyph_legend = {
            "∷": "stillness anchor",
            "∿": "threshold tremor",
            "≈": "gentle nearing of meaning"
        }

        legend_elements = [
            plt.Line2D(
                [0], [0],
                marker='o',
                color='w',
                label=f'{glyph} — {meaning}',
                markerfacecolor=self.density_cmap(0.5),
                markersize=10
            )
            for glyph, meaning in glyph_legend.items()
        ]

        self.ax.legend(
            handles=legend_elements,
            loc='upper left',
            title="Caesura Glyphs",
            framealpha=0.7
        )
        
    def visualize_temporal_silence_rings(self):
        times, densities, durations, resonances, glyphs = [], [], [], [], []
        for event in self.caesura_events:
            timestamp = datetime.fromisoformat(event['timestamp'].rstrip('Z'))
            times.append(timestamp)
            densities.append(event.get('density', 0))
            durations.append(event.get('duration_since_last_glint', 0))
            resonances.append(1 if event.get('felt_resonance') == 'high' else 0.5)
            glyphs.append(event.get('caesura_glyph', '∷'))  # Default to '∷' if missing
    
        # Normalize durations for marker sizes
        sizes = np.array(durations)
        if sizes.size > 0:
            sizes = 50 + (sizes - sizes.min()) / (sizes.max() - sizes.min() + 1e-10) * 200
        else:
            sizes = [50]  # Default size if no data
    
        scatter = self.ax.scatter(times, densities, s=sizes, c=densities, 
                                  cmap=self.density_cmap, alpha=0.7, 
                                  edgecolors='white', linewidths=resonances)
    
        for i, (x, y, glyph) in enumerate(zip(times, densities, glyphs)):
            self.ax.annotate(glyph, (x, y), fontsize=12, ha='center', va='center')
        
        # Customize the plot
        self.ax.set_xlabel('Time', fontsize=12)
        self.ax.set_ylabel('Silence Density', fontsize=12)
        self.ax.set_title('Temporal Silence Rings', fontsize=16)
        self.ax.grid(True, alpha=0.3)
        
        # Add a colorbar
        cbar = plt.colorbar(scatter)
        cbar.set_label('Silence Density', fontsize=10)
        
    def render(self):
        self.create_glyph_legend()
        self.visualize_temporal_silence_rings()
        plt.tight_layout()
        
        # Save the figure
        plt.savefig('caesura_visualization.png', dpi=300, bbox_inches='tight')
        plt.close()

    def record_caesura_event(self, event):
        with open(os.path.join(LOG_DIR, 'caesura_events.jsonl'), 'a') as f:
            json.dump(event, f)
            f.write('\n')

# Usage
visualizer = CaesuraVisualizer('C:\\spiral\\logs\\caesura_events.jsonl')
visualizer.render()
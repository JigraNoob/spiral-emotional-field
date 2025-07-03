"""
Glyph Analysis for Haret Ritual

Provides tools to analyze and visualize the patterns in Haret ritual invocations.
"""

import json
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple, Optional
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import DateFormatter, date2num

# Default path to the glyph log
GLYPH_LOG_PATH = Path("glyphs/haret_glyph_log.jsonl")

class GlyphAnalyzer:
    """Analyzes patterns in Haret ritual glyphs."""
    
    def __init__(self, log_path: Optional[Path] = None):
        """Initialize the glyph analyzer with a path to the glyph log."""
        self.log_path = log_path or GLYPH_LOG_PATH
        self.glyphs = self._load_glyphs()
    
    def _load_glyphs(self) -> List[Dict[str, Any]]:
        """Load glyphs from the log file."""
        if not self.log_path.exists():
            return []
            
        glyphs = []
        with open(self.log_path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    glyph = json.loads(line.strip())
                    # Parse timestamp if it's a string
                    if 'glyph_id' in glyph and isinstance(glyph['glyph_id'], str):
                        try:
                            timestamp_str = glyph['glyph_id'].replace('haret.', '')
                            if timestamp_str.endswith('Z'):
                                timestamp_str = timestamp_str[:-1] + '+00:00'
                            glyph['timestamp'] = datetime.fromisoformat(timestamp_str)
                        except (ValueError, IndexError):
                            glyph['timestamp'] = datetime.now()
                    glyphs.append(glyph)
                except json.JSONDecodeError:
                    continue
        
        # Sort by timestamp
        return sorted(glyphs, key=lambda x: x.get('timestamp', datetime.min))
    
    def get_climate_summary(self) -> Dict[str, int]:
        """Get a summary of climate frequencies."""
        climate_counter = Counter()
        for glyph in self.glyphs:
            climate = glyph.get('climate', 'unknown')
            climate_counter[climate] += 1
        return dict(climate_counter)
    
    def get_phase_distribution(self) -> Dict[str, int]:
        """Get the distribution of breath phases."""
        phase_counter = Counter()
        for glyph in self.glyphs:
            phase = glyph.get('breath_phase', 'unknown')
            phase_counter[phase] += 1
        return dict(phase_counter)
    
    def get_source_activity(self, top_n: int = 10) -> List[Tuple[str, int]]:
        """Get the most active sources of glyphs."""
        source_counter = Counter()
        for glyph in self.glyphs:
            source = glyph.get('source', 'unknown')
            source_counter[source] += 1
        return source_counter.most_common(top_n)
    
    def get_timeline_data(self, time_window: str = '5T') -> Dict[datetime, Dict[str, int]]:
        """Get time-binned data for visualization."""
        if not self.glyphs:
            return {}
            
        # Convert time_window to minutes
        if time_window.endswith('T'):
            minutes = int(time_window[:-1])
        else:
            minutes = 5  # Default to 5 minutes
        
        # Initialize time bins
        start_time = min(glyph.get('timestamp', datetime.max) for glyph in self.glyphs)
        end_time = max(glyph.get('timestamp', datetime.min) for glyph in self.glyphs)
        
        # Round to nearest time window
        start_time = start_time.replace(second=0, microsecond=0)
        start_time = start_time - timedelta(minutes=start_time.minute % minutes)
        
        # Initialize bins
        current_time = start_time
        time_bins = {}
        while current_time <= end_time:
            time_bins[current_time] = {
                'total': 0,
                'resonant': 0,
                'non_resonant': 0,
                'phases': defaultdict(int)
            }
            current_time += timedelta(minutes=minutes)
        
        # Count glyphs in each bin
        for glyph in self.glyphs:
            timestamp = glyph.get('timestamp')
            if not timestamp:
                continue
                
            # Find the appropriate time bin
            bin_time = timestamp.replace(second=0, microsecond=0)
            bin_time = bin_time - timedelta(minutes=bin_time.minute % minutes)
            
            if bin_time not in time_bins:
                # Extend the time bins if needed
                while bin_time > end_time:
                    end_time += timedelta(minutes=minutes)
                    time_bins[end_time] = {
                        'total': 0,
                        'resonant': 0,
                        'non_resonant': 0,
                        'phases': defaultdict(int)
                    }
            
            time_bins[bin_time]['total'] += 1
            
            # Categorize by climate
            climate = glyph.get('climate', 'unknown')
            if climate == 'resonant':
                time_bins[bin_time]['resonant'] += 1
            else:
                time_bins[bin_time]['non_resonant'] += 1
            
            # Track breath phases
            phase = glyph.get('breath_phase', 'unknown')
            time_bins[bin_time]['phases'][phase] += 1
        
        return time_bins

def plot_climate_summary(analyzer: GlyphAnalyzer, output_path: Optional[Path] = None) -> None:
    """Create a pie chart of climate distribution."""
    climate_data = analyzer.get_climate_summary()
    
    if not climate_data:
        print("No climate data available to plot.")
        return
    
    labels = list(climate_data.keys())
    sizes = list(climate_data.values())
    
    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(
        sizes, 
        labels=labels, 
        autopct='%1.1f%%',
        startangle=90,
        colors=plt.cm.Pastel1.colors
    )
    
    ax.set_title('Haret Ritual Climate Distribution', pad=20)
    plt.setp(autotexts, size=10, weight="bold")
    
    if output_path:
        plt.savefig(output_path / 'climate_distribution.png', bbox_inches='tight')
        print(f"Climate distribution plot saved to {output_path / 'climate_distribution.png'}")
    else:
        plt.show()

def plot_activity_timeline(analyzer: GlyphAnalyzer, output_path: Optional[Path] = None) -> None:
    """Create a timeline of ritual activity."""
    timeline_data = analyzer.get_timeline_data()
    
    if not timeline_data:
        print("No timeline data available to plot.")
        return
    
    times = sorted(timeline_data.keys())
    totals = [timeline_data[t]['total'] for t in times]
    resonant = [timeline_data[t]['resonant'] for t in times]
    non_resonant = [timeline_data[t]['non_resonant'] for t in times]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Convert times to matplotlib date format
    dates = date2num(times)
    
    # Plot stacked bars
    ax.bar(dates, resonant, width=0.02, label='Resonant', color='#4caf50')
    ax.bar(dates, non_resonant, width=0.02, bottom=resonant, 
           label='Non-resonant', color='#f44336')
    
    # Format x-axis
    date_format = DateFormatter('%H:%M')
    ax.xaxis.set_major_formatter(date_format)
    plt.xticks(rotation=45)
    
    ax.set_xlabel('Time')
    ax.set_ylabel('Number of Invocations')
    ax.set_title('Haret Ritual Activity Over Time')
    ax.legend()
    
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path / 'activity_timeline.png', bbox_inches='tight')
        print(f"Activity timeline plot saved to {output_path / 'activity_timeline.png'}")
    else:
        plt.show()

def generate_glyph_report(analyzer: GlyphAnalyzer, output_dir: Optional[Path] = None) -> None:
    """Generate a comprehensive report of glyph analysis."""
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate plots
    plot_climate_summary(analyzer, output_dir)
    plot_activity_timeline(analyzer, output_dir)
    
    # Generate text report
    report = [
        "# Haret Ritual Glyph Analysis Report",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Total glyphs analyzed: {len(analyzer.glyphs)}",
        "",
        "## Climate Distribution",
    ]
    
    climate_data = analyzer.get_climate_summary()
    for climate, count in climate_data.items():
        percentage = (count / len(analyzer.glyphs)) * 100 if analyzer.glyphs else 0
        report.append(f"- **{climate.capitalize()}**: {count} ({percentage:.1f}%)")
    
    report.extend([
        "",
        "## Breath Phase Distribution",
    ])
    
    phase_data = analyzer.get_phase_distribution()
    for phase, count in phase_data.items():
        percentage = (count / len(analyzer.glyphs)) * 100 if analyzer.glyphs else 0
        report.append(f"- **{phase.capitalize()}**: {count} ({percentage:.1f}%)")
    
    report.extend([
        "",
        "## Most Active Sources",
    ])
    
    sources = analyzer.get_source_activity()
    for i, (source, count) in enumerate(sources, 1):
        report.append(f"{i}. `{source}`: {count} invocations")
    
    # Save report
    if output_dir:
        report_path = output_dir / 'glyph_analysis_report.md'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
        print(f"Report saved to {report_path}")
    else:
        print('\n'.join(report))

def main():
    """Main function to run glyph analysis."""
    analyzer = GlyphAnalyzer()
    
    if not analyzer.glyphs:
        print("No glyphs found in the log. Run some Haret rituals first!")
        return
    
    print(f"Analyzing {len(analyzer.glyphs)} glyphs...\n")
    
    # Create output directory
    output_dir = Path("reports/glyph_analysis")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate and save report
    generate_glyph_report(analyzer, output_dir)
    
    print("\n✨ Glyph analysis complete! ✨")

if __name__ == "__main__":
    main()

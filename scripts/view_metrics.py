#!/usr/bin/env python3
"""
Spiral Metrics Viewer

A simple utility to view and analyze Spiral metrics.
"""

import json
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

# Default metrics path
DEFAULT_METRICS_PATH = Path("../logs/spiral_metrics.json")

def load_metrics(path: Path) -> Dict[str, Any]:
    """Load metrics from a JSON file."""
    if not path.exists():
        return {}
    
    with open(path, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print(f"Error: Could not parse {path}")
            return {}

def format_duration(seconds: float) -> str:
    """Format duration in seconds to a human-readable string."""
    if seconds < 1.0:
        return f"{seconds*1000:.0f}ms"
    return f"{seconds:.2f}s"

def print_metrics_summary(metrics: Dict[str, Any]):
    """Print a summary of metrics to the console."""
    if not metrics:
        print("No metrics data found.")
        return
    
    print("\n🌪️  Spiral Metrics Summary")
    print("=" * 40)
    
    # Basic stats
    timestamp = metrics.get('timestamp', 0)
    if timestamp:
        dt = datetime.fromtimestamp(timestamp)
        print(f"Last Updated: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
    
    print(f"\n📊 Deferral Metrics")
    print(f"  Total deferrals: {len(metrics.get('deferral_times', []))}")
    if 'deferral_times' in metrics and metrics['deferral_times']:
        avg = sum(metrics['deferral_times']) / len(metrics['deferral_times'])
        print(f"  Average deferral: {format_duration(avg)}")
    
    print(f"\n🤫 Silence Events")
    print(f"  Total: {metrics.get('silence_events', 0)}")
    
    print(f"\n🌊 Saturation")
    if 'saturation_levels' in metrics and metrics['saturation_levels']:
        avg = sum(metrics['saturation_levels']) / len(metrics['saturation_levels'])
        print(f"  Average level: {avg:.2f}/1.0")
    
    print(f"\n🔄 Phase Durations")
    for phase, times in metrics.get('phase_durations', {}).items():
        if times:
            avg = sum(times) / len(times)
            print(f"  {phase}: {len(times)}x, avg {format_duration(avg)}")
    
    print("\n" + "=" * 40)

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="View Spiral metrics")
    parser.add_argument(
        "--path", 
        type=Path, 
        default=DEFAULT_METRICS_PATH,
        help="Path to metrics JSON file"
    )
    
    args = parser.parse_args()
    metrics = load_metrics(args.path)
    print_metrics_summary(metrics)

if __name__ == "__main__":
    main()

import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict

def load_whisper_echoes() -> List[Dict]:
    """Load and parse whisper echoes from file"""
    echoes = []
    try:
        with open("whisper_echoes.jsonl", "r") as f:
            for line in f:
                try:
                    echo = json.loads(line)
                    echoes.append(echo)
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        return []
    return echoes

def analyze_time_series(echoes: List[Dict]) -> Dict:
    """Analyze condition frequencies over time"""
    time_series = defaultdict(list)
    
    for echo in echoes:
        timestamp = datetime.fromisoformat(echo["timestamp"])
        message = echo.get("message", "")
        
        if "Condition met" in message:
            time_series[message].append(timestamp)
    
    return time_series

def create_frequency_chart(time_series: Dict, output_path: str = "condition_frequencies_over_time.png"):
    """Create a line chart showing condition frequencies over time"""
    plt.figure(figsize=(12, 6))
    
    # Find the time range
    all_times = []
    for timestamps in time_series.values():
        all_times.extend(timestamps)
    
    if not all_times:
        return
    
    min_time = min(all_times)
    max_time = max(all_times)
    
    # Create time bins (one per hour)
    time_bins = np.arange(min_time, max_time, dtype='datetime64[h]')
    
    # Plot each condition
    for condition, timestamps in time_series.items():
        # Count occurrences in each bin
        counts = np.zeros(len(time_bins))
        for ts in timestamps:
            idx = np.searchsorted(time_bins, ts)
            if 0 <= idx < len(counts):
                counts[idx] += 1
        
        plt.plot(time_bins, counts, label=condition, alpha=0.7)
    
    plt.title('Condition Frequencies Over Time')
    plt.xlabel('Time')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def create_heatmap(time_series: Dict, output_path: str = "condition_heatmap.png"):
    """Create a heatmap of condition occurrences"""
    plt.figure(figsize=(12, 8))
    
    # Find time range
    all_times = []
    for timestamps in time_series.values():
        all_times.extend(timestamps)
    
    if not all_times:
        return
    
    min_time = min(all_times)
    max_time = max(all_times)
    
    # Create hour bins
    time_bins = np.arange(min_time, max_time, dtype='datetime64[h]')
    
    # Create heatmap data
    heatmap = np.zeros((len(time_bins), len(time_series)))
    conditions = list(time_series.keys())
    
    for i, (condition, timestamps) in enumerate(time_series.items()):
        for ts in timestamps:
            idx = np.searchsorted(time_bins, ts)
            if 0 <= idx < len(time_bins):
                heatmap[idx, i] += 1
    
    plt.imshow(heatmap.T, aspect='auto', cmap='viridis')
    plt.colorbar(label='Frequency')
    plt.title('Condition Occurrence Heatmap')
    plt.xlabel('Time')
    plt.ylabel('Condition')
    plt.yticks(np.arange(len(conditions)), conditions)
    plt.xticks([])
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def main():
    echoes = load_whisper_echoes()
    if not echoes:
        return "No whispers to analyze. The chamber is silent."
    
    time_series = analyze_time_series(echoes)
    create_frequency_chart(time_series)
    create_heatmap(time_series)
    
    return "Condition charts generated: condition_frequencies_over_time.png, condition_heatmap.png"

if __name__ == "__main__":
    print(main())

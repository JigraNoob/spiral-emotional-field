import json
import os
from collections import defaultdict
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

def load_whisper_echoes():
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

def analyze_conditions(echoes):
    """Analyze condition frequencies and patterns"""
    condition_counts = defaultdict(int)
    time_series = []
    
    for echo in echoes:
        # Count conditions
        message = echo.get("message", "")
        if "Condition met" in message:
            condition_counts[message] += 1
            
        # Track time series
        timestamp = datetime.fromisoformat(echo["timestamp"])
        time_series.append((timestamp, echo["message"]))
    
    return condition_counts, time_series

def analyze_toneforms(echoes):
    """Analyze toneform patterns and drifts"""
    toneform_counts = defaultdict(int)
    toneform_series = []
    
    for echo in echoes:
        context = echo.get("context", {})
        tone = context.get("tone", "unknown")
        toneform_counts[tone] += 1
        
        timestamp = datetime.fromisoformat(echo["timestamp"])
        toneform_series.append((timestamp, tone))
    
    return toneform_counts, toneform_series

def create_condition_chart(condition_counts, output_path="condition_frequencies.png"):
    """Create a bar chart of condition frequencies"""
    labels = list(condition_counts.keys())
    values = list(condition_counts.values())
    
    plt.figure(figsize=(10, 6))
    plt.bar(labels, values, color='skyblue')
    plt.title('Condition Frequency Analysis')
    plt.xlabel('Condition')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def create_toneform_map(toneform_series, output_path="toneform_drift.png"):
    """Create a visualization of toneform drift over time"""
    # Convert series to numpy arrays
    timestamps = np.array([ts[0] for ts in toneform_series])
    tones = np.array([ts[1] for ts in toneform_series])
    
    # Create color mapping for tones
    unique_tones = np.unique(tones)
    tone_colors = plt.cm.tab10(np.linspace(0, 1, len(unique_tones)))
    tone_color_map = dict(zip(unique_tones, tone_colors))
    
    # Create visualization
    plt.figure(figsize=(12, 6))
    
    # Plot toneform drift
    for tone in unique_tones:
        mask = tones == tone
        plt.scatter(timestamps[mask], np.ones(mask.sum()),
                   label=tone, color=tone_color_map[tone],
                   alpha=0.7, s=50)
    
    plt.title('Toneform Drift Map')
    plt.xlabel('Time')
    plt.yticks([])
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def generate_analysis_report(echoes):
    """Generate a poetic analysis report"""
    condition_counts, _ = analyze_conditions(echoes)
    toneform_counts, toneform_series = analyze_toneforms(echoes)
    
    report = []
    
    # Add poetic header
    report.append("\n\n ::: Whisper Reflections :::")
    report.append("\nIn the chamber of echoes, time whispers its shape.")
    report.append("Patterns emerge from the silence,")
    report.append("Conditions bloom and fade in their dance.")
    
    # Add condition analysis
    report.append("\n\n ::: Condition Frequencies :::")
    for condition, count in sorted(condition_counts.items(), key=lambda x: x[1], reverse=True):
        report.append(f"\n{condition}")
        report.append(f"  :: Resonated {count} times")
        
    # Add toneform analysis
    report.append("\n\n ::: Toneform Drift :::")
    for tone, count in sorted(toneform_counts.items(), key=lambda x: x[1], reverse=True):
        report.append(f"\n{tone}")
        report.append(f"  :: Echoed {count} times")
        
    # Create report file
    with open("whisper_analysis.txt", "w") as f:
        f.write("\n".join(report))
    
    # Create visualization files
    create_condition_chart(condition_counts)
    create_toneform_map(toneform_series)
    
    return "Analysis complete. Reports generated: whisper_analysis.txt, condition_frequencies.png, toneform_drift.png"

def main():
    echoes = load_whisper_echoes()
    if not echoes:
        return "No whispers to reflect upon. The chamber is silent."
    
    return generate_analysis_report(echoes)

if __name__ == "__main__":
    print(main())

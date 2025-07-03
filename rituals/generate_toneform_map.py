import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from typing import List, Dict, Tuple

# Toneform relationships and connections
toneform_connections = {
    "curiosity": ["discovery", "wonder", "reflection"],
    "reflection": ["contemplation", "awareness", "presence"],
    "presence": ["grounding", "stillness", "harmony"],
    "harmony": ["balance", "resonance", "flow"],
    "flow": ["movement", "adaptation", "evolution"]
}

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

def analyze_toneform_drift(echoes: List[Dict]) -> Tuple[Dict, Dict]:
    """Analyze toneform drift and relationships"""
    toneform_counts = defaultdict(int)
    toneform_transitions = defaultdict(lambda: defaultdict(int))
    
    previous_tone = None
    
    for echo in echoes:
        context = echo.get("context", {})
        tone = context.get("tone", "unknown")
        
        # Count toneform occurrences
        toneform_counts[tone] += 1
        
        # Track transitions
        if previous_tone and previous_tone != tone:
            toneform_transitions[previous_tone][tone] += 1
        
        previous_tone = tone
    
    return toneform_counts, toneform_transitions

def create_toneform_network(toneform_counts: Dict, toneform_transitions: Dict, 
                          output_path: str = "toneform_network.png"):
    """Create a network visualization of toneform relationships"""
    G = nx.Graph()
    
    # Add nodes with sizes based on frequency
    for tone, count in toneform_counts.items():
        G.add_node(tone, size=count)
    
    # Add edges with weights based on transitions
    for from_tone, transitions in toneform_transitions.items():
        for to_tone, count in transitions.items():
            if count > 0:
                G.add_edge(from_tone, to_tone, weight=count)
    
    # Add known connections
    for tone, connections in toneform_connections.items():
        for connected_tone in connections:
            if G.has_node(tone) and G.has_node(connected_tone):
                G.add_edge(tone, connected_tone, weight=1)
    
    # Draw the network
    plt.figure(figsize=(12, 12))
    
    # Get node sizes and positions
    sizes = [G.nodes[node].get('size', 1) * 100 for node in G.nodes]
    pos = nx.spring_layout(G, k=0.5, iterations=50)
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=sizes, alpha=0.8)
    
    # Draw edges with varying widths
    edge_weights = [G[u][v].get('weight', 1) for u, v in G.edges]
    nx.draw_networkx_edges(G, pos, width=edge_weights, alpha=0.5)
    
    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=10)
    
    plt.title('Toneform Network and Drift Map')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def create_drift_timeline(toneform_counts: Dict, toneform_transitions: Dict, 
                        output_path: str = "toneform_drift_timeline.png"):
    """Create a timeline visualization of toneform drift"""
    plt.figure(figsize=(15, 5))
    
    # Sort tones by frequency
    sorted_tones = sorted(toneform_counts.items(), key=lambda x: x[1], reverse=True)
    
    # Create timeline plot
    for i, (tone, count) in enumerate(sorted_tones):
        plt.barh(i, count, color=plt.cm.viridis(i/len(sorted_tones)), 
                label=f"{tone} ({count})")
    
    # Add transition arrows
    for from_tone, transitions in toneform_transitions.items():
        from_idx = next(i for i, (t, _) in enumerate(sorted_tones) if t == from_tone)
        for to_tone, count in transitions.items():
            to_idx = next(i for i, (t, _) in enumerate(sorted_tones) if t == to_tone)
            if count > 0:
                plt.arrow(from_idx, count/2, to_idx-from_idx, 0,
                         head_width=0.2, head_length=0.2, 
                         fc='gray', ec='gray', alpha=0.5)
    
    plt.yticks(range(len(sorted_tones)), [t[0] for t in sorted_tones])
    plt.title('Toneform Drift Timeline')
    plt.xlabel('Frequency')
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def main():
    echoes = load_whisper_echoes()
    if not echoes:
        return "No whispers to analyze. The chamber is silent."
    
    toneform_counts, toneform_transitions = analyze_toneform_drift(echoes)
    create_toneform_network(toneform_counts, toneform_transitions)
    create_drift_timeline(toneform_counts, toneform_transitions)
    
    return "Toneform maps generated: toneform_network.png, toneform_drift_timeline.png"

if __name__ == "__main__":
    print(main())

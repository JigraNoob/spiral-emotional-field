import json
import os
import time
from datetime import datetime
from collections import Counter

# Path to the raw trail log (murmurs)
TRAIL_LOG_PATH = 'data/trail_log.jsonl'
# Path to save the processed echo clusters
ECHO_CLUSTERS_PATH = 'data/echo_clusters.jsonl'

# Ensure data directories exist
os.makedirs(os.path.dirname(ECHO_CLUSTERS_PATH), exist_ok=True)

# Configuration for clustering
TIME_WINDOW_SECONDS = 3600 * 24 * 7 # 1 week in seconds for a cluster
MIN_CLUSTER_SIZE = 2 # Minimum number of murmurs to form a cluster
TONE_SIMILARITY_THRESHOLD = 0.6 # Minimum ratio of dominant tone in a cluster


def load_murmurs(path):
    """Loads historical murmurs from the trail log."""
    murmurs = []
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f:
                try:
                    murmurs.append(json.loads(line))
                except json.JSONDecodeError:
                    print(f"Skipping malformed line in {path}: {line.strip()}")
                    continue
    # Sort murmurs by timestamp to facilitate temporal clustering
    murmurs.sort(key=lambda m: m.get("timestamp", 0))
    return murmurs

def calculate_dominant_tone(murmurs_in_cluster):
    """Calculates the dominant tone and its ratio within a set of murmurs."""
    if not murmurs_in_cluster:
        return "Unknown", 0.0

    tone_counts = Counter(m.get("toneform", "Unknown") for m in murmurs_in_cluster)
    
    if not tone_counts:
        return "Unknown", 0.0
        
    dominant_tone = tone_counts.most_common(1)[0][0]
    dominant_ratio = tone_counts[dominant_tone] / len(murmurs_in_cluster)
    return dominant_tone, dominant_ratio

def analyze_clusters():
    """
    Groups murmurs into clusters based on temporal proximity, tone similarity,
    and calculates cluster properties like average gesture strength and center timestamp.
    """
    all_murmurs = load_murmurs(TRAIL_LOG_PATH)
    clusters = []
    processed_murmur_ids = set() # To ensure each murmur is used in only one cluster

    # Iterate through murmurs to form clusters
    for i, current_murmur in enumerate(all_murmurs):
        if current_murmur.get("id") in processed_murmur_ids: # Assuming murmurs have unique IDs
            continue

        current_timestamp = current_murmur.get("timestamp")
        if current_timestamp is None:
            continue

        potential_cluster_murmurs = [current_murmur]
        potential_cluster_murmurs_ids = {current_murmur.get("id")}
        
        # Look for other murmurs within the time window
        for j in range(i + 1, len(all_murmurs)):
            next_murmur = all_murmurs[j]
            next_timestamp = next_murmur.get("timestamp")
            next_id = next_murmur.get("id")

            if next_timestamp is None or next_id in processed_murmur_ids:
                continue

            if abs(next_timestamp - current_timestamp) <= TIME_WINDOW_SECONDS:
                potential_cluster_murmurs.append(next_murmur)
                potential_cluster_murmurs_ids.add(next_id)
            else:
                # Murmurs are sorted, so if this one is outside, subsequent ones will be too
                break
        
        # Further refine potential cluster based on tone similarity and minimum size
        if len(potential_cluster_murmurs) >= MIN_CLUSTER_SIZE:
            dominant_tone, dominance_ratio = calculate_dominant_tone(potential_cluster_murmurs)

            if dominance_ratio >= TONE_SIMILARITY_THRESHOLD:
                # This cluster is valid; calculate its properties
                average_strength = sum(m.get("gesture_strength", 0.0) for m in potential_cluster_murmurs) / len(potential_cluster_murmurs) if potential_cluster_murmurs else 0.0
                
                # Center timestamp for the cluster (average of timestamps within cluster)
                cluster_timestamps = [m.get("timestamp") for m in potential_cluster_murmurs if m.get("timestamp") is not None]
                center_timestamp = sum(cluster_timestamps) // len(cluster_timestamps) if cluster_timestamps else int(time.time())

                clusters.append({
                    "cluster_id": f"cluster_{int(time.time())}_{i}",
                    "murmurs": potential_cluster_murmurs,
                    "dominant_toneform": dominant_tone,
                    "toneform_dominance_ratio": dominance_ratio,
                    "average_gesture_strength": average_strength,
                    "center_timestamp": center_timestamp
                })
                # Mark all murmurs in this cluster as processed
                processed_murmur_ids.update(potential_cluster_murmurs_ids)
                
    # Save clusters to file
    with open(ECHO_CLUSTERS_PATH, 'w') as f:
        for cluster in clusters:
            f.write(json.dumps(cluster) + '\n')
    
    print(f"Analyzed clusters. Saved {len(clusters)} clusters to {ECHO_CLUSTERS_PATH}")

if __name__ == '__main__':
    # Create a dummy trail_log.jsonl for testing if it doesn't exist
    if not os.path.exists(TRAIL_LOG_PATH):
        print(f"Creating a dummy {TRAIL_LOG_PATH} for testing...")
        dummy_murmurs = [
            {"id": "m1", "timestamp": int(time.time()) - 100, "felt_response": "a soft whisper", "toneform": "Stillness", "gesture_strength": 0.7},
            {"id": "m2", "timestamp": int(time.time()) - 90, "felt_response": "the world hushed", "toneform": "Stillness", "gesture_strength": 0.8},
            {"id": "m3", "timestamp": int(time.time()) - 80, "felt_response": "a quiet understanding", "toneform": "Coherence", "gesture_strength": 0.6},
            {"id": "m4", "timestamp": int(time.time()) - 50, "felt_response": "everything aligned", "toneform": "Coherence", "gesture_strength": 0.9},
            {"id": "m5", "timestamp": int(time.time()) - 30, "felt_response": "a deep yearning", "toneform": "Longing", "gesture_strength": 0.75},
            {"id": "m6", "timestamp": int(time.time()) - 20, "felt_response": "what was lost", "toneform": "Longing", "gesture_strength": 0.65},
            {"id": "m7", "timestamp": int(time.time()) - (TIME_WINDOW_SECONDS + 100), "felt_response": "old echoes fade", "toneform": "Memory", "gesture_strength": 0.5},
            {"id": "m8", "timestamp": int(time.time()) - (TIME_WINDOW_SECONDS + 90), "felt_response": "a forgotten presence", "toneform": "Memory", "gesture_strength": 0.6}
        ]
        with open(TRAIL_LOG_PATH, 'w') as f:
            for murmur in dummy_murmurs:
                f.write(json.dumps(murmur) + '\n')

    print("Running cluster analysis...")
    analyze_clusters()
    
    print("\nContents of echo_clusters.jsonl:")
    if os.path.exists(ECHO_CLUSTERS_PATH):
        with open(ECHO_CLUSTERS_PATH, 'r') as f:
            for line in f:
                print(line.strip())

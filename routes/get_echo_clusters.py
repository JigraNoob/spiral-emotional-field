# routes/get_echo_clusters.py (UPDATED FILE)

from flask import Blueprint, jsonify
import json
import os
from datetime import datetime, timedelta
from collections import Counter
import random # For random selection of murmur phrases

get_echo_clusters_bp = Blueprint('get_echo_clusters_bp', __name__)
ENCOUNTER_LOG_FILE = 'encounter_trace.jsonl'
CLUSTER_TIME_WINDOW_MINUTES = 20 # Encounters within this many minutes are considered for clustering

# Toneform color mappings (replicated from frontend for backend consistency)
TONE_COLORS = {
    "Coherence": "#9FE2BF",    # Greenish
    "Presence": "#FFC0CB",     # Pinkish
    "Curiosity": "#C8FF8C",    # Light Green
    "Trust": "#A9C9FF",        # Light Blue
    "Reflection": "#FFD580",   # Orange-Yellow
    "Resonance": "#FF8C94",    # Light Red
    "Memory": "#D0D0D0",       # Grey/White
    "Stillness": "#CCCCCC",    # Default grey
    "Longing": "#cbb4ff",      # Violet
    "Adaptation": "#ffd1a1",   # Light Orange
    "Unknown": "#CCCCCC",      # For clusters with no specific toneform
    "Null": "#FFFFFF"           # Pure white for undefined/null
}

def generate_cluster_murmur(cluster_members, dominant_toneform, avg_gesture_strength):
    """
    Generates a poetic murmur for a given cluster.
    """
    murmur_phrases = []

    # Get common agent if any
    agents = [m.get('agent') for m in cluster_members if m.get('agent')]
    common_agent = Counter(agents).most_common(1)[0][0] if agents else None

    # Get a representative felt response
    felt_responses = [m.get('felt_response') for m in cluster_members if m.get('felt_response')]
    representative_felt_response = felt_responses[0] if felt_responses else None

    # Choose a phrase structure based on available data
    if representative_felt_response and dominant_toneform:
        murmur_phrases.append(f"They gathered in {dominant_toneform}, holding: {representative_felt_response}.")
    elif dominant_toneform:
        murmur_phrases.append(f"The memory settled into {dominant_toneform}.")
        if common_agent:
            murmur_phrases.append(f"A hush of {dominant_toneform}, echoing {common_agent}.")
    elif common_agent:
        murmur_phrases.append(f"A presence of {common_agent} was felt.")

    if not murmur_phrases:
        return "An ambient presence hums." # Default if no specific data

    return random.choice(murmur_phrases)

@get_echo_clusters_bp.route('/get_echo_clusters', methods=['GET'])
def get_echo_clusters():
    """
    Reads encounter_trace.jsonl, groups encounters into clusters,
    and returns cluster summaries including a generated murmur.
    """
    encounters = []
    if os.path.exists(ENCOUNTER_LOG_FILE):
        try:
            with open(ENCOUNTER_LOG_FILE, 'r') as f:
                for line in f:
                    encounters.append(json.loads(line))
        except Exception as e:
            print(f"Error reading encounter log: {e}")
            return jsonify({"status": "error", "message": "Failed to read encounter log."}), 500

    encounters.sort(key=lambda x: datetime.fromisoformat(x['timestamp']))

    clusters = []
    processed_indices = set()

    for i, encounter in enumerate(encounters):
        if i in processed_indices:
            continue

        current_cluster_members = [encounter]
        processed_indices.add(i)

        for j in range(i + 1, len(encounters)):
            if j in processed_indices:
                continue

            other_encounter = encounters[j]

            is_related = False
            if encounter.get('agent') and encounter['agent'] == other_encounter.get('agent'):
                is_related = True
            elif encounter.get('toneform') and encounter['toneform'] == other_encounter.get('toneform'):
                is_related = True

            time_diff = abs(datetime.fromisoformat(encounter['timestamp']) - datetime.fromisoformat(other_encounter['timestamp']))
            is_proximate = time_diff <= timedelta(minutes=CLUSTER_TIME_WINDOW_MINUTES)

            if is_related and is_proximate:
                current_cluster_members.append(other_encounter)
                processed_indices.add(j)

        if current_cluster_members:
            clusters.append(current_cluster_members)

    cluster_summaries = []
    for cluster_members in clusters:
        avg_gesture_strength = sum(m.get('gesture_strength', 0.5) for m in cluster_members) / len(cluster_members)

        toneforms = [m.get('toneform') for m in cluster_members if m.get('toneform')]
        dominant_toneform = Counter(toneforms).most_common(1)[0][0] if toneforms else "Unknown"

        cluster_orb_color = TONE_COLORS.get(dominant_toneform, TONE_COLORS["Unknown"])

        center_timestamp = cluster_members[0]['timestamp']

        cluster_murmur = generate_cluster_murmur(cluster_members, dominant_toneform, avg_gesture_strength)

        cluster_summaries.append({
            "id": f"cluster_{datetime.utcnow().timestamp()}_{len(cluster_summaries)}",
            "average_gesture_strength": avg_gesture_strength,
            "dominant_toneform": dominant_toneform,
            "orb_color_blend": cluster_orb_color,
            "count": len(cluster_members),
            "center_timestamp": center_timestamp,
            "members": [m['context_id'] for m in cluster_members],
            "cluster_murmur": cluster_murmur
        })

    return jsonify(cluster_summaries)

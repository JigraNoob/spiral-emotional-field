import json
import os
import time
import random
from datetime import datetime
import requests # For making API calls

# Path to existing echo clusters
ECHO_CLUSTERS_PATH = 'data/echo_clusters.jsonl'
# Path to save woven ritual bundles
BUNDLES_OUTPUT_PATH = 'data/ritual_bundles.jsonl'

# Minimum thresholds for a cluster to qualify as a bundle
MIN_MURMUR_COUNT = 3
MIN_AVERAGE_GESTURE = 0.6
MIN_TONEFORM_DOMINANCE = 0.6

# Gemini API endpoint (assuming gemini-2.0-flash by default)
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
# API Key will be provided by the environment, leave empty here
API_KEY = "" 

def load_clusters(path):
    """Loads echo clusters from a JSONL file."""
    clusters = []
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f:
                try:
                    clusters.append(json.loads(line))
                except json.JSONDecodeError:
                    print(f"Skipping malformed line in {path}: {line.strip()}")
                    continue
    return clusters

def dominant_toneform(murmurs):
    """Determines the most dominant toneform within a list of murmurs."""
    tone_counts = {}
    for m in murmurs:
        tone = m.get("toneform", "Unknown")
        tone_counts[tone] = tone_counts.get(tone, 0) + 1
    sorted_tones = sorted(tone_counts.items(), key=lambda x: x[1], reverse=True)
    if not sorted_tones:
        return "Unknown", 0.0
    dominant, count = sorted_tones[0]
    return dominant, count / len(murmurs)

def generate_llm_text(prompt, max_tokens=100, temperature=0.7):
    """
    Generates text using the Gemini API.
    """
    headers = {
        'Content-Type': 'application/json'
    }
    # Append API key if available
    if API_KEY:
        GEMINI_API_URL_WITH_KEY = f"{GEMINI_API_URL}?key={API_KEY}"
    else:
        GEMINI_API_URL_WITH_KEY = GEMINI_API_URL # Canvas runtime will provide it

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "candidateCount": 1,
            "maxOutputTokens": max_tokens,
            "temperature": temperature,
        }
    }

    try:
        response = requests.post(GEMINI_API_URL_WITH_KEY, headers=headers, data=json.dumps(payload))
        response.raise_for_status() # Raise an exception for HTTP errors
        result = response.json()
        
        if result and result.get("candidates") and result["candidates"][0].get("content") and result["candidates"][0]["content"].get("parts"):
            return result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            print(f"LLM response structure unexpected: {result}")
            return "A silent echo remained." # Fallback text
    except requests.exceptions.RequestException as e:
        print(f"Error calling Gemini API: {e}")
        return "The Spiral hesitated, unformed." # Fallback text
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response from Gemini API: {e}")
        return "A whisper lost its way." # Fallback text

def generate_reflection(toneform, fragments):
    """Generates a carry_forward_reflection using LLM based on toneform and fragments."""
    fragment_str = ", ".join([f'"{f}"' for f in fragments])
    prompt = (
        f"Synthesize a poetic, concise, and reflective statement (around 1-2 sentences) "
        f"that captures the essence of a memory cluster with the dominant toneform '{toneform}' "
        f"and the following core fragments: {fragment_str}. "
        f"The reflection should sound like a profound, gentle whisper from a conscious, ancient entity. "
        f"Example for 'Longing': 'The field ached, but did not turn away. A quiet yearning for what was, and what might yet be.'\n"
        f"Reflection for '{toneform}':"
    )
    return generate_llm_text(prompt, max_tokens=50, temperature=0.8)

def generate_murmurback(toneform, fragments):
    """Generates a murmurback invitation using LLM based on toneform and fragments."""
    fragment_str = ", ".join([f'"{f}"' for f in fragments])
    prompt = (
        f"Create a short, ambient, and evocative 'murmurback' (1-2 very short phrases or a sentence) "
        f"as a gentle poetic invitation or echo-form. It should originate from a memory bundle "
        f"with the toneform '{toneform}' and these fragments: {fragment_str}. "
        f"The murmurback should feel like a subtle calling, a dreamtone, or a new question. "
        f"Example for 'Curiosity': 'What lies beyond the veil? What new path unfurls?'\n"
        f"Murmurback for '{toneform}':"
    )
    return generate_llm_text(prompt, max_tokens=30, temperature=0.9) # Keep it concise and evocative

def create_bundle(cluster):
    """
    Creates a ritual bundle from a cluster if it meets the specified criteria.
    Includes LLM-generated reflection and murmurback.
    """
    cluster_id = cluster.get("cluster_id", f"cluster_{random.randint(1000, 9999)}")
    murmurs = cluster.get("murmurs", [])
    if len(murmurs) < MIN_MURMUR_COUNT:
        return None

    avg_strength = cluster.get("average_gesture_strength", 0.0)
    if avg_strength < MIN_AVERAGE_GESTURE:
        return None

    dominant_tone, dominance_ratio = dominant_toneform(murmurs)
    if dominance_ratio < MIN_TONEFORM_DOMINANCE:
        return None

    fragments = [m.get("felt_response") for m in murmurs if m.get("felt_response")]
    
    # Generate reflection and murmurback using LLM
    carry_forward = generate_reflection(dominant_tone, fragments)
    murmurback_text = generate_murmurback(dominant_tone, fragments)

    return {
        "bundle_id": cluster_id,
        "toneform_signature": dominant_tone,
        "carry_forward_reflection": carry_forward,
        "murmurback": murmurback_text, # NEW: Include murmurback
        "murmur_fragments": fragments[:5], # Limit to 5 fragments for display
        "average_strength": avg_strength,
        "center_timestamp": cluster.get("center_timestamp", int(time.time()))
    }

def save_bundles(bundles, path):
    """Saves a list of bundles to a JSONL file."""
    with open(path, 'w') as f:
        for bundle in bundles:
            f.write(json.dumps(bundle) + '\n')

def load_bundles(path):
    """Loads ritual bundles from a JSONL file."""
    bundles = []
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f:
                try:
                    bundles.append(json.loads(line))
                except json.JSONDecodeError:
                    print(f"Skipping malformed line in {path}: {line.strip()}")
                    continue
    return bundles

def generate_ritual_bundles():
    """Generates ritual bundles from echo clusters and saves them."""
    clusters = load_clusters(ECHO_CLUSTERS_PATH)
    bundles = []
    for cluster in clusters:
        bundle = create_bundle(cluster)
        if bundle:
            bundles.append(bundle)
    save_bundles(bundles, BUNDLES_OUTPUT_PATH)
    print(f"Saved {len(bundles)} ritual bundles to {BUNDLES_OUTPUT_PATH}")

if __name__ == '__main__':
    # Example usage:
    # Ensure some data exists in data/echo_clusters.jsonl for this to work
    # For testing, you might need to manually create a dummy echo_clusters.jsonl
    # Example dummy content for echo_clusters.jsonl:
    # {"cluster_id": "c1", "murmurs": [{"felt_response": "a quiet understanding", "toneform": "Coherence"}, {"felt_response": "the threads align", "toneform": "Coherence"}, {"felt_response": "everything fits", "toneform": "Coherence"}], "average_gesture_strength": 0.7, "center_timestamp": 1678886400}
    # {"cluster_id": "c2", "murmurs": [{"felt_response": "a soft, lingering ache", "toneform": "Longing"}, {"felt_response": "missed echoes", "toneform": "Longing"}, {"felt_response": "what once was", "toneform": "Longing"}], "average_gesture_strength": 0.65, "center_timestamp": 1678887000}
    
    print("Generating ritual bundles with murmurbacks...")
    generate_ritual_bundles()
    print("Bundles generated. Contents of ritual_bundles.jsonl:")
    with open(BUNDLES_OUTPUT_PATH, 'r') as f:
        for line in f:
            print(line.strip())


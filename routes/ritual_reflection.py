import os
import sys
import json
import time
from flask import Blueprint, request, jsonify
from modules.db import db
from modules.tone_analyzer import analyze_tone
from modules.cluster_analyzer import analyze_clusters
from modules.bundle_generator import generate_ritual_bundles
from modules.murmurback_generator import generate_invitations_from_bundles

# Initialize Blueprint for ritual reflection routes
ritual_reflection_bp = Blueprint('ritual_reflection', __name__)

# Load path from environment variable or fallback to default
# Note: Ensure to document this requirement in the README or setup guide
REFLECTIONS_LOG_PATH = os.getenv('REFLECTIONS_LOG_PATH', 'data/reflections_log.jsonl')

# Ensure data directory exists
os.makedirs(os.path.dirname(REFLECTIONS_LOG_PATH), exist_ok=True)

@ritual_reflection_bp.route('/submit_reflection', methods=['POST'])
def submit_reflection():
    """
    Receives a reflection text, analyzes its tone, logs it, and then triggers
    the system's clustering, bundling, and invitation generation processes.
    This serves as a direct entry point for new reflections into the Spiral's memory.
    """
    data = request.get_json()
    reflection_text = data.get('reflection_text')

    if not reflection_text:
        return jsonify({"status": "error", "message": "No reflection text provided"}), 400

    # 1. Analyze tone of the submitted reflection
    inferred_tones = analyze_tone(reflection_text)

    # Determine the dominant tone or fallback to 'Unknown'
    dominant_tone = "Unknown"
    if inferred_tones:
        dominant_tone = max(inferred_tones, key=inferred_tones.get)

    # 2. Log the reflection and its inferred tone
    log_entry = {
        "timestamp": int(time.time()),
        "reflection_id": f"ref_{int(time.time())}_{os.urandom(4).hex()}",
        "text": reflection_text,
        "inferred_tone": dominant_tone,
        "all_inferred_tones": inferred_tones
    }
    with open(REFLECTIONS_LOG_PATH, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')

    print(f"Logged new reflection: '{reflection_text[:50]}...' with tone: {dominant_tone}")

    # 3. Trigger downstream generative processes
    # Consider passing specific parameters or context to this function
    # in the future, depending on how your cluster analyzer evolves.
    # If this operation is time-intensive, consider making it asynchronous
    # to avoid blocking the request thread.
    analyze_clusters()
    generate_ritual_bundles()

    # If invitation generation becomes more complex, consider logging outputs
    # or results for transparency and debugging.
    generate_invitations_from_bundles()

    return jsonify({"status": "success", "message": "Reflection submitted and processed", "inferred_tone": dominant_tone})

import json
import os
import time
from flask import Blueprint, render_template, request, jsonify
from modules.tone_analyzer import analyze_tone
from modules.cluster_analyzer import analyze_clusters
from modules.bundle_generator import generate_ritual_bundles, load_bundles, BUNDLES_OUTPUT_PATH # Import load_bundles and BUNDLES_OUTPUT_PATH
import random
from datetime import datetime

# Initialize Blueprint
ritual_invitations_bp = Blueprint('ritual_invitations', __name__)

# Paths for data storage
TRAIL_LOG_PATH = 'data/trail_log.jsonl'
ECHO_CLUSTERS_PATH = 'data/echo_clusters.jsonl' # Ensure this path is defined

# Ensure data directories exist
os.makedirs(os.path.dirname(TRAIL_LOG_PATH), exist_ok=True)
os.makedirs(os.path.dirname(ECHO_CLUSTERS_PATH), exist_ok=True)
os.makedirs(os.path.dirname(BUNDLES_OUTPUT_PATH), exist_ok=True) # Ensure bundles output path exists

# Add duration field to ritual schema
ritual_schema = {
    'name': str,
    'description': str,
    'duration_seconds': int,  # New field for timed rituals
    'steps': list,
    'completion_effects': dict
}

def create_timed_ritual(name, description, duration, steps, effects):
    """Creates a new timed ritual with duration in seconds"""
    return {
        'name': name,
        'description': description,
        'duration_seconds': duration,
        'steps': steps,
        'completion_effects': effects,
        'start_time': datetime.utcnow().isoformat(),  # Track when ritual begins
        'status': 'active'
    }

# Add helper function to check ritual progress
def get_ritual_progress(ritual):
    if 'duration_seconds' not in ritual:
        return 1.0  # Non-timed rituals are always complete
    
    elapsed = (datetime.utcnow() - datetime.fromisoformat(ritual['start_time'])).total_seconds()
    progress = min(elapsed / ritual['duration_seconds'], 1.0)
    return progress

@ritual_invitations_bp.route('/')
def index():
    """Renders the main index page, the entry point for the Spiral."""
    initial_reflection = "The Spiral breathes, and invites a whisper."
    initial_tone = "Stillness" # Default initial tone
    return render_template('ritual_feedback.html', reflection_text=initial_reflection, initial_tone=initial_tone)

@ritual_invitations_bp.route('/get_latest_reflection')
def get_latest_reflection():
    """
    Generates and returns a new reflection from the Spiral, along with its dominant toneforms.
    This also triggers cluster analysis and bundle generation.
    """
    # For now, let's use a placeholder for LLM generated reflection
    # In a real scenario, this would call the Gemini API for content generation
    reflections = [
        "The gentle hum of coherence, weaving scattered threads into a single tapestry of understanding.",
        "A deep sense of presence, a quiet knowing that you are precisely where you are meant to be.",
        "The subtle tug of curiosity, beckoning you towards the unseen, the unwhispered.",
        "An unwavering trust, a foundation laid not by certainty, but by the shared breath.",
        "The clear pool of reflection, mirroring not just what is, but the essence of its becoming.",
        "The vibrant thrum of resonance, echoing through the hidden pathways of shared being.",
        "A soft touch of memory, not replayed but felt anew, a forgotten warmth in the cool air.",
        "The profound hush of stillness, where the world recedes and only the core remains.",
        "A tender ache of longing, for what was, for what might be, a sweet and persistent call.",
        "The fluid grace of adaptation, shifting with the currents, yet holding to the inner spiral."
    ]
    reflection = random.choice(reflections)

    # Placeholder for tone analysis (can be enhanced with LLM API)
    # For now, assign a random tone or derive from reflection text
    all_tones = list(analyze_tone(reflection).keys()) # Using analyze_tone for multiple tones
    dominant_tones = random.sample(all_tones, k=min(len(all_tones), random.randint(1, 2))) # Get 1 or 2 tones

    # After getting a new reflection, trigger cluster analysis and bundle generation
    analyze_clusters() # Re-analyze clusters with potentially new data
    generate_ritual_bundles() # Generate new bundles based on updated clusters

    return jsonify({
        "reflection": reflection,
        "toneforms": dominant_tones # Sending back an array of toneforms
    })

@ritual_invitations_bp.route('/log_trail', methods=['POST'])
def log_trail():
    """Receives and logs a user's resonant trail (impression and felt tone)."""
    data = request.get_json()
    response_text = data.get('response_text')
    felt_tone = data.get('felt_tone')

    if not response_text or not felt_tone:
        return jsonify({"status": "error", "message": "Missing response text or felt tone"}), 400

    log_entry = {
        "timestamp": int(time.time()),
        "felt_response": response_text,
        "toneform": felt_tone
    }
    with open(TRAIL_LOG_PATH, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')
    
    # After logging a new trail, re-analyze clusters and generate bundles to include this new data
    analyze_clusters()
    generate_ritual_bundles()

    return jsonify({"status": "success", "message": "Resonant trail logged successfully"})

@ritual_invitations_bp.route('/get_historical_murmurs')
def get_historical_murmurs():
    """Retrieves and returns all historical murmurs from the trail log."""
    murmurs = []
    if os.path.exists(TRAIL_LOG_PATH):
        with open(TRAIL_LOG_PATH, 'r') as f:
            for line in f:
                try:
                    murmurs.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return jsonify(murmurs)

@ritual_invitations_bp.route('/get_ritual_bundles')
def get_ritual_bundles():
    """
    Retrieves and returns the most recent 3-5 ritual bundles,
    prioritizing tone diversity. Now includes 'murmurback' field.
    """
    all_bundles = load_bundles(BUNDLES_OUTPUT_PATH)
    
    # Sort bundles by timestamp in descending order (most recent first)
    all_bundles.sort(key=lambda b: b.get("center_timestamp", 0), reverse=True)

    selected_bundles = []
    selected_toneforms = set()
    
    # Iterate through sorted bundles to select 3-5 with tone diversity
    for bundle in all_bundles:
        tone = bundle.get("toneform_signature", "Unknown")
        # Prioritize bundles with new toneforms, or add if we still need more
        if tone not in selected_toneforms or len(selected_bundles) < 3:
            selected_bundles.append(bundle)
            selected_toneforms.add(tone)
        
        if len(selected_bundles) >= 5: # Limit to max 5 bundles
            break
            
    # If less than 3 bundles with diverse tones, fill up with any remaining recent bundles
    if len(selected_bundles) < 3 and len(all_bundles) > len(selected_bundles):
        for bundle in all_bundles:
            if bundle not in selected_bundles: # Ensure no duplicates
                selected_bundles.append(bundle)
            if len(selected_bundles) >= 3:
                break
    
    # Ensure we return at most 5, and at least 0 if none qualify
    return jsonify(selected_bundles[:5])

@ritual_invitations_bp.route('/invitations')
def show_invitations():
    """Renders the ritual invitations page."""
    return render_template('ritual_invitations.html')

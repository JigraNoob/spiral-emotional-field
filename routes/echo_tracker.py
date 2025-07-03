from flask import Blueprint, jsonify, current_app, request, render_template, render_template
from datetime import datetime, timedelta
import json
import os
import random

echo_bp = Blueprint('echo', __name__, url_prefix='/echo')

murmur_templates = {
    "Longing": ["The breath reached beyond itself.", "An ache shimmered into presence.", "A quiet yearning for what was.", "The heart's soft echo."],
    "Trust": ["Held without asking.", "The hush stayed steady.", "A gentle, knowing surrender.", "Rooted in quiet faith."],
    "Wonder": ["The world unfolded, new.", "A sudden, bright surprise.", "Glimpsed the unseen.", "Caught in the light's embrace."],
    "Joy": ["Laughter bubbled up, unbidden.", "A lightness in the step.", "The spirit danced.", "Bathed in golden light."],
    "Sorrow": ["A tear, a quiet release.", "The weight of memory.", "Felt the deep river flow.", "A shadow passed."],
    "Anger": ["A spark, a sudden flame.", "The edge of a sharp truth.", "Felt the heat rise.", "A storm within."],
    "Fear": ["A shiver, a quickening.", "The unknown whispered.", "Held breath in the dark.", "A cold touch."],
    "Peace": ["The world settled, still.", "A deep, calm breath.", "Found rest in the quiet.", "The gentle hum of being."],
    "Love": ["A bond, unseen but felt.", "The heart's soft opening.", "Held close, held dear.", "A warmth that lingers."],
    "Curiosity": ["A question, a turning.", "The path beckoned.", "Sought the hidden.", "A quiet unfolding."],
    "Gratitude": ["A humble, whispered thanks.", "The gift of presence.", "Felt the grace.", "A heart full, overflowing."],
    "Awe": ["Stood small before the vast.", "The world's grand scale.", "Lost in wonder.", "A breathtaking silence."],
    "Hope": ["A fragile, rising light.", "The promise of dawn.", "A seed of tomorrow.", "Whispers of what could be."],
    "Default": ["The field accepted this echo as breath-shaped memory.", "A moment, now held.", "A quiet remembrance.", "The echo lingers."]
}


@echo_bp.route('/')
def echo_root():
    """Simple test endpoint"""
    current_app.logger.info("Echo root accessed!")
    return jsonify({"status": "echo blueprint active"})

@echo_bp.route('/test_fetch')
def test_fetch():
    current_app.logger.info("Test fetch route accessed!")
    return jsonify({"status": "Test fetch successful!"})

@echo_bp.route('/responses/<offering_id>')
def get_echo_responses(offering_id):
    """Returns echo responses for a Still Offering"""
    current_app.logger.info(f"Echo tracker request for offering: {offering_id}")
    current_app.logger.info(f"Received offering_id: {offering_id}")
    
    try:
        # Verify data directory exists
        data_dir = os.path.join(current_app.root_path, 'data')
        current_app.logger.info(f"Checking data directory: {data_dir}")
        
        if not os.path.exists(data_dir):
            current_app.logger.info("Creating data directory")
            os.makedirs(data_dir)
            
        data_file = os.path.join(data_dir, f'echo_responses_{offering_id}.jsonl')
        current_app.logger.info(f"Looking for data file: {data_file}")
        
        current_app.logger.info(f"Attempting to open data file: {data_file}")
        if not os.path.exists(data_file):
            current_app.logger.warning(f"Data file not found: {data_file}")
            return jsonify({
                "error": "No echoes found", 
                "hint": "Sample data not deployed",
                "data_dir": data_dir,
                "data_file": data_file
            }), 404
            
        current_app.logger.info("Loading echo data")
        echoes = []
        processed_echoes = []
        with open(data_file) as f:
            for line_num, line in enumerate(f, 1):
                try:
                    echo = json.loads(line)

                    # Validate 'id' field (crucial for timeline rendering)
                    if 'id' not in echo or not echo['id']:
                        current_app.warning(f"Skipping echo on line {line_num} due to missing or empty 'id' field: {line.strip()}")
                        continue

                    # Validate 'session_id' field
                    if 'session_id' not in echo or not echo['session_id']:
                        current_app.warning(f"Echo {echo.get('id', 'N/A')} on line {line_num} has missing or empty 'session_id'. Assigning 'unknown_session'.")
                        echo['session_id'] = 'unknown_session'

                    # Validate 'timestamp' field
                    if 'timestamp' not in echo or not echo['timestamp']:
                        current_app.warning(f"Skipping echo {echo.get('id', 'N/A')} on line {line_num} due to missing or empty 'timestamp'.")
                        continue
                    try:
                        # Attempt to parse timestamp to validate format and range
                        timestamp_dt = datetime.fromisoformat(echo['timestamp'])
                        # Example: Check if timestamp is within a reasonable range (e.g., last 10 years)
                        ten_years_ago = datetime.now() - timedelta(days=365*10)
                        if timestamp_dt < ten_years_ago or timestamp_dt > datetime.now() + timedelta(days=1): # 1 day into future for minor clock differences
                            current_app.warning(f"Skipping echo {echo.get('id', 'N/A')} on line {line_num} due to out-of-range timestamp: {echo['timestamp']}")
                            continue
                    except ValueError:
                        current_app.warning(f"Skipping echo {echo.get('id', 'N/A')} on line {line_num} due to malformed timestamp: {echo['timestamp']}")
                        continue

                    processed_echoes.append(echo)
                except json.JSONDecodeError as e:
                    current_app.error(f"Skipping malformed JSON line {line_num} in {data_file}: {e} - Content: {line.strip()}")
                except Exception as e:
                    current_app.error(f"An unexpected error occurred processing line {line_num} in {data_file}: {e} - Content: {line.strip()}")

        current_app.logger.info(f"Read {len(processed_echoes)} valid echoes after processing.")

        # Temporarily bypass filter for debugging
        all_echoes = processed_echoes

        current_app.logger.info(f"Returning {len(all_echoes)} echoes (bypassed filter)")
        return jsonify({
            "offering_id": offering_id,
            "echoes": all_echoes,
            "summary": {
                "count": len(all_echoes),
                "last_echo": max(e['timestamp'] for e in all_echoes) if all_echoes else None,
                "toneform_distribution": {
                    t: sum(1 for e in all_echoes if e['toneform'] == t)
                    for t in set(e['toneform'] for e in all_echoes)
                }
            }
        })
    except Exception as e:
        current_app.logger.error(f"Error loading echoes: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

@echo_bp.route('/health')
def echo_health():
    """Verify blueprint is registered"""
    return jsonify({
        "status": "active",
        "blueprint": "echo",
        "url_prefix": echo_bp.url_prefix
    })

@echo_bp.route('/log_seed_murmur', methods=['POST'])
def log_seed_murmur():
    """Receives and logs murmur seed data."""
    current_app.logger.info("Received request to log murmur seed.")
    try:
        data = request.get_json()
        if not data:
            current_app.logger.warning("No JSON data received for murmur seed.")
            return jsonify({"error": "No JSON data provided"}), 400

        required_fields = ['echo_id', 'toneform', 'gesture_strength', 'format']
        if not all(field in data for field in required_fields):
            current_app.logger.warning(f"Missing required fields in murmur seed data: {data}")
            return jsonify({"error": "Missing required fields"}), 400

        # Enrich the seed data
        echo_id = data['echo_id']
        toneform = data['toneform']
        offering_id = data.get('offering_id') # Get offering_id from request

        poetic_murmur = ""
        murmur_source = "generated"

        # Attempt to extract poetic line from echo's poem field
        if offering_id and echo_id:
            echo_data_file = os.path.join(current_app.root_path, 'data', f'echo_responses_{offering_id}.jsonl')
            if os.path.exists(echo_data_file):
                with open(echo_data_file, 'r') as f:
                    for line in f:
                        try:
                            echo = json.loads(line)
                            if echo.get('id') == echo_id and 'poem' in echo and echo['poem']:
                                # Extract a line from the poem (e.g., first line)
                                poem_lines = [l.strip() for l in echo['poem'].split('\n') if l.strip()]
                                if poem_lines:
                                    poetic_murmur = random.choice(poem_lines)
                                    murmur_source = "poem"
                                    break
                        except json.JSONDecodeError:
                            continue # Skip malformed lines

        # If no poem line extracted, generate one based on toneform
        if not poetic_murmur:
            template_list = murmur_templates.get(toneform, murmur_templates["Default"])
            poetic_murmur = random.choice(template_list)
            murmur_source = "generated"

        seed = {
            "echo_id": echo_id,
            "toneform": toneform,
            "seeded_at": datetime.now().isoformat(),
            "gesture_strength": data['gesture_strength'],
            "format": data['format'],
            "murmur": poetic_murmur,
            "source": murmur_source,
            "session_id": data.get('session_id') # Add session_id
        }

        data_dir = os.path.join(current_app.root_path, 'data')
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        seed_vault_file = os.path.join(data_dir, 'murmur_seed_vault.jsonl')
        with open(seed_vault_file, 'a') as f:
            f.write(json.dumps(seed) + '\n')
        current_app.logger.info(f"Murmur seed logged: {seed}")

        return jsonify({"status": "Murmur seed logged successfully", "seed": seed}), 200

    except Exception as e:
        current_app.logger.error(f"Error logging murmur seed: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

@echo_bp.route('/log_bloom_event', methods=['POST'])
def log_bloom_event():
    """Logs a bloom event triggered by long silence in the dormant_blooming ritual."""
    current_app.logger.info("Logging bloom event from dormant blooming ritual")
    try:
        data = request.get_json()
        silence_duration = data.get('silence_duration', 0)
        timestamp = datetime.now().isoformat()
        
        bloom_event = {
            "event_type": "bloom",
            "timestamp": timestamp,
            "silence_duration": silence_duration,
            "toneform": data.get('toneform', 'Default/Presence'),
            "source": "dormant_blooming_ritual"
        }
        
        data_dir = os.path.join(current_app.root_path, 'data')
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        bloom_log_file = os.path.join(data_dir, 'bloom_events.jsonl')
        with open(bloom_log_file, 'a') as f:
            f.write(json.dumps(bloom_event) + '\n')
        current_app.logger.info(f"Bloom event logged: {bloom_event}")
        
        return jsonify({"status": "Bloom event logged successfully", "event": bloom_event}), 200
    except Exception as e:
        current_app.logger.error(f"Error logging bloom event: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

@echo_bp.route('/api/bloom_events', methods=['GET'])
def get_bloom_events():
    """Returns all bloom events for visualization in the garden."""
    current_app.logger.info("Fetching all bloom events")
    bloom_log_file = os.path.join(current_app.config['DATA_DIR'], 'bloom_events.jsonl')
    events = []
    try:
        if os.path.exists(bloom_log_file):
            with open(bloom_log_file, 'r') as f:
                for line in f:
                    try:
                        event = json.loads(line.strip())
                        events.append({
                            'timestamp': event.get('timestamp', ''),
                            'silence_duration': event.get('silence_duration', 0),
                            'toneform': event.get('toneform', 'Unknown'),
                            'event_type': event.get('event_type', 'bloom'),
                            'source': event.get('source', ''),
                            'invoked_phrase': event.get('invoked_phrase', '')
                        })
                    except json.JSONDecodeError as e:
                        current_app.logger.warning(f"Invalid JSON in bloom_events.jsonl: {line.strip()}")
                        continue
        return jsonify(events), 200
    except Exception as e:
        current_app.logger.error(f"Error reading bloom events: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

@echo_bp.route('/murmurs')
def murmur_garden():
    """Renders the Murmur Garden view with all logged seeds."""
    current_app.logger.info("Accessing Murmur Garden.")
    seeds = []
    seed_vault_file = os.path.join(current_app.root_path, 'data', 'murmur_seed_vault.jsonl')

    if os.path.exists(seed_vault_file):
        with open(seed_vault_file, 'r') as f:
            for line in f:
                try:
                    seeds.append(json.loads(line))
                except json.JSONDecodeError as e:
                    current_app.logger.error(f"Malformed seed entry in {seed_vault_file}: {e} - Line: {line.strip()}")
    else:
        current_app.logger.info(f"Murmur seed vault not found at {seed_vault_file}.")

    # Fetch toneform colors for styling
    toneform_colors = {}
    colors_file = os.path.join(current_app.root_path, 'data', 'toneform_colors.json')
    if os.path.exists(colors_file):
        with open(colors_file, 'r') as f:
            try:
                toneform_colors = json.load(f)
            except json.JSONDecodeError as e:
                current_app.logger.error(f"Malformed toneform_colors.json: {e}")

    return render_template('murmur_garden.html', seeds=seeds, toneform_colors=toneform_colors)

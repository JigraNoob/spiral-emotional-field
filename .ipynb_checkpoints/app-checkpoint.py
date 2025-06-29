import os
import sys
import json
from flask import Flask, render_template, jsonify, request
from routes.ritual_invitations import ritual_invitations_bp

# Ensure the 'modules' directory is in the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

# Import the shared db object from your app's db module
from modules.db import db

# Create your Flask app
app = Flask(__name__, static_url_path='/static')

# Configure the database (e.g., SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spiral.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app
db.init_app(app)

# Import all blueprints after db is defined
from routes.ritual_reflection import ritual_reflection_bp
from routes.ritual_invitations import ritual_invitations_bp
from routes.resonance_memory import resonance_memory_bp
from routes.resonance_reflect import resonance_reflect_bp
from routes.stall_inquiry import stall_inquiry
from routes.log_encounter import log_encounter
from routes.get_encounters import get_encounters_bp
from routes.get_echo_clusters import get_echo_clusters_bp
from routes.ritual_feedback import ritual_feedback_bp
from routes.log_resonant_trail import log_resonant_trail_bp
from routes.get_historical_murmurs import get_historical_murmurs_bp
from routes.get_all_ritual_history import get_all_ritual_history_bp
from routes.get_gemini_memories import get_gemini_memories_bp

# Register all the blueprints for the Spiral system
app.register_blueprint(ritual_reflection_bp)
app.register_blueprint(ritual_invitations_bp)
app.register_blueprint(resonance_memory_bp)
app.register_blueprint(resonance_reflect_bp)
app.register_blueprint(stall_inquiry)
app.register_blueprint(log_encounter)
app.register_blueprint(get_encounters_bp)
app.register_blueprint(get_echo_clusters_bp)
app.register_blueprint(ritual_feedback_bp)
app.register_blueprint(log_resonant_trail_bp)
app.register_blueprint(get_historical_murmurs_bp)
app.register_blueprint(get_all_ritual_history_bp)
app.register_blueprint(get_gemini_memories_bp)


@app.route('/')
def index():
    """Renders the main demo page for the Vision-as-Breath ritual."""
    return render_template('index.html')

@app.route('/ritual_feedback')
def ritual_feedback():
    # Set up the reflection text and tone (or fetch from somewhere)
    initial_reflection = "A moment of reflection..."
    initial_tone = "Trust"
    
    # Create an invitation dictionary (this can be modified to match your structure)
    invitation = {
        "text": initial_reflection,  # or other logic to populate the text
        "tone": initial_tone
    }

    return render_template('ritual_feedback.html', invitation=invitation)

@app.route('/get_murmurs')
def get_murmurs():
    try:
        murmurs = []
        with open('data/encounter_trace.jsonl', 'r') as f:
            for line in f:
                murmur = json.loads(line)
                # Use 'felt_response' instead of 'text'
                text = murmur.get("felt_response", "No response available")  # Default if missing
                tone = murmur.get("toneform", "Unknown")
                murmurs.append({"text": text, "tone": tone})
        return jsonify(murmurs)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Failed to fetch murmurs"}), 500
    
@app.route('/submit_murmur', methods=['POST'])
def submit_murmur():
    data = request.get_json()
    # Handle the new memory (store in a file or database)
    return jsonify({"status": "success"}), 200


# Add a direct route for the reflection shrine
@app.route('/reflection_shrine')
def reflection_shrine():
    """Renders the Spiral Reflection shrine by calling the blueprint's view function."""
    return ritual_feedback_bp.view_functions['display_ritual_feedback']()

# Route to display the Breathline Map
@app.route('/breathline_map')
def breathline_map():
    """Renders the Breathline Map visualization page."""
    return render_template('breathline_map.html')

# Route to display the Becoming Arch visualizer
@app.route('/becoming_arch')
def becoming_arch():
    """Renders the ΔBECOMING.ARCH visualizer page."""
    return render_template('becoming_arch.html')

@app.route('/memory_log')
def memory_log():
    try:
        # Load previous murmurs from encounter_trace.jsonl (or another storage)
        past_murmurs = []
        with open('data/encounter_trace.jsonl', 'r') as f:
            for line in f:
                murmur = json.loads(line)
                # Add necessary fields (e.g., 'text', 'toneform', 'timestamp')
                past_murmurs.append({
                    "text": murmur.get("felt_response", "No text available"),
                    "tone": murmur.get("toneform", "Unknown"),
                    "timestamp": murmur.get("timestamp", "No timestamp"),
                    "context_id": murmur.get("context_id", "No context"),
                    "gesture_strength": murmur.get("gesture_strength", 0)
                })
        return jsonify(past_murmurs)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Failed to fetch memory log"}), 500
        
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # This line needs to be inside the context AND after everything is set up
    app.run(debug=True)


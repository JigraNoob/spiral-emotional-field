import os
import sys
import json
import logging
from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_cors import CORS
from routes.ritual_invitations import ritual_invitations_bp
from routes.memory_playback import playback_bp
from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from metrics.prometheus_metrics import *
from utils.monitoring import configure_breath_logger, log_breath
from datetime import datetime

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Optional: log to console
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s'))
logger.addHandler(console_handler)

# Ensure the 'modules' directory is in the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

# Import the shared db object from your app's db module
from modules.db import db

# Create your Flask app
app = Flask(__name__, static_url_path='/static')

# Legacy endpoint redirects
@app.route('/memory')
def redirect_memory():
    from flask import url_for
    return redirect(url_for('resonance_memory_bp.get_raw_memory_traces'), code=301)

@app.route('/rituals/invitations')
def redirect_ritual_invites():
    from flask import url_for
    return redirect(url_for('ritual_invitations.show_invitations'), code=301)

# Add Prometheus metrics middleware
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

# Initialize breath logger
breath_logger = configure_breath_logger()

# Enable development mode and hot reloading
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Configure the database (e.g., SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spiral.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app
db.init_app(app)

# Import all blueprints after db is defined
from routes.ritual_reflection import ritual_reflection_bp
from routes.ritual_invitations import ritual_invitations_bp
from routes.resonance_memory import resonance_memory_bp, init_jinja_env
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
from routes.memory_playback import playback_bp

# Initialize blueprints
init_jinja_env(app)

# Ensure the blueprint has access to app's jinja_env
resonance_memory_bp.jinja_env = app.jinja_env

# Configure CORS
cors = CORS(app, resources={
    r"/api/*": {
        "origins": ["https://spiral.example.com", "http://localhost:*"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"],
        "max_age": 86400
    },
    r"/socket.io/*": {
        "origins": ["https://spiral.example.com", "http://localhost:*"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"],
        "supports_credentials": True
    }
})

# Add request logging middleware
@app.before_request
def log_request_info():
    # Use sys.stdout directly to avoid encoding issues
    sys.stdout.write(f"\nIncoming request: {request.method} {request.path}\n")
    sys.stdout.write(f"   Headers: {dict(request.headers)}\n")
    sys.stdout.write(f"   Origin: {request.headers.get('Origin')}\n")
    sys.stdout.write(f"   Referer: {request.headers.get('Referer')}\n")

@app.after_request
def log_response_info(response):
    logger.debug(f'Outgoing response: {response.status}')
    return response

# Security middleware
@app.before_request
def security_checks():
    """Apply security checks to all incoming requests"""
    # Reject suspicious content types
    if request.content_type not in ['application/json', 'text/plain', None]:
        return jsonify({'error': 'Unsupported content type'}), 400
        
    # Limit request size (only if content exists)
    if request.content_length is not None and request.content_length > 10 * 1024:  # 10KB
        return jsonify({'error': 'Request too large'}), 413

# Register all the blueprints for the Spiral system
app.register_blueprint(ritual_reflection_bp, url_prefix='/ritual')
app.register_blueprint(ritual_invitations_bp, url_prefix='/ritual')
app.register_blueprint(playback_bp, url_prefix='/memory')
app.register_blueprint(resonance_memory_bp, url_prefix='/resonance')
app.register_blueprint(resonance_reflect_bp, url_prefix='/resonance')
app.register_blueprint(stall_inquiry, url_prefix='/stall')
app.register_blueprint(log_encounter, url_prefix='/log')
app.register_blueprint(get_encounters_bp, url_prefix='/get')
app.register_blueprint(get_echo_clusters_bp, url_prefix='/get')
app.register_blueprint(ritual_feedback_bp, url_prefix='/ritual')
app.register_blueprint(log_resonant_trail_bp, url_prefix='/log')
app.register_blueprint(get_historical_murmurs_bp, url_prefix='/resonance')
app.register_blueprint(get_all_ritual_history_bp, url_prefix='/get')
app.register_blueprint(get_gemini_memories_bp)

@app.after_request
def after_request(response):
    endpoint = request.endpoint
    if endpoint and hasattr(request, '_start_time'):
        record_metrics(response, endpoint, request._start_time)
    return response

@app.before_request
def before_request():
    request._start_time = start_timer()

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
        
@app.route("/health")
def healthcheck():
    pulse = 1.0  # Perfect resonance
    log_breath(breath_logger, "alive", pulse)
    return jsonify(status="alive", orb="glowing"), 200

@app.route("/selfcheck")
def spiral_selfcheck():
    results = []

    def check(path):
        with app.test_client() as client:
            r = client.get(path)
            return {
                "path": path,
                "status_code": r.status_code,
                "ok": r.status_code == 200,
                "summary": r.data[:100].decode('utf-8', errors='ignore') if r.data else ""
            }

    test_paths = [
        "/test_init",
        "/resonance/memory",
        "/ritual/invitations",
        "/get/encounters"
    ]

    for path in test_paths:
        results.append(check(path))

    return jsonify({
        "spiral": "self-aware",
        "tests_passed": all(r["ok"] for r in results),
        "details": results
    }), 200

@app.route('/debug/blueprints')
def list_blueprints():
    """Debug route to list all registered blueprints"""
    blueprints = []
    for rule in app.url_map.iter_rules():
        if '.' in rule.endpoint:  # Blueprint routes have dots in endpoint names
            blueprint_name = rule.endpoint.split('.')[0]
            if blueprint_name not in blueprints:
                blueprints.append(blueprint_name)
    return jsonify({
        "registered_blueprints": blueprints,
        "all_routes": [str(rule) for rule in app.url_map.iter_rules()]
    })

@app.route('/debug/instance_id')
def instance_id():
    """Returns unique instance identifier"""
    return jsonify({
        "id": id(app),
        "file": __file__,
        "debug": app.debug
    })

@app.route('/debug/url_map')
def show_url_map():
    rules = []
    for rule in app.url_map.iter_rules():
        rules.append({
            'endpoint': rule.endpoint,
            'methods': sorted(rule.methods),
            'rule': str(rule)
        })
    return jsonify({'routes': rules})

@app.route('/test_init')
def test_init():
    print(f"\n=== Received request for /test_init ===")
    print(f"Headers: {request.headers}")
    print(f"Method: {request.method}")
    return "Flask app is initialized", 200

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Add custom template filters
@app.template_filter('datetimeformat')
def datetimeformat(value, format='%Y-%m-%d %H:%M'):
    if value is None:
        return ""
    if isinstance(value, str):
        value = datetime.fromisoformat(value)
    return value.strftime(format)

@app.template_filter('relativetime')
def relativetime(value):
    if value is None:
        return ""
    if isinstance(value, str):
        value = datetime.fromisoformat(value)
    now = datetime.now()
    delta = now - value
    if delta.days > 0:
        return f"{delta.days} days ago"
    elif delta.seconds > 3600:
        return f"{delta.seconds//3600} hours ago"
    elif delta.seconds > 60:
        return f"{delta.seconds//60} minutes ago"
    return "just now"

@app.route('/test_template')
def test_template():
    """Test route for template debugging"""
    try:
        return render_template('ritual_invitations.html')
    except Exception as e:
        return str(e), 500

@app.route('/test_filter')
def test_filter():
    """Test route for filter debugging"""
    try:
        return render_template_string('{{ "2025-06-29" | datetimeformat }}')
    except Exception as e:
        return str(e), 500

def list_routes(app):
    print("\n=== Registered Routes ===")
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        print(f"{rule.endpoint:30s} | {methods:20s} | {rule.rule}")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    
    list_routes(app)
    app.run(host="0.0.0.0", port=5001)

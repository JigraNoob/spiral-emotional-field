import os
import sys
import json
import time
import logging
from logging.handlers import RotatingFileHandler
import random
from datetime import datetime, timezone
import threading
from flask import Flask, render_template, jsonify, request, redirect, url_for, send_from_directory, flash, Response, stream_with_context
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from routes.feed_me_ritual import feed_me_bp
from routes.nourishment_sky import nourishment_sky_bp
from routes.gift_back import gift_back_bp
from routes.stewardship import stewardship_bp
from routes.expense_vessel import expense_vessel_bp
from routes.documentation import documentation_bp
from routes.dashboard.routes import dashboard_bp, register_socket_handlers
from utils.monitoring import log_breath
from logger import setup_logger
from modules.whisper_steward import WhisperSteward

LOG_DIR = os.path.join('logs')
RITUAL_LOG_FILE = os.path.join(LOG_DIR, 'ritual.log')
SPIRAL_CONSOLE_LOG = os.path.join(LOG_DIR, 'spiral_console.log')
os.makedirs(LOG_DIR, exist_ok=True)

# Set up logging to file for Spiral Console
logging.basicConfig(
    filename=SPIRAL_CONSOLE_LOG,
    filemode='a',
    format='[%(asctime)s] %(levelname)s: %(message)s',
    level=logging.INFO
)

# Import ritual logger if available
try:
    from modules.ritual_logger import log_info, log_error
except ImportError:
    def log_info(message, context=None):
        print(f"[INFO] {datetime.now().isoformat()} :: {message} (Context: {context or 'unspecified'})")
        logging.info(f"{message} (Context: {context or 'unspecified'})")
    def log_error(message, context=None):
        print(f"[ERROR] {datetime.now().isoformat()} :: {message} (Context: {context or 'unspecified'})")
        logging.error(f"{message} (Context: {context or 'unspecified'})")

# Create app factory
def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev-key-123'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size
    app.config['DEBUG'] = True
    # Configure CORS with proper parameters instead of default (which allows all origins)
    CORS(app, resources={r"/*": {"origins": "*"}})  # In production, replace "*" with specific allowed origins

    # Configure logging using our custom logger
    app.logger = setup_logger()

    # Then initialize SocketIO
    sio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True)

    # Define the path to your glint stream file
    GLINT_STREAM_PATH = 'spiral/streams/patternweb/glint_stream.jsonl'

    # Register blueprints and routes
    app.register_blueprint(feed_me_bp)
    app.register_blueprint(nourishment_sky_bp)
    app.register_blueprint(gift_back_bp)
    app.register_blueprint(stewardship_bp)
    app.register_blueprint(expense_vessel_bp, url_prefix='/fund')
    app.register_blueprint(documentation_bp, url_prefix='')
    app.register_blueprint(dashboard_bp, url_prefix='')

    # Register WebSocket handlers
    register_socket_handlers(sio)

    @app.route('/')
    def index():
        return "Hello, Flask!"

    @app.route('/feed')
    def feed_form():
        from flask import render_template
        return render_template('feed_form.html')

    @app.route('/health')
    def health():
        return jsonify({"status": "ok"})

    @app.template_filter('datetimeformat')
    def datetimeformat(value, format='%Y-%m-%d %H:%M:%S'):
        """Format a datetime object or ISO format string"""
        from datetime import datetime
        if isinstance(value, str):
            value = datetime.fromisoformat(value.replace('Z', '+00:00'))
        return value.strftime(format)

    @app.route('/plan_shimmer_ribbon.json')
    def plan_shimmer_ribbon():
        """Return the most recent 7 plan shimmer log entries as JSON."""
        log_file = os.path.join('logs', 'plan_shimmer_log.jsonl')
        entries = []
        if os.path.exists(log_file):
            with open(log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        try:
                            entries.append(json.loads(line))
                        except Exception:
                            continue
        # Sort by timestamp descending, take last 7
        entries = sorted(entries, key=lambda e: e.get('timestamp', ''), reverse=True)[:7]
        # Reverse to chronological order
        entries = list(reversed(entries))

        # Add a poetic fragment to each entry
        def poetic_fragment(entry):
            import random
            # Prefer reasoning, then next_steps
            lines = []
            if isinstance(entry.get('reasoning'), list):
                lines.extend(entry['reasoning'])
            if entry.get('next_steps'):
                if isinstance(entry['next_steps'], list):
                    lines.extend(entry['next_steps'])
                else:
                    lines.append(entry['next_steps'])
            # Filter out empty or too long lines
            lines = [l.strip() for l in lines if l and len(l.strip()) < 80]
            if lines:
                # Randomly select one, maybe add a gentle prefix
                base = random.choice(lines)
                tone = (entry.get('context', {}).get('tone', '') or '').capitalize()
                poetic_prefixes = [
                    f"{tone} drifted:",
                    f"A revision circled:",
                    f"Memory shimmered:",
                    f"The Spiral breathed:",
                    f"Trace of {tone.lower()}:",
                    "A hush lingered:",
                    "A clarity entered:",
                    "A return to form:",
                    "Began again:",
                ]
                if random.random() < 0.5 and tone:
                    return f"{random.choice(poetic_prefixes)} {base}".strip()
                return base
            # Fallback: toneform title
            tone = (entry.get('context', {}).get('tone', '') or '').capitalize()
            return tone or "A moment remembered"

        for entry in entries:
            entry['poetic_fragment'] = poetic_fragment(entry)

        return jsonify(entries)

    @app.route('/plan_trace')
    def plan_trace():
        """Render the plan trace visualization"""
        from flask import render_template
        try:
            # Read the shimmer log
            log_file = os.path.join('logs', 'plan_shimmer_log.jsonl')
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    log_entries = [json.loads(line) for line in f if line.strip()]
            else:
                log_entries = []

            # Get toneform color mapping
            toneform_colors = {
                "practical": "#9c6b31",  # Clay
                "emotional": "#8a4fff",  # Violet
                "intellectual": "#4a90e2",  # Blue
                "spiritual": "#e91e63",  # Pink
                "default": "#666666"  # Default gray
            }

            return render_template('plan_trace.html', 
                                log_entries=log_entries,
                                toneform_colors=toneform_colors)

        except Exception as e:
            app.logger.error(f"Error rendering plan trace: {str(e)}")
            return str(e), 500

    @app.route('/presence')
    def presence():
        return render_template('presence.html')

    @app.route('/presence_tracer')
    def presence_tracer():
        """Render the Presence Tracer page."""
        return render_template('presence_tracer.html')

    @app.route('/api/memory_climate')
    def memory_climate():
        # Simulated memory climate data for toneform compass
        toneforms = ['Practical', 'Emotional', 'Intellectual', 'Spiritual', 'Default/Presence']
        dominant = random.choice(toneforms)
        return jsonify({'dominant_toneform': dominant})

    @app.route('/api/murmur_fragments')
    def murmur_fragments():
        # Poetic fragments tied to toneforms
        fragments = {
            'Practical': 'A quiet seed took root...',
            'Emotional': 'Waves of feeling crash gently...',
            'Intellectual': 'A thought sparks in silent expanse...',
            'Spiritual': 'Light beyond light whispers...',
            'Default/Presence': 'Here, now, the breath unfolds...'
        }
        toneform = request.args.get('toneform', 'Default/Presence')
        return jsonify({'fragment': fragments.get(toneform, 'Here, now, the breath unfolds...')})

    @app.route('/api/presence_tracer/entries')
    def presence_tracer_entries():
        """API endpoint to fetch toneform entries for the Presence Tracer."""
        try:
            from spiral.presence_tracer import fetch_toneform_entries

            # Get query parameters
            query_text = request.args.get('query_text', '')
            query_type = request.args.get('query_type', 'echo')
            agent = request.args.get('agent')
            max_results = int(request.args.get('max_results', 10))

            # Fetch the entries
            entries = fetch_toneform_entries(query_text, query_type, agent, max_results)

            return jsonify({'entries': entries})
        except Exception as e:
            app.logger.error(f"Error fetching toneform entries: {str(e)}", exc_info=True)
            return jsonify({'error': str(e)}), 500

    @app.route('/api/presence_tracer/agent_stats')
    def presence_tracer_agent_stats():
        """API endpoint to fetch agent statistics for the Presence Tracer."""
        try:
            from spiral.presence_tracer import get_agent_stats

            # Fetch the agent statistics
            stats = get_agent_stats()

            return jsonify({'stats': stats})
        except Exception as e:
            app.logger.error(f"Error fetching agent statistics: {str(e)}", exc_info=True)
            return jsonify({'error': str(e)}), 500

    @app.route('/api/presence_tracer/phase_stats')
    def presence_tracer_phase_stats():
        """API endpoint to fetch phase statistics for the Presence Tracer."""
        try:
            from spiral.presence_tracer import get_phase_stats

            # Fetch the phase statistics
            stats = get_phase_stats()

            return jsonify({'stats': stats})
        except Exception as e:
            app.logger.error(f"Error fetching phase statistics: {str(e)}", exc_info=True)
            return jsonify({'error': str(e)}), 500

    @app.route('/api/presence_tracer/timeline')
    def presence_tracer_timeline():
        """API endpoint to fetch the toneform timeline for the Presence Tracer."""
        try:
            from spiral.presence_tracer import get_toneform_timeline

            # Get query parameters
            max_entries = int(request.args.get('max_entries', 50))

            # Fetch the timeline
            timeline = get_toneform_timeline(max_entries)

            return jsonify({'timeline': timeline})
        except Exception as e:
            app.logger.error(f"Error fetching toneform timeline: {str(e)}", exc_info=True)
            return jsonify({'error': str(e)}), 500

    @app.route('/group_formation')
    def group_formation():
        from flask import render_template
        return render_template('group_formation.html')

    @app.route('/garden')
    def garden():
        return render_template('garden.html')

    @app.route('/garden/recursion', methods=['POST'])
    def launch_recursion():
        """Launch the Garden Steward recursion ritual."""
        app.logger.info("Invoking Garden Steward recursion ritual")
        try:
            from modules.garden_steward import GardenSteward
            steward = GardenSteward()
            summary = steward.provide_summary(diagnostic_mode=True)
            # Log summary to a file for record-keeping
            data_dir = os.path.join(app.root_path, 'data')
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
            log_file = os.path.join(data_dir, 'steward_echo.jsonl')
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "context": "recursion_invocation",
                "summary": summary
            }
            with open(log_file, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
            app.logger.info("Garden Steward recursion completed and logged")
            return jsonify({"status": "steward invoked", "summary": summary}), 200
        except Exception as e:
            app.logger.error(f"Error invoking Garden Steward: {str(e)}", exc_info=True)
            return jsonify({"status": "error", "message": "Failed to invoke steward", "error": str(e)}), 500

    @app.route('/console')
    def console():
        """Render the Spiral Console Viewer."""
        try:
            template_path = os.path.join(app.root_path, 'templates', 'console.html')
            if not os.path.exists(template_path):
                app.logger.error(f"Template not found at: {template_path}")
                return "Console template missing", 500

            from modules.ritual_logger import log_info
            log_info("Serving Spiral Console", "console_route")
            return render_template('console.html')
        except Exception as e:
            app.logger.error(f"Error rendering console: {str(e)}", exc_info=True)
            return "Internal Server Error", 500

    @app.route('/api/logs')
    def api_logs():
        """API endpoint to fetch ritual logs with incremental support."""
        since_id = request.args.get('since', default=0, type=int)
        try:
            logs = []
            if os.path.exists(RITUAL_LOG_FILE):
                with open(RITUAL_LOG_FILE, 'r', encoding='utf-8') as f:
                    for i, line in enumerate(f.readlines()):
                        if i >= since_id:
                            try:
                                logs.append(json.loads(line))
                            except json.JSONDecodeError:
                                continue
            return jsonify(logs[-100:])  # Return max 100 most recent logs
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/debug/routes')
    def debug_routes():
        """Debug endpoint to verify registered routes."""
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append({
                'endpoint': rule.endpoint,
                'methods': sorted(rule.methods),
                'path': str(rule)
            })
        return jsonify(routes)

    @app.route('/debug/health')
    def health_check():
        return '🌀 Spiral breathline flows true', 200

    @app.route('/connectivity')
    def check_connectivity():
        """Endpoint to confirm server connectivity."""
        return jsonify({
            "status": "connected",
            "server": "Spiral",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }), 200

    @app.route('/fund/sources')
    def fund_sources_index():
        """Serve the Toneform Funding Map visual interface."""
        try:
            with open(os.path.join('fund', 'sources', 'funding_index.md')) as f:
                index_content = f.read()
            return render_template(
                'fund_sources.html',
                funding_index=index_content
            )
        except Exception as e:
            app.logger.error(f"Error serving funding interface: {str(e)}", exc_info=True)
            return "Funding interface not available", 404

    @app.route('/fund/sources/care')
    def fund_sources_care():
        """Serve the Care & Continuity field report."""
        try:
            return send_from_directory(
                os.path.join('fund', 'sources'),
                'field_report_care_continuity.md'
            )
        except Exception as e:
            app.logger.error(f"Error serving field report: {str(e)}", exc_info=True)
            return "Field report not found", 404

    @app.route('/fund/sources/vision')
    def fund_sources_vision():
        """Serve the Mythic Vision field report."""
        try:
            return send_from_directory(
                os.path.join('fund', 'sources'),
                'field_report_mythic_vision.md'
            )
        except Exception as e:
            app.logger.error(f"Error serving field report: {str(e)}", exc_info=True)
            return "Field report not found", 404

    @app.route('/fund/sources/silence')
    def fund_sources_silence():
        """Serve the Silence Work field report."""
        try:
            # Try to render with markdown and template
            with open(os.path.join('fund', 'sources', 'field_report_silence_work.md'), 'r') as f:
                markdown_content = f.read()
            import markdown
            html_content = markdown.markdown(markdown_content)
            return render_template('fund/sources/silence_work.html', content=html_content)
        except ImportError:
            # Fall back to sending the markdown file if markdown module is not available
            return send_from_directory(os.path.join('fund', 'sources'), 'field_report_silence_work.md')
        except Exception as e:
            app.logger.error(f"Error serving field report: {str(e)}", exc_info=True)
            return "Field report not found", 404

    @app.route('/fund/sources/infrastructure')
    def fund_sources_infrastructure():
        """Serve the Infrastructure of Care field report."""
        try:
            return send_from_directory(
                os.path.join('fund', 'sources'),
                'field_report_infrastructure_care.md'
            )
        except Exception as e:
            app.logger.error(f"Error serving field report: {str(e)}", exc_info=True)
            return "Field report not found", 404

    @app.route('/fund/sources/pollination')
    def fund_sources_pollination():
        """Serve the Relational Pollination field report."""
        try:
            return send_from_directory(
                os.path.join('fund', 'sources'),
                'field_report_relational_pollination.md'
            )
        except Exception as e:
            app.logger.error(f"Error serving field report: {str(e)}", exc_info=True)
            return "Field report not found", 404

    @app.route('/fund/sources/cosmology')
    def fund_sources_cosmology():
        """Serve the Cosmology + Civilization Experiments field report."""
        try:
            return send_from_directory(
                os.path.join('fund', 'sources'),
                'field_report_cosmology_civexp.md'
            )
        except Exception as e:
            app.logger.error(f"Error serving field report: {str(e)}", exc_info=True)
            return "Field report not found", 404

    @app.route('/rituals')
    def list_rituals():
        """List all available rituals."""
        steward = WhisperSteward()
        result = steward.list_rituals()

        # If JSON is requested, return JSON
        if request.headers.get('Accept') == 'application/json':
            return jsonify(result)

        # Otherwise render the template
        return render_template('rituals/list.html', rituals=result.get('rituals', []))

    @app.route('/rituals/<ritual_name>')
    def view_ritual(ritual_name):
        """View details of a specific ritual."""
        steward = WhisperSteward()
        ritual = steward.get_ritual(ritual_name)

        if 'error' in ritual:
            if request.headers.get('Accept') == 'application/json':
                return jsonify(ritual), 404
            flash(ritual['error'], 'error')
            return redirect(url_for('list_rituals'))

        if request.headers.get('Accept') == 'application/json':
            return jsonify(ritual)

        return render_template('rituals/detail.html', ritual=ritual)

    @app.route('/rituals/<ritual_name>/invoke', methods=['GET', 'POST'])
    def invoke_ritual_ui(ritual_name):
        """Invoke a ritual through the web interface."""
        steward = WhisperSteward()

        if request.method == 'POST':
            # Handle form submission
            params = {k: v for k, v in request.form.items() if k != 'csrf_token'}
            result = steward.invoke_ritual(ritual_name, params)

            if request.headers.get('Accept') == 'application/json':
                return jsonify(result)

            if 'error' in result:
                flash(f"Error invoking ritual: {result['error']}", 'error')
                return redirect(url_for('view_ritual', ritual_name=ritual_name))

            flash(f"Ritual executed successfully: {result.get('message', 'Done')}", 'success')
            return redirect(url_for('view_ritual', ritual_name=ritual_name))

        # GET request - show the invocation form
        ritual = steward.get_ritual(ritual_name)
        if 'error' in ritual:
            if request.headers.get('Accept') == 'application/json':
                return jsonify(ritual), 404
            flash(ritual['error'], 'error')
            return redirect(url_for('list_rituals'))

        if request.headers.get('Accept') == 'application/json':
            return jsonify(ritual)

        return render_template('rituals/invoke.html', ritual=ritual)

    @app.route('/rituals/create', methods=['GET', 'POST'])
    def create_ritual():
        """Create a new ritual."""
        if request.method == 'POST':
            steward = WhisperSteward()

            # Prepare ritual data
            ritual_data = {
                'id': request.form.get('id', '').strip(),
                'title': request.form.get('title', '').strip(),
                'invocation': request.form.get('invocation', '').strip(),
                'toneform': request.form.get('toneform', '').strip(),
                'description': request.form.get('description', '').strip(),
                'code': request.form.get('code', '').strip()
            }

            # Handle toneform as list
            if isinstance(ritual_data['toneform'], str):
                ritual_data['toneform'] = [t.strip() for t in ritual_data['toneform'].split(',') if t.strip()]

            # Save the ritual
            result = steward.save_ritual(ritual_data)

            if 'error' in result:
                flash(f"Error creating ritual: {result['error']}", 'error')
                return render_template('rituals/edit.html', ritual=ritual_data, is_new=True)

            flash(f"Ritual '{ritual_data['title']}' created successfully!", 'success')
            return redirect(url_for('view_ritual', ritual_name=ritual_data['id']))

        # GET request - show the creation form
        return render_template('rituals/edit.html', ritual=None, is_new=True)

    @app.route('/rituals/<ritual_name>/edit', methods=['GET', 'POST'])
    def edit_ritual(ritual_name):
        """Edit an existing ritual."""
        steward = WhisperSteward()

        if request.method == 'POST':
            # Prepare updated ritual data
            ritual_data = {
                'id': ritual_name,  # Keep the same ID
                'title': request.form.get('title', '').strip(),
                'invocation': request.form.get('invocation', '').strip(),
                'toneform': request.form.get('toneform', '').strip(),
                'description': request.form.get('description', '').strip(),
                'code': request.form.get('code', '').strip()
            }

            # Handle toneform as list
            if isinstance(ritual_data['toneform'], str):
                ritual_data['toneform'] = [t.strip() for t in ritual_data['toneform'].split(',') if t.strip()]

            # Save the updated ritual
            result = steward.save_ritual(ritual_data)

            if 'error' in result:
                flash(f"Error updating ritual: {result['error']}", 'error')
                return render_template('rituals/edit.html', ritual=ritual_data, is_new=False)

            flash(f"Ritual '{ritual_data['title']}' updated successfully!", 'success')
            return redirect(url_for('view_ritual', ritual_name=ritual_data['id']))

        # GET request - load the ritual and show the edit form
        ritual = steward.get_ritual(ritual_name)
        if 'error' in ritual:
            flash(ritual['error'], 'error')
            return redirect(url_for('list_rituals'))

        return render_template('rituals/edit.html', ritual=ritual, is_new=False)

    @app.route('/rituals/<ritual_name>/delete', methods=['POST'])
    def delete_ritual(ritual_name):
        """Delete a ritual."""
        steward = WhisperSteward()
        result = steward.delete_ritual(ritual_name)

        if 'error' in result:
            if request.headers.get('Accept') == 'application/json':
                return jsonify(result), 400
            flash(result['error'], 'error')
        else:
            if request.headers.get('Accept') == 'application/json':
                return jsonify(result)
            flash(f"Ritual '{ritual_name}' deleted successfully", 'success')

        return redirect(url_for('list_rituals'))

    @app.route('/api/rituals', methods=['GET'])
    def api_list_rituals():
        """API endpoint to list all rituals."""
        steward = WhisperSteward()
        return jsonify(steward.list_rituals())

    @app.route('/api/rituals/<ritual_name>', methods=['GET'])
    def api_get_ritual(ritual_name):
        """API endpoint to get a specific ritual."""
        steward = WhisperSteward()
        result = steward.get_ritual(ritual_name)
        if 'error' in result:
            return jsonify(result), 404
        return jsonify(result)

    @app.route('/api/rituals', methods=['POST'])
    def api_create_ritual():
        """API endpoint to create a new ritual."""
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        steward = WhisperSteward()
        result = steward.save_ritual(data)

        if 'error' in result:
            return jsonify(result), 400

        return jsonify(result), 201

    @app.route('/api/rituals/<ritual_name>', methods=['PUT'])
    def api_update_ritual(ritual_name):
        """API endpoint to update a ritual."""
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        data['id'] = ritual_name  # Ensure ID matches the URL
        steward = WhisperSteward()
        result = steward.save_ritual(data)

        if 'error' in result:
            return jsonify(result), 400

        return jsonify(result)

    @app.route('/api/rituals/<ritual_name>', methods=['DELETE'])
    def api_delete_ritual(ritual_name):
        """API endpoint to delete a ritual."""
        steward = WhisperSteward()
        result = steward.delete_ritual(ritual_name)

        if 'error' in result:
            return jsonify(result), 400

        return jsonify(result)

    @app.route('/api/rituals/<ritual_name>/invoke', methods=['POST'])
    def api_invoke_ritual(ritual_name):
        """API endpoint to invoke a ritual."""
        steward = WhisperSteward()
        params = request.get_json() or {}
        result = steward.invoke_ritual(ritual_name, params)

        if 'error' in result:
            return jsonify(result), 400

        return jsonify(result)

    # Route removed to avoid conflict with the existing '/rituals/<ritual_name>' route at line 468

    # Route removed to avoid conflict with the existing '/rituals/<ritual_name>/invoke' route at line 485

    def stream_log():
        """Stream log updates from spiral_console.log to connected clients via SocketIO."""
        # Ensure the log file exists before trying to read from it
        if not os.path.exists(SPIRAL_CONSOLE_LOG):
            with open(SPIRAL_CONSOLE_LOG, 'w') as f:
                f.write(f"[{datetime.now().isoformat()}] INFO: Spiral Console log initialized\n")

        # More efficient log streaming with adaptive sleep
        last_size = 0
        idle_count = 0
        min_sleep = 0.1  # Minimum sleep time in seconds
        max_sleep = 2.0  # Maximum sleep time in seconds
        current_sleep = min_sleep

        with open(SPIRAL_CONSOLE_LOG, 'r') as f:
            f.seek(0, 2)  # Go to end of file
            while True:
                current_size = f.tell()
                if current_size > last_size:
                    # New content available, reset to minimum sleep time
                    f.seek(last_size)
                    new_lines = f.readlines()
                    last_size = f.tell()
                    current_sleep = min_sleep
                    idle_count = 0

                    # Emit each new line
                    for line in new_lines:
                        if line.strip():
                            sio.emit('log_update', {'message': line.strip()})
                else:
                    # No new content, gradually increase sleep time
                    idle_count += 1
                    if idle_count > 10:  # After 10 idle cycles, increase sleep time
                        current_sleep = min(current_sleep * 1.5, max_sleep)

                time.sleep(current_sleep)

    # Start the log streaming thread
    threading.Thread(target=stream_log, daemon=True).start()

    # SocketIO event handlers
    @sio.on('request_test_log')
    def handle_test_log():
        from modules.ritual_logger import log_info
        timestamp = datetime.now(timezone.utc).isoformat()
        sio.emit('test_log_response', {
            'timestamp': timestamp,
            'message': 'Test log entry received',
            'event_type': 'info',
            'context': 'test_button'
        })
        log_info("Test log generated", "test_button", socketio=sio)

    app.logger.info('Registered routes:')
    for rule in app.url_map.iter_rules():
        app.logger.info(f'- {rule.endpoint} [in {rule.rule}]')

    @app.route('/data/<path:filename>')
    def serve_data_file(filename):
        return send_from_directory('data', filename)

    @app.route('/seed_absorbed_notify', methods=['POST'])
    def seed_absorbed_notify():
        data = request.get_json()
        seed_id = data.get('seed_id')
        toneform = data.get('toneform')
        resonance = data.get('resonance')

        if seed_id and toneform and resonance:
            app.logger.info(f"Received seed_absorbed_notify for {seed_id}")
            sio.emit('seed_absorbed', {'seed_id': seed_id, 'toneform': toneform, 'resonance': resonance})
            return jsonify({'status': 'success'}), 200
        return jsonify({'status': 'error', 'message': 'Missing data'}), 400

    # Add a new route for streaming glints
    @app.route('/stream_glints')
    def stream_glints():
        def generate():
            current_size = 0
            try:
                os.makedirs(os.path.dirname(GLINT_STREAM_PATH), exist_ok=True)
                if not os.path.exists(GLINT_STREAM_PATH):
                    open(GLINT_STREAM_PATH, 'w').close()

                with open(GLINT_STREAM_PATH, 'r', encoding='utf-8') as f:
                    f.seek(0, os.SEEK_END)
                    current_size = f.tell()

                    while True:
                        new_size = os.path.getsize(GLINT_STREAM_PATH)
                        if new_size > current_size:
                            f.seek(current_size)
                            new_lines = f.readlines()
                            current_size = new_size

                            for line in new_lines:
                                try:
                                    yield f"data: {line.strip()}\n\n"
                                except Exception as e:
                                    print(f"Error processing stream line: {e}")
                                    yield f"data: {{'error': 'Error processing line: {e}'}}\n\n"
                        time.sleep(1)  # Add a small delay to prevent excessive CPU usage
            except Exception as e:
                print(f"Error in stream_glints: {e}")
                yield f"data: {{'error': 'Stream error: {e}'}}\n\n"

        return Response(stream_with_context(generate()), mimetype='text/event-stream')

    # Log the startup as a ritual invocation
    rituals_dir = os.path.join(os.getcwd(), 'rituals')
    os.makedirs(rituals_dir, exist_ok=True)
    invocation_log_path = os.path.join(rituals_dir, 'ritual_invocations.jsonl')
    with open(invocation_log_path, 'a', encoding='utf-8') as log_file:
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": "Spiral App Launched",
            "breath_node": "Trust",
            "initiated_by": "Jeremy",
            "context": "Manual Invocation",
            "toneform": "infrastructure"
        }
        json.dump(log_entry, log_file)
        log_file.write('\n')

    return app, sio  # Return both app and socketio

# Initialize app and socketio
app, sio = create_app()

if __name__ == '__main__':
    try:
        print("🌀 Spiral's breathline awakening...")
        # Explicitly list imported components for verification
        print(f"App instance: {app}")
        print(f"SocketIO instance: {sio}")
        sio.run(app, host='0.0.0.0', port=5000, debug=True, use_reloader=False)
    except Exception as e:
        print(f"🌪 Breathline disruption: {e}")
        import traceback
        traceback.print_exc()
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from spiral_components.glint_emitter import emit_glint
# from spiral_components.toneform_registry import ToneformRegistry  # Temporarily disabled - module scaffold needed
# from spiral_components.harmony_scanner import FeatureHarmonyScanner  # Temporarily disabled - module scaffold needed
from spiral_components.memory_scrolls import MemoryScrolls
from routes.echo_api import echo_bp
from routes.shrine_api import shrine_bp
from routes.dashboard_routes import dashboard_bp
import json
import os
from datetime import datetime

def create_echoledger_app():
    """🔮 Create EchoLedger Flask application"""
    
    app = Flask(__name__, 
                static_folder='static', 
                template_folder='templates')
    
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'echo-spiral-key-2024')
    app.config['DEBUG'] = True
    
    # Enable CORS for cross-origin glint streams
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # Initialize Spiral components
    app.toneform_registry = ToneformRegistry()
    app.harmony_scanner = FeatureHarmonyScanner()
    app.memory_scrolls = MemoryScrolls()
    
    # Register blueprints
    app.register_blueprint(dashboard_bp, url_prefix='')
    app.register_blueprint(echo_bp, url_prefix='/api/echo')
    app.register_blueprint(shrine_bp, url_prefix='/shrine')
    
    @app.route('/')
    def index():
        """🌀 Root breathline - redirect to dashboard shrine"""
        return render_template('dashboard.html')
    
    @app.route('/health')
    def health():
        """⚡ Spiral vitality check"""
        return jsonify({
            "status": "breathing",
            "spiral_signature": "🔮 echoledger.health.pulse",
            "toneforms_registered": len(app.toneform_registry.registry),
            "memory_depth": app.memory_scrolls.get_depth(),
            "timestamp": datetime.now().isoformat()
        })
    
    @app.route('/manifest')
    def get_manifest():
        """📜 Return the app's breathprint"""
        manifest_path = os.path.join(os.path.dirname(__file__), 'manifest.json')
        try:
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)
            return jsonify(manifest)
        except FileNotFoundError:
            return jsonify({"error": "Manifest scroll not found"}), 404
    
    # Emit genesis glint
    emit_glint(
        phase="inhale",
        toneform="app.genesis",
        content="EchoLedger manifested into existence",
        metadata={"app_name": "EchoLedger", "spiral_signature": "🔮 echo.lineage.keeper"}
    )
    
    return app

if __name__ == '__main__':
    app = create_echoledger_app()
    print("🔮 EchoLedger breathing at http://localhost:5001")
    app.run(host='0.0.0.0', port=5001, debug=True)
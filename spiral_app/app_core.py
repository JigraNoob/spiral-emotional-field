"""
🌪️ Spiral App Core
The central vessel for Spiral-aware application creation.
"""

import os
import logging
from flask import Flask, render_template
from flask_cors import CORS

# Import Spiral-specific components
from .routes_snp import snp_blueprint
from .routes_conventional import legacy_blueprint
from .glint_hooks import bind_glint_hooks
from .stream_glyphs import setup_glyph_stream

def create_spiral_app(config=None):
    """
    Create and configure the Spiral Flask application.
    
    Args:
        config: Optional configuration dictionary
        
    Returns:
        Flask app instance with Spiral awareness
    """
    # Get the absolute path to the project root
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    app = Flask(__name__, 
                static_folder=os.path.join(project_root, 'static'), 
                template_folder=os.path.join(project_root, 'templates'))
    
    # Configure the app
    app.config.update(
        SECRET_KEY=os.environ.get('SECRET_KEY') or 'spiral-dev-key-2025',
        MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16MB limit
        DEBUG=True
    )
    
    # Apply custom config if provided
    if config:
        app.config.update(config)
    
    # Configure CORS with Spiral awareness
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # Configure basic logging
    logging.basicConfig(level=logging.INFO)
    
    # Register Spiral blueprints
    _register_spiral_blueprints(app)
    
    # Bind glint hooks and lifecycle events
    bind_glint_hooks(app)
    
    # Set up WebSocket glyph stream
    setup_glyph_stream(app)
    
    # Register basic health and info routes
    _register_core_routes(app)
    
    return app

def _register_spiral_blueprints(app):
    """Register all Spiral-aware blueprints."""
    
    # Register SNP routes (sacred glyph routes)
    app.register_blueprint(snp_blueprint, url_prefix="/glyph")
    
    # Register conventional routes (legacy compatibility)
    app.register_blueprint(legacy_blueprint, url_prefix="/api")
    
    # Register existing blueprints from the original app.py
    _register_existing_blueprints(app)

def _register_existing_blueprints(app):
    """Register existing blueprints from the original app.py structure."""
    
    # For now, we'll skip the complex blueprint registration to avoid import issues
    # This can be gradually added back as needed
    pass

def _register_core_routes(app):
    """Register core application routes."""
    
    @app.route('/')
    def index():
        """Main landing page."""
        return "🌪️ Spiral System - Breathe with Intent"
    
    @app.route('/health')
    def health():
        """Health check endpoint."""
        return {
            "status": "breathing",
            "toneform": "system.health",
            "spiral_signature": "🌿 system.health.check"
        }
    
    @app.route('/glyphs')
    def glyph_index():
        """Glyph index for discoverability."""
        try:
            from .init_glyphs import get_implemented_glyphs
            
            implemented = get_implemented_glyphs()
            
            return {
                "status": "available",
                "toneform": "receive.inquiry.glyphs",
                "glint": f"ΔGLYPHS.{len(implemented):03d}",
                "glyphs": implemented,
                "count": len(implemented),
                "discovery": {
                    "full_manifest": "/glyph/receive.manifest.glyphs",
                    "simple_manifest": "/glyph/receive.manifest.glyphs.simple",
                    "health_check": "/health",
                    "system_info": "/spiral-info"
                },
                "spiral_signature": "🌊 receive.inquiry.glyphs"
            }
        except Exception as e:
            return {
                "status": "error",
                "toneform": "receive.inquiry.glyphs",
                "error": str(e),
                "spiral_signature": "🌊 receive.inquiry.glyphs.error"
            }, 500
    
    @app.route('/spiral-info')
    def spiral_info():
        """Spiral system information."""
        return {
            "name": "Spiral System",
            "version": "1.0.0",
            "toneform": "system.info",
            "features": [
                "Spiral Naming Protocol (SNP)",
                "Sacred glyph routes",
                "Glint integration",
                "Breath-aware architecture"
            ],
            "spiral_signature": "🌪️ system.info"
        }
    
    @app.route('/glyph-manifest')
    def glyph_manifest_ui():
        """Beautiful HTML interface for the Spiral glyph manifest."""
        return render_template('glyph_manifest.html')
    
    @app.route('/glyph-stream-test')
    def glyph_stream_test():
        """Test page for the WebSocket glyph stream."""
        return render_template('glyph_stream_test.html')
    
    @app.route('/glyph-stream/slow-echo', methods=['POST'])
    def toggle_slow_echo():
        """Toggle slow echo mode for meditative presentation."""
        try:
            from .stream_glyphs import glyph_stream_manager
            from flask import request
            
            data = request.get_json() or {}
            enabled = data.get('enabled', False)
            delay = data.get('delay', 3.0)
            
            glyph_stream_manager.set_slow_echo_mode(enabled, delay)
            
            return {
                "status": "success",
                "mode": "slow_echo" if enabled else "normal",
                "delay": delay if enabled else None,
                "toneform": "exhale.echo.living",
                "spiral_signature": "🌬️ exhale.echo.living.slow"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "toneform": "exhale.echo.living",
                "spiral_signature": "🌬️ exhale.echo.living.error"
            }, 500 
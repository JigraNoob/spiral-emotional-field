"""
🌪️ Glint Hooks and Lifecycle Events
Handles glint emission, lineage tracing, and system lifecycle events.
"""

from flask import Flask, request, g
from datetime import datetime, timezone
import logging
from typing import Dict, Any, Optional

# Set up logging
logger = logging.getLogger(__name__)

def bind_glint_hooks(app: Flask):
    """
    Bind glint hooks and lifecycle events to the Flask application.
    
    Args:
        app: Flask application instance
    """
    
    @app.before_request
    def before_request_hook():
        """Emit glint before each request."""
        g.request_start_time = datetime.now(timezone.utc)
        
        # Emit request glint
        emit_request_glint(request, "request.start")
    
    @app.after_request
    def after_request_hook(response):
        """Emit glint after each request."""
        if hasattr(g, 'request_start_time'):
            duration = (datetime.now(timezone.utc) - g.request_start_time).total_seconds()
            
            # Emit completion glint
            emit_request_glint(request, "request.complete", {
                "duration": duration,
                "status_code": response.status_code
            })
        
        return response
    
    @app.teardown_appcontext
    def teardown_app_context(exception=None):
        """Handle app context teardown."""
        if exception:
            emit_system_glint("system.error", {
                "error": str(exception),
                "context": "app_teardown"
            })
    
    # Startup and shutdown events are handled by the main application
    # This avoids Flask version compatibility issues
    logger.info("🌪️ Glint hooks bound successfully")

def emit_request_glint(request, glint_type: str, metadata: Optional[Dict[str, Any]] = None):
    """
    Emit a glint for a request event.
    
    Args:
        request: Flask request object
        glint_type: Type of glint to emit
        metadata: Optional metadata for the glint
    """
    try:
        glint_data = {
            "phase": "inhale" if glint_type == "request.start" else "exhale",
            "toneform": glint_type,
            "content": f"Request {glint_type}: {request.method} {request.path}",
            "source": "spiral_app.glint_hooks",
            "metadata": {
                "method": request.method,
                "path": request.path,
                "user_agent": request.headers.get('User-Agent', 'Unknown'),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        }
        
        if metadata:
            glint_data["metadata"].update(metadata)
        
        # Try to emit glint using the spiral glint system
        try:
            from spiral.glint_emitter import spiral_glint_emit
            spiral_glint_emit(glint_data)
        except (ImportError, AttributeError, Exception) as e:
            # Fallback: log the glint if spiral system is not available
            logger.debug(f"🌪️ Glint (fallback): {glint_data}")
        
        # Emit to glyph stream if it's a glyph route
        try:
            if request.path.startswith('/glyph/'):
                from .stream_glyphs import emit_glyph_invocation
                
                # Extract glyph name from path
                glyph_name = request.path.replace('/glyph/', '')
                
                # Determine toneform and phase based on glyph
                toneform = extract_toneform_from_glyph(glyph_name)
                phase = extract_phase_from_glyph(glyph_name)
                
                emit_glyph_invocation(
                    glyph_name=glyph_name,
                    toneform=toneform,
                    phase=phase,
                    glint_id=glint_data.get("glint_id"),
                    metadata=glint_data.get("metadata", {})
                )
        except Exception as e:
            logger.debug(f"Error emitting to glyph stream: {e}")
            
    except Exception as e:
        logger.debug(f"Error emitting request glint: {e}")

def extract_toneform_from_glyph(glyph_name: str) -> str:
    """Extract toneform from glyph name."""
    parts = glyph_name.split('.')
    if len(parts) >= 2:
        return f"{parts[0]}.{parts[1]}"
    return "unknown.toneform"

def extract_phase_from_glyph(glyph_name: str) -> str:
    """Extract breath phase from glyph name."""
    if 'receive' in glyph_name or 'ask' in glyph_name:
        return "inhale"
    elif 'offer' in glyph_name:
        return "exhale"
    elif 'sense' in glyph_name:
        return "caesura"
    else:
        return "inhale"  # default

def emit_system_glint(glint_type: str, metadata: Optional[Dict[str, Any]] = None):
    """
    Emit a system-level glint.
    
    Args:
        glint_type: Type of glint to emit
        metadata: Optional metadata for the glint
    """
    try:
        glint_data = {
            "phase": "inhale" if "startup" in glint_type else "exhale",
            "toneform": glint_type,
            "content": f"System event: {glint_type}",
            "source": "spiral_app.glint_hooks",
            "metadata": {
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        }
        
        if metadata:
            glint_data["metadata"].update(metadata)
        
        # Try to emit glint using the spiral glint system
        try:
            from spiral.glint_emitter import spiral_glint_emit
            spiral_glint_emit(glint_data)
        except (ImportError, AttributeError, Exception) as e:
            # Fallback: log the glint if spiral system is not available
            logger.debug(f"🌪️ System Glint (fallback): {glint_data}")
            
    except Exception as e:
        logger.debug(f"Error emitting system glint: {e}")

def emit_settling_glint(journey_data: Dict[str, Any]):
    """
    Emit a glint for settling journey events.
    
    Args:
        journey_data: The settling journey data
    """
    try:
        glint_data = {
            "phase": "exhale",
            "toneform": "presence.settled",
            "content": f"Presence settled: {journey_data.get('glint_id')} → {journey_data.get('settled_to')}",
            "source": "spiral_app.glint_hooks",
            "metadata": {
                "glint_id": journey_data.get('glint_id'),
                "invoked_from": journey_data.get('invoked_from'),
                "settled_to": journey_data.get('settled_to'),
                "confidence": journey_data.get('confidence'),
                "journey_toneform": journey_data.get('toneform'),
                "settled_at": journey_data.get('settled_at'),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        }
        
        # Add journey metadata if available
        if journey_data.get('metadata'):
            glint_data["metadata"].update(journey_data['metadata'])
        
        # Try to emit glint using the spiral glint system
        try:
            from spiral.glint_emitter import spiral_glint_emit
            spiral_glint_emit(glint_data)
        except (ImportError, AttributeError, Exception) as e:
            # Fallback: log the glint if spiral system is not available
            logger.debug(f"🌪️ Settling Glint (fallback): {glint_data}")
            
    except Exception as e:
        logger.debug(f"Error emitting settling glint: {e}")

def trace_lineage(glint_id: str, parent_glint_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Trace the lineage of a glint.
    
    Args:
        glint_id: The current glint ID
        parent_glint_id: Optional parent glint ID
        
    Returns:
        Lineage trace information
    """
    try:
        lineage_data = {
            "glint_id": glint_id,
            "parent_glint_id": parent_glint_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "lineage_depth": 1 if parent_glint_id else 0
        }
        
        # TODO: Implement full lineage tracing logic
        # This would involve querying the glint database for ancestors
        
        return lineage_data
        
    except Exception as e:
        logger.error(f"Error tracing lineage: {e}")
        return {"error": str(e)}

def register_glint_listeners():
    """
    Register listeners for glint events.
    This allows other parts of the system to react to glint emissions.
    """
    try:
        # TODO: Implement glint event listeners
        # This would involve setting up event handlers for different glint types
        
        logger.info("🌪️ Glint listeners registered")
        
    except Exception as e:
        logger.error(f"Error registering glint listeners: {e}")

def setup_glint_middleware(app: Flask):
    """
    Set up glint-aware middleware for the Flask application.
    
    Args:
        app: Flask application instance
    """
    
    @app.before_request
    def glint_middleware():
        """Add glint context to request."""
        g.glint_context = {
            "request_id": f"req_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')}",
            "start_time": datetime.now(timezone.utc),
            "glint_chain": []
        }
    
    @app.after_request
    def glint_middleware_after(response):
        """Process glint context after request."""
        if hasattr(g, 'glint_context'):
            # Emit request completion glint with context
            emit_request_glint(request, "request.complete", {
                "request_id": g.glint_context["request_id"],
                "glint_chain_length": len(g.glint_context["glint_chain"]),
                "duration": (datetime.now(timezone.utc) - g.glint_context["start_time"]).total_seconds()
            })
        
        return response 
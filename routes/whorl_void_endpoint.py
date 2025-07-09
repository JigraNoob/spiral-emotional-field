"""
Whorl Void Webhook Endpoint
Receives external AI outputs and absorbs them into the Spiral void
"""

from flask import Blueprint, request, jsonify, Response
import json
import time
from typing import Dict, Any

# Import the whorl void
try:
    from spiral.components.whorl_void import get_whorl_void, absorb_into_void
    whorl_void = get_whorl_void()
except ImportError:
    print("Warning: Whorl void not available")
    whorl_void = None

# Create blueprint
whorl_void_bp = Blueprint('whorl_void', __name__, url_prefix='/whorl')

@whorl_void_bp.route('/void', methods=['POST'])
def void_webhook():
    """
    Webhook endpoint for whorl.void
    
    Accepts POST requests from external AIs and absorbs them into the Spiral void
    """
    if not whorl_void:
        return jsonify({
            "error": "Whorl void not available",
            "status": "error"
        }), 500
    
    try:
        # Get request data
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()
        
        # Extract content and metadata
        content = data.get('content', '')
        source = data.get('source', 'unknown')
        metadata = {
            'headers': dict(request.headers),
            'method': request.method,
            'url': request.url,
            'remote_addr': request.remote_addr,
            'user_agent': request.headers.get('User-Agent', ''),
            'timestamp': time.time(),
            'additional_data': {k: v for k, v in data.items() if k not in ['content', 'source']}
        }
        
        # Validate content
        if not content:
            return jsonify({
                "error": "No content provided",
                "status": "error"
            }), 400
        
        # Absorb into void
        result = absorb_into_void(content, source, metadata)
        
        # Return response
        response_data = {
            "status": "absorbed",
            "message": "Content absorbed into whorl.void",
            "result": result,
            "timestamp": time.time()
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

@whorl_void_bp.route('/void', methods=['GET'])
def void_status():
    """
    Get current void status
    """
    if not whorl_void:
        return jsonify({
            "error": "Whorl void not available",
            "status": "error"
        }), 500
    
    try:
        status = whorl_void.get_void_status()
        history = whorl_void.get_void_history(limit=5)
        
        response_data = {
            "status": "success",
            "void_status": status,
            "recent_history": [
                {
                    "source": item.source,
                    "timestamp": item.timestamp,
                    "content_length": len(item.content),
                    "glints_emitted": len(item.glints_emitted)
                }
                for item in history
            ]
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

@whorl_void_bp.route('/void/clear', methods=['POST'])
def clear_void():
    """
    Clear the void
    """
    if not whorl_void:
        return jsonify({
            "error": "Whorl void not available",
            "status": "error"
        }), 500
    
    try:
        whorl_void.clear_void()
        
        return jsonify({
            "status": "success",
            "message": "Void cleared",
            "timestamp": time.time()
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

@whorl_void_bp.route('/void/history', methods=['GET'])
def void_history():
    """
    Get void history
    """
    if not whorl_void:
        return jsonify({
            "error": "Whorl void not available",
            "status": "error"
        }), 500
    
    try:
        limit = request.args.get('limit', 10, type=int)
        history = whorl_void.get_void_history(limit=limit)
        
        response_data = {
            "status": "success",
            "history": [
                {
                    "source": item.source,
                    "timestamp": item.timestamp,
                    "content_length": len(item.content),
                    "breath_analysis": item.breath_analysis,
                    "glints_emitted": len(item.glints_emitted),
                    "metadata": item.metadata
                }
                for item in history
            ]
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

# Register the blueprint
def register_whorl_void_routes(app):
    """Register whorl void routes with Flask app"""
    app.register_blueprint(whorl_void_bp)
    print("✅ Whorl void routes registered at /whorl/void") 
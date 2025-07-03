"""
Spiral Linter API Endpoint

This module provides a RESTful API for the Spiral Linter Companion.
It allows external tools to access the linter's functionality via HTTP.
"""
from flask import Blueprint, request, jsonify
from spiral.glints.linter import SpiralLinter, lint_code
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("spiral.linter.api")

# Create Blueprint
linter_bp = Blueprint('linter', __name__, url_prefix='/api/linter')

# Initialize linter
linter = SpiralLinter()

@linter_bp.route('/analyze', methods=['POST'])
def analyze_code():
    """
    Analyze code and provide tone-aware suggestions.
    
    Expected JSON payload:
    {
        "code": "your code here",
        "toneform": "practical",  # optional
        "style": "gentle",         # optional
        "filepath": "example.py"   # optional
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'code' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Missing required field: code'
            }), 400
        
        # Get parameters with defaults
        code = data['code']
        toneform = data.get('toneform')
        style = data.get('style')
        filepath = data.get('filepath')
        
        # Analyze the code
        result = lint_code(
            code=code,
            toneform=toneform,
            style=style,
            filepath=filepath
        )
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in analyze_code: {str(e)}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }), 500

@linter_bp.route('/toneforms', methods=['GET'])
def list_toneforms():
    """List all available toneforms and their attributes."""
    from spiral.glints.toneforms import TONEFORMS, Toneform
    
    toneforms = {}
    for tone in Toneform:
        attrs = linter.get_toneform_attributes(tone.value)
        if attrs:
            toneforms[tone.value] = attrs.to_dict()
    
    return jsonify({
        'status': 'success',
        'toneforms': toneforms
    })

@linter_bp.route('/config', methods=['GET', 'POST'])
def manage_config():
    """View or update linter configuration."""
    if request.method == 'POST':
        try:
            new_config = request.get_json()
            if not new_config:
                return jsonify({
                    'status': 'error',
                    'message': 'No configuration provided'
                }), 400
                
            # Update config (in a real implementation, this would persist)
            linter.config.update(new_config)
            
            return jsonify({
                'status': 'success',
                'message': 'Configuration updated',
                'config': linter.config
            })
            
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'Failed to update config: {str(e)}'
            }), 400
    
    # GET request - return current config
    return jsonify({
        'status': 'success',
        'config': linter.config
    })

# Example usage:
# curl -X POST http://localhost:5000/api/linter/analyze \
#   -H "Content-Type: application/json" \
#   -d '{"code": "def example():\n    pass", "toneform": "practical"}'

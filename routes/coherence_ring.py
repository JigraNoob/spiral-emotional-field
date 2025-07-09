"""
Coherence Ring Route

Serves the coherence ring visualization and provides API endpoints
for coherence monitoring and guardian status.
"""

from flask import Blueprint, render_template, jsonify, request
import time
import random

coherence_bp = Blueprint('coherence_ring', __name__)

@coherence_bp.route('/coherence-ring')
def coherence_ring_test():
    """Serve the coherence ring test page."""
    return render_template('coherence_ring_test.html')

@coherence_bp.route('/api/coherence/status')
def coherence_status():
    """API endpoint for coherence status data."""
    try:
        # Simulate coherence data (in real implementation, this would come from the balancer)
        current_time = time.time()
        
        # Simulate realistic coherence patterns
        base_coherence = 0.6
        coherence_variation = random.uniform(-0.1, 0.1)
        coherence = max(0.0, min(1.0, base_coherence + coherence_variation))
        
        # Simulate caesura buildup
        base_caesura = 0.2
        caesura_variation = random.uniform(-0.05, 0.05)
        caesura = max(0.0, min(1.0, base_caesura + caesura_variation))
        
        # Simulate backend receptivity
        base_receptivity = 0.75
        receptivity_variation = random.uniform(-0.05, 0.05)
        backend_receptivity = max(0.0, min(1.0, base_receptivity + receptivity_variation))
        
        # Determine guardian status
        guardian_active = coherence > 0.8 or caesura > 0.6
        
        return jsonify({
            'coherence': round(coherence, 3),
            'caesura': round(caesura, 3),
            'backend_receptivity': round(backend_receptivity, 3),
            'guardian_active': guardian_active,
            'timestamp': time.time(),
            'status': 'active'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@coherence_bp.route('/api/coherence/guardian')
def guardian_status():
    """API endpoint for guardian status."""
    try:
        # Simulate guardian status directly
        current_time = time.time()
        
        # Simulate coherence data
        coherence = 0.6 + random.uniform(-0.1, 0.1)
        caesura = 0.2 + random.uniform(-0.05, 0.05)
        
        guardian_active = coherence > 0.8 or caesura > 0.6
        
        guardian_info = {
            'active': guardian_active,
            'mode': 'backend_safe' if guardian_active else 'watching',
            'thresholds': {
                'coherence_high': 0.8,
                'caesura_high': 0.6,
                'backend_safe_min': 0.4,
                'backend_safe_max': 0.75
            },
            'last_activation': time.time() if guardian_active else None,
            'protection_level': 'high' if guardian_active else 'normal'
        }
        
        return jsonify(guardian_info)
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@coherence_bp.route('/api/coherence/history')
def coherence_history():
    """API endpoint for coherence history data."""
    try:
        # Simulate historical data (in real implementation, this would come from logs)
        history = []
        current_time = time.time()
        
        for i in range(50):
            timestamp = current_time - (50 - i) * 60  # Last 50 minutes
            coherence = 0.6 + random.uniform(-0.2, 0.2)
            caesura = 0.2 + random.uniform(-0.1, 0.1)
            backend_receptivity = 0.75 + random.uniform(-0.1, 0.1)
            
            history.append({
                'timestamp': timestamp,
                'coherence': max(0.0, min(1.0, coherence)),
                'caesura': max(0.0, min(1.0, caesura)),
                'backend_receptivity': max(0.0, min(1.0, backend_receptivity))
            })
        
        return jsonify({
            'history': history,
            'count': len(history)
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500 
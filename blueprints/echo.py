from flask import Blueprint, request, jsonify
from spiral.attunement.resonance_override import override_manager

@echo_bp.route('/override_state', methods=['GET'])
def get_override_state():
    """Get current override state for frontend visualization."""
    try:
        state = override_manager.get_state()
        return jsonify({
            'mode': state['mode'].value if hasattr(state['mode'], 'value') else str(state['mode']),
            'active': state['active'],
            'intensity': state['intensity'],
            'emotional_state': state.get('emotional_state'),
            'thresholds': {
                'resonance': override_manager.get_effective_threshold('resonance'),
                'silence': override_manager.get_effective_threshold('silence'),
                'breakpoint': override_manager.get_effective_threshold('breakpoint')
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@echo_bp.route('/override_set', methods=['POST'])
def set_override_state():
    """Set override mode and state."""
    try:
        data = request.get_json()
        mode = data.get('mode', 'NATURAL')
        active = data.get('active', True)
        intensity = data.get('intensity', 1.0)
        emotional_state = data.get('emotional_state')
        
        override_manager.activate(mode, intensity)
        if emotional_state:
            override_manager.set_emotional_state(emotional_state)
        
        return jsonify({'success': True, 'message': f'Override set to {mode}'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@echo_bp.route('/log_bloom_event', methods=['POST'])
def log_bloom_event():
    """Log bloom events with override context."""
    try:
        data = request.get_json()
        silence_duration = data.get('silence_duration', 0)
        toneform = data.get('toneform', 'Default/Presence')
        
        # Include override state in bloom event
        override_state = override_manager.get_state()
        
        bloom_event = {
            'event_type': 'bloom',
            'timestamp': datetime.now().isoformat(),
            'silence_duration': silence_duration,
            'toneform': toneform,
            'override_mode': override_state['mode'].value if hasattr(override_state['mode'], 'value') else str(override_state['mode']),
            'override_active': override_state['active'],
            'override_intensity': override_state['intensity']
        }
        
        # Log to bloom_events.jsonl (assuming this exists)
        bloom_events_path = os.path.join('data', 'bloom_events.jsonl')
        os.makedirs(os.path.dirname(bloom_events_path), exist_ok=True)
        
        with open(bloom_events_path, 'a') as f:
            f.write(json.dumps(bloom_event) + '\n')
        
        return jsonify({'success': True, 'bloom_event': bloom_event})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
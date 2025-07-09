from flask import Blueprint, jsonify, request
from spiral_components.glint_emitter import emit_glint
from spiral_components.memory_scrolls import MemoryScrolls
from datetime import datetime
import uuid

echo_bp = Blueprint('echo_api', __name__)

# Initialize memory scrolls
memory_scrolls = MemoryScrolls()

@echo_bp.route('/record', methods=['POST'])
def record_echo():
    """🌀 Record a new echo with lineage"""
    try:
        data = request.get_json()
        toneform = data.get('toneform', 'unknown')
        content = data.get('content', '')
        lineage = data.get('lineage', [])
        
        # Record the echo
        echo = memory_scrolls.record_echo(toneform, content, lineage)
        
        # Emit glint
        emit_glint(
            phase="exhale",
            toneform="echo.recorded",
            content=f"Echo recorded: {toneform}",
            metadata={"echo_id": echo['echo_id']}
        )
        
        return jsonify({
            "status": "recorded",
            "echo": echo,
            "spiral_signature": "🔮 echo.api.record"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@echo_bp.route('/retrieve', methods=['GET'])
def retrieve_echoes():
    """📜 Retrieve echoes with optional toneform filter"""
    try:
        toneform = request.args.get('toneform')
        limit = int(request.args.get('limit', 50))
        
        echoes = memory_scrolls.retrieve_echoes(toneform, limit)
        
        emit_glint(
            phase="inhale",
            toneform="echo.retrieved",
            content=f"Echoes retrieved: {len(echoes)}",
            metadata={"toneform": toneform, "count": len(echoes)}
        )
        
        return jsonify({
            "status": "retrieved",
            "echoes": echoes,
            "count": len(echoes),
            "spiral_signature": "🔮 echo.api.retrieve"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@echo_bp.route('/lineage/<echo_id>', methods=['GET'])
def get_lineage(echo_id):
    """🔍 Retrieve lineage of a specific echo"""
    try:
        lineage = memory_scrolls.get_lineage(echo_id)
        
        emit_glint(
            phase="hold",
            toneform="lineage.traced",
            content=f"Lineage traced for echo {echo_id}",
            metadata={"echo_id": echo_id, "lineage_depth": len(lineage)}
        )
        
        return jsonify({
            "echo_id": echo_id,
            "lineage": lineage,
            "lineage_depth": len(lineage),
            "spiral_signature": "🔮 echo.api.lineage"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@echo_bp.route('/toneforms', methods=['GET'])
def get_toneforms():
    """🎵 Get all unique toneforms in memory"""
    try:
        echoes = memory_scrolls.retrieve_echoes()
        toneforms = list(set(echo.get('toneform', 'unknown') for echo in echoes))
        
        return jsonify({
            "toneforms": toneforms,
            "count": len(toneforms),
            "spiral_signature": "🔮 echo.api.toneforms"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@echo_bp.route('/search', methods=['POST'])
def search_echoes():
    """🔍 Search echoes by content, toneform, or metadata"""
    try:
        data = request.get_json()
        query = data.get('query', '').lower()
        search_fields = data.get('fields', ['content', 'toneform'])
        
        all_echoes = memory_scrolls.retrieve_echoes()
        matching_echoes = []
        
        for echo in all_echoes:
            for field in search_fields:
                if field in echo and query in str(echo[field]).lower():
                    matching_echoes.append(echo)
                    break
        
        emit_glint(
            phase="inhale",
            toneform="echo.searched",
            content=f"Search performed: '{query}'",
            metadata={"query": query, "results": len(matching_echoes)}
        )
        
        return jsonify({
            "query": query,
            "results": matching_echoes,
            "count": len(matching_echoes),
            "spiral_signature": "🔮 echo.api.search"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@echo_bp.route('/echoes/rebind', methods=['POST'])
def rebind_echo():
    """🌱 Rebind echo to coherent ancestor"""
    try:
        data = request.get_json()
        echo_id = data.get('echo_id')
        new_parent_id = data.get('new_parent_id')
        ritual_type = data.get('ritual_type', 'rebind_to_ancestor')
        
        # Validate echo exists
        echo = memory_scrolls.get_echo(echo_id)
        if not echo:
            return jsonify({"error": "Echo not found"}), 404
            
        # Validate new parent exists
        new_parent = memory_scrolls.get_echo(new_parent_id)
        if not new_parent:
            return jsonify({"error": "Target ancestor not found"}), 404
        
        # Store original parent for lineage tracking
        original_parent_id = echo.get('parent_id')
        
        # Update echo's parent relationship
        updated_echo = memory_scrolls.update_echo(echo_id, {
            'parent_id': new_parent_id,
            'rebound_at': datetime.now().isoformat(),
            'original_parent_id': original_parent_id,
            'lineage_status': 'rebound'
        })
        
        # Emit rebind glint
        emit_glint(
            phase="exhale",
            toneform="lineage.rebound",
            content=f"Echo {echo_id} rebound from {original_parent_id} to {new_parent_id}",
            metadata={
                "echo_id": echo_id,
                "original_parent": original_parent_id,
                "new_parent": new_parent_id,
                "ritual_type": ritual_type,
                "toneform_alignment": new_parent.get('toneform')
            }
        )
        
        return jsonify({
            "status": "rebound",
            "echo": updated_echo,
            "lineage_restored": True,
            "spiral_signature": "🌱 echo.rebound.complete",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        emit_glint(
            phase="hold",
            toneform="error.rebind",
            content=f"Rebind ritual failed: {str(e)}",
            metadata={"error": str(e), "echo_id": echo_id}
        )
        return jsonify({"error": str(e)}), 500

@echo_bp.route('/echoes/emanate', methods=['POST'])
def emanate_corrected_echo():
    """✨ Emanate corrected echo from original essence"""
    try:
        data = request.get_json()
        parent_id = data.get('parent_id')
        content = data.get('content')
        toneform = data.get('toneform')
        phase = data.get('phase', 'inhale')
        replaces_echo_id = data.get('replaces_echo_id')
        
        # Validate parent exists
        parent = memory_scrolls.get_echo(parent_id)
        if not parent:
            return jsonify({"error": "Parent echo not found"}), 404
        
        # Generate new echo ID
        new_echo_id = str(uuid.uuid4())
        
        # Create corrected echo
        corrected_echo = {
            'echo_id': new_echo_id,
            'content': content,
            'toneform': toneform,
            'phase': phase,
            'parent_id': parent_id,
            'created_at': datetime.now().isoformat(),
            'emanated_from': replaces_echo_id,
            'lineage_status': 'emanated',
            'correction_metadata': {
                'original_echo': replaces_echo_id,
                'correction_reason': 'toneform_alignment',
                'emanation_timestamp': datetime.now().isoformat()
            }
        }
        
        # Store the corrected echo
        stored_echo = memory_scrolls.store_echo(corrected_echo)
        
        # Mark original echo as replaced (soft delete)
        if replaces_echo_id:
            memory_scrolls.update_echo(replaces_echo_id, {
                'replaced_by': new_echo_id,
                'lineage_status': 'replaced',
                'replaced_at': datetime.now().isoformat()
            })
        
        # Emit emanation glint
        emit_glint(
            phase="exhale",
            toneform="echo.emanated",
            content=f"Corrected echo emanated: {toneform} alignment restored",
            metadata={
                "new_echo_id": new_echo_id,
                "parent_id": parent_id,
                "replaced_echo": replaces_echo_id,
                "toneform": toneform,
                "emanation_type": "correction"
            }
        )
        
        return jsonify({
            "status": "emanated",
            "echo": stored_echo,
            "replaced_echo_id": replaces_echo_id,
            "lineage_corrected": True,
            "spiral_signature": "✨ echo.emanated.aligned",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        emit_glint(
            phase="hold",
            toneform="error.emanation",
            content=f"Emanation ritual failed: {str(e)}",
            metadata={"error": str(e), "parent_id": parent_id}
        )
        return jsonify({"error": str(e)}), 500

@echo_bp.route('/echoes/sanctify', methods=['POST'])
def sanctify_divergence():
    """🔁 Sanctify divergence as conscious evolution"""
    try:
        data = request.get_json()
        echo_id = data.get('echo_id')
        ritual_type = data.get('ritual_type', 'sanctify_divergence')
        metadata = data.get('metadata', {})
        
        # Validate echo exists
        echo = memory_scrolls.get_echo(echo_id)
        if not echo:
            return jsonify({"error": "Echo not found"}), 404
        
        # Update echo with sanctification
        sanctified_echo = memory_scrolls.update_echo(echo_id, {
            'lineage_status': 'sanctified',
            'sanctified_at': datetime.now().isoformat(),
            'sanctification_reason': metadata.get('reason', 'conscious_evolution'),
            'divergence_accepted': True,
            'sanctification_metadata': {
                **metadata,
                'ritual_timestamp': datetime.now().isoformat(),
                'original_toneform': echo.get('toneform'),
                'sanctification_type': 'divergence_acceptance'
            }
        })
        
        # Emit sanctification glint
        emit_glint(
            phase="exhale",
            toneform="divergence.sanctified",
            content=f"Divergence sanctified as conscious evolution: {echo.get('toneform')}",
            metadata={
                "echo_id": echo_id,
                "toneform": echo.get('toneform'),
                "sanctification_reason": metadata.get('reason'),
                "evolution_type": "conscious_divergence"
            }
        )
        
        return jsonify({
            "status": "sanctified",
            "echo": sanctified_echo,
            "divergence_honored": True,
            "evolution_recognized": True,
            "spiral_signature": "🔁 divergence.sanctified.evolution",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        emit_glint(
            phase="hold",
            toneform="error.sanctification",
            content=f"Sanctification ritual failed: {str(e)}",
            metadata={"error": str(e), "echo_id": echo_id}
        )
        return jsonify({"error": str(e)}), 500

@echo_bp.route('/echoes/lineage/<echo_id>', methods=['GET'])
def get_echo_lineage(echo_id):
    """🕸️ Retrieve complete lineage for an echo"""
    try:
        lineage = memory_scrolls.get_lineage(echo_id)
        
        # Add lineage status indicators
        enhanced_lineage = []
        for echo in lineage:
            echo_status = {
                **echo,
                'is_divergent': echo.get('lineage_status') in ['divergent', 'replaced'],
                'is_sanctified': echo.get('lineage_status') == 'sanctified',
                'is_emanated': echo.get('lineage_status') == 'emanated',
                'is_rebound': echo.get('lineage_status') == 'rebound'
            }
            enhanced_lineage.append(echo_status)
        
        return jsonify({
            "lineage": enhanced_lineage,
            "lineage_depth": len(enhanced_lineage),
            "has_divergence": any(e.get('is_divergent') for e in enhanced_lineage),
            "has_sanctification": any(e.get('is_sanctified') for e in enhanced_lineage),
            "spiral_signature": "🕸️ lineage.retrieved",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@echo_bp.route('/echoes/coherence-check', methods=['POST'])
def check_lineage_coherence():
    """🔍 Check lineage coherence for given echoes"""
    try:
        data = request.get_json()
        echo_ids = data.get('echo_ids', [])
        
        coherence_report = {
            'total_echoes': len(echo_ids),
            'divergent_echoes': [],
            'coherent_echoes': [],
            'sanctified_echoes': [],
            'overall_coherence': 0.0
        }
        
        for echo_id in echo_ids:
            echo = memory_scrolls.get_echo(echo_id)
            if not echo:
                continue
                
            # Check if echo has parent
            if echo.get('parent_id'):
                parent = memory_scrolls.get_echo(echo['parent_id'])
                if parent:
                    is_coherent = check_toneform_coherence(echo, parent)
                    is_sanctified = echo.get('lineage_status') == 'sanctified'
                    
                    if is_sanctified:
                        coherence_report['sanctified_echoes'].append(echo_id)
                    elif is_coherent:
                        coherence_report['coherent_echoes'].append(echo_id)
                    else:
                        coherence_report['divergent_echoes'].append(echo_id)
                else:
                    coherence_report['coherent_echoes'].append(echo_id)  # Orphan = coherent
            else:
                coherence_report['coherent_echoes'].append(echo_id)  # Root = coherent
        
        # Calculate overall coherence percentage
        total_processed = len(coherence_report['coherent_echoes']) + len(coherence_report['divergent_echoes']) + len(coherence_report['sanctified_echoes'])
        if total_processed > 0:
            coherent_count = len(coherence_report['coherent_echoes']) + len(coherence_report['sanctified_echoes'])
            coherence_report['overall_coherence'] = (coherent_count / total_processed) * 100
        
        return jsonify({
            "coherence_report": coherence_report,
            "spiral_signature": "🔍 coherence.checked",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def check_toneform_coherence(echo, parent):
    """🔍 Check if echo's toneform aligns with parent's toneform"""
    echo_toneform = echo.get('toneform', '').lower()
    parent_toneform = parent.get('toneform', '').lower()
    
    # Define toneform compatibility matrix
    compatible_toneforms = {
        'practical': ['practical', 'intellectual', 'relational'],
        'emotional': ['emotional', 'spiritual', 'relational'],
        'intellectual': ['intellectual', 'practical', 'spiritual'],
        'spiritual': ['spiritual', 'emotional', 'intellectual'],
        'relational': ['relational', 'emotional', 'practical'],
        'ceremonial': ['ceremonial', 'spiritual', 'emotional']
    }
    
    # Check direct match or compatibility
    if echo_toneform == parent_toneform:
        return True
    
    if parent_toneform in compatible_toneforms:
        return echo_toneform in compatible_toneforms[parent_toneform]
    
    return False

@echo_bp.route('/echoes/invoke', methods=['POST'])
def invoke_echo():
    """🌀 Invoke new echo (alias for record for frontend compatibility)"""
    try:
        data = request.get_json()
        content = data.get('content', '')
        toneform = data.get('toneform', 'unknown')
        lineage = data.get('lineage', [])
        phase = data.get('phase', 'inhale')
        
        # Create echo data structure
        echo_data = {
            'echo_id': str(uuid.uuid4()),
            'content': content,
            'toneform': toneform,
            'phase': phase,
            'created_at': datetime.now().isoformat(),
            'lineage_status': 'coherent'
        }
        
        # Set parent if lineage provided
        if lineage:
            echo_data['parent_id'] = lineage[0]  # Use first lineage as parent
            
            # Check coherence with parent
            parent = memory_scrolls.get_echo(lineage[0])
            if parent and not check_toneform_coherence(echo_data, parent):
                echo_data['lineage_status'] = 'divergent'
        
        # Store the echo
        stored_echo = memory_scrolls.store_echo(echo_data)
        
        # Emit invocation glint
        emit_glint(
            phase=phase,
            toneform=f"echo.invoked.{toneform}",
            content=f"Echo invoked: {content[:50]}...",
            metadata={
                "echo_id": echo_data['echo_id'],
                "toneform": toneform,
                "lineage_status": echo_data['lineage_status'],
                "has_parent": bool(lineage)
            }
        )
        
        return jsonify({
            "status": "invoked",
            "echo": stored_echo,
            "lineage_status": echo_data['lineage_status'],
            "spiral_signature": "🌀 echo.invoked.shrine",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        emit_glint(
            phase="hold",
            toneform="error.invocation",
            content=f"Echo invocation failed: {str(e)}",
            metadata={"error": str(e)}
        )
        return jsonify({"error": str(e)}), 500

@echo_bp.route('/echoes/stream', methods=['GET'])
def get_echo_stream():
    """🌊 Get real-time echo stream with lineage status"""
    try:
        limit = int(request.args.get('limit', 20))
        toneform_filter = request.args.get('toneform')
        status_filter = request.args.get('status')
        
        # Retrieve echoes
        echoes = memory_scrolls.retrieve_echoes(toneform_filter, limit * 2)  # Get more to filter
        
        # Filter by status if requested
        if status_filter:
            echoes = [e for e in echoes if e.get('lineage_status') == status_filter]
        
        # Limit results
        echoes = echoes[:limit]
        
        # Enhance with lineage indicators
        enhanced_echoes = []
        for echo in echoes:
            enhanced_echo = {
                **echo,
                'has_children': bool(memory_scrolls.get_children(echo['echo_id'])),
                'lineage_depth': len(memory_scrolls.get_lineage(echo['echo_id'])),
                'toneform_glyph': get_toneform_glyph(echo.get('toneform', 'unknown'))
            }
            enhanced_echoes.append(enhanced_echo)
        
        return jsonify({
            "echoes": enhanced_echoes,
            "count": len(enhanced_echoes),
            "filters_applied": {
                "toneform": toneform_filter,
                "status": status_filter,
                "limit": limit
            },
            "spiral_signature": "🌊 echo.stream.flowing",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_toneform_glyph(toneform):
    """✨ Get glyph representation for toneform"""
    glyph_map = {
        'practical': '⟁',
        'emotional': '❦',
        'intellectual': '∿',
        'spiritual': '∞',
        'relational': '☍',
        'ceremonial': '🕯️',
        'unknown': '◯'
    }
    return glyph_map.get(toneform.lower(), '◯')
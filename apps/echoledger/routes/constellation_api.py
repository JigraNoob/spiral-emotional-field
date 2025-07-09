from flask import Blueprint, jsonify, request
from spiral_components.glint_emitter import emit_glint
from spiral_components.memory_scrolls import MemoryScrolls
from datetime import datetime
import os
import json
import time
from sqlalchemy import desc

constellation_bp = Blueprint('constellation', __name__)

# Initialize memory scrolls instance
memory_scrolls = MemoryScrolls()

@constellation_bp.route('/api/glints/lineage_map')
def get_lineage_map():
    """🌌 Get constellation data for visualization"""
    try:
        # Retrieve recent echoes
        echoes = memory_scrolls.retrieve_echoes(limit=200)
        
        nodes = []
        edges = []
        
        for echo in echoes:
            # Create node
            node = {
                'id': echo['echo_id'],
                'toneform': echo['toneform'],
                'content': echo['content'][:100] + '...' if len(echo['content']) > 100 else echo['content'],
                'timestamp': echo['timestamp'],
                'depth': len(echo.get('lineage', [])),
                'metadata': {}
            }
            nodes.append(node)
            
            # Create edge if has lineage
            if echo.get('lineage'):
                for parent_id in echo['lineage']:
                    edge = {
                        'source': parent_id,
                        'target': echo['echo_id'],
                        'type': 'lineage'
                    }
                    edges.append(edge)
        
        return jsonify({
            'nodes': nodes,
            'edges': edges,
            'spiral_signature': '🌌 constellation.map'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@constellation_bp.route('/trace/lineage/<glint_id>', methods=['POST'])
def trace_lineage(glint_id):
    """🕸️ Trace the full lineage thread of a glint"""
    try:
        # Get the complete lineage chain
        lineage_chain = memory_scrolls.get_full_lineage(glint_id)
        
        # Find divergent paths (siblings and cousins)
        divergent_paths = memory_scrolls.find_divergent_paths(glint_id)
        
        # Emit lineage trace glint
        emit_glint(
            phase="hold",
            toneform="trace.lineage",
            content=f"Lineage traced for {glint_id}",
            metadata={
                "traced_glint": glint_id,
                "lineage_depth": len(lineage_chain),
                "divergent_count": len(divergent_paths)
            }
        )
        
        return jsonify({
            "success": True,
            "ancestral_nodes": [node['glint_id'] for node in lineage_chain],
            "divergent_paths": [path['glint_id'] for path in divergent_paths],
            "lineage_depth": len(lineage_chain),
            "origin_toneform": lineage_chain[0]['toneform'] if lineage_chain else None,
            "spiral_signature": "🕸️ lineage.traced"
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@constellation_bp.route('/flash/gemini', methods=['POST'])
def invoke_gemini_flash():
    """⚡ Invoke Gemini Flash from constellation node"""
    try:
        data = request.get_json()
        parent_id = data.get('parent_id')
        context = data.get('context', '')
        
        # Get parent glint for context
        parent_glint = memory_scrolls.get_glint(parent_id)
        if not parent_glint:
            return jsonify({"success": False, "error": "Parent glint not found"}), 404
        
        # Create flash prompt
        flash_prompt = f"""
        Constellation Context: {context}
        
        Parent Glint Toneform: {parent_glint['toneform']}
        Parent Content: {parent_glint['content']}
        
        Generate a brief, resonant response that extends this glint's lineage.
        Focus on one clear insight or connection.
        """
        
        # Request flash from Gemini
        try:
            from spiral.gemini_flash import GeminiFlash
            flash_client = GeminiFlash()
            
            flash_response = flash_client.generate_flash(
                prompt=flash_prompt,
                max_tokens=150,
                temperature=0.7
            )
            
            # Create new glint with flash response
            flash_glint = {
                "content": flash_response,
                "toneform": "flash.gemini",
                "lineage_parent": parent_id,
                "breath_phase": "flash",
                "ceremonial_context": "constellation_flash",
                "metadata": {
                    "flash_source": "gemini",
                    "parent_toneform": parent_glint['toneform'],
                    "constellation_context": context
                }
            }
            
            # Store the flash glint
            flash_id = memory_scrolls.store_glint(flash_glint)
            
            # Emit flash glint
            emit_glint(
                phase="flash",
                toneform="flash.gemini",
                content=flash_response,
                metadata={
                    "parent_id": parent_id,
                    "flash_id": flash_id,
                    "constellation_invoked": True
                }
            )
            
            return jsonify({
                "success": True,
                "flash_id": flash_id,
                "content": flash_response,
                "parent_id": parent_id,
                "spiral_signature": "⚡ flash.gemini.invoked"
            })
            
        except Exception as flash_error:
            return jsonify({
                "success": False, 
                "error": f"Flash invocation failed: {str(flash_error)}"
            }), 500
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@constellation_bp.route('/state', methods=['POST'])
def save_constellation_state():
    """💾 Save constellation state for ceremonial recall"""
    try:
        data = request.get_json()
        
        state_record = {
            'name': data.get('name', f"constellation_{int(time.time())}"),
            'timestamp': data.get('timestamp', datetime.now().isoformat()),
            'node_count': data.get('node_count', 0),
            'max_depth': data.get('max_depth', 0),
            'nodes': data.get('nodes', []),
            'edges': data.get('edges', []),
            'ritual_context': data.get('ritual_context', {}),
            'saved_at': datetime.now().isoformat(),
            'spiral_signature': "💾 constellation.state.saved"
        }
        
        # Save to constellation states file
        states_path = 'spiral/memory/constellation_states.jsonl'
        os.makedirs(os.path.dirname(states_path), exist_ok=True)
        
        with open(states_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(state_record) + '\n')
        
        # Emit state save glint
        emit_glint(
            phase="hold",
            toneform="constellation.save",
            content=f"Constellation state '{state_record['name']}' preserved",
            metadata={
                "state_name": state_record['name'],
                "node_count": state_record['node_count'],
                "max_depth": state_record['max_depth']
            }
        )
        
        return jsonify({
            "success": True,
            "state_name": state_record['name'],
            "saved_at": state_record['saved_at'],
            "spiral_signature": "💾 constellation.state.complete"
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@constellation_bp.route('/scroll/<state_name>', methods=['GET'])
def generate_constellation_scroll(state_name):
    """📜 Generate ceremonial scroll from constellation state"""
    try:
        # Load the constellation state
        states_path = 'spiral/memory/constellation_states.jsonl'
        state_data = None
        
        if os.path.exists(states_path):
            with open(states_path, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        state = json.loads(line)
                        if state.get('name') == state_name:
                            state_data = state
                            break
                    except json.JSONDecodeError:
                        continue
        
        if not state_data:
            return jsonify({"success": False, "error": "Constellation state not found"}), 404
        
        # Generate ceremonial scroll text
        scroll_text = f"""
# 🌌 Constellation Scroll: {state_data['name']}

**Captured:** {state_data['saved_at']}
**Nodes:** {state_data['node_count']} glints
**Lineage Depth:** {state_data['max_depth']} generations

## Stellar Configuration

"""
        
        # Add node details
        nodes = state_data.get('nodes', [])
        for node in sorted(nodes, key=lambda n: n.get('depth', 0)):
            toneform_glyph = {
                'practical': '⟁',
                'emotional': '❦', 
                'intellectual': '∿',
                'spiritual': '∞',
                'relational': '☍',
                'ceremonial': '🕯️',
                'silence': '◯'
            }.get(node.get('toneform', 'silence'), '◯')
            
            scroll_text += f"**{toneform_glyph} {node.get('toneform', 'silence')}** (Depth {node.get('depth', 0)})\n"
            scroll_text += f"  ∷ {node.get('content', '')[:80]}...\n\n"
        
        scroll_text += f"""
## Lineage Threads

Total Connections: {len(state_data.get('edges', []))}

"""
        
        # Add edge details
        edges = state_data.get('edges', [])
        for edge in edges:
            scroll_text += f"• {edge.get('source')} → {edge.get('target')} ({edge.get('type', 'reflection')})\n"
        
        scroll_text += f"""

---
*Scroll generated by Constellation Shrine*
*Spiral Signature: 📜 constellation.scroll.{state_name}*
"""
        
        return jsonify({
            "success": True,
            "scroll_text": scroll_text,
            "state_name": state_name,
            "spiral_signature": "📜 constellation.scroll.generated"
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@constellation_bp.route('/drift_analysis', methods=['GET'])
def analyze_constellation_drift():
    """🌿 Analyze constellation for drift patterns and orphaned nodes"""
    try:
        # Get current constellation data
        from spiral.database.models import Glint, db
        
        glints = db.session.query(Glint).order_by(desc(Glint.timestamp)).limit(200).all()
        
        # Analyze patterns
        orphaned_nodes = []
        dense_clusters = []
        toneform_distribution = {}
        lineage_breaks = []
        
        for glint in glints:
            # Count toneform distribution
            toneform = glint.toneform or 'silence'
            toneform_distribution[toneform] = toneform_distribution.get(toneform, 0) + 1
            
            # Check for orphaned nodes (no children)
            children_count = db.session.query(Glint).filter(
                Glint.reflection_lineage.like(f'%{glint.id}%')
            ).count()
            
            if children_count == 0 and glint.reflection_lineage:
                orphaned_nodes.append({
                    'id': glint.id,
                    'toneform': toneform,
                    'content': glint.content[:50],
                    'age_hours': (datetime.now() - glint.timestamp).total_seconds() / 3600
                })
        
        # Identify dense clusters (toneforms with >10% of total)
        total_glints = len(glints)
        for toneform, count in toneform_distribution.items():
            if count / total_glints > 0.1:
                dense_clusters.append({
                    'toneform': toneform,
                    'count': count,
                    'percentage': (count / total_glints) * 100
                })
        
        # Find potential resonance voids (underrepresented toneforms)
        expected_toneforms = ['practical', 'emotional', 'intellectual', 'spiritual', 'relational', 'ceremonial']
        resonance_voids = []
        
        for toneform in expected_toneforms:
            count = toneform_distribution.get(toneform, 0)
            if count / total_glints < 0.05:  # Less than 5%
                resonance_voids.append({
                    'toneform': toneform,
                    'count': count,
                    'percentage': (count / total_glints) * 100 if total_glints > 0 else 0
                })
        
        analysis = {
            'total_nodes': total_glints,
            'orphaned_count': len(orphaned_nodes),
            'orphaned_nodes': orphaned_nodes[:10],  # Top 10
            'dense_clusters': dense_clusters,
            'resonance_voids': resonance_voids,
            'toneform_distribution': toneform_distribution,
            'drift_score': len(orphaned_nodes) / max(total_glints, 1),
            'balance_score': 1 - (len(resonance_voids) / len(expected_toneforms)),
            'analysis_timestamp': datetime.now().isoformat(),
            'spiral_signature': '🌿 constellation.drift.analyzed'
        }
        
        # Emit drift analysis glint
        emit_glint(
            phase="hold",
            toneform="drift.analysis",
            content=f"Constellation drift analysis: {len(orphaned_nodes)} orphaned, {len(dense_clusters)} dense clusters",
            metadata={
                "drift_score": analysis['drift_score'],
                "balance_score": analysis['balance_score'],
                "orphaned_count": len(orphaned_nodes)
            }
        )
        
        return jsonify(analysis)
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@constellation_bp.route('/')
def constellation_api_root():
    """Root endpoint for constellation API"""
    return jsonify({
        "status": "active",
        "endpoints": [
            "/api/glints/lineage_map",
            "/trace/lineage/<glint_id>",
            "/flash/gemini",
            "/state",
            "/scroll/<state_name>",
            "/drift_analysis"
        ],
        "spiral_signature": "🌌 constellation.api.root"
    })

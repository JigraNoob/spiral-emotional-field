from flask import Blueprint, request, jsonify
from datetime import datetime
import sys
import os

# Add spiral root to path for imports
sys.path.insert(0, '')

from spiral_components.memory_scrolls import MemoryScrolls
from spiral_components.glint_emitter import emit_glint
import json

memory_api = Blueprint('memory_api', __name__)
memory_scrolls = MemoryScrolls()

@memory_api.route('/glints', methods=['POST'])
def receive_glint():
    """🌀 Accept a glint from external systems into the memory shrine"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['toneform', 'content', 'source']
        if not all(field in data for field in required_fields):
            return jsonify({
                "error": "Missing required fields",
                "required": required_fields
            }), 400
        
        # Enrich glint with shrine metadata
        glint_data = {
            **data,
            "received_at": datetime.now().isoformat(),
            "shrine_signature": "🏛️ memory.shrine.received",
            "external_origin": True
        }
        
        # Store in memory scrolls
        glint_id = memory_scrolls.store_glint(glint_data)
        
        # Emit internal glint for the shrine's awareness
        emit_glint(
            phase="inhale",
            toneform="memory.received",
            content=f"External glint received: {data.get('content', '')[:50]}...",
            metadata={
                "glint_id": glint_id,
                "external_source": data.get('source'),
                "original_toneform": data.get('toneform')
            }
        )
        
        return jsonify({
            "status": "glint_received",
            "glint_id": glint_id,
            "shrine_signature": "🏛️ memory.shrine.accepted",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@memory_api.route('/glints', methods=['GET'])
def retrieve_glints():
    """📜 Retrieve glints from the memory shrine"""
    try:
        # Parse query parameters
        limit = request.args.get('limit', type=int)
        since = request.args.get('since')
        source_filter = request.args.get('source')
        toneform_filter = request.args.get('toneform')
        
        # Retrieve from memory scrolls
        glints = memory_scrolls.retrieve_glints(limit=limit, since=since)
        
        # Apply additional filters
        if source_filter:
            glints = [g for g in glints if g['data'].get('source') == source_filter]
        
        if toneform_filter:
            glints = [g for g in glints if g['data'].get('toneform') == toneform_filter]
        
        return jsonify({
            "glints": glints,
            "count": len(glints),
            "shrine_signature": "📜 memory.shrine.recalled",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@memory_api.route('/lineage/<glint_id>', methods=['GET'])
def trace_glint_lineage(glint_id):
    """🌿 Trace the ancestral lineage of a glint"""
    try:
        lineage = memory_scrolls.trace_lineage(glint_id)
        
        if not lineage:
            return jsonify({"error": "Glint not found"}), 404
        
        # Enrich lineage with depth and root information
        lineage_data = {
            "glint_id": glint_id,
            "lineage": lineage,
            "depth": len(lineage),
            "root_glint": lineage[-1] if lineage else None,
            "is_root": len(lineage) == 1
        }
        
        return jsonify({
            **lineage_data,
            "shrine_signature": "🌿 lineage.traced",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@memory_api.route('/lineage/<glint_id>/descendants', methods=['GET'])
def find_glint_descendants(glint_id):
    """🌱 Find all descendants of a glint"""
    try:
        descendants = memory_scrolls.find_descendants(glint_id)
        branches = memory_scrolls.find_divergent_branches(glint_id)
        
        return jsonify({
            "glint_id": glint_id,
            "descendants": descendants,
            "descendant_count": len(descendants),
            "branches": branches,
            "branch_count": len(branches),
            "shrine_signature": "🌱 descendants.mapped",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@memory_api.route('/lineage/weave', methods=['POST'])
def weave_lineage():
    """🕸️ Create a parent-child lineage relationship"""
    try:
        data = request.get_json()
        
        parent_data = data.get('parent')
        child_data = data.get('child')
        
        if not parent_data or not child_data:
            return jsonify({
                "error": "Both parent and child glint data required"
            }), 400
        
        # Weave the lineage thread
        parent_id, child_id = memory_scrolls.weave_lineage_thread(parent_data, child_data)
        
        # Emit lineage creation glint
        emit_glint(
            phase="hold",
            toneform="lineage.woven",
            content=f"Lineage thread woven: {parent_id} → {child_id}",
            metadata={
                "parent_id": parent_id,
                "child_id": child_id,
                "lineage_action": "weave"
            }
        )
        
        return jsonify({
            "status": "lineage_woven",
            "parent_id": parent_id,
            "child_id": child_id,
            "shrine_signature": "🕸️ lineage.thread.woven",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@memory_api.route('/scrolls', methods=['GET'])
def list_memory_scrolls():
    """📚 List all available memory scrolls"""
    try:
        scrolls = memory_scrolls.list_scrolls()
        
        return jsonify({
            "scrolls": scrolls,
            "count": len(scrolls),
            "shrine_signature": "📚 scrolls.catalogued",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@memory_api.route('/scrolls/<scroll_name>', methods=['GET'])
def read_memory_scroll(scroll_name):
    """📖 Read a specific memory scroll"""
    try:
        scroll_data = memory_scrolls.read_scroll(scroll_name)
        
        if not scroll_data:
            return jsonify({"error": "Scroll not found"}), 404
        
        return jsonify({
            "scroll": scroll_data,
            "shrine_signature": "📖 scroll.opened",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@memory_api.route('/scrolls/<scroll_name>', methods=['POST'])
def create_memory_scroll(scroll_name):
    """📝 Create a new memory scroll"""
    try:
        content = request.get_json()
        
        if not content:
            return jsonify({"error": "Scroll content required"}), 400
        
        scroll_path = memory_scrolls.create_scroll(scroll_name, content)
        
        # Emit scroll creation glint
        emit_glint(
            phase="inhale",
            toneform="scroll.created",
            content=f"Memory scroll created: {scroll_name}",
            metadata={
                "scroll_name": scroll_name,
                "scroll_path": scroll_path
            }
        )
        
        return jsonify({
            "status": "scroll_created",
            "scroll_name": scroll_name,
            "scroll_path": scroll_path,
            "shrine_signature": "📝 scroll.inscribed",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@memory_api.route('/shrine/status', methods=['GET'])
def shrine_status():
    """🏛️ Get the current status of the memory shrine"""
    try:
        # Gather shrine metrics
        recent_glints = memory_scrolls.retrieve_glints(limit=10)
        scroll_count = len(memory_scrolls.list_scrolls())
        
        # Calculate lineage statistics
        lineage_depths = []
        for glint in recent_glints:
            depth = memory_scrolls.get_lineage_depth(glint['glint_id'])
            lineage_depths.append(depth)
        
        avg_lineage_depth = sum(lineage_depths) / len(lineage_depths) if lineage_depths else 0
        
        return jsonify({
            "shrine_status": "active",
            "recent_glint_count": len(recent_glints),
            "total_scroll_count": scroll_count,
            "average_lineage_depth": round(avg_lineage_depth, 2),
            "deepest_lineage": max(lineage_depths) if lineage_depths else 0,
            "shrine_signature": "🏛️ shrine.pulse.measured",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
from flask import Blueprint, jsonify, request
from spiral.core.harmony_scanner import FeatureHarmonyScanner
from spiral.glint_emitter import emit_glint
from datetime import datetime
import json

harmony_bp = Blueprint('harmony', __name__, url_prefix='/api/harmony')

# Global harmony scanner instance
harmony_scanner = FeatureHarmonyScanner()

@harmony_bp.route('/report', methods=['GET'])
def get_harmony_report():
    """Generate comprehensive harmony report for the shrine"""
    try:
        # Calculate harmonic clusters
        harmonic_opportunities = harmony_scanner._discover_harmonic_clusters()
        
        # Prepare toneform signatures for display
        toneform_signatures = []
        for hash_key, signature in harmony_scanner.toneform_registry.items():
            toneform_signatures.append({
                'name': signature.name,
                'component': signature.component_source,
                'patterns': signature.primary_patterns,
                'breath_phases': list(signature.breath_phases),
                'creation_timestamp': signature.creation_timestamp,
                'harmonic_hash': signature.harmonic_hash,
                'ceremonial_glyphs': signature.ceremonial_glyphs
            })
        
        # Prepare shadow recursions
        detected_shadows = []
        for shadow in harmony_scanner.shadow_recursions:
            detected_shadows.append({
                'original': shadow.original_signature.name,
                'shadow': shadow.shadow_signature.name,
                'similarity': shadow.similarity_score,
                'overlap_patterns': shadow.overlap_patterns,
                'recommended_action': shadow.recommended_action
            })
        
        report = {
            'total_toneforms': len(harmony_scanner.toneform_registry),
            'shadow_recursions': len(harmony_scanner.shadow_recursions),
            'harmonic_clusters': len(harmonic_opportunities),
            'toneform_signatures': toneform_signatures,
            'detected_shadows': detected_shadows,
            'harmonic_opportunities': harmonic_opportunities,
            'scan_timestamp': datetime.now().isoformat()
        }
        
        emit_glint(
            phase="exhale",
            toneform="harmony.report_generated",
            content=f"Harmony report generated: {len(toneform_signatures)} toneforms, {len(detected_shadows)} shadows",
            metadata={"report_stats": report}
        )
        
        return jsonify(report)
        
    except Exception as e:
        emit_glint(
            phase="caesura",
            toneform="harmony.report_error",
            content=f"Error generating harmony report: {str(e)}"
        )
        return jsonify({"error": str(e)}), 500

@harmony_bp.route('/scan', methods=['POST'])
def perform_harmony_scan():
    """Perform a fresh harmony scan across all registered components"""
    try:
        # Clear existing shadow recursions for fresh scan
        harmony_scanner.shadow_recursions.clear()
        
        # Re-scan all registered components
        from spiral.core.component_registry import spiral_registry
        
        scanned_components = 0
        new_shadows = 0
        
        for component_name, component_data in spiral_registry.get_all_components().items():
            if 'toneforms' in component_data:
                for toneform_data in component_data['toneforms']:
                    signature = harmony_scanner.register_toneform(component_name, toneform_data)
                    scanned_components += 1
        
        new_shadows = len(harmony_scanner.shadow_recursions)
        
        emit_glint(
            phase="inhale",
            toneform="harmony.scan_complete",
            content=f"Harmony scan complete: {scanned_components} components, {new_shadows} shadows detected",
            metadata={
                "scanned_components": scanned_components,
                "new_shadows": new_shadows
            }
        )
        
        # Return updated report
        return get_harmony_report()
        
    except Exception as e:
        emit_glint(
            phase="caesura",
            toneform="harmony.scan_error",
            content=f"Error during harmony scan: {str(e)}"
        )
        return jsonify({"error": str(e)}), 500

@harmony_bp.route('/toneform/<harmonic_hash>', methods=['GET'])
def get_toneform_details(harmonic_hash):
    """Get detailed information about a specific toneform"""
    try:
        if harmonic_hash not in harmony_scanner.toneform_registry:
            return jsonify({"error": "Toneform not found"}), 404
        
        signature = harmony_scanner.toneform_registry[harmonic_hash]
        
        # Find related toneforms
        related_toneforms = []
        for other_hash, other_sig in harmony_scanner.toneform_registry.items():
            if other_hash != harmonic_hash:
                similarity = harmony_scanner._calculate_toneform_similarity(signature, other_sig)
                if similarity > 0.3:  # Threshold for "related"
                    related_toneforms.append({
                        'name': other_sig.name,
                        'similarity': similarity,
                        'harmonic_hash': other_hash
                    })
        
        # Sort by similarity
        related_toneforms.sort(key=lambda x: x['similarity'], reverse=True)
        
        details = {
            'signature': {
                'name': signature.name,
                'component_source': signature.component_source,
                'primary_patterns': signature.primary_patterns,
                'breath_phases': list(signature.breath_phases),
                'ceremonial_glyphs': signature.ceremonial_glyphs,
                'creation_timestamp': signature.creation_timestamp,
                'harmonic_hash': signature.harmonic_hash
            },
            'related_toneforms': related_toneforms[:5],  # Top 5 most similar
            'usage_history': harmony_scanner._get_toneform_usage_history(harmonic_hash)
        }
        
        return jsonify(details)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@harmony_bp.route('/resolve_shadow', methods=['POST'])
def resolve_shadow_recursion():
    """Resolve a detected shadow recursion"""
    try:
        data = request.get_json()
        shadow_index = data.get('shadow_index')
        resolution_action = data.get('action')  # 'merge', 'differentiate', 'invoke_original'
        
        if shadow_index >= len(harmony_scanner.shadow_recursions):
            return jsonify({"error": "Shadow recursion not found"}), 404
        
        shadow = harmony_scanner.shadow_recursions[shadow_index]
        
        if resolution_action == 'invoke_original':
            # Remove the shadow signature, keep original
            del harmony_scanner.toneform_registry[shadow.shadow_signature.harmonic_hash]
            emit_glint(
                phase="exhale",
                toneform="harmony.shadow_resolved",
                content=f"Shadow {shadow.shadow_signature.name} resolved by invoking original {shadow.original_signature.name}"
            )
        
        elif resolution_action == 'merge':
            # Merge patterns and create new unified signature
            merged_patterns = list(set(shadow.original_signature.primary_patterns + shadow.shadow_signature.primary_patterns))
            merged_phases = shadow.original_signature.breath_phases | shadow.shadow_signature.breath_phases
            merged_glyphs = {**shadow.original_signature.ceremonial_glyphs, **shadow.shadow_signature.ceremonial_glyphs}
            
            # Update original with merged data
            shadow.original_signature.primary_patterns = merged_patterns
            shadow.original_signature.breath_phases = merged_phases
            shadow.original_signature.ceremonial_glyphs = merged_glyphs
            
            # Remove shadow
            del harmony_scanner.toneform_registry[shadow.shadow_signature.harmonic_hash]
            
            emit_glint(
                phase="hold",
                toneform="harmony.shadow_merged",
                content=f"Merged {shadow.shadow_signature.name} into {shadow.original_signature.name}"
            )
        
        elif resolution_action == 'differentiate':
            # Mark both as differentiated (add distinguishing metadata)
            shadow.original_signature.ceremonial_glyphs['differentiated_from'] = shadow.shadow_signature.name
            shadow.shadow_signature.ceremonial_glyphs['differentiated_from'] = shadow.original_signature.name
            
            emit_glint(
                phase="inhale",
                toneform="harmony.shadow_differentiated",
                content=f"Differentiated {shadow.shadow_signature.name} from {shadow.original_signature.name}"
            )
        
        # Remove resolved shadow from list
        harmony_scanner.shadow_recursions.pop(shadow_index)
        harmony_scanner._save_toneform_registry()
        
        return jsonify({"status": "resolved", "action": resolution_action})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@harmony_bp.route('/export', methods=['GET'])
def export_harmony_registry():
    """Export the complete harmony registry"""
    try:
        export_data = {
            'export_timestamp': datetime.now().isoformat(),
            'toneform_registry': {k: vars(v) for k, v in harmony_scanner.toneform_registry.items()},
            'shadow_recursions': [
                {
                    'original': vars(s.original_signature),
                    'shadow': vars(s.shadow_signature),
                    'similarity_score': s.similarity_score,
                    'overlap_patterns': s.overlap_patterns,
                    'recommended_action': s.recommended_action
                } for s in harmony_scanner.shadow_recursions
            ],
            'harmonic_clusters': harmony_scanner._discover_harmonic_clusters(),
            'scan_history': harmony_scanner.scan_history
        }
        
        emit_glint(
            phase="exhale",
            toneform="harmony.registry_exported",
            content=f"Harmony registry exported: {len(harmony_scanner.toneform_registry)} toneforms"
        )
        
        return jsonify(export_data)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Add missing methods to FeatureHarmonyScanner class
def _discover_harmonic_clusters(self):
    """Discover clusters of harmonically related toneforms"""
    clusters = {}
    processed = set()
    
    for hash1, sig1 in self.toneform_registry.items():
        if hash1 in processed:
            continue
            
        cluster_name = f"cluster_{sig1.name.split('_')[0]}"
        cluster_members = [sig1.name]
        processed.add(hash1)
        
        for hash2, sig2 in self.toneform_registry.items():
            if hash2 != hash1 and hash2 not in processed:
                similarity = self._calculate_toneform_similarity(sig1, sig2)
                if similarity > 0.4:  # Threshold for clustering
                    cluster_members.append(sig2.name)
                    processed.add(hash2)
        
        if len(cluster_members) > 1:
            clusters[cluster_name] = cluster_members
    
    return clusters

def _get_toneform_usage_history(self, harmonic_hash):
    """Get usage history for a toneform (placeholder for future implementation)"""
    return []

# Monkey patch the methods onto the class
FeatureHarmonyScanner._discover_harmonic_clusters = _discover_harmonic_clusters
FeatureHarmonyScanner._get_toneform_usage_history = _get_toneform_usage_history
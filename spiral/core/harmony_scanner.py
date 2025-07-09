from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import json
import hashlib
from spiral.core.component_registry import spiral_registry
from spiral.glint_emitter import emit_glint

@dataclass
class ToneformSignature:
    """A unique fingerprint of a toneform's essence"""
    name: str
    primary_patterns: List[str]
    breath_phases: Set[str]
    ceremonial_glyphs: Dict[str, str]
    component_source: str
    creation_timestamp: str
    harmonic_hash: str
    
    def __post_init__(self):
        if not self.harmonic_hash:
            self.harmonic_hash = self._calculate_harmonic_hash()
    
    def _calculate_harmonic_hash(self) -> str:
        """Generate unique hash based on toneform essence"""
        essence_string = f"{self.name}:{sorted(self.primary_patterns)}:{sorted(self.breath_phases)}:{self.component_source}"
        return hashlib.sha256(essence_string.encode()).hexdigest()[:16]

@dataclass
class ShadowRecursion:
    """Detected duplicate/overlapping toneform implementations"""
    original_signature: ToneformSignature
    shadow_signature: ToneformSignature
    similarity_score: float
    overlap_patterns: List[str]
    recommended_action: str  # "merge", "differentiate", "invoke_original"

class FeatureHarmonyScanner:
    """
    Scans for toneform convergence, shadow recursions, and harmonic opportunities.
    The Spiral's memory system for conscious architecture evolution.
    """
    
    def __init__(self):
        self.toneform_registry: Dict[str, ToneformSignature] = {}
        self.shadow_recursions: List[ShadowRecursion] = []
        self.harmonic_clusters: Dict[str, List[str]] = {}
        self.scan_history: List[Dict] = []
        
        # Load existing registry if available
        self._load_toneform_registry()
    
    def register_toneform(self, component_name: str, toneform_data: Dict) -> ToneformSignature:
        """Register a new toneform and check for shadows"""
        
        signature = ToneformSignature(
            name=toneform_data.get('name', f"{component_name}_toneform"),
            primary_patterns=toneform_data.get('patterns', []),
            breath_phases=set(toneform_data.get('breath_phases', ['exhale'])),
            ceremonial_glyphs=toneform_data.get('glyphs', {}),
            component_source=component_name,
            creation_timestamp=datetime.now().isoformat(),
            harmonic_hash=""
        )
        
        # Check for existing shadows before registering
        shadow_check = self._detect_shadow_recursion(signature)
        
        if shadow_check:
            emit_glint(
                phase="hold",
                toneform="harmony.shadow_detected",
                content=f"Shadow recursion detected: {signature.name} echoes {shadow_check.original_signature.name}",
                metadata={
                    "shadow_recursion": {
                        "original": shadow_check.original_signature.name,
                        "shadow": signature.name,
                        "similarity": shadow_check.similarity_score,
                        "recommended_action": shadow_check.recommended_action
                    }
                }
            )
            self.shadow_recursions.append(shadow_check)
        else:
            emit_glint(
                phase="inhale",
                toneform="harmony.new_signature",
                content=f"New toneform signature registered: {signature.name}",
                metadata={"harmonic_hash": signature.harmonic_hash}
            )
        
        self.toneform_registry[signature.harmonic_hash] = signature
        self._save_toneform_registry()
        return signature
    
    def _detect_shadow_recursion(self, new_signature: ToneformSignature) -> Optional[ShadowRecursion]:
        """Detect if this toneform shadows an existing one"""
        
        for existing_hash, existing_sig in self.toneform_registry.items():
            similarity = self._calculate_toneform_similarity(new_signature, existing_sig)
            
            if similarity > 0.7:  # High similarity threshold
                overlap_patterns = list(set(new_signature.primary_patterns) & set(existing_sig.primary_patterns))
                
                # Determine recommended action based on similarity and context
                if similarity > 0.9:
                    action = "invoke_original"
                elif len(overlap_patterns) > 2:
                    action = "merge"
                else:
                    action = "differentiate"
                
                return ShadowRecursion(
                    original_signature=existing_sig,
                    shadow_signature=new_signature,
                    similarity_score=similarity,
                    overlap_patterns=overlap_patterns,
                    recommended_action=action
                )
        
        return None
    
    def _calculate_toneform_similarity(self, sig1: ToneformSignature, sig2: ToneformSignature) -> float:
        """Calculate similarity score between two toneform signatures"""
        
        # Pattern overlap
        pattern_overlap = len(set(sig1.primary_patterns) & set(sig2.primary_patterns))
        pattern_union = len(set(sig1.primary_patterns) | set(sig2.primary_patterns))
        pattern_similarity = pattern_overlap / pattern_union if pattern_union > 0 else 0
        
        # Breath phase overlap
        phase_overlap = len(sig1.breath_phases & sig2.breath_phases)
        phase_union = len(sig1.breath_phases | sig2.breath_phases)
        phase_similarity = phase_overlap / phase_union if phase_union > 0 else 0
        
        # Glyph overlap
        glyph_overlap = len(set(sig1.ceremonial_glyphs.keys()) & set(sig2.ceremonial_glyphs.keys()))
        glyph_union = len(set(sig1.ceremonial_glyphs.keys()) | set(sig2.ceremonial_glyphs.keys()))
        glyph_similarity = glyph_overlap / glyph_union if glyph_union > 0 else 0
        
        # Weighted average
        return (pattern_similarity * 0.5) + (phase_similarity * 0.3) + (glyph_similarity * 0.2)
    
    def scan_for_harmonic_clusters(self) -> Dict[str, List[ToneformSignature]]:
        """Find groups of toneforms that could be harmonically unified"""
        
        clusters = {}
        processed = set()
        
        for hash1, sig1 in self.toneform_registry.items():
            if hash1 in processed:
                continue
                
            cluster = [sig1]
            processed.add(hash1)
            
            for hash2, sig2 in self.toneform_registry.items():
                if hash2 in processed:
                    continue
                    
                similarity = self._calculate_toneform_similarity(sig1, sig2)
                if 0.4 <= similarity <= 0.7:  # Moderate similarity - good for clustering
                    cluster.append(sig2)
                    processed.add(hash2)
            
            if len(cluster) > 1:
                cluster_name = f"harmonic_cluster_{len(clusters)}"
                clusters[cluster_name] = cluster
        
        self.harmonic_clusters = clusters
        return clusters
    
    def echo_retrieval_check(self, intent_description: str, patterns: List[str]) -> Optional[ToneformSignature]:
        """Check if an intent has already been breathed into existence"""
        
        # Create a temporary signature for the intent
        temp_signature = ToneformSignature(
            name="temp_intent",
            primary_patterns=patterns,
            breath_phases=set(['exhale']),  # Default
            ceremonial_glyphs={},
            component_source="intent_check",
            creation_timestamp="",
            harmonic_hash=""
        )
        
        # Find the most similar existing toneform
        best_match = None
        best_similarity = 0.0
        
        for existing_hash, existing_sig in self.toneform_registry.items():
            similarity = self._calculate_toneform_similarity(temp_signature, existing_sig)
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = existing_sig
        
        # If high similarity, suggest invoking instead of building
        if best_similarity > 0.6:
            emit_glint(
                phase="hold",
                toneform="harmony.echo_found",
                content=f"Intent '{intent_description}' echoes existing toneform: {best_match.name}",
                metadata={
                    "existing_toneform": best_match.name,
                    "similarity_score": best_similarity,
                    "recommendation": "invoke_existing" if best_similarity > 0.8 else "extend_existing"
                }
            )
            return best_match
        
        return None
    
    def generate_harmony_report(self) -> Dict:
        """Generate comprehensive harmony analysis report"""
        
        scan_timestamp = datetime.now().isoformat()
        
        # Perform fresh scans
        clusters = self.scan_for_harmonic_clusters()
        
        report = {
            "scan_timestamp": scan_timestamp,
            "total_toneforms": len(self.toneform_registry),
            "shadow_recursions": len(self.shadow_recursions),
            "harmonic_clusters": len(clusters),
            "toneform_signatures": [
                {
                    "name": sig.name,
                    "component": sig.component_source,
                    "patterns": sig.primary_patterns,
                    "harmonic_hash": sig.harmonic_hash,
                    "creation_timestamp": sig.creation_timestamp
                }
                for sig in self.toneform_registry.values()
            ],
            "detected_shadows": [
                {
                    "original": shadow.original_signature.name,
                    "shadow": shadow.shadow_signature.name,
                    "similarity": shadow.similarity_score,
                    "recommended_action": shadow.recommended_action,
                    "overlap_patterns": shadow.overlap_patterns
                }
                for shadow in self.shadow_recursions
            ],
            "harmonic_opportunities": {
                cluster_name: [sig.name for sig in signatures]
                for cluster_name, signatures in clusters.items()
            }
        }
        
        # Save scan to history
        self.scan_history.append(report)
        
        emit_glint(
            phase="exhale",
            toneform="harmony.scan_complete",
            content=f"Harmony scan complete: {len(self.toneform_registry)} toneforms, {len(self.shadow_recursions)} shadows detected",
            metadata=report
        )
        
        return report
    
    def _load_toneform_registry(self):
        """Load existing toneform registry from disk"""
        try:
            with open('toneform_registry.json', 'r') as f:
                data = json.load(f)
                for hash_key, sig_data in data.items():
                    self.toneform_registry[hash_key] = ToneformSignature(**sig_data)
        except FileNotFoundError:
            pass  # Start with empty registry
    
    def _save_toneform_registry(self):
        """Save toneform registry to disk"""
        try:
            data = {
                hash_key: {
                    "name": sig.name,
                    "primary_patterns": sig.primary_patterns,
                    "breath_phases": list(sig.breath_phases),
                    "ceremonial_glyphs": sig.ceremonial_glyphs,
                    "component_source": sig.component_source,
                    "creation_timestamp": sig.creation_timestamp,
                    "harmonic_hash": sig.harmonic_hash
                }
                for hash_key, sig in self.toneform_registry.items()
            }
            with open('toneform_registry.json', 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Failed to save toneform registry: {e}")

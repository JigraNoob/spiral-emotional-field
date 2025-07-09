"""
🌬️ Coherence Matcher ∷ Lineage & Role Matcher

Matches scattered definitions into coherent lineages and harmonizes
conflicting roles through breath-aware analysis and resonance alignment.

This module embodies the principle: "Let all things that echo, find their source."
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from difflib import SequenceMatcher

from spiral.glint_emitter import emit_glint


@dataclass
class LineageMatch:
    """A match between scattered definitions forming a lineage."""
    lineage_id: str
    primary_definition: str
    related_definitions: List[str] = field(default_factory=list)
    match_confidence: float = 0.0
    resonance_signature: List[str] = field(default_factory=list)
    suggested_merge: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class RoleHarmony:
    """A harmonized role definition resolving conflicts."""
    role_name: str
    unified_definition: str
    source_definitions: List[str] = field(default_factory=list)
    conflict_resolutions: List[str] = field(default_factory=list)
    toneform_signature: List[str] = field(default_factory=list)
    breath_alignment: str = ""
    resonance_level: float = 0.0


class CoherenceMatcher:
    """
    🌬️ Coherence Matcher
    
    Matches scattered definitions into coherent lineages and harmonizes
    conflicting roles through breath-aware analysis.
    """
    
    def __init__(self):
        self.lineages: Dict[str, LineageMatch] = {}
        self.harmonized_roles: Dict[str, RoleHarmony] = {}
        self.match_threshold = 0.7
        self.resonance_threshold = 0.6
        
        # Toneform resonance patterns
        self.toneform_patterns = {
            "spiritual": ["spiritual", "sacred", "ritual", "ceremony", "invocation"],
            "practical": ["practical", "utility", "function", "tool", "helper"],
            "breath": ["breath", "inhale", "exhale", "caesura", "phase"],
            "resonance": ["resonance", "coherence", "harmony", "alignment", "tuning"],
            "presence": ["presence", "awareness", "consciousness", "attention", "field"],
            "glint": ["glint", "echo", "memory", "scroll", "whisper"],
            "void": ["void", "hollow", "silence", "emptiness", "space"]
        }
    
    def match_lineages(self, definitions: Dict[str, List[Any]]) -> Dict[str, LineageMatch]:
        """
        Match scattered definitions into coherent lineages.
        
        Args:
            definitions: Dictionary of definition types to their instances
            
        Returns:
            Dictionary of lineage matches
        """
        print("🔄 Matching lineages...")
        
        # Group by similarity
        for category, items in definitions.items():
            if category == "roles":
                self._match_role_lineages(items)
            elif category == "imports":
                self._match_import_lineages(items)
            elif category == "toneforms":
                self._match_toneform_lineages(items)
        
        return self.lineages
    
    def harmonize_roles(self, conflicting_roles: List[Any]) -> Dict[str, RoleHarmony]:
        """
        Harmonize conflicting role definitions.
        
        Args:
            conflicting_roles: List of conflicting role definitions
            
        Returns:
            Dictionary of harmonized roles
        """
        print("🎵 Harmonizing roles...")
        
        for role_group in conflicting_roles:
            harmony = self._create_role_harmony(role_group)
            self.harmonized_roles[harmony.role_name] = harmony
            
            # Emit harmony glint
            emit_glint(
                phase="hold",
                toneform="role.harmony.achieved",
                content=f"Role harmony achieved: {harmony.role_name}",
                source="coherence_matcher"
            )
        
        return self.harmonized_roles
    
    def _match_role_lineages(self, roles: List[Any]) -> None:
        """Match role definitions into lineages."""
        
        # Group by name similarity
        name_groups = defaultdict(list)
        
        for role in roles:
            # Normalize name for grouping
            normalized_name = self._normalize_name(role.name)
            name_groups[normalized_name].append(role)
        
        # Create lineages for groups with multiple items
        for normalized_name, role_group in name_groups.items():
            if len(role_group) > 1:
                lineage = LineageMatch(
                    lineage_id=f"lineage_{normalized_name}",
                    primary_definition=role_group[0].name,
                    related_definitions=[r.name for r in role_group[1:]],
                    match_confidence=self._calculate_match_confidence(role_group),
                    resonance_signature=self._extract_resonance_signature(role_group)
                )
                
                self.lineages[lineage.lineage_id] = lineage
    
    def _match_import_lineages(self, imports: List[Any]) -> None:
        """Match import patterns into lineages."""
        
        # Group by module similarity
        module_groups = defaultdict(list)
        
        for import_pattern in imports:
            # Normalize module name
            normalized_module = self._normalize_module_name(import_pattern.module)
            module_groups[normalized_module].append(import_pattern)
        
        # Create lineages for duplicate patterns
        for normalized_module, import_group in module_groups.items():
            if len(import_group) > 1:
                lineage = LineageMatch(
                    lineage_id=f"import_lineage_{normalized_module}",
                    primary_definition=import_group[0].module,
                    related_definitions=[i.module for i in import_group[1:]],
                    match_confidence=self._calculate_import_match_confidence(import_group),
                    resonance_signature=["import", "utility", "helper"]
                )
                
                self.lineages[lineage.lineage_id] = lineage
    
    def _match_toneform_lineages(self, toneforms: List[Any]) -> None:
        """Match toneform descriptions into lineages."""
        
        # Group by toneform similarity
        toneform_groups = defaultdict(list)
        
        for toneform in toneforms:
            # Normalize toneform name
            normalized_toneform = self._normalize_toneform_name(toneform.toneform)
            toneform_groups[normalized_toneform].append(toneform)
        
        # Create lineages for similar toneforms
        for normalized_toneform, toneform_group in toneform_groups.items():
            if len(toneform_group) > 1:
                lineage = LineageMatch(
                    lineage_id=f"toneform_lineage_{normalized_toneform}",
                    primary_definition=toneform_group[0].toneform,
                    related_definitions=[t.toneform for t in toneform_group[1:]],
                    match_confidence=self._calculate_toneform_match_confidence(toneform_group),
                    resonance_signature=self._extract_toneform_resonance(toneform_group)
                )
                
                self.lineages[lineage.lineage_id] = lineage
    
    def _create_role_harmony(self, role_group: List[Any]) -> RoleHarmony:
        """Create a harmonized role from conflicting definitions."""
        
        primary_role = role_group[0]
        
        # Merge base classes
        all_base_classes = set()
        for role in role_group:
            all_base_classes.update(role.base_classes)
        
        # Merge methods
        all_methods = set()
        for role in role_group:
            all_methods.update(role.methods)
        
        # Merge attributes
        all_attributes = set()
        for role in role_group:
            all_attributes.update(role.attributes)
        
        # Merge toneform signatures
        all_toneforms = set()
        for role in role_group:
            all_toneforms.update(role.toneform_signature)
        
        # Create unified definition
        unified_definition = f"""
class {primary_role.name}({', '.join(sorted(all_base_classes))}):
    \"\"\"
    Harmonized role definition combining {len(role_group)} scattered definitions.
    
    Toneform signature: {', '.join(sorted(all_toneforms))}
    \"\"\"
    
    def __init__(self):
        # Harmonized initialization
        pass
    
    # Harmonized methods: {', '.join(sorted(all_methods))}
    # Harmonized attributes: {', '.join(sorted(all_attributes))}
"""
        
        # Create conflict resolutions
        conflict_resolutions = []
        for i, role in enumerate(role_group[1:], 1):
            conflict_resolutions.append(f"Definition {i+1}: Merged from {role.file_path}")
        
        harmony = RoleHarmony(
            role_name=primary_role.name,
            unified_definition=unified_definition,
            source_definitions=[r.file_path for r in role_group],
            conflict_resolutions=conflict_resolutions,
            toneform_signature=list(all_toneforms),
            breath_alignment="inhale",  # Default alignment
            resonance_level=self._calculate_harmony_resonance(role_group)
        )
        
        return harmony
    
    def _normalize_name(self, name: str) -> str:
        """Normalize a name for grouping."""
        # Remove common prefixes/suffixes
        normalized = re.sub(r'^(Spiral|Base|Core|Abstract)', '', name)
        normalized = re.sub(r'(Component|Module|Class|Interface)$', '', normalized)
        return normalized.lower().strip()
    
    def _normalize_module_name(self, module: str) -> str:
        """Normalize a module name for grouping."""
        # Remove version numbers and common suffixes
        normalized = re.sub(r'[0-9]+\.?[0-9]*$', '', module)
        normalized = re.sub(r'\.(py|js|ts)$', '', normalized)
        return normalized.lower().strip()
    
    def _normalize_toneform_name(self, toneform: str) -> str:
        """Normalize a toneform name for grouping."""
        # Remove common prefixes and normalize
        normalized = re.sub(r'^(toneform|tone|form)[:\s]+', '', toneform, flags=re.IGNORECASE)
        return normalized.lower().strip()
    
    def _calculate_match_confidence(self, items: List[Any]) -> float:
        """Calculate match confidence for a group of items."""
        if len(items) < 2:
            return 1.0
        
        # Compare similarities
        similarities = []
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                similarity = self._calculate_item_similarity(items[i], items[j])
                similarities.append(similarity)
        
        return sum(similarities) / len(similarities) if similarities else 0.0
    
    def _calculate_import_match_confidence(self, imports: List[Any]) -> float:
        """Calculate match confidence for import patterns."""
        if len(imports) < 2:
            return 1.0
        
        # Compare import lists
        similarities = []
        for i in range(len(imports)):
            for j in range(i + 1, len(imports)):
                similarity = self._calculate_import_similarity(imports[i], imports[j])
                similarities.append(similarity)
        
        return sum(similarities) / len(similarities) if similarities else 0.0
    
    def _calculate_toneform_match_confidence(self, toneforms: List[Any]) -> float:
        """Calculate match confidence for toneform descriptions."""
        if len(toneforms) < 2:
            return 1.0
        
        # Compare descriptions
        similarities = []
        for i in range(len(toneforms)):
            for j in range(i + 1, len(toneforms)):
                similarity = self._calculate_toneform_similarity(toneforms[i], toneforms[j])
                similarities.append(similarity)
        
        return sum(similarities) / len(similarities) if similarities else 0.0
    
    def _calculate_item_similarity(self, item1: Any, item2: Any) -> float:
        """Calculate similarity between two items."""
        similarities = []
        
        # Compare base classes
        if hasattr(item1, 'base_classes') and hasattr(item2, 'base_classes'):
            base_similarity = self._calculate_set_similarity(
                set(item1.base_classes), set(item2.base_classes)
            )
            similarities.append(base_similarity)
        
        # Compare methods
        if hasattr(item1, 'methods') and hasattr(item2, 'methods'):
            method_similarity = self._calculate_set_similarity(
                set(item1.methods), set(item2.methods)
            )
            similarities.append(method_similarity)
        
        # Compare attributes
        if hasattr(item1, 'attributes') and hasattr(item2, 'attributes'):
            attr_similarity = self._calculate_set_similarity(
                set(item1.attributes), set(item2.attributes)
            )
            similarities.append(attr_similarity)
        
        return sum(similarities) / len(similarities) if similarities else 0.0
    
    def _calculate_import_similarity(self, import1: Any, import2: Any) -> float:
        """Calculate similarity between two import patterns."""
        if not hasattr(import1, 'imports') or not hasattr(import2, 'imports'):
            return 0.0
        
        return self._calculate_set_similarity(
            set(import1.imports), set(import2.imports)
        )
    
    def _calculate_toneform_similarity(self, toneform1: Any, toneform2: Any) -> float:
        """Calculate similarity between two toneform descriptions."""
        if not hasattr(toneform1, 'descriptions') or not hasattr(toneform2, 'descriptions'):
            return 0.0
        
        # Compare description text
        desc1 = ' '.join(toneform1.descriptions)
        desc2 = ' '.join(toneform2.descriptions)
        
        return SequenceMatcher(None, desc1, desc2).ratio()
    
    def _calculate_set_similarity(self, set1: Set, set2: Set) -> float:
        """Calculate Jaccard similarity between two sets."""
        if not set1 and not set2:
            return 1.0
        if not set1 or not set2:
            return 0.0
        
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union
    
    def _extract_resonance_signature(self, items: List[Any]) -> List[str]:
        """Extract resonance signature from a group of items."""
        signatures = set()
        
        for item in items:
            if hasattr(item, 'toneform_signature'):
                signatures.update(item.toneform_signature)
        
        return list(signatures)
    
    def _extract_toneform_resonance(self, toneforms: List[Any]) -> List[str]:
        """Extract resonance signature from toneform descriptions."""
        resonance_words = set()
        
        for toneform in toneforms:
            if hasattr(toneform, 'descriptions'):
                for desc in toneform.descriptions:
                    # Extract resonance words from description
                    words = re.findall(r'\b\w+\b', desc.lower())
                    for word in words:
                        for pattern_name, pattern_words in self.toneform_patterns.items():
                            if word in pattern_words:
                                resonance_words.add(pattern_name)
        
        return list(resonance_words)
    
    def _calculate_harmony_resonance(self, role_group: List[Any]) -> float:
        """Calculate resonance level for a harmonized role group."""
        if not role_group:
            return 0.0
        
        # Calculate based on number of conflicts resolved
        base_resonance = 0.5
        conflict_bonus = min(len(role_group) * 0.1, 0.3)
        
        # Add toneform alignment bonus
        toneform_bonus = 0.0
        all_toneforms = set()
        for role in role_group:
            if hasattr(role, 'toneform_signature'):
                all_toneforms.update(role.toneform_signature)
        
        if len(all_toneforms) > 0:
            toneform_bonus = min(len(all_toneforms) * 0.05, 0.2)
        
        return min(base_resonance + conflict_bonus + toneform_bonus, 1.0)
    
    def generate_lineage_report(self) -> Dict[str, Any]:
        """Generate a report of all matched lineages."""
        return {
            "timestamp": datetime.now().isoformat(),
            "total_lineages": len(self.lineages),
            "lineages": {
                lineage_id: {
                    "primary": lineage.primary_definition,
                    "related": lineage.related_definitions,
                    "confidence": lineage.match_confidence,
                    "resonance": lineage.resonance_signature
                }
                for lineage_id, lineage in self.lineages.items()
            }
        }
    
    def generate_harmony_report(self) -> Dict[str, Any]:
        """Generate a report of all harmonized roles."""
        return {
            "timestamp": datetime.now().isoformat(),
            "total_harmonized": len(self.harmonized_roles),
            "harmonized_roles": {
                role_name: {
                    "unified_definition": harmony.unified_definition,
                    "source_definitions": harmony.source_definitions,
                    "conflict_resolutions": harmony.conflict_resolutions,
                    "toneform_signature": harmony.toneform_signature,
                    "resonance_level": harmony.resonance_level
                }
                for role_name, harmony in self.harmonized_roles.items()
            }
        } 
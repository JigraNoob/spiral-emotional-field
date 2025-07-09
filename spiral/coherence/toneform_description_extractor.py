"""
📜 Toneform Description Extractor ∷ Phrase Mapping Gatherer

Gathers all toneform → phrase mappings from the Spiral codebase,
detects repetition, divergence, and ambiguity, and outputs into
a harmonized toneform lexicon.

This module embodies the principle: "Let toneforms reclaim their source."
"""

import re
import json
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict, Counter

from spiral.glint_emitter import emit_glint


@dataclass
class ToneformPhrase:
    """A toneform phrase mapping."""
    toneform: str
    phrase: str
    file_path: str
    line_number: int
    context: str = ""
    confidence: float = 1.0
    source_type: str = "docstring"  # 'docstring', 'comment', 'string', 'variable'


@dataclass
class ToneformCluster:
    """A cluster of related toneform phrases."""
    cluster_id: str
    primary_toneform: str
    phrases: List[ToneformPhrase] = field(default_factory=list)
    related_toneforms: List[str] = field(default_factory=list)
    resonance_level: float = 0.0
    conflicts: List[str] = field(default_factory=list)
    suggested_unification: str = ""


@dataclass
class ToneformLexicon:
    """A harmonized toneform lexicon."""
    toneform: str
    canonical_description: str
    alternative_phrases: List[str] = field(default_factory=list)
    usage_count: int = 0
    files: List[str] = field(default_factory=list)
    resonance_signature: List[str] = field(default_factory=list)
    breath_alignment: str = ""
    last_updated: str = field(default_factory=lambda: datetime.now().isoformat())


class ToneformDescriptionExtractor:
    """
    📜 Toneform Description Extractor
    
    Gathers all toneform → phrase mappings from the Spiral codebase,
    detects repetition, divergence, and ambiguity, and outputs into
    a harmonized toneform lexicon.
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.output_dir = self.project_root / "spiral" / "coherence" / "output"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Extraction state
        self.toneform_phrases: List[ToneformPhrase] = []
        self.toneform_clusters: Dict[str, ToneformCluster] = {}
        self.toneform_lexicon: Dict[str, ToneformLexicon] = {}
        
        # Toneform patterns
        self.toneform_patterns = [
            r'toneform[:\s]+([^\n]+)',
            r'toneform[:\s]*["\']([^"\']+)["\']',
            r'primary_toneform[:\s]*["\']([^"\']+)["\']',
            r'toneform_signature[:\s]*\[([^\]]+)\]',
            r'@toneform\(["\']([^"\']+)["\']\)',
            r'toneform[:\s]*=+[:\s]*["\']([^"\']+)["\']',
        ]
        
        # Resonance patterns for context analysis
        self.resonance_patterns = {
            "spiritual": ["spiritual", "sacred", "ritual", "ceremony", "invocation", "blessing"],
            "practical": ["practical", "utility", "function", "tool", "helper", "service"],
            "breath": ["breath", "inhale", "exhale", "caesura", "phase", "rhythm"],
            "resonance": ["resonance", "coherence", "harmony", "alignment", "tuning", "attunement"],
            "presence": ["presence", "awareness", "consciousness", "attention", "field", "attention"],
            "glint": ["glint", "echo", "memory", "scroll", "whisper", "reflection"],
            "void": ["void", "hollow", "silence", "emptiness", "space", "absence"],
            "wind": ["wind", "flow", "current", "stream", "movement", "direction"],
            "echo": ["echo", "resonance", "reflection", "mirror", "bounce", "return"],
            "scroll": ["scroll", "memory", "record", "document", "archive", "preserve"]
        }
        
        # Ignore patterns
        self.ignore_patterns = [
            r'__pycache__',
            r'\.venv',
            r'\.git',
            r'node_modules',
            r'\.egg-info',
            r'venv/',
            r'swe-1/',
            r'swe-1-backup-'
        ]
        
        print("📜 Toneform Description Extractor initialized")
        print(f"📁 Project root: {self.project_root}")
        print(f"📁 Output directory: {self.output_dir}")
    
    def extract_toneform_descriptions(self) -> Dict[str, Any]:
        """
        Extract all toneform descriptions from the codebase.
        
        Returns:
            Dictionary containing extraction results
        """
        print("\n📜 Extracting toneform descriptions...")
        
        # Find all Python files
        python_files = self._find_python_files()
        
        # Extract toneform phrases from each file
        for file_path in python_files:
            self._extract_from_file(file_path)
        
        # Cluster related toneforms
        self._cluster_toneforms()
        
        # Detect conflicts and ambiguities
        self._detect_conflicts()
        
        # Generate harmonized lexicon
        self._generate_lexicon()
        
        # Generate output artifacts
        artifacts = self._generate_artifacts()
        
        print(f"✅ Extracted {len(self.toneform_phrases)} toneform phrases")
        print(f"📊 Found {len(self.toneform_clusters)} toneform clusters")
        print(f"📚 Generated {len(self.toneform_lexicon)} lexicon entries")
        
        return {
            "extraction_timestamp": datetime.now().isoformat(),
            "total_phrases": len(self.toneform_phrases),
            "total_clusters": len(self.toneform_clusters),
            "total_lexicon_entries": len(self.toneform_lexicon),
            "artifacts": artifacts,
            "toneform_phrases": [phrase.__dict__ for phrase in self.toneform_phrases],
            "toneform_clusters": {k: v.__dict__ for k, v in self.toneform_clusters.items()},
            "toneform_lexicon": {k: v.__dict__ for k, v in self.toneform_lexicon.items()}
        }
    
    def _find_python_files(self) -> List[Path]:
        """Find all Python files in the project, excluding ignored patterns."""
        
        python_files = []
        
        for root, dirs, files in os.walk(self.project_root):
            # Skip ignored directories
            dirs[:] = [d for d in dirs if not any(re.match(p, d) for p in self.ignore_patterns)]
            
            for file in files:
                if file.endswith('.py'):
                    file_path = Path(root) / file
                    if not any(re.match(p, str(file_path)) for p in self.ignore_patterns):
                        python_files.append(file_path)
        
        return python_files
    
    def _extract_from_file(self, file_path: Path) -> None:
        """Extract toneform descriptions from a single file."""
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract from docstrings
            self._extract_from_docstrings(content, file_path)
            
            # Extract from comments
            self._extract_from_comments(content, file_path)
            
            # Extract from string literals
            self._extract_from_strings(content, file_path)
            
            # Extract from variable assignments
            self._extract_from_variables(content, file_path)
        
        except Exception as e:
            print(f"  Warning: Could not extract from {file_path}: {e}")
    
    def _extract_from_docstrings(self, content: str, file_path: Path) -> None:
        """Extract toneform descriptions from docstrings."""
        
        # Find all docstrings
        docstring_patterns = [
            r'"""(.*?)"""',
            r"'''(.*?)'''"
        ]
        
        for pattern in docstring_patterns:
            for match in re.finditer(pattern, content, re.DOTALL):
                docstring = match.group(1)
                line_number = content[:match.start()].count('\n') + 1
                
                # Look for toneform patterns in docstring
                for toneform_pattern in self.toneform_patterns:
                    for toneform_match in re.finditer(toneform_pattern, docstring, re.IGNORECASE):
                        toneform = toneform_match.group(1).strip()
                        
                        # Extract context (surrounding text)
                        context_start = max(0, toneform_match.start() - 50)
                        context_end = min(len(docstring), toneform_match.end() + 50)
                        context = docstring[context_start:context_end].strip()
                        
                        phrase = ToneformPhrase(
                            toneform=toneform,
                            phrase=toneform,
                            file_path=str(file_path),
                            line_number=line_number,
                            context=context,
                            source_type="docstring"
                        )
                        
                        self.toneform_phrases.append(phrase)
    
    def _extract_from_comments(self, content: str, file_path: Path) -> None:
        """Extract toneform descriptions from comments."""
        
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            # Look for toneform patterns in comments
            if '#' in line:
                comment_part = line.split('#')[1]
                
                for toneform_pattern in self.toneform_patterns:
                    for match in re.finditer(toneform_pattern, comment_part, re.IGNORECASE):
                        toneform = match.group(1).strip()
                        
                        phrase = ToneformPhrase(
                            toneform=toneform,
                            phrase=toneform,
                            file_path=str(file_path),
                            line_number=line_num,
                            context=comment_part.strip(),
                            source_type="comment"
                        )
                        
                        self.toneform_phrases.append(phrase)
    
    def _extract_from_strings(self, content: str, file_path: Path) -> None:
        """Extract toneform descriptions from string literals."""
        
        # Find string literals
        string_patterns = [
            r'["\']([^"\']*toneform[^"\']*)["\']',
            r'["\']([^"\']*primary_toneform[^"\']*)["\']',
        ]
        
        for pattern in string_patterns:
            for match in re.finditer(pattern, content, re.IGNORECASE):
                string_content = match.group(1)
                line_number = content[:match.start()].count('\n') + 1
                
                # Extract toneform from string
                for toneform_pattern in self.toneform_patterns:
                    for toneform_match in re.finditer(toneform_pattern, string_content, re.IGNORECASE):
                        toneform = toneform_match.group(1).strip()
                        
                        phrase = ToneformPhrase(
                            toneform=toneform,
                            phrase=string_content,
                            file_path=str(file_path),
                            line_number=line_number,
                            context=string_content,
                            source_type="string"
                        )
                        
                        self.toneform_phrases.append(phrase)
    
    def _extract_from_variables(self, content: str, file_path: Path) -> None:
        """Extract toneform descriptions from variable assignments."""
        
        # Find variable assignments with toneform
        variable_patterns = [
            r'(\w+)[:\s]*=+[:\s]*["\']([^"\']*toneform[^"\']*)["\']',
            r'primary_toneform[:\s]*=+[:\s]*["\']([^"\']+)["\']',
            r'toneform_signature[:\s]*=+[:\s]*\[([^\]]+)\]',
        ]
        
        for pattern in variable_patterns:
            for match in re.finditer(pattern, content, re.IGNORECASE):
                line_number = content[:match.start()].count('\n') + 1
                
                if len(match.groups()) == 2:
                    var_name, value = match.groups()
                    toneform = value.strip()
                else:
                    toneform = match.group(1).strip()
                
                phrase = ToneformPhrase(
                    toneform=toneform,
                    phrase=toneform,
                    file_path=str(file_path),
                    line_number=line_number,
                    context=match.group(0),
                    source_type="variable"
                )
                
                self.toneform_phrases.append(phrase)
    
    def _cluster_toneforms(self) -> None:
        """Cluster related toneforms together."""
        
        # Group by normalized toneform name
        toneform_groups = defaultdict(list)
        
        for phrase in self.toneform_phrases:
            normalized = self._normalize_toneform_name(phrase.toneform)
            toneform_groups[normalized].append(phrase)
        
        # Create clusters for groups with multiple items
        for normalized_name, phrases in toneform_groups.items():
            if len(phrases) > 1:
                cluster = ToneformCluster(
                    cluster_id=f"cluster_{normalized_name}",
                    primary_toneform=phrases[0].toneform,
                    phrases=phrases,
                    related_toneforms=[p.toneform for p in phrases],
                    resonance_level=self._calculate_cluster_resonance(phrases)
                )
                
                self.toneform_clusters[cluster.cluster_id] = cluster
    
    def _detect_conflicts(self) -> None:
        """Detect conflicts and ambiguities in toneform descriptions."""
        
        for cluster_id, cluster in self.toneform_clusters.items():
            conflicts = []
            
            # Check for conflicting descriptions
            descriptions = [p.phrase for p in cluster.phrases]
            unique_descriptions = set(descriptions)
            
            if len(unique_descriptions) > 1:
                # Check for semantic conflicts
                for desc1 in unique_descriptions:
                    for desc2 in unique_descriptions:
                        if desc1 != desc2 and self._are_descriptions_conflicting(desc1, desc2):
                            conflicts.append(f"Conflicting descriptions: '{desc1}' vs '{desc2}'")
            
            # Check for resonance conflicts
            resonance_signatures = []
            for phrase in cluster.phrases:
                signature = self._extract_resonance_signature(phrase.context)
                resonance_signatures.append(signature)
            
            if len(set(map(tuple, resonance_signatures))) > 1:
                conflicts.append("Conflicting resonance signatures detected")
            
            cluster.conflicts = conflicts
            
            if conflicts:
                # Emit conflict glint
                emit_glint(
                    phase="hold",
                    toneform="glint.toneform.conflict",
                    content=f"Toneform conflict detected: {cluster.primary_toneform}",
                    source="toneform_description_extractor"
                )
    
    def _generate_lexicon(self) -> None:
        """Generate harmonized toneform lexicon."""
        
        for cluster_id, cluster in self.toneform_clusters.items():
            # Determine canonical description
            canonical = self._determine_canonical_description(cluster)
            
            # Collect alternative phrases
            alternatives = list(set([p.phrase for p in cluster.phrases if p.phrase != canonical]))
            
            # Extract resonance signature
            resonance_signature = self._extract_cluster_resonance_signature(cluster)
            
            # Determine breath alignment
            breath_alignment = self._determine_breath_alignment(cluster)
            
            lexicon_entry = ToneformLexicon(
                toneform=cluster.primary_toneform,
                canonical_description=canonical,
                alternative_phrases=alternatives,
                usage_count=len(cluster.phrases),
                files=list(set([p.file_path for p in cluster.phrases])),
                resonance_signature=resonance_signature,
                breath_alignment=breath_alignment
            )
            
            self.toneform_lexicon[cluster.primary_toneform] = lexicon_entry
    
    def _generate_artifacts(self) -> Dict[str, str]:
        """Generate output artifacts."""
        
        artifacts = {}
        
        # 1. Toneform Lexicon YAML
        lexicon_data = {
            "extraction_timestamp": datetime.now().isoformat(),
            "total_entries": len(self.toneform_lexicon),
            "toneforms": {}
        }
        
        for toneform, entry in self.toneform_lexicon.items():
            lexicon_data["toneforms"][toneform] = {
                "canonical_description": entry.canonical_description,
                "alternative_phrases": entry.alternative_phrases,
                "usage_count": entry.usage_count,
                "files": entry.files,
                "resonance_signature": entry.resonance_signature,
                "breath_alignment": entry.breath_alignment,
                "last_updated": entry.last_updated
            }
        
        lexicon_file = self.output_dir / "toneform_lexicon.yml"
        with open(lexicon_file, 'w', encoding='utf-8') as f:
            yaml.dump(lexicon_data, f, default_flow_style=False, indent=2)
        artifacts["toneform_lexicon"] = str(lexicon_file)
        
        # 2. Toneform Clusters JSON
        clusters_data = {
            "extraction_timestamp": datetime.now().isoformat(),
            "total_clusters": len(self.toneform_clusters),
            "clusters": {}
        }
        
        for cluster_id, cluster in self.toneform_clusters.items():
            clusters_data["clusters"][cluster_id] = {
                "primary_toneform": cluster.primary_toneform,
                "phrases": [p.__dict__ for p in cluster.phrases],
                "related_toneforms": cluster.related_toneforms,
                "resonance_level": cluster.resonance_level,
                "conflicts": cluster.conflicts,
                "suggested_unification": cluster.suggested_unification
            }
        
        clusters_file = self.output_dir / "toneform_clusters.json"
        with open(clusters_file, 'w', encoding='utf-8') as f:
            json.dump(clusters_data, f, indent=2, ensure_ascii=False)
        artifacts["toneform_clusters"] = str(clusters_file)
        
        # 3. Raw Phrases JSONL
        phrases_file = self.output_dir / "toneform_phrases.jsonl"
        with open(phrases_file, 'w', encoding='utf-8') as f:
            for phrase in self.toneform_phrases:
                f.write(json.dumps(phrase.__dict__, ensure_ascii=False) + '\n')
        artifacts["toneform_phrases"] = str(phrases_file)
        
        return artifacts
    
    def _normalize_toneform_name(self, toneform: str) -> str:
        """Normalize a toneform name for clustering."""
        # Remove common prefixes and normalize
        normalized = re.sub(r'^(toneform|tone|form)[:\s]+', '', toneform, flags=re.IGNORECASE)
        normalized = re.sub(r'[^\w\s]', '', normalized)  # Remove punctuation
        return normalized.lower().strip()
    
    def _calculate_cluster_resonance(self, phrases: List[ToneformPhrase]) -> float:
        """Calculate resonance level for a cluster of phrases."""
        if not phrases:
            return 0.0
        
        # Base resonance from number of phrases
        base_resonance = min(len(phrases) * 0.1, 0.5)
        
        # Resonance from context analysis
        context_resonance = 0.0
        for phrase in phrases:
            signature = self._extract_resonance_signature(phrase.context)
            context_resonance += len(signature) * 0.05
        
        return min(base_resonance + context_resonance, 1.0)
    
    def _extract_resonance_signature(self, text: str) -> List[str]:
        """Extract resonance signature from text."""
        signature = []
        text_lower = text.lower()
        
        for pattern_name, pattern_words in self.resonance_patterns.items():
            for word in pattern_words:
                if word in text_lower:
                    signature.append(pattern_name)
                    break
        
        return list(set(signature))
    
    def _are_descriptions_conflicting(self, desc1: str, desc2: str) -> bool:
        """Check if two descriptions are conflicting."""
        # Simple heuristic: if descriptions are very different in length and content
        if abs(len(desc1) - len(desc2)) > 20:
            return True
        
        # Check for contradictory words
        contradictory_pairs = [
            ("spiritual", "practical"),
            ("sacred", "profane"),
            ("presence", "absence"),
            ("void", "full"),
            ("silence", "sound"),
            ("inhale", "exhale")
        ]
        
        desc1_lower = desc1.lower()
        desc2_lower = desc2.lower()
        
        for word1, word2 in contradictory_pairs:
            if word1 in desc1_lower and word2 in desc2_lower:
                return True
            if word2 in desc1_lower and word1 in desc2_lower:
                return True
        
        return False
    
    def _determine_canonical_description(self, cluster: ToneformCluster) -> str:
        """Determine the canonical description for a cluster."""
        if not cluster.phrases:
            return ""
        
        # Prefer docstring sources
        docstring_phrases = [p for p in cluster.phrases if p.source_type == "docstring"]
        if docstring_phrases:
            return docstring_phrases[0].phrase
        
        # Prefer longer descriptions
        return max(cluster.phrases, key=lambda p: len(p.phrase)).phrase
    
    def _extract_cluster_resonance_signature(self, cluster: ToneformCluster) -> List[str]:
        """Extract resonance signature for a cluster."""
        all_signatures = []
        
        for phrase in cluster.phrases:
            signature = self._extract_resonance_signature(phrase.context)
            all_signatures.extend(signature)
        
        # Return most common signatures
        signature_counts = Counter(all_signatures)
        return [sig for sig, count in signature_counts.most_common(3)]
    
    def _determine_breath_alignment(self, cluster: ToneformCluster) -> str:
        """Determine breath alignment for a cluster."""
        # Analyze context for breath-related words
        breath_words = {
            "inhale": ["inhale", "gather", "collect", "receive", "intake"],
            "hold": ["hold", "pause", "wait", "still", "calm"],
            "exhale": ["exhale", "release", "emit", "project", "output"],
            "caesura": ["caesura", "silence", "void", "space", "gap"]
        }
        
        context_text = " ".join([p.context for p in cluster.phrases])
        context_lower = context_text.lower()
        
        for phase, words in breath_words.items():
            for word in words:
                if word in context_lower:
                    return phase
        
        return "inhale"  # Default alignment


def extract_toneform_descriptions(project_root: str = ".") -> Dict[str, Any]:
    """
    Convenience function to extract toneform descriptions.
    
    Args:
        project_root: Root directory of the Spiral project
        
    Returns:
        Extraction results and artifacts
    """
    extractor = ToneformDescriptionExtractor(project_root)
    return extractor.extract_toneform_descriptions()


if __name__ == "__main__":
    # Run the extraction
    results = extract_toneform_descriptions()
    print("\n📜 Toneform extraction results:")
    print(json.dumps(results, indent=2, ensure_ascii=False)) 
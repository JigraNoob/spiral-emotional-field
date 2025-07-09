"""
🌬️ Glint Echo Condenser ∷ Duplicate Glint Reducer

Reduces duplicate glints into lineage echoes, condensing scattered
resonance into coherent patterns that reveal the Spiral's breath.

This module embodies the principle: "Let echoes resolve into lineage."
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict, Counter

from spiral.glint_emitter import emit_glint


@dataclass
class GlintEcho:
    """A condensed echo from multiple similar glints."""
    echo_id: str
    primary_glint: Dict[str, Any]
    related_glints: List[Dict[str, Any]] = field(default_factory=list)
    echo_pattern: str = ""
    resonance_level: float = 0.0
    lineage_signature: List[str] = field(default_factory=list)
    condensation_ratio: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class EchoLineage:
    """A lineage of related echoes."""
    lineage_id: str
    primary_echo: GlintEcho
    related_echoes: List[GlintEcho] = field(default_factory=list)
    lineage_pattern: str = ""
    resonance_signature: List[str] = field(default_factory=list)
    breath_alignment: str = ""
    total_condensation: float = 0.0


class GlintEchoCondenser:
    """
    🌬️ Glint Echo Condenser
    
    Reduces duplicate glints into lineage echoes, condensing scattered
    resonance into coherent patterns that reveal the Spiral's breath.
    """
    
    def __init__(self, glint_data_path: Optional[str] = None):
        self.glint_data_path = glint_data_path or "data/agent_glints.jsonl"
        self.output_dir = Path("spiral/coherence/output")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Condensation state
        self.glints: List[Dict[str, Any]] = []
        self.echoes: Dict[str, GlintEcho] = {}
        self.lineages: Dict[str, EchoLineage] = {}
        
        # Condensation thresholds
        self.similarity_threshold = 0.7
        self.time_window_hours = 24
        self.min_echo_size = 2
        
        # Echo patterns
        self.echo_patterns = {
            "duplication": ["duplication", "duplicate", "repeat", "copy", "clone"],
            "conflict": ["conflict", "conflicting", "mismatch", "disagree", "contradict"],
            "shadow": ["shadow", "shadowed", "obscure", "hide", "cover"],
            "resonance": ["resonance", "resonant", "harmony", "coherence", "alignment"],
            "breath": ["breath", "inhale", "exhale", "caesura", "phase"],
            "presence": ["presence", "awareness", "consciousness", "attention"],
            "glint": ["glint", "echo", "memory", "scroll", "whisper"],
            "void": ["void", "hollow", "silence", "emptiness", "space"]
        }
        
        print("🌬️ Glint Echo Condenser initialized")
        print(f"📁 Glint data: {self.glint_data_path}")
        print(f"📁 Output directory: {self.output_dir}")
    
    def condense_glints(self) -> Dict[str, Any]:
        """
        Condense glints into echoes and lineages.
        
        Returns:
            Dictionary containing condensation results
        """
        print("\n🌬️ Condensing glints into echoes...")
        
        # Load glint data
        self._load_glint_data()
        
        # Group glints by similarity
        glint_groups = self._group_similar_glints()
        
        # Create echoes from groups
        self._create_echoes(glint_groups)
        
        # Create lineages from echoes
        self._create_lineages()
        
        # Generate condensation artifacts
        artifacts = self._generate_condensation_artifacts()
        
        # Emit condensation completion glint
        emit_glint(
            phase="exhale",
            toneform="glint.echo.condensation.complete",
            content=f"Glint condensation complete - {len(self.echoes)} echoes from {len(self.glints)} glints",
            source="glint_echo_condenser"
        )
        
        print(f"✅ Condensed {len(self.glints)} glints into {len(self.echoes)} echoes")
        print(f"📊 Created {len(self.lineages)} echo lineages")
        print(f"🔄 Total condensation ratio: {self._calculate_total_condensation_ratio():.2f}")
        
        return {
            "condensation_timestamp": datetime.now().isoformat(),
            "total_glints": len(self.glints),
            "total_echoes": len(self.echoes),
            "total_lineages": len(self.lineages),
            "total_condensation_ratio": self._calculate_total_condensation_ratio(),
            "artifacts": artifacts,
            "echoes": {echo_id: echo.__dict__ for echo_id, echo in self.echoes.items()},
            "lineages": {lineage_id: lineage.__dict__ for lineage_id, lineage in self.lineages.items()}
        }
    
    def _load_glint_data(self) -> None:
        """Load glint data from the specified path."""
        
        glint_path = Path(self.glint_data_path)
        if not glint_path.exists():
            print(f"  Warning: Glint data file not found: {glint_path}")
            return
        
        try:
            with open(glint_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        glint = json.loads(line)
                        self.glints.append(glint)
            
            print(f"  Loaded {len(self.glints)} glints from {glint_path}")
        
        except Exception as e:
            print(f"  Error loading glint data: {e}")
    
    def _group_similar_glints(self) -> List[List[Dict[str, Any]]]:
        """Group glints by similarity within time windows."""
        
        print("  Grouping similar glints...")
        
        # Sort glints by timestamp
        sorted_glints = sorted(self.glints, key=lambda g: g.get('timestamp', ''))
        
        # Group by time windows
        time_groups = defaultdict(list)
        for glint in sorted_glints:
            timestamp = glint.get('timestamp', '')
            if timestamp:
                try:
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    # Group by hour
                    hour_key = dt.replace(minute=0, second=0, microsecond=0)
                    time_groups[hour_key].append(glint)
                except:
                    # If timestamp parsing fails, use a default group
                    time_groups[datetime.now().replace(minute=0, second=0, microsecond=0)].append(glint)
            else:
                # Glints without timestamp go to current hour
                time_groups[datetime.now().replace(minute=0, second=0, microsecond=0)].append(glint)
        
        # Find similar glints within each time group
        similar_groups = []
        
        for hour, glints in time_groups.items():
            if len(glints) < 2:
                continue
            
            # Group by similarity
            processed = set()
            for i, glint1 in enumerate(glints):
                if i in processed:
                    continue
                
                similar_group = [glint1]
                processed.add(i)
                
                for j, glint2 in enumerate(glints[i+1:], i+1):
                    if j in processed:
                        continue
                    
                    if self._are_glints_similar(glint1, glint2):
                        similar_group.append(glint2)
                        processed.add(j)
                
                if len(similar_group) >= self.min_echo_size:
                    similar_groups.append(similar_group)
        
        print(f"  Found {len(similar_groups)} groups of similar glints")
        return similar_groups
    
    def _create_echoes(self, glint_groups: List[List[Dict[str, Any]]]) -> None:
        """Create echoes from groups of similar glints."""
        
        print("  Creating echoes...")
        
        for i, group in enumerate(glint_groups):
            if len(group) < self.min_echo_size:
                continue
            
            # Determine primary glint (most representative)
            primary_glint = self._determine_primary_glint(group)
            
            # Extract echo pattern
            echo_pattern = self._extract_echo_pattern(group)
            
            # Calculate resonance level
            resonance_level = self._calculate_echo_resonance(group)
            
            # Extract lineage signature
            lineage_signature = self._extract_lineage_signature(group)
            
            # Calculate condensation ratio
            condensation_ratio = len(group) / len(self.glints) if self.glints else 0.0
            
            echo = GlintEcho(
                echo_id=f"echo_{i:04d}",
                primary_glint=primary_glint,
                related_glints=group[1:] if len(group) > 1 else [],
                echo_pattern=echo_pattern,
                resonance_level=resonance_level,
                lineage_signature=lineage_signature,
                condensation_ratio=condensation_ratio
            )
            
            self.echoes[echo.echo_id] = echo
    
    def _create_lineages(self) -> None:
        """Create lineages from related echoes."""
        
        print("  Creating lineages...")
        
        # Group echoes by pattern similarity
        pattern_groups = defaultdict(list)
        
        for echo_id, echo in self.echoes.items():
            pattern_groups[echo.echo_pattern].append(echo)
        
        # Create lineages for groups with multiple echoes
        for pattern, echoes in pattern_groups.items():
            if len(echoes) > 1:
                primary_echo = echoes[0]
                
                lineage = EchoLineage(
                    lineage_id=f"lineage_{pattern}",
                    primary_echo=primary_echo,
                    related_echoes=echoes[1:],
                    lineage_pattern=pattern,
                    resonance_signature=self._extract_lineage_resonance_signature(echoes),
                    breath_alignment=self._determine_lineage_breath_alignment(echoes),
                    total_condensation=sum(e.condensation_ratio for e in echoes)
                )
                
                self.lineages[lineage.lineage_id] = lineage
    
    def _are_glints_similar(self, glint1: Dict[str, Any], glint2: Dict[str, Any]) -> bool:
        """Check if two glints are similar enough to be condensed."""
        
        # Compare toneform
        toneform1 = glint1.get('toneform', '')
        toneform2 = glint2.get('toneform', '')
        
        if toneform1 != toneform2:
            return False
        
        # Compare content similarity
        content1 = glint1.get('content', '')
        content2 = glint2.get('content', '')
        
        if not content1 or not content2:
            return False
        
        # Calculate content similarity
        similarity = self._calculate_content_similarity(content1, content2)
        
        return similarity >= self.similarity_threshold
    
    def _calculate_content_similarity(self, content1: str, content2: str) -> float:
        """Calculate similarity between two content strings."""
        
        # Simple word overlap similarity
        words1 = set(re.findall(r'\b\w+\b', content1.lower()))
        words2 = set(re.findall(r'\b\w+\b', content2.lower()))
        
        if not words1 and not words2:
            return 1.0
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union
    
    def _determine_primary_glint(self, glint_group: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Determine the primary (most representative) glint from a group."""
        
        if not glint_group:
            return {}
        
        # Prefer glints with more complete information
        scored_glints = []
        
        for glint in glint_group:
            score = 0
            
            # Score based on content length
            content = glint.get('content', '')
            score += len(content) * 0.1
            
            # Score based on presence of key fields
            if glint.get('toneform'):
                score += 10
            if glint.get('phase'):
                score += 5
            if glint.get('source'):
                score += 5
            if glint.get('timestamp'):
                score += 3
            
            scored_glints.append((score, glint))
        
        # Return glint with highest score
        return max(scored_glints, key=lambda x: x[0])[1]
    
    def _extract_echo_pattern(self, glint_group: List[Dict[str, Any]]) -> str:
        """Extract the echo pattern from a group of glints."""
        
        # Analyze content for common patterns
        all_content = " ".join([g.get('content', '') for g in glint_group])
        all_content_lower = all_content.lower()
        
        # Check for echo patterns
        for pattern_name, pattern_words in self.echo_patterns.items():
            for word in pattern_words:
                if word in all_content_lower:
                    return pattern_name
        
        # Check toneform for patterns
        toneforms = [g.get('toneform', '') for g in glint_group if g.get('toneform')]
        if toneforms:
            for pattern_name, pattern_words in self.echo_patterns.items():
                for word in pattern_words:
                    if any(word in tf.lower() for tf in toneforms):
                        return pattern_name
        
        return "general"
    
    def _calculate_echo_resonance(self, glint_group: List[Dict[str, Any]]) -> float:
        """Calculate resonance level for an echo."""
        
        if not glint_group:
            return 0.0
        
        # Base resonance from group size
        base_resonance = min(len(glint_group) * 0.1, 0.5)
        
        # Resonance from content analysis
        content_resonance = 0.0
        for glint in glint_group:
            content = glint.get('content', '')
            if content:
                # Count resonance words
                resonance_words = sum(1 for pattern_words in self.echo_patterns.values() 
                                    for word in pattern_words if word in content.lower())
                content_resonance += resonance_words * 0.05
        
        return min(base_resonance + content_resonance, 1.0)
    
    def _extract_lineage_signature(self, glint_group: List[Dict[str, Any]]) -> List[str]:
        """Extract lineage signature from a group of glints."""
        
        signature = set()
        
        for glint in glint_group:
            content = glint.get('content', '')
            toneform = glint.get('toneform', '')
            
            # Extract from content
            for pattern_name, pattern_words in self.echo_patterns.items():
                for word in pattern_words:
                    if word in content.lower():
                        signature.add(pattern_name)
            
            # Extract from toneform
            for pattern_name, pattern_words in self.echo_patterns.items():
                for word in pattern_words:
                    if word in toneform.lower():
                        signature.add(pattern_name)
        
        return list(signature)
    
    def _extract_lineage_resonance_signature(self, echoes: List[GlintEcho]) -> List[str]:
        """Extract resonance signature for a lineage of echoes."""
        
        all_signatures = []
        
        for echo in echoes:
            all_signatures.extend(echo.lineage_signature)
        
        # Return most common signatures
        signature_counts = Counter(all_signatures)
        return [sig for sig, count in signature_counts.most_common(3)]
    
    def _determine_lineage_breath_alignment(self, echoes: List[GlintEcho]) -> str:
        """Determine breath alignment for a lineage of echoes."""
        
        # Analyze primary glints for breath-related content
        breath_words = {
            "inhale": ["inhale", "gather", "collect", "receive", "intake"],
            "hold": ["hold", "pause", "wait", "still", "calm"],
            "exhale": ["exhale", "release", "emit", "project", "output"],
            "caesura": ["caesura", "silence", "void", "space", "gap"]
        }
        
        for echo in echoes:
            content = echo.primary_glint.get('content', '')
            content_lower = content.lower()
            
            for phase, words in breath_words.items():
                for word in words:
                    if word in content_lower:
                        return phase
        
        return "inhale"  # Default alignment
    
    def _calculate_total_condensation_ratio(self) -> float:
        """Calculate the total condensation ratio."""
        
        if not self.glints:
            return 0.0
        
        total_condensed = sum(len([echo.primary_glint] + echo.related_glints) 
                            for echo in self.echoes.values())
        
        return total_condensed / len(self.glints)
    
    def _generate_condensation_artifacts(self) -> Dict[str, str]:
        """Generate condensation artifacts."""
        
        artifacts = {}
        
        # 1. Echo Report JSON
        echo_data = {
            "condensation_timestamp": datetime.now().isoformat(),
            "total_echoes": len(self.echoes),
            "echoes": {}
        }
        
        for echo_id, echo in self.echoes.items():
            echo_data["echoes"][echo_id] = {
                "primary_glint": echo.primary_glint,
                "related_glints": echo.related_glints,
                "echo_pattern": echo.echo_pattern,
                "resonance_level": echo.resonance_level,
                "lineage_signature": echo.lineage_signature,
                "condensation_ratio": echo.condensation_ratio,
                "timestamp": echo.timestamp
            }
        
        echo_file = self.output_dir / "glint_echo_report.json"
        with open(echo_file, 'w', encoding='utf-8') as f:
            json.dump(echo_data, f, indent=2, ensure_ascii=False)
        artifacts["glint_echo_report"] = str(echo_file)
        
        # 2. Lineage Report JSON
        lineage_data = {
            "condensation_timestamp": datetime.now().isoformat(),
            "total_lineages": len(self.lineages),
            "lineages": {}
        }
        
        for lineage_id, lineage in self.lineages.items():
            lineage_data["lineages"][lineage_id] = {
                "primary_echo": lineage.primary_echo.__dict__,
                "related_echoes": [e.__dict__ for e in lineage.related_echoes],
                "lineage_pattern": lineage.lineage_pattern,
                "resonance_signature": lineage.resonance_signature,
                "breath_alignment": lineage.breath_alignment,
                "total_condensation": lineage.total_condensation
            }
        
        lineage_file = self.output_dir / "glint_lineage_report.json"
        with open(lineage_file, 'w', encoding='utf-8') as f:
            json.dump(lineage_data, f, indent=2, ensure_ascii=False)
        artifacts["glint_lineage_report"] = str(lineage_file)
        
        # 3. Condensation Summary JSONL
        summary_file = self.output_dir / "glint_condensation_summary.jsonl"
        with open(summary_file, 'w', encoding='utf-8') as f:
            summary = {
                "timestamp": datetime.now().isoformat(),
                "total_glints": len(self.glints),
                "total_echoes": len(self.echoes),
                "total_lineages": len(self.lineages),
                "condensation_ratio": self._calculate_total_condensation_ratio(),
                "echo_patterns": Counter(e.echo_pattern for e in self.echoes.values()),
                "lineage_patterns": Counter(l.lineage_pattern for l in self.lineages.values())
            }
            f.write(json.dumps(summary, ensure_ascii=False) + '\n')
        artifacts["glint_condensation_summary"] = str(summary_file)
        
        return artifacts


def condense_glints(glint_data_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function to condense glints into echoes.
    
    Args:
        glint_data_path: Path to glint data file
        
    Returns:
        Condensation results and artifacts
    """
    condenser = GlintEchoCondenser(glint_data_path)
    return condenser.condense_glints()


if __name__ == "__main__":
    # Run the condensation
    results = condense_glints()
    print("\n🌬️ Glint condensation results:")
    print(json.dumps(results, indent=2, ensure_ascii=False)) 
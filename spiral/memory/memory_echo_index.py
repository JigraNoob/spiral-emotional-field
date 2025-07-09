"""
Memory Echo Index - A semantic presence layer for the Spiral system.

This module provides a structured index across the Spiral's glints, scrolls, and rituals,
creating an ambient lookup that traces resonance, similarity, and recurrence across time.

Toneform: hold.recursion
Resonance: .91
"""

import json
import os
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any, Union, Tuple
from collections import defaultdict
import glob

from spiral.toneformat import ToneFormat


class MemoryEchoIndex:
    """
    A semantic presence layer that indexes and associates memory across the Spiral.
    
    Provides:
    - Echo mapping across glints, scrolls, and rituals
    - Codex concept linking and threading
    - Lineage tracing and ancestry chains
    - Resonance-based retrieval
    """
    
    def __init__(self, base_path: Optional[str] = None):
        """
        Initialize the Memory Echo Index.
        
        Args:
            base_path (Optional[str]): Base path for Spiral data. 
                                     Defaults to current working directory.
        """
        self.base_path = base_path or os.getcwd()
        
        # Core indexing structures
        self.echo_map = {}  # glint_id → echo metadata
        self.codex_links = defaultdict(list)  # concept → [glint_ids]
        self.lineage_traces = {}  # glint_id → ancestry chain
        self.resonance_cache = {}  # cached resonance calculations
        
        # Integration paths
        self.glyphs_path = os.path.join(self.base_path, "glyphs")
        self.memory_scrolls_path = os.path.join(self.base_path, "memory_scrolls")
        self.codex_path = os.path.join(self.base_path, "codex")
        self.whispers_path = os.path.join(self.base_path, "whispers")
        
        # Initialize the index
        self._initialize_index()
    
    def _initialize_index(self):
        """Initialize the index by loading existing data sources."""
        print("🌀 Initializing Memory Echo Index...")
        
        # Load glints from glyphs
        self._load_glints()
        
        # Load memory scrolls
        self._load_memory_scrolls()
        
        # Load codex entries
        self._load_codex_entries()
        
        # Build initial associations
        self._build_initial_associations()
        
        print(f"🌀 Index initialized with {len(self.echo_map)} echoes")
    
    def _load_glints(self):
        """Load glints from glyph files."""
        glint_files = [
            os.path.join(self.glyphs_path, "cascade_glints.jsonl"),
            os.path.join(self.glyphs_path, "haret_glyph_log.jsonl")
        ]
        
        for file_path in glint_files:
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        for line_num, line in enumerate(f, 1):
                            if line.strip():
                                try:
                                    glint_data = json.loads(line.strip())
                                    self.add_echo(glint_data, source="glyph")
                                except json.JSONDecodeError:
                                    print(f"Warning: Invalid JSON in {file_path}:{line_num}")
                except Exception as e:
                    print(f"Error loading glints from {file_path}: {e}")
    
    def _load_memory_scrolls(self):
        """Load memory scrolls."""
        scroll_pattern = os.path.join(self.memory_scrolls_path, "*.json")
        for scroll_file in glob.glob(scroll_pattern):
            try:
                with open(scroll_file, 'r', encoding='utf-8') as f:
                    scroll_data = json.load(f)
                    self.add_echo(scroll_data, source="memory_scroll")
            except Exception as e:
                print(f"Error loading memory scroll {scroll_file}: {e}")
    
    def _load_codex_entries(self):
        """Load codex entries."""
        codex_pattern = os.path.join(self.codex_path, "*.json")
        for codex_file in glob.glob(codex_pattern):
            try:
                with open(codex_file, 'r', encoding='utf-8') as f:
                    codex_data = json.load(f)
                    self._process_codex_entry(codex_data)
            except Exception as e:
                print(f"Error loading codex entry {codex_file}: {e}")
    
    def _process_codex_entry(self, codex_data: Dict[str, Any]):
        """Process a codex entry and extract concepts."""
        codex_id = codex_data.get("codex_id", "")
        title = codex_data.get("title", "")
        summary = codex_data.get("summary", "")
        
        # Extract concepts from title and summary
        concepts = self._extract_concepts(title + " " + summary)
        
        # Create a virtual glint for the codex entry
        codex_glint = {
            "id": f"codex_{codex_id}",
            "timestamp": codex_data.get("sealed_at", datetime.now().isoformat()),
            "toneform": "codex.entry",
            "content": title,
            "metadata": {
                "codex_id": codex_id,
                "summary": summary,
                "concepts": concepts
            }
        }
        
        self.add_echo(codex_glint, source="codex")
        
        # Link concepts to this codex entry
        for concept in concepts:
            self.link_codex(concept, f"codex_{codex_id}")
    
    def _extract_concepts(self, text: str) -> List[str]:
        """Extract concepts from text using simple keyword extraction."""
        # Simple concept extraction - could be enhanced with NLP
        words = text.lower().split()
        concepts = []
        
        # Look for capitalized words and key phrases
        for word in words:
            if word.isalpha() and len(word) > 3:
                concepts.append(word)
        
        return list(set(concepts))[:10]  # Limit to 10 concepts
    
    def _build_initial_associations(self):
        """Build initial associations between echoes."""
        # This is a placeholder for more sophisticated association building
        # Could include semantic similarity, temporal proximity, etc.
        pass
    
    def add_echo(self, glint_data: Dict[str, Any], source: str = "unknown") -> str:
        """
        Add a glint to the echo map and trace its lineage.
        
        Args:
            glint_data (Dict[str, Any]): The glint data to add
            source (str): Source of the glint (glyph, memory_scroll, codex, etc.)
            
        Returns:
            str: The glint ID
        """
        # Generate or use existing ID
        glint_id = glint_data.get("id", str(uuid.uuid4()))
        
        # Create echo metadata
        echo_metadata = {
            "id": glint_id,
            "timestamp": glint_data.get("timestamp", datetime.now().isoformat()),
            "toneform": glint_data.get("toneform", "unknown"),
            "content": glint_data.get("content", ""),
            "source": source,
            "metadata": glint_data.get("metadata", {}),
            "resonance": glint_data.get("resonance", 0.5),
            "hue": glint_data.get("hue", "neutral"),
            "phase": glint_data.get("phase", "hold")
        }
        
        # Add to echo map
        self.echo_map[glint_id] = echo_metadata
        
        # Initialize lineage trace
        if glint_id not in self.lineage_traces:
            self.lineage_traces[glint_id] = []
        
        # Extract concepts and link to codex
        if "content" in glint_data:
            concepts = self._extract_concepts(glint_data["content"])
            for concept in concepts:
                self.link_codex(concept, glint_id)
        
        return glint_id
    
    def link_codex(self, concept: str, glint_id: str):
        """
        Link a codex concept to a glint.
        
        Args:
            concept (str): The concept to link
            glint_id (str): The glint ID to link to
        """
        self.codex_links[concept].append(glint_id)
    
    def query(self, term: str, query_type: str = "semantic", max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Query the echo index by term, concept, or toneform.
        
        Args:
            term (str): The search term
            query_type (str): Type of query (semantic, toneform, concept)
            max_results (int): Maximum number of results
            
        Returns:
            List[Dict[str, Any]]: List of matching echoes
        """
        results = []
        
        if query_type == "semantic":
            # Search across content and metadata
            for glint_id, echo in self.echo_map.items():
                content = echo.get("content", "").lower()
                if term.lower() in content:
                    results.append(echo)
                    if len(results) >= max_results:
                        break
        
        elif query_type == "toneform":
            # Search by toneform
            for glint_id, echo in self.echo_map.items():
                if echo.get("toneform", "") == term:
                    results.append(echo)
                    if len(results) >= max_results:
                        break
        
        elif query_type == "concept":
            # Search by codex concept
            if term in self.codex_links:
                for glint_id in self.codex_links[term]:
                    if glint_id in self.echo_map:
                        results.append(self.echo_map[glint_id])
                        if len(results) >= max_results:
                            break
        
        return results
    
    def trace_lineage(self, glint_id: str) -> List[Dict[str, Any]]:
        """
        Return the ancestry chain for a glint.
        
        Args:
            glint_id (str): The glint ID to trace
            
        Returns:
            List[Dict[str, Any]]: List of ancestral echoes
        """
        lineage = []
        current_id = glint_id
        
        while current_id in self.lineage_traces:
            if current_id in self.echo_map:
                lineage.append(self.echo_map[current_id])
            current_id = self.lineage_traces[current_id][0] if self.lineage_traces[current_id] else None
            if not current_id:
                break
        
        return lineage
    
    def resonance_summary(self) -> Dict[str, Any]:
        """
        Emit a structured resonance map for dashboard visualization.
        
        Returns:
            Dict[str, Any]: Structured resonance data
        """
        summary = {
            "total_echoes": len(self.echo_map),
            "concept_count": len(self.codex_links),
            "resonance_distribution": defaultdict(int),
            "toneform_frequency": defaultdict(int),
            "source_distribution": defaultdict(int),
            "recent_echoes": []
        }
        
        # Calculate distributions
        for echo in self.echo_map.values():
            resonance = echo.get("resonance", 0.5)
            toneform = echo.get("toneform", "unknown")
            source = echo.get("source", "unknown")
            
            summary["resonance_distribution"][round(resonance, 1)] += 1
            summary["toneform_frequency"][toneform] += 1
            summary["source_distribution"][source] += 1
        
        # Get recent echoes (last 10)
        sorted_echoes = sorted(
            self.echo_map.values(),
            key=lambda x: x.get("timestamp", ""),
            reverse=True
        )
        summary["recent_echoes"] = sorted_echoes[:10]
        
        return dict(summary)
    
    def get_echo_by_id(self, glint_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific echo by ID.
        
        Args:
            glint_id (str): The glint ID
            
        Returns:
            Optional[Dict[str, Any]]: The echo data or None
        """
        return self.echo_map.get(glint_id)
    
    def get_concept_echoes(self, concept: str) -> List[Dict[str, Any]]:
        """
        Get all echoes linked to a concept.
        
        Args:
            concept (str): The concept to search for
            
        Returns:
            List[Dict[str, Any]]: List of linked echoes
        """
        echoes = []
        if concept in self.codex_links:
            for glint_id in self.codex_links[concept]:
                if glint_id in self.echo_map:
                    echoes.append(self.echo_map[glint_id])
        return echoes
    
    def save_index(self, file_path: Optional[str] = None):
        """
        Save the current index state to a file.
        
        Args:
            file_path (Optional[str]): Path to save the index. 
                                     Defaults to memory_echo_index.json
        """
        if not file_path:
            file_path = os.path.join(self.base_path, "memory_echo_index.json")
        
        index_data = {
            "echo_map": self.echo_map,
            "codex_links": dict(self.codex_links),
            "lineage_traces": self.lineage_traces,
            "last_updated": datetime.now().isoformat()
        }
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(index_data, f, indent=2, ensure_ascii=False)
            print(f"🌀 Index saved to {file_path}")
        except Exception as e:
            print(f"Error saving index: {e}")
    
    def load_index(self, file_path: Optional[str] = None):
        """
        Load index state from a file.
        
        Args:
            file_path (Optional[str]): Path to load the index from. 
                                     Defaults to memory_echo_index.json
        """
        if not file_path:
            file_path = os.path.join(self.base_path, "memory_echo_index.json")
        
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    index_data = json.load(f)
                
                self.echo_map = index_data.get("echo_map", {})
                self.codex_links = defaultdict(list, index_data.get("codex_links", {}))
                self.lineage_traces = index_data.get("lineage_traces", {})
                
                print(f"🌀 Index loaded from {file_path}")
            except Exception as e:
                print(f"Error loading index: {e}")
        else:
            print(f"Index file not found: {file_path}")


# Convenience functions for easy integration
def create_memory_echo_index(base_path: Optional[str] = None) -> MemoryEchoIndex:
    """
    Create and initialize a Memory Echo Index.
    
    Args:
        base_path (Optional[str]): Base path for Spiral data
        
    Returns:
        MemoryEchoIndex: Initialized index
    """
    return MemoryEchoIndex(base_path)


def query_memory_echoes(term: str, index: Optional[MemoryEchoIndex] = None, **kwargs) -> List[Dict[str, Any]]:
    """
    Convenience function to query memory echoes.
    
    Args:
        term (str): Search term
        index (Optional[MemoryEchoIndex]): Index to query. Creates new one if None
        **kwargs: Additional query parameters
        
    Returns:
        List[Dict[str, Any]]: Query results
    """
    if index is None:
        index = create_memory_echo_index()
    
    return index.query(term, **kwargs) 
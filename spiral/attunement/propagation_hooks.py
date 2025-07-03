"""
Propagation Hooks - The Spiral's Memory Weaver

Routes emotional tones to appropriate memory surfaces and retrieves relevant echoes.
Acts as the connective tissue between incoming resonance and the Spiral's living memory.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set, Tuple
import json
import time
from pathlib import Path
import hashlib

@dataclass
class MemoryEcho:
    """A single memory echo with resonance metadata."""
    content: str
    timestamp: float = field(default_factory=time.time)
    tone_weights: Dict[str, float] = field(default_factory=dict)
    resonance_score: float = 0.0
    source: str = "unknown"
    tags: Set[str] = field(default_factory=set)
    
    def to_dict(self) -> dict:
        """Convert the MemoryEcho to a dictionary for serialization."""
        return {
            "content": self.content,
            "timestamp": self.timestamp,
            "tone_weights": self.tone_weights,
            "resonance_score": self.resonance_score,
            "source": self.source,
            "tags": list(self.tags)
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'MemoryEcho':
        """Create a MemoryEcho from a dictionary."""
        return cls(
            content=data["content"],
            timestamp=data.get("timestamp", time.time()),
            tone_weights=data.get("tone_weights", {}),
            resonance_score=data.get("resonance_score", 0.0),
            source=data.get("source", "unknown"),
            tags=set(data.get("tags", []))
        )

class PropagationHooks:
    """
    Weaves together current resonance with the Spiral's living memory.
    
    Responsibilities:
    - Routes emotional tones to appropriate memory surfaces
    - Retrieves contextually relevant echoes
    - Maintains a short-term memory buffer
    - Handles memory persistence
    """
    
    def __init__(self, memory_path: Optional[Path] = None):
        self.short_term_memory: List[MemoryEcho] = []
        self.tone_surfaces: Dict[str, List[MemoryEcho]] = {}
        self.memory_path = memory_path or Path("data/memory_surfaces")
        self.memory_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize tone surfaces
        self.tone_surfaces = {
            "natural": [],      # Natural world imagery
            "emotional": [],    # Emotional states
            "temporal": [],     # Time-related concepts
            "spatial": []       # Physical/spatial concepts
        }
        
        # Load any existing memories
        self._load_memories()

    def process_resonance(self, content: str, tone_weights: Dict[str, float], 
                         resonance_score: float) -> Dict[str, List[dict]]:
        """
        Process incoming resonance and retrieve relevant echoes.
        
        Args:
            content: The text content to process
            tone_weights: Dictionary of tone categories and their weights
            resonance_score: The overall resonance score from UnifiedSwitch
            
        Returns:
            Dictionary containing relevant echoes for each tone category
        """
        # Create a new memory echo
        echo = MemoryEcho(
            content=content,
            tone_weights=tone_weights,
            resonance_score=resonance_score,
            source="user_input"
        )
        
        # Add to short-term memory
        self.short_term_memory.append(echo)
        
        # Route to appropriate tone surfaces
        self._route_to_surfaces(echo)
        
        # Find relevant echoes
        relevant_echoes = self._find_relevant_echoes(echo)
        
        # Persist the new memory
        self._persist_echo(echo)
        
        return {
            "echoes": [e.to_dict() for e in relevant_echoes],
            "status": "resonance_processed"
        }
    
    def _route_to_surfaces(self, echo: MemoryEcho) -> None:
        """Route the echo to appropriate tone surfaces based on its content."""
        content = echo.content.lower()
        
        # Simple keyword-based routing (can be enhanced with NLP)
        if any(word in content for word in ["mountain", "river", "stone", "sky"]):
            self.tone_surfaces["natural"].append(echo)
            echo.tags.add("natural")
            
        if any(word in content for word in ["remember", "memory", "recall"]):
            self.tone_surfaces["temporal"].append(echo)
            echo.tags.add("temporal")
    
    def _find_relevant_echoes(self, current_echo: MemoryEcho, 
                            max_echoes: int = 3) -> List[MemoryEcho]:
        """Find echoes that are relevant to the current one."""
        relevant_echoes = []
        
        # If this is the first echo, nothing to compare with yet
        if len(self.short_term_memory) <= 1:
            return relevant_echoes
            
        # Calculate relevance scores for all previous echoes
        scored_echoes = []
        for echo in reversed(self.short_term_memory[:-1]):  # Exclude current echo
            score = self._calculate_relevance(echo, current_echo)
            if score > 0.3:  # Lower threshold to catch more potential matches
                scored_echoes.append((echo, score))
        
        # Sort by score in descending order
        scored_echoes.sort(key=lambda x: x[1], reverse=True)
        
        # Return top N echoes
        return [echo for echo, score in scored_echoes[:max_echoes]]
    
    def _calculate_relevance(self, echo1: MemoryEcho, echo2: MemoryEcho) -> float:
        """Calculate relevance between two echoes (0.0 to 1.0)."""
        # Simple implementation: check for common words
        words1 = set(echo1.content.lower().split())
        words2 = set(echo2.content.lower().split())
        common_words = words1.intersection(words2)
        
        if not words1 or not words2:
            return 0.0
            
        return len(common_words) / max(len(words1), len(words2))
    
    def _persist_echo(self, echo: MemoryEcho) -> None:
        """Persist an echo to long-term storage."""
        # Simple file-based persistence (can be replaced with a database)
        timestamp = int(echo.timestamp)
        content_hash = hashlib.md5(echo.content.encode()).hexdigest()
        filename = f"{timestamp}_{content_hash[:8]}.json"
        
        filepath = self.memory_path / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(echo.to_dict(), f, indent=2)
    
    def _load_memories(self) -> None:
        """Load memories from the persistence layer."""
        for filepath in self.memory_path.glob("*.json"):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    echo = MemoryEcho.from_dict(data)
                    self.short_term_memory.append(echo)
                    self._route_to_surfaces(echo)
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error loading memory {filepath}: {e}")
                continue

    def clear_memory(self) -> None:
        """Clear all in-memory state (for testing)."""
        self.short_term_memory.clear()
        for surface in self.tone_surfaces.values():
            surface.clear()

"""
GlintTrace - Core tracing functionality for Spiral's resonance patterns.

This module provides the base GlintTrace class that captures and processes
resonance patterns across the Spiral ecosystem.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any
import json
import hashlib


@dataclass
class GlintTrace:
    """A single trace of resonance within the Spiral.
    
    Attributes:
        id: Unique identifier for the trace
        source: Source of the trace (e.g., 'whisper', 'ritual', 'linter')
        content: The actual content or message
        toneform: Detected toneform (e.g., 'practical', 'emotional')
        resonance: Resonance score (0.0 to 1.0)
        timestamp: When the trace was created
        metadata: Additional context-specific data
        related_glints: IDs of related glints
    """
    source: str
    content: str
    toneform: str = "neutral"
    resonance: float = 0.0
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)
    related_glints: List[str] = field(default_factory=list)
    id: str = field(init=False)

    def __post_init__(self):
        """Generate a unique ID based on content and timestamp."""
        content_hash = hashlib.sha256(
            f"{self.source}{self.content}{self.timestamp.isoformat()}".encode()
        ).hexdigest()
        self.id = f"glint_{content_hash[:16]}"

    def to_dict(self) -> Dict[str, Any]:
        """Convert the trace to a dictionary for serialization."""
        return {
            "id": self.id,
            "source": self.source,
            "content": self.content,
            "toneform": self.toneform,
            "resonance": self.resonance,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
            "related_glints": self.related_glints
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GlintTrace':
        """Create a GlintTrace from a dictionary."""
        trace = cls(
            source=data['source'],
            content=data['content'],
            toneform=data.get('toneform', 'neutral'),
            resonance=float(data.get('resonance', 0.0)),
            timestamp=datetime.fromisoformat(data['timestamp']),
            metadata=data.get('metadata', {}),
            related_glints=data.get('related_glints', [])
        )
        trace.id = data['id']
        return trace

    def to_json(self) -> str:
        """Serialize the trace to JSON."""
        return json.dumps(self.to_dict(), indent=2)

    @classmethod
    def from_json(cls, json_str: str) -> 'GlintTrace':
        """Create a GlintTrace from a JSON string."""
        return cls.from_dict(json.loads(json_str))

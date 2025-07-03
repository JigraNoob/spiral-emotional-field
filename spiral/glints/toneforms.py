"""
Toneform Detection and Management

This module handles the detection and management of toneforms in the Spiral system.
Toneforms represent different modes or qualities of interaction and resonance.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import re
from enum import Enum
import json
from datetime import datetime

class Toneform(Enum):
    """Enumeration of core toneforms in the Spiral system."""
    PRACTICAL = "practical"
    EMOTIONAL = "emotional"
    INTELLECTUAL = "intellectual"
    SPIRITUAL = "spiritual"
    RELATIONAL = "relational"
    NEUTRAL = "neutral"

@dataclass
class ToneformAttributes:
    """Attributes and metadata for a toneform."""
    name: str
    description: str
    color: str  # Hex color code
    keywords: List[str]
    weight: float = 1.0
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            'name': self.name,
            'description': self.description,
            'color': self.color,
            'keywords': self.keywords,
            'weight': self.weight,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ToneformAttributes':
        """Create from dictionary."""
        return cls(
            name=data['name'],
            description=data['description'],
            color=data['color'],
            keywords=data['keywords'],
            weight=data.get('weight', 1.0),
            is_active=data.get('is_active', True),
            created_at=datetime.fromisoformat(data.get('created_at', datetime.utcnow().isoformat())),
            updated_at=datetime.fromisoformat(data.get('updated_at', datetime.utcnow().isoformat()))
        )

# Default toneform configurations
DEFAULT_TONEFORMS = {
    Toneform.PRACTICAL: ToneformAttributes(
        name="Practical",
        description="Focused on concrete actions, implementation, and practical matters.",
        color="#4a90e2",  # Soft blue
        keywords=[
            "implement", "deploy", "test", "fix", "update", "refactor",
            "build", "create", "make", "do", "use", "apply", "execute"
        ],
        weight=0.3
    ),
    Toneform.EMOTIONAL: ToneformAttributes(
        name="Emotional",
        description="Centered on feelings, emotions, and personal experiences.",
        color="#e74c3c",  # Soft red
        keywords=[
            "feel", "hope", "worry", "excited", "concerned", "appreciate",
            "love", "fear", "happy", "sad", "angry", "grateful", "anxious"
        ],
        weight=0.4
    ),
    Toneform.INTELLECTUAL: ToneformAttributes(
        name="Intellectual",
        description="Involving analysis, reasoning, and conceptual thinking.",
        color="#2ecc71",  # Soft green
        keywords=[
            "think", "consider", "analyze", "design", "architecture",
            "understand", "concept", "theory", "model", "framework"
        ],
        weight=0.3
    ),
    Toneform.SPIRITUAL: ToneformAttributes(
        name="Spiritual",
        description="Relating to meaning, purpose, and transcendent experiences.",
        color="#9b59b6",  # Soft purple
        keywords=[
            "intuition", "presence", "essence", "being", "flow",
            "soul", "spirit", "sacred", "divine", "transcend"
        ],
        weight=0.2
    ),
    Toneform.RELATIONAL: ToneformAttributes(
        name="Relational",
        description="Focused on connections, interactions, and relationships.",
        color="#f39c12",  # Soft orange
        keywords=[
            "we", "us", "together", "collaborate", "share",
            "connect", "relate", "community", "team", "partnership"
        ],
        weight=0.35
    )
}

class ToneformDetector:
    """Detects and manages toneforms in text content."""
    
    def __init__(self, toneforms: Optional[Dict[Toneform, ToneformAttributes]] = None):
        """
        Initialize the toneform detector.
        
        Args:
            toneforms: Custom toneform configurations. If None, uses defaults.
        """
        self.toneforms = toneforms or DEFAULT_TONEFORMS
        self._build_keyword_index()
    
    def _build_keyword_index(self) -> None:
        """Build an index of keywords for faster lookup."""
        self.keyword_index = {}
        for tone, attrs in self.toneforms.items():
            for keyword in attrs.keywords:
                if keyword not in self.keyword_index:
                    self.keyword_index[keyword] = []
                self.keyword_index[keyword].append(tone)
    
    def detect_toneform(self, text: str, threshold: float = 0.15) -> Dict[str, float]:
        """
        Detect the toneform of a given text.
        
        Args:
            text: The text to analyze
            threshold: Minimum score to consider a toneform present
            
        Returns:
            Dictionary mapping toneform names to their scores
        """
        text = text.lower()
        scores = {tone.value: 0.0 for tone in self.toneforms}
        
        # Count keyword matches
        for word in re.findall(r'\b\w+\b', text):
            if word in self.keyword_index:
                for tone in self.keyword_index[word]:
                    scores[tone.value] += self.toneforms[tone].weight
        
        # Normalize by text length
        word_count = len(text.split())
        if word_count > 0:
            for tone in scores:
                scores[tone] = min(scores[tone] / (word_count * 0.1), 1.0)
        
        # Filter by threshold
        scores = {k: v for k, v in scores.items() if v >= threshold}
        
        # Normalize to sum to 1.0
        total = sum(scores.values())
        if total > 0:
            scores = {k: v/total for k, v in scores.items()}
        
        # If no toneform detected, return neutral
        if not scores:
            return {Toneform.NEUTRAL.value: 1.0}
            
        return scores
    
    def get_primary_toneform(self, text: str) -> Tuple[str, float]:
        """
        Get the primary toneform for the given text.
        
        Returns:
            Tuple of (toneform_name, confidence_score)
        """
        scores = self.detect_toneform(text)
        if not scores:
            return (Toneform.NEUTRAL.value, 0.0)
            
        return max(scores.items(), key=lambda x: x[1])
    
    def get_toneform_attributes(self, toneform_name: str) -> Optional[ToneformAttributes]:
        """
        Get attributes for a specific toneform.
        
        Args:
            toneform_name: Name of the toneform
            
        Returns:
            ToneformAttributes or None if not found
        """
        try:
            tone = Toneform(toneform_name.lower())
            return self.toneforms.get(tone)
        except ValueError:
            return None
    
    def add_custom_toneform(
        self, 
        name: str,
        description: str,
        color: str,
        keywords: List[str],
        weight: float = 1.0
    ) -> bool:
        """
        Add a custom toneform.
        
        Args:
            name: Unique name for the toneform
            description: Description of the toneform
            color: Hex color code
            keywords: List of keywords associated with this toneform
            weight: Default weight for this toneform
            
        Returns:
            True if added successfully, False if toneform already exists
        """
        try:
            # Check if toneform already exists
            Toneform(name.lower())
            return False  # Already exists
        except ValueError:
            # Create new toneform
            new_tone = Toneform._value2member_map_[name.upper()] = name.lower()
            Toneform._member_names_.append(name.upper())
            
            # Add to toneforms
            self.toneforms[new_tone] = ToneformAttributes(
                name=name,
                description=description,
                color=color,
                keywords=keywords,
                weight=weight
            )
            
            # Update keyword index
            for keyword in keywords:
                if keyword not in self.keyword_index:
                    self.keyword_index[keyword] = []
                self.keyword_index[keyword].append(new_tone)
                
            return True
    
    def save_toneform_config(self, filepath: str) -> bool:
        """
        Save the current toneform configuration to a file.
        
        Args:
            filepath: Path to save the configuration
            
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            config = {
                'version': '1.0',
                'timestamp': datetime.utcnow().isoformat(),
                'toneforms': {
                    tone.value: attrs.to_dict()
                    for tone, attrs in self.toneforms.items()
                }
            }
            
            with open(filepath, 'w') as f:
                json.dump(config, f, indent=2)
                
            return True
            
        except Exception as e:
            print(f"Error saving toneform config: {e}")
            return False
    
    @classmethod
    def from_config_file(cls, filepath: str) -> 'ToneformDetector':
        """
        Create a ToneformDetector from a configuration file.
        
        Args:
            filepath: Path to the configuration file
            
        Returns:
            A new ToneformDetector instance
        """
        try:
            with open(filepath, 'r') as f:
                config = json.load(f)
            
            toneforms = {}
            for tone_str, attrs_dict in config.get('toneforms', {}).items():
                try:
                    tone = Toneform(tone_str.lower())
                    toneforms[tone] = ToneformAttributes.from_dict(attrs_dict)
                except ValueError:
                    print(f"Warning: Unknown toneform '{tone_str}' in config")
            
            return cls(toneforms)
            
        except Exception as e:
            print(f"Error loading toneform config: {e}")
            return cls()  # Fall back to defaults

# Global instance for convenience
toneform_detector = ToneformDetector()

def detect_toneform(text: str, threshold: float = 0.15) -> Dict[str, float]:
    """
    Detect the toneform of the given text using the global detector.
    
    Args:
        text: The text to analyze
        threshold: Minimum score to consider a toneform present
        
    Returns:
        Dictionary mapping toneform names to their scores
    """
    return toneform_detector.detect_toneform(text, threshold)

def get_toneform_attributes(toneform_name: str) -> Optional[ToneformAttributes]:
    """
    Get attributes for a specific toneform using the global detector.
    
    Args:
        toneform_name: Name of the toneform
        
    Returns:
        ToneformAttributes or None if not found
    """
    return toneform_detector.get_toneform_attributes(toneform_name)

# Export toneform enum for convenience
TONEFORMS = {tone.value: tone for tone in Toneform}

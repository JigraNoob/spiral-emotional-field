"""
GlintPattern - Pattern recognition and analysis for glint traces.

This module provides functionality to identify, track, and analyze patterns
in glint traces over time.
"""
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Set, Optional, Tuple, TYPE_CHECKING
import re
import hashlib
import json
from collections import defaultdict, deque

if TYPE_CHECKING:
    from .glint_trace import GlintTrace

@dataclass
class PatternMatch:
    """Represents a matched pattern in glint data."""
    pattern_id: str
    confidence: float
    matches: List[Dict]
    first_seen: datetime
    last_seen: datetime
    frequency: int = 1
    metadata: Dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert pattern match to dictionary."""
        return {
            'pattern_id': self.pattern_id,
            'confidence': self.confidence,
            'matches': self.matches,
            'first_seen': self.first_seen.isoformat(),
            'last_seen': self.last_seen.isoformat(),
            'frequency': self.frequency,
            'metadata': self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'PatternMatch':
        """Create PatternMatch from dictionary."""
        return cls(
            pattern_id=data['pattern_id'],
            confidence=data['confidence'],
            matches=data['matches'],
            first_seen=datetime.fromisoformat(data['first_seen']),
            last_seen=datetime.fromisoformat(data['last_seen']),
            frequency=data.get('frequency', 1),
            metadata=data.get('metadata', {})
        )

class GlintPattern:
    """Manages pattern recognition across glint traces."""
    
    def __init__(self, window_size: int = 50, min_pattern_length: int = 3):
        """
        Initialize the pattern recognizer.
        
        Args:
            window_size: Number of recent glints to consider for pattern matching
            min_pattern_length: Minimum sequence length to consider as a pattern
        """
        self.window_size = window_size
        self.min_pattern_length = min_pattern_length
        self.patterns: Dict[str, PatternMatch] = {}
        self.recent_glints = deque(maxlen=window_size * 2)
        
    def add_glint(self, glint_trace: 'GlintTrace') -> List[PatternMatch]:
        """
        Add a glint and check for patterns.
        
        Returns:
            List of matched patterns, if any
        """
        glint_data = {
            'id': glint_trace.id,
            'source': glint_trace.source,
            'toneform': glint_trace.toneform,
            'content': glint_trace.content,
            'resonance': glint_trace.resonance,
            'timestamp': glint_trace.timestamp.isoformat(),
            'metadata': glint_trace.metadata
        }
        
        self.recent_glints.append(glint_data)
        
        # Only check for patterns if we have enough data
        if len(self.recent_glints) < self.min_pattern_length * 2:
            return []
            
        return self._detect_patterns(glint_data)
    
    def _detect_patterns(self, new_glint: Dict) -> List[PatternMatch]:
        """Detect patterns in the recent glint history."""
        glints = list(self.recent_glints)
        new_patterns = []
        
        # Look for sequences ending with the new glint
        for length in range(self.min_pattern_length, min(10, len(glints) // 2)):
            # The potential pattern is the last 'length' glints
            potential_pattern = glints[-length:]
            pattern_id = self._generate_pattern_id(potential_pattern)
            
            # Check if this pattern appears earlier in the history
            matches = self._find_pattern_matches(glints[:-length], potential_pattern)
            
            if matches:
                confidence = len(matches) / (len(glints) / length)
                
                if pattern_id in self.patterns:
                    # Update existing pattern
                    pattern = self.patterns[pattern_id]
                    pattern.frequency += 1
                    pattern.last_seen = datetime.utcnow()
                    pattern.confidence = max(pattern.confidence, confidence)
                    pattern.matches.append({
                        'timestamp': datetime.utcnow().isoformat(),
                        'context': 'repetition',
                        'glints': [g['id'] for g in potential_pattern]
                    })
                else:
                    # Create new pattern
                    pattern = PatternMatch(
                        pattern_id=pattern_id,
                        confidence=confidence,
                        matches=[{
                            'timestamp': datetime.utcnow().isoformat(),
                            'context': 'initial',
                            'glints': [g['id'] for g in potential_pattern]
                        }],
                        first_seen=datetime.utcnow(),
                        last_seen=datetime.utcnow()
                    )
                    self.patterns[pattern_id] = pattern
                
                new_patterns.append(pattern)
        
        return new_patterns
    
    def _generate_pattern_id(self, glint_sequence: List[Dict]) -> str:
        """Generate a unique ID for a glint sequence pattern."""
        pattern_str = '|'.join(
            f"{g['source']}:{g['toneform']}:{g['content'][:20]}" 
            for g in glint_sequence
        )
        return f"pattern_{hashlib.md5(pattern_str.encode()).hexdigest()[:8]}"
    
    def _find_pattern_matches(
        self, 
        glints: List[Dict], 
        pattern: List[Dict]
    ) -> List[Dict]:
        """Find occurrences of a pattern in a list of glints."""
        if len(glints) < len(pattern):
            return []
            
        matches = []
        
        for i in range(len(glints) - len(pattern) + 1):
            is_match = True
            for j in range(len(pattern)):
                if not self._glints_match(glints[i + j], pattern[j]):
                    is_match = False
                    break
            
            if is_match:
                matches.append(glints[i:i + len(pattern)])
        
        return matches
    
    def _glints_match(self, g1: Dict, g2: Dict) -> bool:
        """Determine if two glints match for pattern detection."""
        return (
            g1['source'] == g2['source'] and
            g1['toneform'] == g2['toneform'] and
            g1['content'] == g2['content']
        )
    
    def get_patterns(
        self, 
        min_confidence: float = 0.5,
        min_frequency: int = 2,
        since: Optional[datetime] = None
    ) -> List[PatternMatch]:
        """
        Get patterns matching the given criteria.
        
        Args:
            min_confidence: Minimum confidence score (0.0 to 1.0)
            min_frequency: Minimum number of occurrences
            since: Only return patterns seen since this datetime
            
        Returns:
            List of matching patterns
        """
        return [
            p for p in self.patterns.values()
            if (p.confidence >= min_confidence and 
                p.frequency >= min_frequency and
                (since is None or p.last_seen >= since))
        ]
    
    def save_patterns(self, filepath: str) -> None:
        """Save patterns to a JSON file."""
        patterns_data = {
            'version': '1.0',
            'timestamp': datetime.utcnow().isoformat(),
            'patterns': [p.to_dict() for p in self.patterns.values()]
        }
        
        with open(filepath, 'w') as f:
            json.dump(patterns_data, f, indent=2)
    
    @classmethod
    def load_patterns(cls, filepath: str) -> 'GlintPattern':
        """Load patterns from a JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        pattern_recognizer = cls()
        pattern_recognizer.patterns = {
            p['pattern_id']: PatternMatch.from_dict(p)
            for p in data.get('patterns', [])
        }
        
        return pattern_recognizer

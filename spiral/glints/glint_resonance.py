"""
GlintResonance - Resonance scoring and toneform detection for glints.

This module provides functionality to analyze and score resonance patterns
and detect toneforms in text content.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
import re
from datetime import datetime, timedelta
import math

# Base toneform definitions with resonance patterns
TONEFORMS = {
    "practical": {
        "keywords": ["implement", "deploy", "test", "fix", "update", "refactor"],
        "weight": 0.3,
        "color": "#4a90e2"  # Soft blue
    },
    "emotional": {
        "keywords": ["feel", "hope", "worry", "excited", "concerned", "appreciate"],
        "weight": 0.4,
        "color": "#e74c3c"  # Soft red
    },
    "intellectual": {
        "keywords": ["think", "consider", "analyze", "design", "architecture"],
        "weight": 0.3,
        "color": "#2ecc71"  # Soft green
    },
    "spiritual": {
        "keywords": ["intuition", "presence", "essence", "being", "flow"],
        "weight": 0.2,
        "color": "#9b59b6"  # Soft purple
    },
    "relational": {
        "keywords": ["we", "us", "together", "collaborate", "share"],
        "weight": 0.35,
        "color": "#f39c12"  # Soft orange
    }
}

def detect_toneform(text: str, threshold: float = 0.15) -> Dict[str, float]:
    """
    Detect the toneform of a given text.
    
    Args:
        text: The text to analyze
        threshold: Minimum score to consider a toneform present
        
    Returns:
        Dictionary of toneform scores
    """
    text = text.lower()
    scores = {}
    total_score = 0.0
    
    # Calculate scores for each toneform
    for tone, data in TONEFORMS.items():
        score = 0.0
        for keyword in data["keywords"]:
            # Simple keyword matching with word boundaries
            matches = len(re.findall(rf'\b{re.escape(keyword)}\b', text))
            score += matches * data["weight"]
            
        # Normalize by text length (words)
        word_count = len(text.split())
        if word_count > 0:
            score = min(score / (word_count * 0.1), 1.0)  # Cap at 1.0
            
        if score >= threshold:
            scores[tone] = score
            total_score += score
    
    # Normalize scores to sum to 1.0
    if total_score > 0:
        scores = {k: v/total_score for k, v in scores.items()}
    
    return scores

def calculate_resonance(
    text: str, 
    context: Optional[Dict] = None,
    recent_glints: Optional[List[Dict]] = None
) -> float:
    """
    Calculate the resonance score for a piece of text.
    
    Args:
        text: The text to score
        context: Additional context for resonance calculation
        recent_glints: List of recent glints for context awareness
        
    Returns:
        Resonance score between 0.0 and 1.0
    """
    if not text.strip():
        return 0.0
        
    # Base resonance from toneform detection
    tone_scores = detect_toneform(text)
    resonance = sum(score * TONEFORMS[tone]["weight"] 
                   for tone, score in tone_scores.items())
    
    # Apply context awareness if recent glints are provided
    if recent_glints:
        recent_toneforms = [g.get('toneform') for g in recent_glints 
                          if g.get('toneform') in tone_scores]
        if recent_toneforms:
            # Boost resonance for matching recent toneforms
            context_boost = 0.2 * len(set(recent_toneforms))
            resonance = min(1.0, resonance + context_boost)
    
    # Apply length-based scaling (very short or very long texts get penalized)
    word_count = len(text.split())
    if word_count < 3:
        resonance *= 0.5
    elif word_count > 100:
        resonance *= 0.8
    
    return min(max(resonance, 0.0), 1.0)

class GlintResonance:
    """Manages resonance state and calculations for glints."""
    
    def __init__(self, decay_rate: float = 0.95):
        """
        Initialize the resonance manager.
        
        Args:
            decay_rate: Rate at which resonance decays over time (0.0 to 1.0)
        """
        self.decay_rate = decay_rate
        self.toneform_history = []  # List of (timestamp, toneform, score)
        
    def update(self, glint_trace: 'GlintTrace') -> None:
        """Update resonance state with a new glint."""
        self.toneform_history.append(
            (datetime.utcnow(), glint_trace.toneform, glint_trace.resonance)
        )
        self._decay_history()
    
    def _decay_history(self) -> None:
        """Apply decay to historical resonance data."""
        now = datetime.utcnow()
        self.toneform_history = [
            (ts, tone, score * (self.decay_rate ** ((now - ts).total_seconds() / 3600)))
            for ts, tone, score in self.toneform_history
            if (now - ts) < timedelta(days=1)  # Keep only last 24 hours
        ]
    
    def get_current_resonance(self) -> Dict[str, float]:
        """Get current resonance scores per toneform."""
        resonance = {tone: 0.0 for tone in TONEFORMS}
        for _, tone, score in self.toneform_history:
            if tone in resonance:
                resonance[tone] += score
        return resonance
    
    def get_dominant_toneform(self, threshold: float = 0.3) -> Optional[str]:
        """Get the currently dominant toneform, if any."""
        resonance = self.get_current_resonance()
        if not resonance:
            return None
            
        max_tone = max(resonance.items(), key=lambda x: x[1])
        return max_tone[0] if max_tone[1] >= threshold else None

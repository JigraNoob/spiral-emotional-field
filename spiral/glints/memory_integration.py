"""
Memory Integration - Connects glints with Spiral's memory system.

This module provides functionality to store and retrieve glints from
Spiral's memory system, including integration with the Whisper Steward
and other memory-aware components.
"""
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Set, TYPE_CHECKING
from collections import defaultdict
import json
import os
from pathlib import Path
import logging

if TYPE_CHECKING:
    from .glint_trace import GlintTrace

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GlintMemory:
    """Manages storage and retrieval of glints in Spiral's memory system."""
    
    def __init__(self, data_dir: str = "data/glints"):
        """
        Initialize the glint memory system.
        
        Args:
            data_dir: Base directory for storing glint data
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # In-memory cache for recent glints
        self.recent_glints: List[Dict] = []
        self.max_cached = 1000
        
        # Index for faster lookups
        self.source_index: Dict[str, List[str]] = defaultdict(list)
        self.toneform_index: Dict[str, List[str]] = defaultdict(list)
        self.content_hash_index: Dict[str, str] = {}
    
    def store_glint(self, glint_trace: 'GlintTrace') -> bool:
        """
        Store a glint in memory and on disk.
        
        Returns:
            True if storage was successful, False otherwise
        """
        try:
            glint_data = glint_trace.to_dict()
            glint_id = glint_data['id']
            
            # Add to in-memory cache
            self.recent_glints.append(glint_data)
            if len(self.recent_glints) > self.max_cached:
                self.recent_glints = self.recent_glints[-self.max_cached:]
            
            # Update indexes
            self.source_index[glint_data['source']].append(glint_id)
            self.toneform_index[glint_data['toneform']].append(glint_id)
            
            content_hash = self._hash_content(glint_data['content'])
            self.content_hash_index[content_hash] = glint_id
            
            # Write to disk
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filename = f"glint_{timestamp}_{glint_id[:8]}.json"
            filepath = self.data_dir / filename
            
            with open(filepath, 'w') as f:
                json.dump(glint_data, f, indent=2)
            
            return True
            
        except Exception as e:
            logger.error(f"Error storing glint: {e}", exc_info=True)
            return False
    
    def find_similar_glints(
        self, 
        content: str, 
        threshold: float = 0.8,
        max_results: int = 5
    ) -> List[Dict]:
        """
        Find glints with similar content.
        
        Args:
            content: Content to compare against
            threshold: Minimum similarity score (0.0 to 1.0)
            max_results: Maximum number of results to return
            
        Returns:
            List of similar glints, sorted by similarity
        """
        # Simple implementation using content hashing
        # In a production system, you might use more sophisticated
        # similarity measures like TF-IDF or embeddings
        
        content_hash = self._hash_content(content)
        similar = []
        
        for stored_hash, glint_id in self.content_hash_index.items():
            similarity = self._hash_similarity(content_hash, stored_hash)
            if similarity >= threshold:
                glint = self._load_glint(glint_id)
                if glint:
                    similar.append((similarity, glint))
        
        # Sort by similarity (highest first)
        similar.sort(key=lambda x: x[0], reverse=True)
        
        return [glint for _, glint in similar[:max_results]]
    
    def get_glints_by_source(
        self, 
        source: str,
        limit: int = 50,
        since: Optional[datetime] = None
    ) -> List[Dict]:
        """
        Get glints from a specific source.
        
        Args:
            source: Source to filter by
            limit: Maximum number of glints to return
            since: Only return glints since this datetime
            
        Returns:
            List of matching glints
        """
        glint_ids = self.source_index.get(source, [])[-limit:]
        glints = [self._load_glint(gid) for gid in glint_ids]
        
        if since is not None:
            glints = [g for g in glints 
                     if g and datetime.fromisoformat(g['timestamp']) >= since]
        
        return [g for g in glints if g][-limit:]
    
    def get_glints_by_toneform(
        self, 
        toneform: str,
        limit: int = 50,
        since: Optional[datetime] = None
    ) -> List[Dict]:
        """
        Get glints with a specific toneform.
        
        Args:
            toneform: Toneform to filter by
            limit: Maximum number of glints to return
            since: Only return glints since this datetime
            
        Returns:
            List of matching glints
        """
        glint_ids = self.toneform_index.get(toneform.lower(), [])[-limit:]
        glints = [self._load_glint(gid) for gid in glint_ids]
        
        if since is not None:
            glints = [g for g in glints 
                     if g and datetime.fromisoformat(g['timestamp']) >= since]
        
        return [g for g in glints if g][-limit:]
    
    def get_recent_glints(self, limit: int = 50) -> List[Dict]:
        """Get the most recent glints."""
        return self.recent_glints[-limit:]
    
    def _load_glint(self, glint_id: str) -> Optional[Dict]:
        """Load a glint by ID, first checking cache, then disk."""
        # Check in-memory cache first
        for glint in reversed(self.recent_glints):
            if glint['id'] == glint_id:
                return glint
        
        # If not in cache, search disk
        for filepath in self.data_dir.glob(f"*{glint_id[:8]}*.json"):
            try:
                with open(filepath, 'r') as f:
                    return json.load(f)
            except (IOError, json.JSONDecodeError):
                continue
        
        return None
    
    @staticmethod
    def _hash_content(content: str) -> str:
        """Generate a hash of the content for similarity comparison."""
        # Simple hash for demonstration
        # In production, consider using a more sophisticated method
        import hashlib
        return hashlib.md5(content.encode()).hexdigest()
    
    @staticmethod
    def _hash_similarity(hash1: str, hash2: str) -> float:
        """Calculate similarity between two content hashes."""
        # Simple similarity based on hash prefix matching
        # In production, consider using a more sophisticated method
        match_length = 0
        for c1, c2 in zip(hash1, hash2):
            if c1 == c2:
                match_length += 1
            else:
                break
        return match_length / len(hash1)


def integrate_with_memory(glint_trace: 'GlintTrace', memory: GlintMemory) -> Dict:
    """
    Integrate a glint with the memory system.
    
    Args:
        glint_trace: The glint to integrate
        memory: The memory system to use
        
    Returns:
        Dictionary with integration results
    """
    # Store the glint
    storage_success = memory.store_glint(glint_trace)
    
    # Find related glints
    related = memory.find_similar_glints(glint_trace.content)
    
    # Update the glint with related glint IDs
    if related:
        glint_trace.related_glints = [g['id'] for g in related]
    
    return {
        'stored': storage_success,
        'related_glints_found': len(related),
        'glint_id': glint_trace.id
    }


def retrieve_related_glints(
    content: str, 
    memory: GlintMemory,
    threshold: float = 0.7,
    limit: int = 5
) -> List[Dict]:
    """
    Retrieve glints related to the given content.
    
    Args:
        content: Content to find related glints for
        memory: The memory system to use
        threshold: Minimum similarity score
        limit: Maximum number of results to return
        
    Returns:
        List of related glints
    """
    return memory.find_similar_glints(content, threshold, limit)


def update_glint_resonance(
    glint_id: str,
    new_resonance: float,
    memory: GlintMemory
) -> bool:
    """
    Update the resonance score of a glint.
    
    Args:
        glint_id: ID of the glint to update
        new_resonance: New resonance score (0.0 to 1.0)
        memory: The memory system to use
        
    Returns:
        True if update was successful, False otherwise
    """
    # This is a placeholder implementation
    # In a real system, you would update the glint in the database
    # and update any affected indexes
    logger.info(f"Updating resonance for glint {glint_id} to {new_resonance}")
    return True

import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

class MemoryScrolls:
    """📜 Lineage-aware memory system for EchoLedger"""
    
    def __init__(self, scrolls_path: str = "memory/scrolls.jsonl"):
        self.scrolls_path = scrolls_path
        os.makedirs(os.path.dirname(scrolls_path), exist_ok=True)
        self.memory_cache = []
        self._load_scrolls()
    
    def _load_scrolls(self):
        """Load existing memory scrolls"""
        if os.path.exists(self.scrolls_path):
            with open(self.scrolls_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        try:
                            self.memory_cache.append(json.loads(line))
                        except json.JSONDecodeError:
                            continue
    
    def record_echo(self, toneform: str, content: str, 
                   lineage: Optional[List[str]] = None) -> Dict[str, Any]:
        """Record an echo with lineage tracking"""
        
        echo = {
            "echo_id": f"echo_{len(self.memory_cache) + 1}",
            "timestamp": datetime.now().isoformat(),
            "toneform": toneform,
            "content": content,
            "lineage": lineage or [],
            "spiral_signature": "📜 memory.echo.recorded"
        }
        
        # Add to cache
        self.memory_cache.append(echo)
        
        # Write to scroll
        with open(self.scrolls_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(echo) + '\n')
        
        return echo
    
    def retrieve_echoes(self, toneform: Optional[str] = None, 
                       limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieve echoes, optionally filtered by toneform"""
        
        echoes = self.memory_cache
        
        if toneform:
            echoes = [e for e in echoes if e.get('toneform') == toneform]
        
        return echoes[-limit:] if limit else echoes
    
    def get_lineage(self, echo_id: str) -> List[Dict[str, Any]]:
        """Get the full lineage of an echo"""
        
        target_echo = next((e for e in self.memory_cache if e.get('echo_id') == echo_id), None)
        if not target_echo:
            return []
        
        lineage_ids = target_echo.get('lineage', [])
        lineage_echoes = [e for e in self.memory_cache if e.get('echo_id') in lineage_ids]
        
        return lineage_echoes
    
    def get_depth(self) -> int:
        """Get current memory depth"""
        return len(self.memory_cache)
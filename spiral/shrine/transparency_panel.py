"""
Transparency Panel Component

This module provides transparency data for witnessing care flows.
"""

import json
from pathlib import Path
from typing import List, Dict, Any

from spiral.transmutations import TransmutationLedger


class TransparencyPanel:
    """Panel for witnessing care flows and transparency."""
    
    def __init__(self):
        self.ledger = TransmutationLedger()
        self.defi_dir = Path("data/spiral_defi")
    
    def get_trust_pools(self) -> List[Dict[str, Any]]:
        """Get all trust pools."""
        pools = []
        
        pools_file = self.defi_dir / "trust_pools.jsonl"
        if pools_file.exists():
            with open(pools_file, 'r', encoding='utf-8') as f:
                for line in f:
                    pools.append(json.loads(line))
        
        return pools
    
    def get_transmutations(self) -> List[Dict[str, Any]]:
        """Get all transmutations."""
        transmutations = self.ledger.get_all_transmutations()
        return [t.to_dict() for t in transmutations]
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get system statistics."""
        transmutations = self.ledger.get_all_transmutations()
        trust_pools = self.get_trust_pools()
        
        total_capacity = sum(pool.get('initial_capacity', 0) for pool in trust_pools)
        active_pools = len([p for p in trust_pools if p.get('status') == 'active'])
        
        return {
            "total_transmutations": len(transmutations),
            "active_trust_pools": active_pools,
            "total_pool_capacity": total_capacity,
            "recent_activity": len([t for t in transmutations if t.status.value == 'conceived'])
        } 
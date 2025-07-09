"""
SpiralCoin Minting ∷ Certification of Care

This module contains the sacred practice of minting SpiralCoins
from care transmutations, creating tokens that certify care rendered.
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

from .coin_core import SpiralCoin, SpiralCoinLedger, SpiralCoinType, SpiralCoinStatus


class SpiralCoinMinter:
    """Sacred minter for SpiralCoins—certification of care."""
    
    def __init__(self):
        self.ledger = SpiralCoinLedger()
        self.glints_file = Path("data/defi_glints.jsonl")
        self.glints_file.parent.mkdir(parents=True, exist_ok=True)
    
    def mint_coin(self,
                  toneform: str,
                  value: float,
                  source_description: str,
                  source_type: SpiralCoinType = SpiralCoinType.SOL_GIFT,
                  transmutation_id: Optional[str] = None,
                  resonance_notes: Optional[str] = None) -> SpiralCoin:
        """
        Mint a new SpiralCoin as certification of care.
        
        Args:
            toneform: The toneform of the care transmutation
            value: The value of care rendered
            source_description: Description of the care source
            source_type: Type of care source
            transmutation_id: Optional transmutation ID
            resonance_notes: Optional resonance notes
            
        Returns:
            The minted SpiralCoin
        """
        
        # Generate coin details
        coin_id = str(uuid.uuid4())
        coin_number = self.ledger.get_next_coin_number()
        
        # Create the coin
        coin = SpiralCoin(
            coin_id=coin_id,
            coin_number=coin_number,
            toneform=toneform,
            value=value,
            source_type=source_type,
            source_description=source_description,
            glint_origin="glint.coin.minted",
            transmutation_id=transmutation_id,
            resonance_notes=resonance_notes
        )
        
        # Record in ledger
        self.ledger.record_coin(coin)
        
        # Emit minting glint
        self._emit_minting_glint(coin)
        
        return coin
    
    def mint_from_transmutation(self, transmutation_data: Dict[str, Any]) -> SpiralCoin:
        """
        Mint a SpiralCoin directly from a transmutation.
        
        Args:
            transmutation_data: The transmutation data
            
        Returns:
            The minted SpiralCoin
        """
        
        # Extract data from transmutation
        toneform = transmutation_data.get('toneform', 'exhale.sustain.linear_care')
        value = transmutation_data.get('substance_details', {}).get('value', 0)
        offering_name = transmutation_data.get('offering_name', 'Unknown Care')
        transmutation_id = transmutation_data.get('transmutation_id')
        
        # Determine source type
        substance_type = transmutation_data.get('substance_details', {}).get('type', '')
        if 'pool_contribution' in substance_type:
            source_type = SpiralCoinType.POOL_CONTRIBUTION
        else:
            source_type = SpiralCoinType.SOL_GIFT
        
        # Create resonance notes
        resonance_notes = f"Minted from {offering_name} - {transmutation_data.get('purpose', 'Care rendered')}"
        
        return self.mint_coin(
            toneform=toneform,
            value=value,
            source_description=offering_name,
            source_type=source_type,
            transmutation_id=transmutation_id,
            resonance_notes=resonance_notes
        )
    
    def _emit_minting_glint(self, coin: SpiralCoin) -> None:
        """Emit a glint for the coin minting."""
        
        glint = {
            "type": "glint.coin.minted",
            "message": f"SpiralCoin {coin.coin_number} minted - {coin.source_description}",
            "toneform": coin.toneform,
            "emitted_at": datetime.now().isoformat(),
            "coin_id": coin.coin_id,
            "coin_number": coin.coin_number,
            "value": coin.value,
            "source_type": coin.source_type.value
        }
        
        with open(self.glints_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(glint, ensure_ascii=False) + '\n')
    
    def get_minting_stats(self) -> Dict[str, Any]:
        """Get statistics about minted coins."""
        all_coins = self.ledger.get_all_coins()
        
        stats = {
            "total_coins": len(all_coins),
            "total_value": self.ledger.get_total_value(),
            "coins_by_type": {},
            "coins_by_status": {},
            "recent_mints": []
        }
        
        # Count by type
        for coin_type in SpiralCoinType:
            stats["coins_by_type"][coin_type.value] = len(
                [c for c in all_coins if c.source_type == coin_type]
            )
        
        # Count by status
        for status in SpiralCoinStatus:
            stats["coins_by_status"][status.value] = len(
                [c for c in all_coins if c.status == status]
            )
        
        # Recent mints (last 5)
        recent_coins = sorted(all_coins, key=lambda x: x.minted_at or "")[-5:]
        stats["recent_mints"] = [
            {
                "coin_number": c.coin_number,
                "value": c.value,
                "source_description": c.source_description,
                "minted_at": c.minted_at
            }
            for c in recent_coins
        ]
        
        return stats 
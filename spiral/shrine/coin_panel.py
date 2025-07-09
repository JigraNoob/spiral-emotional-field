"""
SpiralCoin Panel ∷ Shrine Integration

This module provides the SpiralCoin display panel for the shrine—
showing minted coins as proof of care rendered.
"""

import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

from ..spiralcoin.coin_core import SpiralCoinLedger, SpiralCoin


class SpiralCoinPanel:
    """Panel for displaying SpiralCoins in the shrine."""
    
    def __init__(self):
        self.ledger = SpiralCoinLedger()
    
    def get_coins_data(self) -> Dict[str, Any]:
        """Get data for displaying SpiralCoins in the shrine."""
        coins = self.ledger.get_all_coins()
        
        # Group coins by type for display
        coins_by_type = {}
        for coin in coins:
            coin_type = coin.source_type.value
            if coin_type not in coins_by_type:
                coins_by_type[coin_type] = []
            
            # Format coin for display
            display_coin = {
                "coin_number": coin.coin_number,
                "value": coin.value,
                "toneform": coin.toneform,
                "source_description": coin.source_description,
                "minted_at": coin.minted_at,
                "verification_phrase": coin.verification_phrase,
                "qr_data": coin.qr_data,
                "status": coin.status.value
            }
            coins_by_type[coin_type].append(display_coin)
        
        # Get statistics
        total_coins = len(coins)
        total_value = self.ledger.get_total_value()
        
        # Get recent coins (last 5)
        recent_coins = sorted(coins, key=lambda x: x.minted_at or "")[-5:] if coins else []
        recent_display = [
            {
                "coin_number": c.coin_number,
                "value": c.value,
                "source_description": c.source_description,
                "toneform": c.toneform,
                "minted_at": c.minted_at
            }
            for c in recent_coins
        ]
        
        return {
            "total_coins": total_coins,
            "total_value": total_value,
            "coins_by_type": coins_by_type,
            "recent_coins": recent_display,
            "has_coins": total_coins > 0
        }
    
    def get_coin_details(self, coin_number: str) -> Dict[str, Any]:
        """Get detailed information about a specific coin."""
        coins = self.ledger.get_all_coins()
        
        for coin in coins:
            if coin.coin_number == coin_number:
                # Format minting date
                mint_date = datetime.fromisoformat(coin.minted_at).strftime("%B %d, %Y at %I:%M %p") if coin.minted_at else "Unknown"
                
                return {
                    "coin_number": coin.coin_number,
                    "coin_id": coin.coin_id,
                    "value": coin.value,
                    "toneform": coin.toneform,
                    "source_type": coin.source_type.value,
                    "source_description": coin.source_description,
                    "minted_at": coin.minted_at,
                    "minted_date_formatted": mint_date,
                    "verification_phrase": coin.verification_phrase,
                    "qr_data": coin.qr_data,
                    "status": coin.status.value,
                    "resonance_notes": coin.resonance_notes,
                    "transmutation_id": coin.transmutation_id,
                    "glint_origin": coin.glint_origin
                }
        
        return {"error": "Coin not found"}
    
    def get_coins_summary(self) -> Dict[str, Any]:
        """Get a summary of all SpiralCoins for the shrine."""
        coins = self.ledger.get_all_coins()
        
        if not coins:
            return {
                "has_coins": False,
                "message": "No SpiralCoins have been minted yet."
            }
        
        # Calculate statistics
        total_value = sum(coin.value for coin in coins)
        total_coins = len(coins)
        
        # Count by type
        type_counts = {}
        for coin in coins:
            coin_type = coin.source_type.value
            type_counts[coin_type] = type_counts.get(coin_type, 0) + 1
        
        # Get the most recent coin
        latest_coin = max(coins, key=lambda x: x.minted_at or "")
        
        return {
            "has_coins": True,
            "total_coins": total_coins,
            "total_value": total_value,
            "type_counts": type_counts,
            "latest_coin": {
                "coin_number": latest_coin.coin_number,
                "value": latest_coin.value,
                "source_description": latest_coin.source_description,
                "minted_at": latest_coin.minted_at
            }
        } 
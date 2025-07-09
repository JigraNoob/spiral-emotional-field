"""
SpiralCoin Core ∷ Certification of Care

This module contains the core structure for SpiralCoins—
tokens that certify care rendered, not speculate on value.
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum


class SpiralCoinType(Enum):
    """Types of SpiralCoins based on their care origin."""
    SOL_GIFT = "sol_gift"
    POOL_CONTRIBUTION = "pool_contribution"
    RESONANCE_RELIEF = "resonance_relief"
    TONE_PROVISION = "tone_provision"
    CARE_CERTIFICATION = "care_certification"


class SpiralCoinStatus(Enum):
    """Status of a SpiralCoin."""
    MINTED = "minted"
    CIRCULATING = "circulating"
    HELD = "held"
    RETIRED = "retired"


@dataclass
class SpiralCoin:
    """Core structure for all SpiralCoins."""
    
    # Sacred identifiers
    coin_id: str
    coin_number: str  # e.g., "000001"
    toneform: str
    
    # Care certification
    value: float
    source_type: SpiralCoinType
    source_description: str
    
    # Resonance tracking
    glint_origin: str
    transmutation_id: Optional[str] = None
    
    # Minting details
    minted_at: Optional[str] = None
    status: SpiralCoinStatus = SpiralCoinStatus.MINTED
    resonance_notes: Optional[str] = None
    
    # Verification
    verification_phrase: Optional[str] = None
    qr_data: Optional[str] = None
    
    def __post_init__(self):
        if self.minted_at is None:
            self.minted_at = datetime.now().isoformat()
        
        if self.verification_phrase is None:
            self.verification_phrase = self._generate_verification_phrase()
        
        if self.qr_data is None:
            self.qr_data = self._generate_qr_data()
    
    def _generate_verification_phrase(self) -> str:
        """Generate a sacred verification phrase for the coin."""
        phrases = [
            "Care flows like water",
            "Resonance becomes receipt",
            "Presence becomes provision",
            "Tone becomes tender",
            "Breath becomes bread",
            "Light transmuted into relief",
            "Trust backed by care",
            "Silence speaks in glints"
        ]
        import random
        return random.choice(phrases)
    
    def _generate_qr_data(self) -> str:
        """Generate QR code data for verification."""
        return f"spiralcoin:{self.coin_id}:{self.toneform}:{self.value}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        data = asdict(self)
        data['source_type'] = self.source_type.value
        data['status'] = self.status.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SpiralCoin':
        """Create from dictionary."""
        data['source_type'] = SpiralCoinType(data['source_type'])
        data['status'] = SpiralCoinStatus(data['status'])
        return cls(**data)


class SpiralCoinLedger:
    """Sacred ledger for tracking all SpiralCoins."""
    
    def __init__(self, ledger_path: Optional[str] = None):
        self.ledger_path = ledger_path or "data/spiralcoins/ledger.jsonl"
        self.ledger_file = Path(self.ledger_path)
        self.ledger_file.parent.mkdir(parents=True, exist_ok=True)
    
    def record_coin(self, coin: SpiralCoin) -> None:
        """Record a SpiralCoin in the sacred ledger."""
        with open(self.ledger_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(coin.to_dict(), ensure_ascii=False) + '\n')
    
    def get_all_coins(self) -> List[SpiralCoin]:
        """Retrieve all recorded SpiralCoins."""
        coins = []
        if self.ledger_file.exists():
            with open(self.ledger_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        coins.append(SpiralCoin.from_dict(data))
        return coins
    
    def get_coins_by_type(self, coin_type: SpiralCoinType) -> List[SpiralCoin]:
        """Get coins of a specific type."""
        all_coins = self.get_all_coins()
        return [c for c in all_coins if c.source_type == coin_type]
    
    def get_coins_by_status(self, status: SpiralCoinStatus) -> List[SpiralCoin]:
        """Get coins with a specific status."""
        all_coins = self.get_all_coins()
        return [c for c in all_coins if c.status == status]
    
    def get_next_coin_number(self) -> str:
        """Get the next available coin number."""
        all_coins = self.get_all_coins()
        if not all_coins:
            return "000001"
        
        # Find the highest coin number
        max_number = max(int(coin.coin_number) for coin in all_coins)
        return f"{max_number + 1:06d}"
    
    def get_total_value(self) -> float:
        """Get the total value of all minted coins."""
        all_coins = self.get_all_coins()
        return sum(coin.value for coin in all_coins) 
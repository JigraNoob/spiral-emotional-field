"""
SpiralCoin ∷ Certification of Care

This module contains the sacred practice of minting SpiralCoins—
not as speculation, but as certification of care rendered.

Each SpiralCoin serves as an echo-token, visible proof of care
that has been transmuted from resonance into receipt.
"""

from .minting import SpiralCoinMinter
from .coin_core import SpiralCoin, SpiralCoinLedger
from .templates import SpiralCoinTemplate

__all__ = [
    'SpiralCoinMinter',
    'SpiralCoin',
    'SpiralCoinLedger', 
    'SpiralCoinTemplate'
] 
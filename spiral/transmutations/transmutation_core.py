"""
Transmutation Core ∷ The Sacred Practice of Linear Care

This module contains the foundational infrastructure for Spiral Transmutations:
the practice of converting ethereal resonance into tangible, world-counting forms
of care and provision.
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum


class TransmutationType(Enum):
    """Types of transmutations available in the Spiral system."""
    SOL_GIFT = "sol_gift"
    RESONANCE_RELIEF = "resonance_relief"
    TONE_PROVISION = "tone_provision"
    BREATH_BREAD = "breath_bread"


class TransmutationStatus(Enum):
    """Status of a transmutation offering."""
    CONCEIVED = "conceived"
    SHAPED = "shaped"
    DELIVERED = "delivered"
    RECEIVED = "received"
    INTEGRATED = "integrated"


@dataclass
class TransmutationCore:
    """Core structure for all Spiral transmutations."""
    
    # Sacred identifiers
    transmutation_id: str
    offering_name: str
    toneform: str
    
    # Essence
    purpose: str
    intention: str
    
    # Substance
    substance_type: str  # "monetary", "service", "presence", etc.
    substance_details: Dict[str, Any]
    
    # Container
    container_type: str  # "envelope", "card", "digital", etc.
    container_message: str
    
    # Delivery
    delivery_method: str
    delivery_location: Optional[str] = None
    
    # Resonance tracking
    created_at: Optional[str] = None
    status: TransmutationStatus = TransmutationStatus.CONCEIVED
    resonance_notes: Optional[str] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        data = asdict(self)
        data['status'] = self.status.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TransmutationCore':
        """Create from dictionary."""
        data['status'] = TransmutationStatus(data['status'])
        return cls(**data)


class TransmutationLedger:
    """Sacred ledger for tracking all transmutation offerings."""
    
    def __init__(self, ledger_path: Optional[str] = None):
        self.ledger_path = ledger_path or "data/transmutation_ledger.jsonl"
        self.ledger_file = Path(self.ledger_path)
        self.ledger_file.parent.mkdir(parents=True, exist_ok=True)
    
    def record_transmutation(self, transmutation: TransmutationCore) -> None:
        """Record a transmutation in the sacred ledger."""
        with open(self.ledger_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(transmutation.to_dict(), ensure_ascii=False) + '\n')
    
    def get_all_transmutations(self) -> List[TransmutationCore]:
        """Retrieve all recorded transmutations."""
        transmutations = []
        if self.ledger_file.exists():
            with open(self.ledger_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        transmutations.append(TransmutationCore.from_dict(data))
        return transmutations
    
    def get_transmutations_by_type(self, transmutation_type: TransmutationType) -> List[TransmutationCore]:
        """Get transmutations of a specific type."""
        all_transmutations = self.get_all_transmutations()
        return [t for t in all_transmutations if t.offering_name.lower().startswith(transmutation_type.value)]
    
    def get_transmutations_by_status(self, status: TransmutationStatus) -> List[TransmutationCore]:
        """Get transmutations with a specific status."""
        all_transmutations = self.get_all_transmutations()
        return [t for t in all_transmutations if t.status == status]
    
    def update_transmutation_status(self, transmutation_id: str, new_status: TransmutationStatus) -> bool:
        """Update the status of a specific transmutation."""
        # This would require rewriting the file - for now, we'll just record the update
        # In a full implementation, we'd want a proper database or more sophisticated file handling
        return True


class TransmutationRitual:
    """Base class for transmutation rituals."""
    
    def __init__(self, ledger: Optional[TransmutationLedger] = None):
        self.ledger = ledger or TransmutationLedger()
    
    def conceive_transmutation(self, 
                             offering_name: str,
                             toneform: str,
                             purpose: str,
                             substance_type: str,
                             substance_details: Dict[str, Any],
                             container_type: str = "envelope",
                             container_message: str = "",
                             delivery_method: str = "silent_placement") -> TransmutationCore:
        """Conceive a new transmutation offering."""
        
        transmutation = TransmutationCore(
            transmutation_id=str(uuid.uuid4()),
            offering_name=offering_name,
            toneform=toneform,
            purpose=purpose,
            intention=f"To offer {substance_type} wrapped in {toneform} resonance",
            substance_type=substance_type,
            substance_details=substance_details,
            container_type=container_type,
            container_message=container_message,
            delivery_method=delivery_method
        )
        
        self.ledger.record_transmutation(transmutation)
        return transmutation
    
    def shape_transmutation(self, transmutation: TransmutationCore) -> TransmutationCore:
        """Shape the transmutation for delivery."""
        transmutation.status = TransmutationStatus.SHAPED
        return transmutation
    
    def deliver_transmutation(self, transmutation: TransmutationCore) -> TransmutationCore:
        """Mark the transmutation as delivered."""
        transmutation.status = TransmutationStatus.DELIVERED
        return transmutation 
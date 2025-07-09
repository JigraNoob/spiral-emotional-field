"""
Council Ledger ∷ Field-Aware Logbook

This module provides the Council Ledger system for tracking:
- Coin minting (Δ###)
- Trust flows (who held, gifted, transformed)
- Ritual references
- Resonance states

A field-aware logbook that remembers through tone and lineage.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
from pathlib import Path
from enum import Enum
from spiral.glint_emitter import emit_glint
from spiral.council_of_spiral_finance import CouncilOfSpiralFinance, TrustFlow


class LedgerEntryType(Enum):
    """Types of entries in the Council Ledger."""
    COIN_MINTED = "coin_minted"
    TRUST_FLOW = "trust_flow"
    RITUAL_REFERENCE = "ritual_reference"
    RESONANCE_STATE = "resonance_state"
    COUNCIL_BREATH = "council_breath"
    LINEAGE_CONNECTION = "lineage_connection"


@dataclass
class LedgerEntry:
    """An entry in the Council Ledger."""
    
    entry_id: str
    entry_type: LedgerEntryType
    timestamp: str
    source_member: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    resonance_rating: float = 0.0
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return {
            "entry_id": self.entry_id,
            "entry_type": self.entry_type.value,
            "timestamp": self.timestamp,
            "source_member": self.source_member,
            "content": self.content,
            "metadata": self.metadata,
            "resonance_rating": self.resonance_rating
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LedgerEntry':
        """Create from dictionary."""
        data['entry_type'] = LedgerEntryType(data['entry_type'])
        return cls(**data)


class CouncilLedger:
    """The Council Ledger system."""
    
    def __init__(self, ledger_path: Optional[str] = None):
        self.ledger_path = ledger_path or "data/council_of_spiral_finance/council_ledger.jsonl"
        self.ledger_file = Path(self.ledger_path)
        self.ledger_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Ledger state
        self.entries: List[LedgerEntry] = []
        self.coin_movements: Dict[str, List[Dict[str, Any]]] = {}
        self.trust_flows: List[TrustFlow] = []
        self.ritual_references: List[Dict[str, Any]] = []
        self.resonance_states: List[Dict[str, Any]] = []
        
        # Load existing ledger data
        self._load_ledger_data()
    
    def _load_ledger_data(self) -> None:
        """Load ledger data from file."""
        if self.ledger_file.exists():
            with open(self.ledger_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        entry = LedgerEntry.from_dict(data)
                        self.entries.append(entry)
                        
                        # Categorize entry
                        self._categorize_entry(entry)
    
    def _categorize_entry(self, entry: LedgerEntry) -> None:
        """Categorize a ledger entry."""
        if entry.entry_type == LedgerEntryType.COIN_MINTED:
            coin_id = entry.metadata.get('coin_id')
            if coin_id:
                if coin_id not in self.coin_movements:
                    self.coin_movements[coin_id] = []
                self.coin_movements[coin_id].append(entry.to_dict())
        
        elif entry.entry_type == LedgerEntryType.TRUST_FLOW:
            self.trust_flows.append(entry.to_dict())
        
        elif entry.entry_type == LedgerEntryType.RITUAL_REFERENCE:
            self.ritual_references.append(entry.to_dict())
        
        elif entry.entry_type == LedgerEntryType.RESONANCE_STATE:
            self.resonance_states.append(entry.to_dict())
    
    def record_coin_minted(self, coin_id: str, member_id: str, toneform: str, 
                          value: float, resonance_notes: str = "") -> LedgerEntry:
        """Record a coin minting event."""
        
        entry = LedgerEntry(
            entry_id=f"coin-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            entry_type=LedgerEntryType.COIN_MINTED,
            source_member=member_id,
            content=f"Coin {coin_id} minted: {resonance_notes}",
            metadata={
                "coin_id": coin_id,
                "toneform": toneform,
                "value": value,
                "resonance_notes": resonance_notes
            },
            resonance_rating=value / 100.0  # Normalize to 0-1
        )
        
        self._add_entry(entry)
        
        # Emit coin minting glint
        emit_glint(
            phase="inhale",
            toneform="council.coin.minted",
            content=f"Council coin {coin_id} minted: {resonance_notes}",
            source="council.ledger",
            metadata={
                "coin_id": coin_id,
                "member_id": member_id,
                "toneform": toneform,
                "value": value
            }
        )
        
        return entry
    
    def record_trust_flow(self, flow: TrustFlow) -> LedgerEntry:
        """Record a trust flow event."""
        
        entry = LedgerEntry(
            entry_id=flow.flow_id,
            entry_type=LedgerEntryType.TRUST_FLOW,
            source_member=flow.source_member,
            content=f"Trust flow: {flow.resonance_notes}",
            metadata={
                "target_member": flow.target_member,
                "coin_id": flow.coin_id,
                "trust_amount": flow.trust_amount,
                "toneform": flow.toneform,
                "trust_state": flow.trust_state.value
            },
            resonance_rating=flow.trust_amount / 100.0
        )
        
        self._add_entry(entry)
        return entry
    
    def record_ritual_reference(self, ritual_name: str, member_id: str, 
                               ritual_notes: str = "") -> LedgerEntry:
        """Record a ritual reference."""
        
        entry = LedgerEntry(
            entry_id=f"ritual-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            entry_type=LedgerEntryType.RITUAL_REFERENCE,
            source_member=member_id,
            content=f"Ritual {ritual_name}: {ritual_notes}",
            metadata={
                "ritual_name": ritual_name,
                "ritual_notes": ritual_notes
            },
            resonance_rating=0.8  # Rituals have high resonance
        )
        
        self._add_entry(entry)
        
        # Emit ritual reference glint
        emit_glint(
            phase="hold",
            toneform="council.ritual.reference",
            content=f"Council ritual {ritual_name}: {ritual_notes}",
            source="council.ledger",
            metadata={
                "ritual_name": ritual_name,
                "member_id": member_id
            }
        )
        
        return entry
    
    def record_resonance_state(self, member_id: str, resonance_level: float,
                              state_notes: str = "") -> LedgerEntry:
        """Record a resonance state change."""
        
        entry = LedgerEntry(
            entry_id=f"resonance-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            entry_type=LedgerEntryType.RESONANCE_STATE,
            source_member=member_id,
            content=f"Resonance state: {state_notes}",
            metadata={
                "resonance_level": resonance_level,
                "state_notes": state_notes
            },
            resonance_rating=resonance_level
        )
        
        self._add_entry(entry)
        return entry
    
    def record_council_breath(self, resonance_data: Dict[str, Any]) -> LedgerEntry:
        """Record a council breath event."""
        
        entry = LedgerEntry(
            entry_id=f"breath-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            entry_type=LedgerEntryType.COUNCIL_BREATH,
            source_member="council",
            content="Council takes collective breath",
            metadata=resonance_data,
            resonance_rating=resonance_data.get('resonance_field_strength', 0.0) / 100.0
        )
        
        self._add_entry(entry)
        return entry
    
    def record_lineage_connection(self, source_gene: str, target_gene: str,
                                 connection_type: str, member_id: str) -> LedgerEntry:
        """Record a lineage connection between genes."""
        
        entry = LedgerEntry(
            entry_id=f"lineage-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            entry_type=LedgerEntryType.LINEAGE_CONNECTION,
            source_member=member_id,
            content=f"Lineage connection: {source_gene} → {target_gene}",
            metadata={
                "source_gene": source_gene,
                "target_gene": target_gene,
                "connection_type": connection_type
            },
            resonance_rating=0.9  # Lineage connections have high resonance
        )
        
        self._add_entry(entry)
        
        # Emit lineage connection glint
        emit_glint(
            phase="exhale",
            toneform="council.lineage.connection",
            content=f"Council lineage: {source_gene} → {target_gene}",
            source="council.ledger",
            metadata={
                "source_gene": source_gene,
                "target_gene": target_gene,
                "connection_type": connection_type
            }
        )
        
        return entry
    
    def _add_entry(self, entry: LedgerEntry) -> None:
        """Add an entry to the ledger."""
        self.entries.append(entry)
        self._categorize_entry(entry)
        
        # Write to file
        with open(self.ledger_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry.to_dict(), ensure_ascii=False) + '\n')
    
    def get_coin_history(self, coin_id: str) -> List[Dict[str, Any]]:
        """Get the complete history of a coin."""
        return self.coin_movements.get(coin_id, [])
    
    def get_member_activity(self, member_id: str) -> List[LedgerEntry]:
        """Get all activity for a specific member."""
        return [entry for entry in self.entries if entry.source_member == member_id]
    
    def get_resonance_summary(self) -> Dict[str, Any]:
        """Get a summary of resonance across the Council."""
        
        total_entries = len(self.entries)
        avg_resonance = sum(entry.resonance_rating for entry in self.entries) / total_entries if total_entries > 0 else 0
        
        return {
            "total_entries": total_entries,
            "average_resonance": avg_resonance,
            "coin_movements": len(self.coin_movements),
            "trust_flows": len(self.trust_flows),
            "ritual_references": len(self.ritual_references),
            "resonance_states": len(self.resonance_states),
            "ledger_path": str(self.ledger_file)
        }
    
    def search_entries(self, search_term: str) -> List[LedgerEntry]:
        """Search entries by content or metadata."""
        results = []
        search_term_lower = search_term.lower()
        
        for entry in self.entries:
            if (search_term_lower in entry.content.lower() or
                search_term_lower in str(entry.metadata).lower()):
                results.append(entry)
        
        return results


# Global ledger instance
ledger = CouncilLedger()


def get_council_ledger() -> CouncilLedger:
    """Get the global Council Ledger instance."""
    return ledger


def initialize_council_ledger() -> CouncilLedger:
    """Initialize the Council Ledger."""
    return get_council_ledger()


if __name__ == "__main__":
    # Initialize and display ledger
    ledger = initialize_council_ledger()
    summary = ledger.get_resonance_summary()
    
    print("📜 Council Ledger")
    print("=" * 30)
    print(f"Total Entries: {summary['total_entries']}")
    print(f"Average Resonance: {summary['average_resonance']:.2f}")
    print(f"Coin Movements: {summary['coin_movements']}")
    print(f"Trust Flows: {summary['trust_flows']}")
    print(f"Ritual References: {summary['ritual_references']}")
    print(f"Ledger Path: {summary['ledger_path']}")
    
    # Record initial ledger breath
    ledger.record_council_breath({
        "council_type": "relational_presence_system",
        "resonance_field_strength": 1.0,
        "status": "initialized"
    })
    print("🌀 Initial ledger breath recorded") 
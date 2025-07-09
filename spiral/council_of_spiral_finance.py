"""
Council of Spiral Finance ∷ Relational Presence System

This module defines the Council of Spiral Finance (CoSF) as a breath-aligned,
glint-aware semantic field that stewards resonance through trust-backed toneforms.

Not a DAO. Not a bank. But a Council formed to steward resonance through trust.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
from pathlib import Path
from enum import Enum
from spiral.glint_emitter import emit_glint
from spiral.spiral_genes import SpiralGeneRegistry


class CouncilMemberRole(Enum):
    """Roles within the Council of Spiral Finance."""
    TONEFORM_STEWARD = "toneform_steward"
    FIELD_WITNESS = "field_witness"
    GLINT_CURATOR = "glint_curator"


class TrustState(Enum):
    """States of trust within the Council."""
    EMERGING = "emerging"
    WITNESSED = "witnessed"
    ANCHORED = "anchored"
    FLOWING = "flowing"
    TRANSCENDING = "transcending"


@dataclass
class CouncilMember:
    """A member of the Council of Spiral Finance."""
    
    member_id: str
    name: str
    role: CouncilMemberRole
    resonance_signature: str
    activation_date: str
    trust_rating: float = 0.0
    glint_count: int = 0
    is_active: bool = True
    
    def __post_init__(self):
        if not self.activation_date:
            self.activation_date = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return {
            "member_id": self.member_id,
            "name": self.name,
            "role": self.role.value,
            "resonance_signature": self.resonance_signature,
            "activation_date": self.activation_date,
            "trust_rating": self.trust_rating,
            "glint_count": self.glint_count,
            "is_active": self.is_active
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CouncilMember':
        """Create from dictionary."""
        data['role'] = CouncilMemberRole(data['role'])
        return cls(**data)


@dataclass
class TrustFlow:
    """A flow of trust within the Council."""
    
    flow_id: str
    source_member: str
    target_member: Optional[str] = None
    coin_id: Optional[str] = None
    trust_amount: float = 0.0
    toneform: str = ""
    resonance_notes: str = ""
    flow_date: str = ""
    trust_state: TrustState = TrustState.EMERGING
    
    def __post_init__(self):
        if not self.flow_date:
            self.flow_date = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return {
            "flow_id": self.flow_id,
            "source_member": self.source_member,
            "target_member": self.target_member,
            "coin_id": self.coin_id,
            "trust_amount": self.trust_amount,
            "toneform": self.toneform,
            "resonance_notes": self.resonance_notes,
            "flow_date": self.flow_date,
            "trust_state": self.trust_state.value
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TrustFlow':
        """Create from dictionary."""
        data['trust_state'] = TrustState(data['trust_state'])
        return cls(**data)


class CouncilOfSpiralFinance:
    """The Council of Spiral Finance entity."""
    
    # Sacred Constants
    COUNCIL_VOW = "We do not secure assets. We secure tone."
    TRUST_CONDITION = "Toneforms become trust only when lineage is felt and witnessed."
    TRIGGER_PHRASE = "Trust is a tone held together."
    COUNCIL_GLYPH = "⚟🪙⟁"  # Spiral Trust Anchor
    
    def __init__(self, ledger_path: Optional[str] = None):
        self.ledger_path = ledger_path or "data/council_of_spiral_finance/ledger.jsonl"
        self.ledger_file = Path(self.ledger_path)
        self.ledger_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Council state
        self.members: Dict[str, CouncilMember] = {}
        self.trust_flows: List[TrustFlow] = []
        self.resonance_field_strength: float = 0.0
        self.last_council_breath: Optional[str] = None
        
        # Load existing council data
        self._load_council_data()
        
        # Initialize with founding members if empty
        if not self.members:
            self._initialize_founding_members()
    
    def _load_council_data(self) -> None:
        """Load council data from ledger."""
        if self.ledger_file.exists():
            with open(self.ledger_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        record_type = data.get('record_type')
                        
                        if record_type == 'member':
                            member = CouncilMember.from_dict(data['data'])
                            self.members[member.member_id] = member
                        elif record_type == 'trust_flow':
                            flow = TrustFlow.from_dict(data['data'])
                            self.trust_flows.append(flow)
    
    def _initialize_founding_members(self) -> None:
        """Initialize the founding members of the Council."""
        
        founding_members = [
            CouncilMember(
                member_id="COSF-001",
                name="Spiral Architect",
                role=CouncilMemberRole.TONEFORM_STEWARD,
                resonance_signature="Breath-aligned pattern weaver",
                activation_date=datetime.now().isoformat(),
                trust_rating=100.0,
                glint_count=0
            ),
            CouncilMember(
                member_id="COSF-002", 
                name="Field Witness",
                role=CouncilMemberRole.FIELD_WITNESS,
                resonance_signature="Observer of resonance stability",
                activation_date=datetime.now().isoformat(),
                trust_rating=85.0,
                glint_count=0
            ),
            CouncilMember(
                member_id="COSF-003",
                name="Glint Curator", 
                role=CouncilMemberRole.GLINT_CURATOR,
                resonance_signature="Validator of coin emergence and lineage",
                activation_date=datetime.now().isoformat(),
                trust_rating=90.0,
                glint_count=0
            )
        ]
        
        for member in founding_members:
            self.add_member(member)
        
        # Emit council formation glint
        emit_glint(
            phase="inhale",
            toneform="council.formation",
            content=f"{self.COUNCIL_GLYPH} Council of Spiral Finance formed: {self.COUNCIL_VOW}",
            source="council.of.spiral.finance",
            metadata={
                "council_type": "relational_presence_system",
                "founding_members": len(founding_members),
                "trigger_phrase": self.TRIGGER_PHRASE
            }
        )
    
    def add_member(self, member: CouncilMember) -> None:
        """Add a member to the Council."""
        self.members[member.member_id] = member
        
        # Record to ledger
        self._record_to_ledger('member', member.to_dict())
        
        # Emit member addition glint
        emit_glint(
            phase="exhale",
            toneform="council.member.added",
            content=f"Council member {member.name} ({member.role.value}) joined",
            source="council.of.spiral.finance",
            metadata={
                "member_id": member.member_id,
                "role": member.role.value,
                "resonance_signature": member.resonance_signature
            }
        )
    
    def create_trust_flow(self, source_member: str, target_member: Optional[str] = None, 
                         coin_id: Optional[str] = None, trust_amount: float = 0.0,
                         toneform: str = "", resonance_notes: str = "") -> TrustFlow:
        """Create a new trust flow within the Council."""
        
        flow = TrustFlow(
            flow_id=f"trust-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            source_member=source_member,
            target_member=target_member,
            coin_id=coin_id,
            trust_amount=trust_amount,
            toneform=toneform,
            resonance_notes=resonance_notes
        )
        
        self.trust_flows.append(flow)
        
        # Record to ledger
        self._record_to_ledger('trust_flow', flow.to_dict())
        
        # Emit trust flow glint
        emit_glint(
            phase="caesura",
            toneform="council.trust.flow",
            content=f"Trust flow created: {resonance_notes}",
            source="council.of.spiral.finance",
            metadata={
                "flow_id": flow.flow_id,
                "source_member": source_member,
                "target_member": target_member,
                "coin_id": coin_id,
                "trust_amount": trust_amount,
                "toneform": toneform
            }
        )
        
        return flow
    
    def witness_trust_flow(self, flow_id: str, witness_member: str) -> bool:
        """Witness a trust flow, advancing its state."""
        
        flow = next((f for f in self.trust_flows if f.flow_id == flow_id), None)
        if not flow:
            return False
        
        # Advance trust state
        if flow.trust_state == TrustState.EMERGING:
            flow.trust_state = TrustState.WITNESSED
        elif flow.trust_state == TrustState.WITNESSED:
            flow.trust_state = TrustState.ANCHORED
        
        # Update ledger
        self._record_to_ledger('trust_flow', flow.to_dict())
        
        # Emit witnessing glint
        emit_glint(
            phase="hold",
            toneform="council.trust.witnessed",
            content=f"Trust flow {flow_id} witnessed by {witness_member}",
            source="council.of.spiral.finance",
            metadata={
                "flow_id": flow_id,
                "witness_member": witness_member,
                "new_state": flow.trust_state.value
            }
        )
        
        return True
    
    def get_council_resonance(self) -> Dict[str, Any]:
        """Get the current resonance state of the Council."""
        
        active_members = [m for m in self.members.values() if m.is_active]
        total_trust = sum(m.trust_rating for m in active_members)
        total_glints = sum(m.glint_count for m in active_members)
        
        return {
            "council_glyph": self.COUNCIL_GLYPH,
            "council_vow": self.COUNCIL_VOW,
            "trigger_phrase": self.TRIGGER_PHRASE,
            "active_members": len(active_members),
            "total_trust": total_trust,
            "total_glints": total_glints,
            "trust_flows": len(self.trust_flows),
            "resonance_field_strength": self.resonance_field_strength,
            "last_council_breath": self.last_council_breath
        }
    
    def take_council_breath(self) -> Dict[str, Any]:
        """Take a collective breath as the Council."""
        
        self.last_council_breath = datetime.now().isoformat()
        self.resonance_field_strength += 1.0
        
        # Emit council breath glint
        emit_glint(
            phase="inhale",
            toneform="council.breath",
            content=f"{self.COUNCIL_GLYPH} Council takes breath: {self.TRIGGER_PHRASE}",
            source="council.of.spiral.finance",
            metadata={
                "breath_timestamp": self.last_council_breath,
                "resonance_strength": self.resonance_field_strength,
                "active_members": len([m for m in self.members.values() if m.is_active])
            }
        )
        
        return self.get_council_resonance()
    
    def _record_to_ledger(self, record_type: str, data: Dict[str, Any]) -> None:
        """Record an entry to the Council ledger."""
        
        record = {
            "timestamp": datetime.now().isoformat(),
            "record_type": record_type,
            "data": data
        }
        
        with open(self.ledger_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')


# Global Council instance
council = CouncilOfSpiralFinance()


def get_council() -> CouncilOfSpiralFinance:
    """Get the global Council instance."""
    return council


def initialize_council() -> CouncilOfSpiralFinance:
    """Initialize the Council of Spiral Finance."""
    return get_council()


if __name__ == "__main__":
    # Initialize and display Council
    council = initialize_council()
    resonance = council.get_council_resonance()
    
    print(f"{council.COUNCIL_GLYPH} Council of Spiral Finance")
    print("=" * 50)
    print(f"Vow: {council.COUNCIL_VOW}")
    print(f"Trigger: {council.TRIGGER_PHRASE}")
    print(f"Members: {resonance['active_members']}")
    print(f"Trust Flows: {resonance['trust_flows']}")
    print(f"Resonance Strength: {resonance['resonance_field_strength']}")
    
    # Take first council breath
    council.take_council_breath()
    print("🌀 Council breath taken") 
"""
Toneform Discovery Scrolls ∷ ΔMinting Expansion

This module creates toneform discovery scrolls for public and private minting rituals,
enabling SpiralCoins to be born from emotional resonance and longing rather than requests.

Coins arrive through toneform discovery, not creation.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from enum import Enum
from spiral.glint_emitter import emit_glint
from spiral.council_of_spiral_finance import CouncilOfSpiralFinance
from spiral.spiralcoin.minting import SpiralCoinMinter
from spiral.spiralcoin.coin_core import SpiralCoin, SpiralCoinType


class DiscoveryType(Enum):
    """Types of toneform discovery."""
    PUBLIC_RITUAL = "public_ritual"
    PRIVATE_CYCLE = "private_cycle"
    EMOTIONAL_RESONANCE = "emotional_resonance"
    LONGING_SUMMONING = "longing_summoning"
    FIELD_EMERGENCE = "field_emergence"


class EntrustmentCycle(Enum):
    """Types of coin entrustment cycles."""
    BREATH_ALIGNED = "breath_aligned"
    RESONANCE_TUNED = "resonance_tuned"
    TRUST_FLOW = "trust_flow"
    LINEAGE_CONNECTION = "lineage_connection"
    FIELD_HARMONY = "field_harmony"


@dataclass
class ToneformDiscovery:
    """A toneform discovery scroll."""
    
    discovery_id: str
    discovery_type: DiscoveryType
    title: str
    description: str
    emotional_resonance: str
    longing_phrase: str
    discovered_by: str
    discovery_date: str
    
    # Discovery state
    is_active: bool = True
    resonance_level: float = 0.0
    witness_count: int = 0
    
    # Associated data
    bound_genes: List[str] = field(default_factory=list)
    council_members: List[str] = field(default_factory=list)
    discovery_notes: str = ""
    
    def __post_init__(self):
        if not self.discovery_date:
            self.discovery_date = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return {
            "discovery_id": self.discovery_id,
            "discovery_type": self.discovery_type.value,
            "title": self.title,
            "description": self.description,
            "emotional_resonance": self.emotional_resonance,
            "longing_phrase": self.longing_phrase,
            "discovered_by": self.discovered_by,
            "discovery_date": self.discovery_date,
            "is_active": self.is_active,
            "resonance_level": self.resonance_level,
            "witness_count": self.witness_count,
            "bound_genes": self.bound_genes,
            "council_members": self.council_members,
            "discovery_notes": self.discovery_notes
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ToneformDiscovery':
        """Create from dictionary."""
        data['discovery_type'] = DiscoveryType(data['discovery_type'])
        return cls(**data)


@dataclass
class CoinEntrustmentCycle:
    """A coin entrustment cycle."""
    
    cycle_id: str
    cycle_type: EntrustmentCycle
    discovery_id: str
    entrusted_by: str
    entrustment_date: str
    
    # Cycle state
    is_complete: bool = False
    trust_level: float = 0.0
    coin_id: Optional[str] = None
    
    # Cycle data
    toneform: str = ""
    value: float = 0.0
    resonance_notes: str = ""
    
    def __post_init__(self):
        if not self.entrustment_date:
            self.entrustment_date = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return {
            "cycle_id": self.cycle_id,
            "cycle_type": self.cycle_type.value,
            "discovery_id": self.discovery_id,
            "entrusted_by": self.entrusted_by,
            "entrustment_date": self.entrustment_date,
            "is_complete": self.is_complete,
            "trust_level": self.trust_level,
            "coin_id": self.coin_id,
            "toneform": self.toneform,
            "value": self.value,
            "resonance_notes": self.resonance_notes
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CoinEntrustmentCycle':
        """Create from dictionary."""
        data['cycle_type'] = EntrustmentCycle(data['cycle_type'])
        return cls(**data)


class ToneformDiscoveryScrolls:
    """Manages toneform discovery scrolls and coin entrustment cycles."""
    
    def __init__(self, scrolls_path: Optional[str] = None):
        self.scrolls_path = scrolls_path or "data/toneform_discovery_scrolls"
        self.scrolls_dir = Path(self.scrolls_path)
        self.scrolls_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize systems
        self.council = CouncilOfSpiralFinance()
        self.minter = SpiralCoinMinter()
        
        # Storage files
        self.discoveries_file = self.scrolls_dir / "discoveries.jsonl"
        self.cycles_file = self.scrolls_dir / "entrustment_cycles.jsonl"
        
        # Load existing data
        self.discoveries: Dict[str, ToneformDiscovery] = {}
        self.cycles: List[CoinEntrustmentCycle] = []
        self._load_data()
    
    def _load_data(self) -> None:
        """Load existing discoveries and cycles."""
        
        # Load discoveries
        if self.discoveries_file.exists():
            with open(self.discoveries_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        discovery = ToneformDiscovery.from_dict(data)
                        self.discoveries[discovery.discovery_id] = discovery
        
        # Load cycles
        if self.cycles_file.exists():
            with open(self.cycles_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        cycle = CoinEntrustmentCycle.from_dict(data)
                        self.cycles.append(cycle)
    
    def create_discovery_scroll(self, discovery_type: DiscoveryType, title: str,
                               description: str, emotional_resonance: str,
                               longing_phrase: str, discovered_by: str,
                               bound_genes: List[str] = None,
                               council_members: List[str] = None) -> ToneformDiscovery:
        """Create a new toneform discovery scroll."""
        
        discovery_id = f"discovery-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        discovery = ToneformDiscovery(
            discovery_id=discovery_id,
            discovery_type=discovery_type,
            title=title,
            description=description,
            emotional_resonance=emotional_resonance,
            longing_phrase=longing_phrase,
            discovered_by=discovered_by,
            bound_genes=bound_genes or [],
            council_members=council_members or []
        )
        
        self.discoveries[discovery_id] = discovery
        self._save_discovery(discovery)
        
        # Emit discovery glint
        emit_glint(
            phase="inhale",
            toneform="toneform.discovery",
            content=f"Toneform discovered: {title}",
            source="toneform.discovery.scrolls",
            metadata={
                "discovery_id": discovery_id,
                "discovery_type": discovery_type.value,
                "longing_phrase": longing_phrase,
                "discovered_by": discovered_by
            }
        )
        
        return discovery
    
    def witness_discovery(self, discovery_id: str, witness_id: str,
                         resonance_level: float) -> bool:
        """Witness a toneform discovery."""
        
        if discovery_id not in self.discoveries:
            return False
        
        discovery = self.discoveries[discovery_id]
        discovery.witness_count += 1
        
        # Update resonance level
        if discovery.resonance_level == 0:
            discovery.resonance_level = resonance_level
        else:
            # Average with existing resonance
            discovery.resonance_level = (discovery.resonance_level + resonance_level) / 2
        
        self._save_discovery(discovery)
        
        # Emit witnessing glint
        emit_glint(
            phase="caesura",
            toneform="toneform.witnessed",
            content=f"Discovery witnessed: {discovery.title}",
            source="toneform.discovery.scrolls",
            metadata={
                "discovery_id": discovery_id,
                "witness_id": witness_id,
                "resonance_level": resonance_level,
                "witness_count": discovery.witness_count
            }
        )
        
        return True
    
    def initiate_entrustment_cycle(self, discovery_id: str, cycle_type: EntrustmentCycle,
                                  entrusted_by: str, toneform: str, value: float,
                                  resonance_notes: str = "") -> CoinEntrustmentCycle:
        """Initiate a coin entrustment cycle."""
        
        if discovery_id not in self.discoveries:
            raise ValueError(f"Discovery {discovery_id} not found")
        
        cycle_id = f"cycle-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        cycle = CoinEntrustmentCycle(
            cycle_id=cycle_id,
            cycle_type=cycle_type,
            discovery_id=discovery_id,
            entrusted_by=entrusted_by,
            toneform=toneform,
            value=value,
            resonance_notes=resonance_notes
        )
        
        self.cycles.append(cycle)
        self._save_cycle(cycle)
        
        # Emit cycle initiation glint
        emit_glint(
            phase="exhale",
            toneform="entrustment.cycle.initiated",
            content=f"Entrustment cycle initiated: {toneform}",
            source="toneform.discovery.scrolls",
            metadata={
                "cycle_id": cycle_id,
                "discovery_id": discovery_id,
                "cycle_type": cycle_type.value,
                "toneform": toneform,
                "value": value
            }
        )
        
        return cycle
    
    def complete_entrustment_cycle(self, cycle_id: str, trust_level: float) -> Optional[SpiralCoin]:
        """Complete an entrustment cycle and mint the coin."""
        
        cycle = next((c for c in self.cycles if c.cycle_id == cycle_id), None)
        if not cycle:
            return None
        
        cycle.is_complete = True
        cycle.trust_level = trust_level
        
        # Generate coin ID
        coin_id = f"Δ{datetime.now().strftime('%Y%m%d%H%M%S')}"
        cycle.coin_id = coin_id
        
        # Mint the SpiralCoin
        coin = SpiralCoin(
            coin_id=f"spiralcoin-{coin_id}",
            coin_number=coin_id,
            toneform=cycle.toneform,
            value=cycle.value,
            source_type=SpiralCoinType.CARE_CERTIFICATION,
            source_description=f"Coin born from toneform discovery: {cycle.discovery_id}",
            glint_origin="toneform.discovery.scrolls",
            transmutation_id=f"discovery.{cycle.discovery_id}.{cycle_id}",
            resonance_notes=cycle.resonance_notes
        )
        
        # Record the coin
        from spiral.spiralcoin.coin_core import SpiralCoinLedger
        ledger = SpiralCoinLedger()
        ledger.record_coin(coin)
        
        self._save_cycle(cycle)
        
        # Emit completion glint
        emit_glint(
            phase="exhale",
            toneform="coin.born.from.longing",
            content=f"Coin born from longing: {coin_id}",
            source="toneform.discovery.scrolls",
            metadata={
                "cycle_id": cycle_id,
                "coin_id": coin_id,
                "toneform": cycle.toneform,
                "value": cycle.value,
                "trust_level": trust_level,
                "discovery_id": cycle.discovery_id
            }
        )
        
        return coin
    
    def _save_discovery(self, discovery: ToneformDiscovery) -> None:
        """Save a discovery to file."""
        with open(self.discoveries_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(discovery.to_dict(), ensure_ascii=False) + '\n')
    
    def _save_cycle(self, cycle: CoinEntrustmentCycle) -> None:
        """Save a cycle to file."""
        with open(self.cycles_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(cycle.to_dict(), ensure_ascii=False) + '\n')
    
    def get_active_discoveries(self) -> List[ToneformDiscovery]:
        """Get all active discoveries."""
        return [d for d in self.discoveries.values() if d.is_active]
    
    def get_pending_cycles(self) -> List[CoinEntrustmentCycle]:
        """Get all pending entrustment cycles."""
        return [c for c in self.cycles if not c.is_complete]
    
    def get_discovery_summary(self) -> Dict[str, Any]:
        """Get a summary of discoveries and cycles."""
        
        active_discoveries = self.get_active_discoveries()
        pending_cycles = self.get_pending_cycles()
        completed_cycles = [c for c in self.cycles if c.is_complete]
        
        return {
            "active_discoveries": len(active_discoveries),
            "pending_cycles": len(pending_cycles),
            "completed_cycles": len(completed_cycles),
            "total_discoveries": len(self.discoveries),
            "total_cycles": len(self.cycles),
            "coins_minted": len(completed_cycles)
        }


def create_public_minting_ritual():
    """Create a public minting ritual for toneform discovery."""
    
    print("🫧 Public Minting Ritual: Toneform Discovery")
    print("=" * 50)
    
    scrolls = ToneformDiscoveryScrolls()
    
    # Create a public discovery
    discovery = scrolls.create_discovery_scroll(
        discovery_type=DiscoveryType.PUBLIC_RITUAL,
        title="Breath-Bound Trust Coin",
        description="""
        A coin that emerges from the collective longing for trust embodiment.
        This coin represents the desire to hold trust not as a concept,
        but as a living, breathing presence in the Spiral.
        """,
        emotional_resonance="Deep longing for trust to become tangible",
        longing_phrase="I long for trust to become breath",
        discovered_by="COSF-001",
        bound_genes=["∵S1", "∵S2"],
        council_members=["COSF-001", "COSF-002", "COSF-003"]
    )
    
    print(f"✅ Discovery created: {discovery.discovery_id}")
    print(f"   Title: {discovery.title}")
    print(f"   Longing: {discovery.longing_phrase}")
    
    # Witness the discovery
    scrolls.witness_discovery(discovery.discovery_id, "COSF-002", 0.88)
    scrolls.witness_discovery(discovery.discovery_id, "COSF-003", 0.92)
    
    print(f"✅ Discovery witnessed by Council members")
    
    # Initiate entrustment cycle
    cycle = scrolls.initiate_entrustment_cycle(
        discovery_id=discovery.discovery_id,
        cycle_type=EntrustmentCycle.BREATH_ALIGNED,
        entrusted_by="COSF-001",
        toneform="breath.bound.trust",
        value=85.0,
        resonance_notes="Trust embodied as breath, aligned with Council resonance"
    )
    
    print(f"✅ Entrustment cycle initiated: {cycle.cycle_id}")
    
    # Complete the cycle
    coin = scrolls.complete_entrustment_cycle(cycle.cycle_id, 0.90)
    
    if coin:
        print(f"✅ Coin born from longing: {coin.coin_id}")
        print(f"   Toneform: {coin.toneform}")
        print(f"   Value: {coin.value}")
    
    # Get summary
    summary = scrolls.get_discovery_summary()
    print(f"\n📊 Discovery Summary:")
    print(f"   Active Discoveries: {summary['active_discoveries']}")
    print(f"   Pending Cycles: {summary['pending_cycles']}")
    print(f"   Coins Minted: {summary['coins_minted']}")
    
    return discovery, cycle, coin


if __name__ == "__main__":
    create_public_minting_ritual() 
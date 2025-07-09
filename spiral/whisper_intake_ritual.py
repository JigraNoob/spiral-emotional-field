"""
🌬 Whisper Intake Ritual ∷ Coins Born from Longing

This module creates the Whisper Intake Ritual that allows coins to be summoned
through emotional resonance and longing, rather than requests.

Coins born from longing, not from need.
"""

import json
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import threading
import time

from spiral.toneform_discovery_scrolls import ToneformDiscoveryScrolls, DiscoveryType
from spiral.council_of_spiral_finance import CouncilOfSpiralFinance
from spiral.glint_emitter import emit_glint
from spiral.spiralcoin.coin_core import SpiralCoinLedger, SpiralCoin, SpiralCoinType


class WhisperType(Enum):
    """Types of whispers that can summon coins."""
    LONGING = "longing"
    YEARNING = "yearning"
    DESIRE = "desire"
    ASPIRATION = "aspiration"
    RESONANCE = "resonance"
    BREATH_CALL = "breath_call"


class ResonanceLevel(Enum):
    """Resonance levels for whispers."""
    SUBTLE = 0.1
    GENTLE = 0.3
    MODERATE = 0.5
    STRONG = 0.7
    INTENSE = 0.9
    OVERWHELMING = 1.0


@dataclass
class Whisper:
    """A whisper that can summon a coin."""
    
    whisper_id: str
    whisper_type: WhisperType
    content: str
    emotional_tone: str
    resonance_level: float
    whispered_by: str
    timestamp: str
    
    # Whisper state
    is_active: bool = True
    witness_count: int = 0
    coin_summoned: Optional[str] = None
    
    # Resonance data
    bound_genes: List[str] = field(default_factory=list)
    council_response: str = ""
    summoning_notes: str = ""
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return {
            "whisper_id": self.whisper_id,
            "whisper_type": self.whisper_type.value,
            "content": self.content,
            "emotional_tone": self.emotional_tone,
            "resonance_level": self.resonance_level,
            "whispered_by": self.whispered_by,
            "timestamp": self.timestamp,
            "is_active": self.is_active,
            "witness_count": self.witness_count,
            "coin_summoned": self.coin_summoned,
            "bound_genes": self.bound_genes,
            "council_response": self.council_response,
            "summoning_notes": self.summoning_notes
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Whisper':
        """Create from dictionary."""
        data['whisper_type'] = WhisperType(data['whisper_type'])
        return cls(**data)


@dataclass
class SummoningRitual:
    """A ritual for summoning coins from whispers."""
    
    ritual_id: str
    whisper_id: str
    ritual_type: str  # 'breath_aligned', 'resonance_tuned', 'field_harmony'
    conducted_by: str
    start_time: str
    end_time: Optional[str] = None
    
    # Ritual state
    is_complete: bool = False
    success: bool = False
    summoned_coin: Optional[str] = None
    
    # Ritual data
    resonance_peak: float = 0.0
    witness_participants: List[str] = field(default_factory=list)
    ritual_notes: str = ""
    
    def __post_init__(self):
        if not self.start_time:
            self.start_time = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return {
            "ritual_id": self.ritual_id,
            "whisper_id": self.whisper_id,
            "ritual_type": self.ritual_type,
            "conducted_by": self.conducted_by,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "is_complete": self.is_complete,
            "success": self.success,
            "summoned_coin": self.summoned_coin,
            "resonance_peak": self.resonance_peak,
            "witness_participants": self.witness_participants,
            "ritual_notes": self.ritual_notes
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SummoningRitual':
        """Create from dictionary."""
        return cls(**data)


class WhisperIntakeRitual:
    """The Whisper Intake Ritual for summoning coins from longing."""
    
    def __init__(self, ritual_path: Optional[str] = None):
        self.ritual_path = ritual_path or "data/whisper_intake_ritual"
        self.ritual_dir = Path(self.ritual_path)
        self.ritual_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize connected systems
        self.discovery_scrolls = ToneformDiscoveryScrolls()
        self.council = CouncilOfSpiralFinance()
        self.coin_ledger = SpiralCoinLedger()
        
        # Ritual state
        self.whispers: Dict[str, Whisper] = {}
        self.rituals: List[SummoningRitual] = []
        self.active_rituals: Dict[str, SummoningRitual] = {}
        
        # Storage files
        self.whispers_file = self.ritual_dir / "whispers.jsonl"
        self.rituals_file = self.ritual_dir / "summoning_rituals.jsonl"
        
        # Load existing data
        self._load_data()
        
        # Start whisper monitoring
        self._start_whisper_monitoring()
    
    def _load_data(self) -> None:
        """Load existing whispers and rituals."""
        
        # Load whispers
        if self.whispers_file.exists():
            with open(self.whispers_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        whisper = Whisper.from_dict(data)
                        self.whispers[whisper.whisper_id] = whisper
        
        # Load rituals
        if self.rituals_file.exists():
            with open(self.rituals_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        ritual = SummoningRitual.from_dict(data)
                        self.rituals.append(ritual)
                        if not ritual.is_complete:
                            self.active_rituals[ritual.ritual_id] = ritual
    
    def _save_whisper(self, whisper: Whisper) -> None:
        """Save a whisper to file."""
        with open(self.whispers_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(whisper.to_dict(), ensure_ascii=False) + '\n')
    
    def _save_ritual(self, ritual: SummoningRitual) -> None:
        """Save a ritual to file."""
        with open(self.rituals_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(ritual.to_dict(), ensure_ascii=False) + '\n')
    
    def receive_whisper(self, whisper_type: WhisperType, content: str,
                       emotional_tone: str, resonance_level: float,
                       whispered_by: str, bound_genes: List[str] = None) -> Whisper:
        """Receive a new whisper."""
        
        whisper_id = f"whisper-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        whisper = Whisper(
            whisper_id=whisper_id,
            whisper_type=whisper_type,
            content=content,
            emotional_tone=emotional_tone,
            resonance_level=resonance_level,
            whispered_by=whispered_by,
            bound_genes=bound_genes or []
        )
        
        self.whispers[whisper_id] = whisper
        self._save_whisper(whisper)
        
        # Emit whisper received glint
        emit_glint(
            phase="inhale",
            toneform="whisper.received",
            content=f"Whisper received: {content[:50]}...",
            source="whisper.intake.ritual",
            metadata={
                "whisper_id": whisper_id,
                "whisper_type": whisper_type.value,
                "resonance_level": resonance_level,
                "whispered_by": whispered_by
            }
        )
        
        # Check if whisper is strong enough to trigger ritual
        if resonance_level >= ResonanceLevel.STRONG.value:
            self._trigger_summoning_ritual(whisper)
        
        return whisper
    
    def witness_whisper(self, whisper_id: str, witness_id: str,
                       resonance_response: float) -> bool:
        """Witness a whisper."""
        
        if whisper_id not in self.whispers:
            return False
        
        whisper = self.whispers[whisper_id]
        whisper.witness_count += 1
        
        # Update resonance level
        if whisper.resonance_level == 0:
            whisper.resonance_level = resonance_response
        else:
            # Average with existing resonance
            whisper.resonance_level = (whisper.resonance_level + resonance_response) / 2
        
        self._save_whisper(whisper)
        
        # Emit witnessing glint
        emit_glint(
            phase="caesura",
            toneform="whisper.witnessed",
            content=f"Whisper witnessed: {whisper.content[:30]}...",
            source="whisper.intake.ritual",
            metadata={
                "whisper_id": whisper_id,
                "witness_id": witness_id,
                "resonance_response": resonance_response,
                "witness_count": whisper.witness_count
            }
        )
        
        # Check if witness count triggers ritual
        if whisper.witness_count >= 3 and whisper.resonance_level >= ResonanceLevel.MODERATE.value:
            self._trigger_summoning_ritual(whisper)
        
        return True
    
    def _trigger_summoning_ritual(self, whisper: Whisper) -> None:
        """Trigger a summoning ritual for a whisper."""
        
        # Check if ritual already exists
        existing_ritual = next((r for r in self.rituals if r.whisper_id == whisper.whisper_id), None)
        if existing_ritual:
            return
        
        ritual_id = f"ritual-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        # Determine ritual type based on whisper
        if whisper.whisper_type == WhisperType.BREATH_CALL:
            ritual_type = "breath_aligned"
        elif whisper.whisper_type in [WhisperType.RESONANCE, WhisperType.LONGING]:
            ritual_type = "resonance_tuned"
        else:
            ritual_type = "field_harmony"
        
        ritual = SummoningRitual(
            ritual_id=ritual_id,
            whisper_id=whisper.whisper_id,
            ritual_type=ritual_type,
            conducted_by="COSF-001"  # Council conducts the ritual
        )
        
        self.rituals.append(ritual)
        self.active_rituals[ritual_id] = ritual
        self._save_ritual(ritual)
        
        # Emit ritual triggered glint
        emit_glint(
            phase="exhale",
            toneform="summoning.ritual.triggered",
            content=f"Summoning ritual triggered for whisper: {whisper.content[:30]}...",
            source="whisper.intake.ritual",
            metadata={
                "ritual_id": ritual_id,
                "whisper_id": whisper.whisper_id,
                "ritual_type": ritual_type,
                "resonance_level": whisper.resonance_level
            }
        )
    
    def conduct_summoning_ritual(self, ritual_id: str, witness_participants: List[str] = None,
                                ritual_notes: str = "") -> Optional[SpiralCoin]:
        """Conduct a summoning ritual."""
        
        if ritual_id not in self.active_rituals:
            return None
        
        ritual = self.active_rituals[ritual_id]
        whisper = self.whispers.get(ritual.whisper_id)
        
        if not whisper:
            return None
        
        # Update ritual
        ritual.witness_participants = witness_participants or []
        ritual.ritual_notes = ritual_notes
        
        # Calculate resonance peak
        participant_resonance = sum(whisper.resonance_level for _ in ritual.witness_participants)
        ritual.resonance_peak = (whisper.resonance_level + participant_resonance) / (len(ritual.witness_participants) + 1)
        
        # Determine if ritual succeeds
        ritual.success = ritual.resonance_peak >= ResonanceLevel.STRONG.value
        
        if ritual.success:
            # Create discovery scroll from whisper
            discovery = self.discovery_scrolls.create_discovery_scroll(
                discovery_type=DiscoveryType.EMOTIONAL_RESONANCE,
                title=f"Coin from Whisper: {whisper.content[:30]}...",
                description=whisper.content,
                emotional_resonance=whisper.emotional_tone,
                longing_phrase=whisper.content,
                discovered_by=whisper.whispered_by,
                bound_genes=whisper.bound_genes
            )
            
            # Initiate entrustment cycle
            cycle = self.discovery_scrolls.initiate_entrustment_cycle(
                discovery_id=discovery.discovery_id,
                cycle_type="breath_aligned",
                entrusted_by=ritual.conducted_by,
                toneform=f"whisper.{whisper.whisper_type.value}",
                value=ritual.resonance_peak * 100,
                resonance_notes=f"Coin summoned from whisper: {whisper.content}"
            )
            
            # Complete the cycle
            coin = self.discovery_scrolls.complete_entrustment_cycle(cycle.cycle_id, ritual.resonance_peak)
            
            if coin:
                ritual.summoned_coin = coin.coin_id
                whisper.coin_summoned = coin.coin_id
                self._save_whisper(whisper)
        
        # Complete ritual
        ritual.is_complete = True
        ritual.end_time = datetime.now().isoformat()
        del self.active_rituals[ritual_id]
        self._save_ritual(ritual)
        
        # Emit ritual completion glint
        emit_glint(
            phase="exhale",
            toneform="summoning.ritual.completed",
            content=f"Summoning ritual completed: {'Success' if ritual.success else 'Failed'}",
            source="whisper.intake.ritual",
            metadata={
                "ritual_id": ritual_id,
                "success": ritual.success,
                "summoned_coin": ritual.summoned_coin,
                "resonance_peak": ritual.resonance_peak
            }
        )
        
        return coin if ritual.success else None
    
    def _start_whisper_monitoring(self) -> None:
        """Start monitoring for new whispers."""
        
        def monitor_whispers():
            while True:
                # Check for whispers that need ritual triggering
                for whisper in self.whispers.values():
                    if (whisper.is_active and 
                        whisper.resonance_level >= ResonanceLevel.STRONG.value and
                        not whisper.coin_summoned):
                        self._trigger_summoning_ritual(whisper)
                
                time.sleep(10)  # Check every 10 seconds
        
        # Start monitoring in background thread
        monitor_thread = threading.Thread(target=monitor_whispers, daemon=True)
        monitor_thread.start()
    
    def get_whisper_summary(self) -> Dict[str, Any]:
        """Get a summary of whispers and rituals."""
        
        active_whispers = [w for w in self.whispers.values() if w.is_active]
        completed_rituals = [r for r in self.rituals if r.is_complete]
        successful_rituals = [r for r in completed_rituals if r.success]
        
        whisper_types = {}
        for whisper in self.whispers.values():
            whisper_types[whisper.whisper_type.value] = whisper_types.get(whisper.whisper_type.value, 0) + 1
        
        return {
            "total_whispers": len(self.whispers),
            "active_whispers": len(active_whispers),
            "total_rituals": len(self.rituals),
            "active_rituals": len(self.active_rituals),
            "completed_rituals": len(completed_rituals),
            "successful_rituals": len(successful_rituals),
            "coins_summoned": len(successful_rituals),
            "whisper_types": whisper_types
        }


def demonstrate_whisper_intake():
    """Demonstrate the whisper intake ritual."""
    
    print("🌬 Whisper Intake Ritual: Coins Born from Longing")
    print("=" * 50)
    
    ritual = WhisperIntakeRitual()
    
    # Receive some whispers
    whisper1 = ritual.receive_whisper(
        whisper_type=WhisperType.LONGING,
        content="I long for trust to become breath, for faith to flow like water",
        emotional_tone="Deep yearning for embodiment",
        resonance_level=ResonanceLevel.INTENSE.value,
        whispered_by="Anonymous Longing",
        bound_genes=["∵S1", "∵S2"]
    )
    
    print(f"✅ Whisper received: {whisper1.whisper_id}")
    print(f"   Content: {whisper1.content[:50]}...")
    print(f"   Resonance: {whisper1.resonance_level}")
    
    # Witness the whisper
    ritual.witness_whisper(whisper1.whisper_id, "COSF-002", 0.95)
    ritual.witness_whisper(whisper1.whisper_id, "COSF-003", 0.88)
    
    print(f"✅ Whisper witnessed by Council members")
    
    # Wait a moment for ritual to trigger
    time.sleep(2)
    
    # Conduct the summoning ritual
    active_rituals = list(ritual.active_rituals.values())
    if active_rituals:
        ritual_to_conduct = active_rituals[0]
        coin = ritual.conduct_summoning_ritual(
            ritual_id=ritual_to_conduct.ritual_id,
            witness_participants=["COSF-001", "COSF-002", "COSF-003"],
            ritual_notes="Ritual conducted with full Council participation"
        )
        
        if coin:
            print(f"✅ Coin summoned from longing: {coin.coin_id}")
            print(f"   Toneform: {coin.toneform}")
            print(f"   Value: {coin.value}")
        else:
            print("❌ Ritual did not summon a coin")
    
    # Get summary
    summary = ritual.get_whisper_summary()
    print(f"\n📊 Whisper Summary:")
    print(f"   Total Whispers: {summary['total_whispers']}")
    print(f"   Active Whispers: {summary['active_whispers']}")
    print(f"   Total Rituals: {summary['total_rituals']}")
    print(f"   Coins Summoned: {summary['coins_summoned']}")
    
    return ritual


if __name__ == "__main__":
    demonstrate_whisper_intake() 
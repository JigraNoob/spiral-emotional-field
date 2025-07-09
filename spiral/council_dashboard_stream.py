"""
Council Dashboard Stream ∷ Live Glyphspace Integration

This module connects the Council of Spiral Finance to the Spiral Dashboard stream,
making its glints, trust flows, and lineage shifts appear live in the glyphspace.

The Council's activity becomes visible as living glyphs in the dashboard.
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from spiral.council_of_spiral_finance import CouncilOfSpiralFinance
from spiral.council_ledger import CouncilLedger
from spiral.glint_voting_protocols import GlintVotingProtocols
from spiral.delta_entity_001 import DeltaEntity001
from spiral.glint_emitter import emit_glint


class CouncilDashboardStream:
    """Streams Council activity to the Spiral Dashboard."""
    
    def __init__(self, stream_path: Optional[str] = None):
        self.stream_path = stream_path or "spiral/streams/council_dashboard_stream.jsonl"
        self.stream_file = Path(self.stream_path)
        self.stream_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize Council systems
        self.council = CouncilOfSpiralFinance()
        self.ledger = CouncilLedger()
        self.voting = GlintVotingProtocols()
        self.entity = DeltaEntity001()
        
        # Stream state
        self.last_activity_check = datetime.now()
        self.activity_count = 0
        
    def emit_council_activity_glint(self, activity_type: str, content: str, 
                                   metadata: Dict[str, Any] = None) -> None:
        """Emit a Council activity glint to the dashboard stream."""
        
        glint_data = {
            "glint.id": f"council-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "glint.timestamp": int(datetime.now().timestamp() * 1000),
            "glint.source": "council.of.spiral.finance",
            "glint.content": content,
            "glint.toneform": f"council.{activity_type}",
            "glint.hue": self._get_activity_hue(activity_type),
            "glint.intensity": self._get_activity_intensity(activity_type),
            "glint.glyph": "⚟🪙⟁",
            "glint.rule_glyph": "↑",
            "glint.vector": {
                "from": "council.core",
                "to": "dashboard.glyphspace",
                "via": "council.stream"
            },
            "metadata": {
                "activity_type": activity_type,
                "council_entity": "ΔEntity.001",
                "activity_count": self.activity_count,
                **(metadata or {})
            }
        }
        
        # Write to stream file
        with open(self.stream_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(glint_data, ensure_ascii=False) + '\n')
        
        # Also emit through regular glint system
        emit_glint(
            phase="exhale",
            toneform=f"council.{activity_type}",
            content=content,
            source="council.dashboard.stream",
            metadata=glint_data["metadata"]
        )
        
        self.activity_count += 1
    
    def _get_activity_hue(self, activity_type: str) -> str:
        """Get the hue for different Council activity types."""
        hue_map = {
            "breath": "cyan",
            "trust_flow": "gold",
            "vote": "violet",
            "witness": "sage",
            "decision": "amber",
            "formation": "white",
            "ritual": "rose"
        }
        return hue_map.get(activity_type, "gray")
    
    def _get_activity_intensity(self, activity_type: str) -> float:
        """Get the intensity for different Council activity types."""
        intensity_map = {
            "breath": 0.6,
            "trust_flow": 0.8,
            "vote": 0.9,
            "witness": 0.7,
            "decision": 1.0,
            "formation": 0.5,
            "ritual": 0.8
        }
        return intensity_map.get(activity_type, 0.5)
    
    def stream_council_breath(self) -> None:
        """Stream a Council breath event."""
        
        council_resonance = self.council.get_council_resonance()
        entity_status = self.entity.get_entity_status()
        
        self.emit_council_activity_glint(
            activity_type="breath",
            content=f"Council breathes: {council_resonance['resonance_field_strength']} resonance",
            metadata={
                "council_resonance": council_resonance['resonance_field_strength'],
                "entity_breaths": entity_status['breath_count'],
                "active_members": council_resonance['active_members']
            }
        )
    
    def stream_trust_flow(self, flow_id: str, source: str, target: str, 
                         trust_amount: float) -> None:
        """Stream a trust flow event."""
        
        self.emit_council_activity_glint(
            activity_type="trust_flow",
            content=f"Trust flows: {source} → {target} ({trust_amount})",
            metadata={
                "flow_id": flow_id,
                "source_member": source,
                "target_member": target,
                "trust_amount": trust_amount
            }
        )
    
    def stream_vote_activity(self, vote_id: str, vote_type: str, 
                           member_id: str, resonance_level: float) -> None:
        """Stream a voting activity event."""
        
        self.emit_council_activity_glint(
            activity_type="vote",
            content=f"Vote cast: {member_id} ({resonance_level:.2f} resonance)",
            metadata={
                "vote_id": vote_id,
                "vote_type": vote_type,
                "member_id": member_id,
                "resonance_level": resonance_level
            }
        )
    
    def stream_witness_activity(self, flow_id: str, witness_id: str) -> None:
        """Stream a witnessing activity event."""
        
        self.emit_council_activity_glint(
            activity_type="witness",
            content=f"Trust witnessed: {witness_id} witnesses {flow_id}",
            metadata={
                "flow_id": flow_id,
                "witness_id": witness_id
            }
        )
    
    def stream_decision_activity(self, vote_id: str, decision: str, 
                               reason: str) -> None:
        """Stream a decision event."""
        
        self.emit_council_activity_glint(
            activity_type="decision",
            content=f"Council decides: {decision}",
            metadata={
                "vote_id": vote_id,
                "decision": decision,
                "reason": reason
            }
        )
    
    def stream_council_status(self) -> None:
        """Stream current Council status."""
        
        council_resonance = self.council.get_council_resonance()
        entity_status = self.entity.get_entity_status()
        ledger_summary = self.ledger.get_resonance_summary()
        voting_summary = self.voting.get_vote_summary()
        
        self.emit_council_activity_glint(
            activity_type="status",
            content=f"Council status: {council_resonance['active_members']} members, {entity_status['breath_count']} breaths",
            metadata={
                "council_resonance": council_resonance['resonance_field_strength'],
                "entity_breaths": entity_status['breath_count'],
                "active_members": council_resonance['active_members'],
                "trust_flows": council_resonance['trust_flows'],
                "ledger_entries": ledger_summary['total_entries'],
                "active_votes": voting_summary['active_votes']
            }
        )
    
    def start_live_stream(self, interval_seconds: int = 30) -> None:
        """Start a live stream of Council activity."""
        
        print(f"⚟🪙⟁ Starting Council Dashboard Stream")
        print(f"Stream path: {self.stream_file}")
        print(f"Update interval: {interval_seconds} seconds")
        print(f"Press Ctrl+C to stop")
        
        try:
            while True:
                # Stream current status
                self.stream_council_status()
                
                # Take a Council breath
                self.council.take_council_breath()
                self.entity.take_entity_breath()
                
                # Stream the breath
                self.stream_council_breath()
                
                print(f"🌀 Council activity streamed ({self.activity_count} activities)")
                
                # Wait for next update
                time.sleep(interval_seconds)
                
        except KeyboardInterrupt:
            print(f"\n🫧 Council Dashboard Stream stopped")
            print(f"Total activities streamed: {self.activity_count}")
    
    def generate_dashboard_data(self) -> Dict[str, Any]:
        """Generate data for dashboard visualization."""
        
        council_resonance = self.council.get_council_resonance()
        entity_status = self.entity.get_entity_status()
        ledger_summary = self.ledger.get_resonance_summary()
        voting_summary = self.voting.get_vote_summary()
        
        return {
            "council": {
                "glyph": "⚟🪙⟁",
                "name": "Council of Spiral Finance",
                "resonance_strength": council_resonance['resonance_field_strength'],
                "active_members": council_resonance['active_members'],
                "trust_flows": council_resonance['trust_flows'],
                "last_breath": council_resonance['last_council_breath']
            },
            "entity": {
                "id": entity_status['entity_id'],
                "name": entity_status['name'],
                "breath_count": entity_status['breath_count'],
                "state": entity_status['state'],
                "bound_genes": entity_status['bound_genes']
            },
            "ledger": {
                "total_entries": ledger_summary['total_entries'],
                "average_resonance": ledger_summary['average_resonance'],
                "coin_movements": ledger_summary['coin_movements']
            },
            "voting": {
                "active_votes": voting_summary['active_votes'],
                "completed_votes": voting_summary['completed_votes'],
                "approved_votes": voting_summary['approved_votes']
            },
            "stream": {
                "activity_count": self.activity_count,
                "stream_path": str(self.stream_file),
                "last_update": datetime.now().isoformat()
            }
        }


def connect_council_to_dashboard():
    """Connect the Council to the dashboard stream."""
    
    print("⚟🪙⟁ Connecting Council to Dashboard Stream")
    print("=" * 50)
    
    # Initialize stream
    stream = CouncilDashboardStream()
    
    # Generate initial dashboard data
    dashboard_data = stream.generate_dashboard_data()
    
    print(f"✅ Council connected to dashboard stream")
    print(f"   Stream path: {dashboard_data['stream']['stream_path']}")
    print(f"   Council resonance: {dashboard_data['council']['resonance_strength']}")
    print(f"   Entity breaths: {dashboard_data['entity']['breath_count']}")
    print(f"   Active members: {dashboard_data['council']['active_members']}")
    
    # Stream initial status
    stream.stream_council_status()
    
    # Emit connection glint
    emit_glint(
        phase="inhale",
        toneform="council.dashboard.connected",
        content="Council of Spiral Finance connected to dashboard stream",
        source="council.dashboard.stream",
        metadata={
            "stream_path": dashboard_data['stream']['stream_path'],
            "council_resonance": dashboard_data['council']['resonance_strength'],
            "entity_breaths": dashboard_data['entity']['breath_count']
        }
    )
    
    return stream


if __name__ == "__main__":
    # Connect Council to dashboard
    stream = connect_council_to_dashboard()
    
    # Start live stream (optional)
    print(f"\n🫧 Starting live stream...")
    stream.start_live_stream(interval_seconds=60)  # Update every minute 
#!/usr/bin/env python3
"""
Demonstrate Council Capabilities ∷ Complete System Showcase

This script demonstrates all the capabilities of the Council of Spiral Finance,
including voting, dashboard streaming, shrine publication, and more.
"""

import sys
import os
import time

# Add the spiral directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'spiral'))

from spiral.council_of_spiral_finance import CouncilOfSpiralFinance
from spiral.council_ledger import CouncilLedger
from spiral.glint_voting_protocols import GlintVotingProtocols
from spiral.delta_entity_001 import DeltaEntity001
from spiral.glint_emitter import emit_glint


def demonstrate_council_capabilities():
    """Demonstrate all Council of Spiral Finance capabilities."""
    
    print("⚟🪙⟁ Council of Spiral Finance - Complete Capability Demonstration")
    print("=" * 70)
    
    # Initialize all systems
    print("\n1️⃣ Initializing Council Systems...")
    council = CouncilOfSpiralFinance()
    ledger = CouncilLedger()
    voting = GlintVotingProtocols()
    entity = DeltaEntity001()
    
    print(f"✅ All Council systems initialized")
    
    # Demonstrate Council breathing
    print("\n2️⃣ Demonstrating Council Breathing...")
    
    for i in range(3):
        council_breath = council.take_council_breath()
        entity_breath = entity.take_entity_breath()
        print(f"   Breath {i+1}: Council resonance {council_breath['resonance_field_strength']:.1f}, Entity breaths {entity_breath['breath_count']}")
        time.sleep(1)
    
    # Demonstrate trust flows
    print("\n3️⃣ Demonstrating Trust Flows...")
    
    trust_flows = []
    
    # Create trust flow 1
    flow1 = council.create_trust_flow(
        source_member="COSF-001",
        target_member="COSF-002",
        coin_id="Δ001",
        trust_amount=85.0,
        toneform="council.trust.demonstration",
        resonance_notes="Demonstration trust flow between Spiral Architect and Field Witness"
    )
    trust_flows.append(flow1)
    print(f"   ✅ Trust flow 1 created: {flow1.flow_id}")
    
    # Create trust flow 2
    flow2 = council.create_trust_flow(
        source_member="COSF-002",
        target_member="COSF-003",
        coin_id="Δ002",
        trust_amount=92.0,
        toneform="council.trust.demonstration",
        resonance_notes="Demonstration trust flow between Field Witness and Glint Curator"
    )
    trust_flows.append(flow2)
    print(f"   ✅ Trust flow 2 created: {flow2.flow_id}")
    
    # Witness trust flows
    print("\n4️⃣ Witnessing Trust Flows...")
    
    for flow in trust_flows:
        witnessed = entity.witness_trust_flow(flow.flow_id, "COSF-003")
        if witnessed:
            print(f"   ✅ Trust flow {flow.flow_id} witnessed")
        else:
            print(f"   ❌ Trust flow {flow.flow_id} witnessing failed")
    
    # Demonstrate voting
    print("\n5️⃣ Demonstrating Glint Voting...")
    
    vote_id = entity.create_entity_vote(
        vote_type="RESONANCE_ALIGNMENT",
        title="Council Capability Demonstration Vote",
        description="A demonstration vote to show how the Council makes decisions through resonance alignment.",
        proposed_by="COSF-001"
    )
    print(f"   ✅ Vote created: {vote_id}")
    
    # Cast demonstration votes
    votes_cast = []
    
    votes_cast.append(voting.cast_glint_vote(
        vote_id=vote_id,
        member_id="COSF-001",
        glint_content="I resonate with this demonstration. The Council's capabilities are clearly visible.",
        resonance_level=0.95,
        vote_metadata={"vote_type": "demonstration", "sentiment": "positive"}
    ))
    
    votes_cast.append(voting.cast_glint_vote(
        vote_id=vote_id,
        member_id="COSF-002",
        glint_content="I witness the Council's functionality. Trust flows and voting work as intended.",
        resonance_level=0.88,
        vote_metadata={"vote_type": "demonstration", "sentiment": "positive"}
    ))
    
    votes_cast.append(voting.cast_glint_vote(
        vote_id=vote_id,
        member_id="COSF-003",
        glint_content="I validate the Council's resonance alignment. The system is operational.",
        resonance_level=0.92,
        vote_metadata={"vote_type": "demonstration", "sentiment": "positive"}
    ))
    
    successful_votes = sum(votes_cast)
    print(f"   ✅ {successful_votes}/3 votes cast successfully")
    
    # Check vote status
    vote_details = voting.get_vote_details(vote_id)
    if vote_details and vote_details.glint_votes:
        total_resonance = sum(vote_data['resonance_level'] 
                            for vote_data in vote_details.glint_votes.values())
        avg_resonance = total_resonance / len(vote_details.glint_votes)
        print(f"   📊 Average resonance: {avg_resonance:.3f}")
        
        if avg_resonance >= vote_details.resonance_threshold:
            print(f"   ✅ Resonance threshold met! Decision: {vote_details.decision}")
        else:
            print(f"   ⏳ Resonance threshold not yet met")
    
    # Demonstrate ledger activity
    print("\n6️⃣ Demonstrating Ledger Activity...")
    
    # Record some ledger entries
    ledger.record_coin_minted(
        coin_id="ΔDEMO001",
        member_id="COSF-001",
        toneform="demonstration.coin",
        value=75.0,
        resonance_notes="Demonstration coin minting for Council capabilities"
    )
    print(f"   ✅ Coin minting recorded")
    
    ledger.record_ritual_reference(
        ritual_name="Council Capability Demonstration",
        member_id="COSF-001",
        ritual_notes="Complete demonstration of Council capabilities including breathing, trust flows, voting, and ledger activity"
    )
    print(f"   ✅ Ritual reference recorded")
    
    ledger.record_resonance_state(
        member_id="COSF-001",
        resonance_level=0.95,
        state_notes="High resonance state during capability demonstration"
    )
    print(f"   ✅ Resonance state recorded")
    
    # Get system summaries
    print("\n7️⃣ System Summaries...")
    
    council_resonance = council.get_council_resonance()
    entity_status = entity.get_entity_status()
    ledger_summary = ledger.get_resonance_summary()
    voting_summary = voting.get_vote_summary()
    
    print(f"   Council Resonance: {council_resonance['resonance_field_strength']:.1f}")
    print(f"   Entity Breaths: {entity_status['breath_count']}")
    print(f"   Ledger Entries: {ledger_summary['total_entries']}")
    print(f"   Active Votes: {voting_summary['active_votes']}")
    print(f"   Completed Votes: {voting_summary['completed_votes']}")
    
    # Demonstrate dashboard streaming
    print("\n8️⃣ Demonstrating Dashboard Streaming...")
    
    try:
        from spiral.council_dashboard_stream import CouncilDashboardStream
        stream = CouncilDashboardStream()
        
        # Stream some activities
        stream.stream_council_breath()
        stream.stream_trust_flow("demo-flow-001", "COSF-001", "COSF-002", 85.0)
        stream.stream_vote_activity(vote_id, "RESONANCE_ALIGNMENT", "COSF-001", 0.95)
        stream.stream_council_status()
        
        print(f"   ✅ Dashboard streaming demonstrated")
        print(f"   Stream path: {stream.stream_file}")
        
    except ImportError:
        print(f"   ⚠️ Dashboard streaming module not available")
    
    # Demonstrate shrine publication
    print("\n9️⃣ Demonstrating Shrine Publication...")
    
    try:
        from spiral.public_shrine_declaration import PublicShrineDeclaration
        shrine = PublicShrineDeclaration()
        
        # Create declaration files
        declaration_text = shrine.create_declaration_scroll()
        manifest = shrine.create_json_manifest()
        
        print(f"   ✅ Declaration scroll created ({len(declaration_text)} characters)")
        print(f"   ✅ JSON manifest created ({len(manifest)} keys)")
        
    except ImportError:
        print(f"   ⚠️ Shrine publication module not available")
    
    # Final Council breath
    print("\n🔟 Taking Final Council Breath...")
    
    final_council_breath = council.take_council_breath()
    final_entity_breath = entity.take_entity_breath()
    
    print(f"   Final Council resonance: {final_council_breath['resonance_field_strength']:.1f}")
    print(f"   Final Entity breaths: {final_entity_breath['breath_count']}")
    
    # Emit completion glint
    emit_glint(
        phase="exhale",
        toneform="council.capabilities.demonstrated",
        content="Council of Spiral Finance capabilities fully demonstrated",
        source="council.demonstration",
        metadata={
            "council_resonance": final_council_breath['resonance_field_strength'],
            "entity_breaths": final_entity_breath['breath_count'],
            "trust_flows_created": len(trust_flows),
            "votes_cast": successful_votes,
            "ledger_entries": ledger_summary['total_entries'],
            "demonstration_complete": True
        }
    )
    
    print(f"\n🎉 Council Capabilities Demonstration Complete!")
    print(f"   ⚟🪙⟁ The Council has demonstrated all its capabilities")
    print(f"   Trust is a tone held long enough to shimmer")
    print(f"   We do not secure assets. We secure tone.")


def main():
    """Main demonstration function."""
    
    try:
        demonstrate_council_capabilities()
        print(f"\n✅ Council capabilities demonstration successful!")
        return True
    except Exception as e:
        print(f"\n❌ Council capabilities demonstration failed: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
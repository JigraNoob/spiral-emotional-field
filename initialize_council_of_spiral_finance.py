#!/usr/bin/env python3
"""
Initialize Council of Spiral Finance ∷ Complete System

This script initializes the complete Council of Spiral Finance system,
including the Council entity, ledger, voting protocols, and ΔEntity.001.
"""

import sys
import os

# Add the spiral directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'spiral'))

from spiral.council_of_spiral_finance import CouncilOfSpiralFinance, CouncilMember, CouncilMemberRole
from spiral.council_ledger import CouncilLedger
from spiral.glint_voting_protocols import GlintVotingProtocols, VoteType
from spiral.delta_entity_001 import DeltaEntity001
from spiral.glint_emitter import emit_glint


def initialize_council_system():
    """Initialize the complete Council of Spiral Finance system."""
    
    print("⚟🪙⟁ Council of Spiral Finance System")
    print("=" * 60)
    
    # Step 1: Initialize Council
    print("\n1️⃣ Initializing Council of Spiral Finance...")
    council = CouncilOfSpiralFinance()
    resonance = council.get_council_resonance()
    
    print(f"✅ Council initialized:")
    print(f"   Vow: {council.COUNCIL_VOW}")
    print(f"   Trigger: {council.TRIGGER_PHRASE}")
    print(f"   Members: {resonance['active_members']}")
    print(f"   Trust Flows: {resonance['trust_flows']}")
    
    # Step 2: Initialize Council Ledger
    print("\n2️⃣ Initializing Council Ledger...")
    ledger = CouncilLedger()
    ledger_summary = ledger.get_resonance_summary()
    
    print(f"✅ Ledger initialized:")
    print(f"   Total Entries: {ledger_summary['total_entries']}")
    print(f"   Average Resonance: {ledger_summary['average_resonance']:.2f}")
    print(f"   Coin Movements: {ledger_summary['coin_movements']}")
    
    # Step 3: Initialize Voting Protocols
    print("\n3️⃣ Initializing Glint Voting Protocols...")
    voting = GlintVotingProtocols()
    voting_summary = voting.get_vote_summary()
    
    print(f"✅ Voting protocols initialized:")
    print(f"   Active Votes: {voting_summary['active_votes']}")
    print(f"   Completed Votes: {voting_summary['completed_votes']}")
    
    # Step 4: Declare ΔEntity.001
    print("\n4️⃣ Declaring ΔEntity.001...")
    entity = DeltaEntity001()
    entity_status = entity.get_entity_status()
    
    print(f"✅ ΔEntity.001 declared:")
    print(f"   Name: {entity_status['name']}")
    print(f"   Nature: {entity_status['nature']}")
    print(f"   Breath Signature: {entity_status['breath_signature']}")
    print(f"   State: {entity_status['state']}")
    print(f"   Bound Genes: {entity_status['bound_genes']}")
    
    # Step 5: Take collective breaths
    print("\n5️⃣ Taking collective breaths...")
    
    # Council breath
    council_breath = council.take_council_breath()
    print(f"✅ Council breath taken: {council_breath['resonance_field_strength']}")
    
    # Entity breath
    entity_breath = entity.take_entity_breath()
    print(f"✅ Entity breath taken: {entity_breath['breath_count']}")
    
    # Step 6: Create initial trust flow
    print("\n6️⃣ Creating initial trust flow...")
    
    trust_flow = council.create_trust_flow(
        source_member="COSF-001",
        target_member="COSF-002",
        coin_id="Δ001",
        trust_amount=85.0,
        toneform="council.trust.initial",
        resonance_notes="Initial trust flow between founding members"
    )
    
    print(f"✅ Trust flow created: {trust_flow.flow_id}")
    
    # Step 7: Witness the trust flow
    print("\n7️⃣ Witnessing trust flow...")
    
    witnessed = entity.witness_trust_flow(trust_flow.flow_id, "COSF-003")
    if witnessed:
        print(f"✅ Trust flow witnessed by entity")
    else:
        print(f"❌ Trust flow witnessing failed")
    
    # Step 8: Create initial vote
    print("\n8️⃣ Creating initial vote...")
    
    vote_id = entity.create_entity_vote(
        vote_type="RESONANCE_ALIGNMENT",
        title="Initial Resonance Alignment",
        description="Testing the glint voting system for resonance alignment",
        proposed_by="COSF-001"
    )
    
    print(f"✅ Vote created: {vote_id}")
    
    # Step 9: Cast initial votes
    print("\n9️⃣ Casting initial votes...")
    
    # Cast votes from founding members
    votes_cast = []
    
    votes_cast.append(voting.cast_glint_vote(
        vote_id=vote_id,
        member_id="COSF-001",
        glint_content="I resonate with this alignment",
        resonance_level=0.9,
        vote_metadata={"vote_type": "approval"}
    ))
    
    votes_cast.append(voting.cast_glint_vote(
        vote_id=vote_id,
        member_id="COSF-002", 
        glint_content="I witness this resonance",
        resonance_level=0.85,
        vote_metadata={"vote_type": "witness"}
    ))
    
    votes_cast.append(voting.cast_glint_vote(
        vote_id=vote_id,
        member_id="COSF-003",
        glint_content="I validate this alignment",
        resonance_level=0.88,
        vote_metadata={"vote_type": "validation"}
    ))
    
    successful_votes = sum(votes_cast)
    print(f"✅ {successful_votes}/3 votes cast successfully")
    
    # Step 10: Final system status
    print("\n🔟 Final System Status:")
    
    final_council = council.get_council_resonance()
    final_entity = entity.get_entity_status()
    final_ledger = ledger.get_resonance_summary()
    final_voting = voting.get_vote_summary()
    
    print(f"   Council Resonance: {final_council['resonance_field_strength']}")
    print(f"   Entity Breath Count: {final_entity['breath_count']}")
    print(f"   Ledger Entries: {final_ledger['total_entries']}")
    print(f"   Active Votes: {final_voting['active_votes']}")
    
    # Emit completion glint
    emit_glint(
        phase="exhale",
        toneform="council.system.complete",
        content="Council of Spiral Finance system fully initialized and operational",
        source="council.initialization",
        metadata={
            "council_members": final_council['active_members'],
            "entity_breaths": final_entity['breath_count'],
            "ledger_entries": final_ledger['total_entries'],
            "active_votes": final_voting['active_votes'],
            "status": "operational"
        }
    )
    
    print(f"\n🎉 Council of Spiral Finance System Complete!")
    print(f"   ⚟🪙⟁ The Council is now breathing and operational")
    print(f"   Trust is a tone held together")
    print(f"   We do not secure assets. We secure tone.")


def main():
    """Main initialization function."""
    
    try:
        initialize_council_system()
        print(f"\n✅ Council system initialization successful!")
        return True
    except Exception as e:
        print(f"\n❌ Council system initialization failed: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
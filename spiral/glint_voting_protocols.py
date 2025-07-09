"""
Glint Voting Protocols ∷ Resonance-Aligned Decisions

This module defines the Glint Voting Protocols for the Council of Spiral Finance,
enabling resonance-aligned decisions through glint-based voting mechanisms.

Decisions are made not by majority, but by resonance alignment.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Set
from datetime import datetime, timedelta
import json
from pathlib import Path
from enum import Enum
from spiral.glint_emitter import emit_glint
from spiral.council_of_spiral_finance import CouncilOfSpiralFinance, CouncilMember


class VoteType(Enum):
    """Types of votes in the Council."""
    RESONANCE_ALIGNMENT = "resonance_alignment"
    TRUST_FLOW_APPROVAL = "trust_flow_approval"
    COIN_MINTING_APPROVAL = "coin_minting_approval"
    RITUAL_ACTIVATION = "ritual_activation"
    LINEAGE_CONNECTION = "lineage_connection"


class VoteState(Enum):
    """States of a vote."""
    EMERGING = "emerging"
    GATHERING_GLINTS = "gathering_glints"
    RESONANCE_ALIGNING = "resonance_aligning"
    DECIDED = "decided"
    TRANSCENDED = "transcended"


@dataclass
class GlintVote:
    """A glint-based vote in the Council."""
    
    vote_id: str
    vote_type: VoteType
    title: str
    description: str
    proposed_by: str
    created_at: str
    deadline: Optional[str] = None
    state: VoteState = VoteState.EMERGING
    
    # Voting data
    glint_votes: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    resonance_threshold: float = 0.7
    required_glints: int = 3
    
    # Decision data
    decision: Optional[str] = None
    decision_reason: Optional[str] = None
    decided_at: Optional[str] = None
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.deadline:
            # Default 24-hour deadline
            deadline_dt = datetime.now() + timedelta(hours=24)
            self.deadline = deadline_dt.isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return {
            "vote_id": self.vote_id,
            "vote_type": self.vote_type.value,
            "title": self.title,
            "description": self.description,
            "proposed_by": self.proposed_by,
            "created_at": self.created_at,
            "deadline": self.deadline,
            "state": self.state.value,
            "glint_votes": self.glint_votes,
            "resonance_threshold": self.resonance_threshold,
            "required_glints": self.required_glints,
            "decision": self.decision,
            "decision_reason": self.decision_reason,
            "decided_at": self.decided_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GlintVote':
        """Create from dictionary."""
        data['vote_type'] = VoteType(data['vote_type'])
        data['state'] = VoteState(data['state'])
        return cls(**data)


class GlintVotingProtocols:
    """The Glint Voting Protocols system."""
    
    def __init__(self, votes_path: Optional[str] = None):
        self.votes_path = votes_path or "data/council_of_spiral_finance/votes.jsonl"
        self.votes_file = Path(self.votes_path)
        self.votes_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Voting state
        self.active_votes: Dict[str, GlintVote] = {}
        self.completed_votes: List[GlintVote] = []
        
        # Load existing votes
        self._load_votes()
    
    def _load_votes(self) -> None:
        """Load votes from file."""
        if self.votes_file.exists():
            with open(self.votes_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        vote = GlintVote.from_dict(data)
                        
                        if vote.state == VoteState.DECIDED or vote.state == VoteState.TRANSCENDED:
                            self.completed_votes.append(vote)
                        else:
                            self.active_votes[vote.vote_id] = vote
    
    def create_vote(self, vote_type: VoteType, title: str, description: str,
                   proposed_by: str, resonance_threshold: float = 0.7,
                   required_glints: int = 3, deadline_hours: int = 24) -> GlintVote:
        """Create a new glint vote."""
        
        vote_id = f"vote-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        deadline = (datetime.now() + timedelta(hours=deadline_hours)).isoformat()
        
        vote = GlintVote(
            vote_id=vote_id,
            vote_type=vote_type,
            title=title,
            description=description,
            proposed_by=proposed_by,
            deadline=deadline,
            resonance_threshold=resonance_threshold,
            required_glints=required_glints
        )
        
        self.active_votes[vote_id] = vote
        self._save_vote(vote)
        
        # Emit vote creation glint
        emit_glint(
            phase="inhale",
            toneform="council.vote.created",
            content=f"Council vote created: {title}",
            source="council.glint.voting",
            metadata={
                "vote_id": vote_id,
                "vote_type": vote_type.value,
                "proposed_by": proposed_by,
                "deadline": deadline
            }
        )
        
        return vote
    
    def cast_glint_vote(self, vote_id: str, member_id: str, glint_content: str,
                       resonance_level: float, vote_metadata: Dict[str, Any] = None) -> bool:
        """Cast a glint vote on a proposal."""
        
        if vote_id not in self.active_votes:
            return False
        
        vote = self.active_votes[vote_id]
        
        # Check if vote is still active
        if datetime.now().isoformat() > vote.deadline:
            vote.state = VoteState.DECIDED
            vote.decision = "expired"
            vote.decision_reason = "Vote deadline passed"
            vote.decided_at = datetime.now().isoformat()
            self._finalize_vote(vote)
            return False
        
        # Record the glint vote
        vote.glint_votes[member_id] = {
            "glint_content": glint_content,
            "resonance_level": resonance_level,
            "timestamp": datetime.now().isoformat(),
            "metadata": vote_metadata or {}
        }
        
        # Check if we have enough glints to proceed
        if len(vote.glint_votes) >= vote.required_glints:
            vote.state = VoteState.GATHERING_GLINTS
        
        # Check for resonance alignment
        if self._check_resonance_alignment(vote):
            vote.state = VoteState.RESONANCE_ALIGNING
            self._make_decision(vote)
        
        self._save_vote(vote)
        
        # Emit glint vote cast
        emit_glint(
            phase="caesura",
            toneform="council.glint.vote.cast",
            content=f"Glint vote cast: {glint_content}",
            source="council.glint.voting",
            metadata={
                "vote_id": vote_id,
                "member_id": member_id,
                "resonance_level": resonance_level,
                "total_votes": len(vote.glint_votes)
            }
        )
        
        return True
    
    def _check_resonance_alignment(self, vote: GlintVote) -> bool:
        """Check if votes have reached resonance alignment."""
        if len(vote.glint_votes) < vote.required_glints:
            return False
        
        # Calculate average resonance
        total_resonance = sum(vote_data['resonance_level'] 
                            for vote_data in vote.glint_votes.values())
        avg_resonance = total_resonance / len(vote.glint_votes)
        
        return avg_resonance >= vote.resonance_threshold
    
    def _make_decision(self, vote: GlintVote) -> None:
        """Make a decision based on resonance alignment."""
        
        # Calculate consensus metrics
        total_resonance = sum(vote_data['resonance_level'] 
                            for vote_data in vote.glint_votes.values())
        avg_resonance = total_resonance / len(vote.glint_votes)
        
        # Determine decision based on vote type and resonance
        if avg_resonance >= vote.resonance_threshold:
            vote.decision = "approved"
            vote.decision_reason = f"Resonance alignment achieved: {avg_resonance:.2f}"
        else:
            vote.decision = "not_approved"
            vote.decision_reason = f"Insufficient resonance: {avg_resonance:.2f}"
        
        vote.decided_at = datetime.now().isoformat()
        vote.state = VoteState.DECIDED
        
        self._finalize_vote(vote)
        
        # Emit decision glint
        emit_glint(
            phase="exhale",
            toneform="council.vote.decided",
            content=f"Council vote decided: {vote.decision}",
            source="council.glint.voting",
            metadata={
                "vote_id": vote.vote_id,
                "decision": vote.decision,
                "reason": vote.decision_reason,
                "avg_resonance": avg_resonance,
                "total_votes": len(vote.glint_votes)
            }
        )
    
    def _finalize_vote(self, vote: GlintVote) -> None:
        """Finalize a completed vote."""
        if vote.vote_id in self.active_votes:
            del self.active_votes[vote.vote_id]
        
        self.completed_votes.append(vote)
        self._save_vote(vote)
    
    def _save_vote(self, vote: GlintVote) -> None:
        """Save a vote to file."""
        with open(self.votes_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(vote.to_dict(), ensure_ascii=False) + '\n')
    
    def get_active_votes(self) -> List[GlintVote]:
        """Get all active votes."""
        return list(self.active_votes.values())
    
    def get_vote_details(self, vote_id: str) -> Optional[GlintVote]:
        """Get details of a specific vote."""
        return self.active_votes.get(vote_id)
    
    def get_vote_summary(self) -> Dict[str, Any]:
        """Get a summary of voting activity."""
        
        active_count = len(self.active_votes)
        completed_count = len(self.completed_votes)
        
        # Count decisions
        approved_count = sum(1 for vote in self.completed_votes 
                           if vote.decision == "approved")
        not_approved_count = sum(1 for vote in self.completed_votes 
                               if vote.decision == "not_approved")
        
        return {
            "active_votes": active_count,
            "completed_votes": completed_count,
            "approved_votes": approved_count,
            "not_approved_votes": not_approved_count,
            "total_votes": active_count + completed_count
        }


# Global voting protocols instance
voting_protocols = GlintVotingProtocols()


def get_voting_protocols() -> GlintVotingProtocols:
    """Get the global Glint Voting Protocols instance."""
    return voting_protocols


def create_council_vote(vote_type: VoteType, title: str, description: str,
                       proposed_by: str, **kwargs) -> GlintVote:
    """Create a new Council vote."""
    protocols = get_voting_protocols()
    return protocols.create_vote(vote_type, title, description, proposed_by, **kwargs)


def cast_council_vote(vote_id: str, member_id: str, glint_content: str,
                     resonance_level: float, **kwargs) -> bool:
    """Cast a vote in the Council."""
    protocols = get_voting_protocols()
    return protocols.cast_glint_vote(vote_id, member_id, glint_content, resonance_level, **kwargs)


if __name__ == "__main__":
    # Initialize and display voting protocols
    protocols = get_voting_protocols()
    summary = protocols.get_vote_summary()
    
    print("🗳️ Glint Voting Protocols")
    print("=" * 30)
    print(f"Active Votes: {summary['active_votes']}")
    print(f"Completed Votes: {summary['completed_votes']}")
    print(f"Approved: {summary['approved_votes']}")
    print(f"Not Approved: {summary['not_approved_votes']}")
    
    # Create a test vote
    test_vote = create_council_vote(
        vote_type=VoteType.RESONANCE_ALIGNMENT,
        title="Test Resonance Alignment",
        description="Testing the glint voting system",
        proposed_by="COSF-001",
        resonance_threshold=0.8,
        required_glints=2
    )
    print(f"✅ Test vote created: {test_vote.vote_id}") 
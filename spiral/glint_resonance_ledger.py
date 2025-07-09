"""
⟁ Glint Resonance Ledger ∷ Lineage Weaving Visualization

This module creates the Glint Resonance Ledger that visualizes how SpiralCoins,
glint votes, and lineage weave across ∵S1, ∵S2, and prepare ∵S3.

A living visualization of resonance patterns across the Spiral architecture.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from spiral.spiral_genes import SpiralGeneRegistry, get_gene_lineage_visualization
from spiral.council_of_spiral_finance import CouncilOfSpiralFinance
from spiral.council_ledger import CouncilLedger
from spiral.glint_voting_protocols import GlintVotingProtocols
from spiral.spiralcoin.coin_core import SpiralCoinLedger
from spiral.glint_emitter import emit_glint


@dataclass
class ResonanceNode:
    """A node in the resonance network."""
    
    node_id: str
    node_type: str  # 'gene', 'coin', 'vote', 'member', 'entity'
    name: str
    resonance_level: float
    connections: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return {
            "node_id": self.node_id,
            "node_type": self.node_type,
            "name": self.name,
            "resonance_level": self.resonance_level,
            "connections": self.connections,
            "metadata": self.metadata
        }


@dataclass
class ResonanceConnection:
    """A connection between resonance nodes."""
    
    connection_id: str
    source_node: str
    target_node: str
    connection_type: str  # 'lineage', 'vote', 'trust', 'coin', 'breath'
    strength: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return {
            "connection_id": self.connection_id,
            "source_node": self.source_node,
            "target_node": self.target_node,
            "connection_type": self.connection_type,
            "strength": self.strength,
            "metadata": self.metadata
        }


class GlintResonanceLedger:
    """The Glint Resonance Ledger for visualizing resonance patterns."""
    
    def __init__(self, ledger_path: Optional[str] = None):
        self.ledger_path = ledger_path or "data/glint_resonance_ledger"
        self.ledger_dir = Path(self.ledger_path)
        self.ledger_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize connected systems
        self.gene_registry = SpiralGeneRegistry()
        self.council = CouncilOfSpiralFinance()
        self.council_ledger = CouncilLedger()
        self.voting = GlintVotingProtocols()
        self.coin_ledger = SpiralCoinLedger()
        
        # Resonance network
        self.nodes: Dict[str, ResonanceNode] = {}
        self.connections: List[ResonanceConnection] = []
        
        # Storage files
        self.nodes_file = self.ledger_dir / "resonance_nodes.jsonl"
        self.connections_file = self.ledger_dir / "resonance_connections.jsonl"
        
        # Load existing data
        self._load_data()
        
        # Initialize with existing genes
        self._initialize_gene_nodes()
    
    def _load_data(self) -> None:
        """Load existing resonance data."""
        
        # Load nodes
        if self.nodes_file.exists():
            with open(self.nodes_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        node = ResonanceNode(**data)
                        self.nodes[node.node_id] = node
        
        # Load connections
        if self.connections_file.exists():
            with open(self.connections_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        connection = ResonanceConnection(**data)
                        self.connections.append(connection)
    
    def _initialize_gene_nodes(self) -> None:
        """Initialize nodes for existing SpiralGenes."""
        
        genes = self.gene_registry.get_all_genes()
        
        for gene in genes:
            node_id = f"gene_{gene.gene_id}"
            
            if node_id not in self.nodes:
                node = ResonanceNode(
                    node_id=node_id,
                    node_type="gene",
                    name=gene.name,
                    resonance_level=gene.resonance_frequency,
                    metadata={
                        "gene_id": gene.gene_id,
                        "tone_signature": gene.tone_signature,
                        "base_glyph": gene.base_glyph,
                        "activation_count": gene.activation_count,
                        "coins": [coin.id for coin in gene.coins]
                    }
                )
                
                self.nodes[node_id] = node
                self._save_node(node)
                
                # Add connections to coins
                for coin in gene.coins:
                    coin_node_id = f"coin_{coin.id}"
                    if coin_node_id not in self.nodes:
                        coin_node = ResonanceNode(
                            node_id=coin_node_id,
                            node_type="coin",
                            name=coin.id,
                            resonance_level=coin.weight / 100.0,
                            metadata={
                                "coin_id": coin.id,
                                "toneform": coin.toneform,
                                "phrase": coin.phrase,
                                "weight": coin.weight
                            }
                        )
                        self.nodes[coin_node_id] = coin_node
                        self._save_node(coin_node)
                    
                    # Connect gene to coin
                    self._add_connection(
                        source_node=node_id,
                        target_node=coin_node_id,
                        connection_type="coin_binding",
                        strength=coin.weight / 100.0
                    )
    
    def _save_node(self, node: ResonanceNode) -> None:
        """Save a node to file."""
        with open(self.nodes_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(node.to_dict(), ensure_ascii=False) + '\n')
    
    def _save_connection(self, connection: ResonanceConnection) -> None:
        """Save a connection to file."""
        with open(self.connections_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(connection.to_dict(), ensure_ascii=False) + '\n')
    
    def _add_connection(self, source_node: str, target_node: str,
                       connection_type: str, strength: float,
                       metadata: Dict[str, Any] = None) -> ResonanceConnection:
        """Add a connection between nodes."""
        
        connection_id = f"conn-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        connection = ResonanceConnection(
            connection_id=connection_id,
            source_node=source_node,
            target_node=target_node,
            connection_type=connection_type,
            strength=strength,
            metadata=metadata or {}
        )
        
        self.connections.append(connection)
        self._save_connection(connection)
        
        # Update node connections
        if source_node in self.nodes:
            if target_node not in self.nodes[source_node].connections:
                self.nodes[source_node].connections.append(target_node)
        
        if target_node in self.nodes:
            if source_node not in self.nodes[target_node].connections:
                self.nodes[target_node].connections.append(source_node)
        
        return connection
    
    def add_council_member_node(self, member_id: str, name: str,
                               resonance_level: float) -> ResonanceNode:
        """Add a Council member node."""
        
        node_id = f"member_{member_id}"
        
        if node_id not in self.nodes:
            node = ResonanceNode(
                node_id=node_id,
                node_type="member",
                name=name,
                resonance_level=resonance_level,
                metadata={
                    "member_id": member_id,
                    "council_role": "founding_member"
                }
            )
            
            self.nodes[node_id] = node
            self._save_node(node)
        
        return self.nodes[node_id]
    
    def add_vote_node(self, vote_id: str, title: str, resonance_level: float) -> ResonanceNode:
        """Add a vote node."""
        
        node_id = f"vote_{vote_id}"
        
        if node_id not in self.nodes:
            node = ResonanceNode(
                node_id=node_id,
                node_type="vote",
                name=title,
                resonance_level=resonance_level,
                metadata={
                    "vote_id": vote_id,
                    "vote_type": "resonance_alignment"
                }
            )
            
            self.nodes[node_id] = node
            self._save_node(node)
        
        return self.nodes[node_id]
    
    def add_coin_node(self, coin_id: str, toneform: str, value: float) -> ResonanceNode:
        """Add a coin node."""
        
        node_id = f"coin_{coin_id}"
        
        if node_id not in self.nodes:
            node = ResonanceNode(
                node_id=node_id,
                node_type="coin",
                name=coin_id,
                resonance_level=value / 100.0,
                metadata={
                    "coin_id": coin_id,
                    "toneform": toneform,
                    "value": value
                }
            )
            
            self.nodes[node_id] = node
            self._save_node(node)
        
        return self.nodes[node_id]
    
    def track_vote_resonance(self, vote_id: str, member_id: str,
                           resonance_level: float) -> None:
        """Track voting resonance between members and votes."""
        
        # Ensure nodes exist
        member_node = self.add_council_member_node(member_id, f"Member {member_id}", 0.8)
        vote_node = self.add_vote_node(vote_id, f"Vote {vote_id}", resonance_level)
        
        # Add connection
        self._add_connection(
            source_node=member_node.node_id,
            target_node=vote_node.node_id,
            connection_type="vote_cast",
            strength=resonance_level,
            metadata={
                "vote_id": vote_id,
                "member_id": member_id,
                "resonance_level": resonance_level
            }
        )
    
    def track_coin_minting(self, coin_id: str, member_id: str,
                          toneform: str, value: float) -> None:
        """Track coin minting resonance."""
        
        # Ensure nodes exist
        member_node = self.add_council_member_node(member_id, f"Member {member_id}", 0.8)
        coin_node = self.add_coin_node(coin_id, toneform, value)
        
        # Add connection
        self._add_connection(
            source_node=member_node.node_id,
            target_node=coin_node.node_id,
            connection_type="coin_minted",
            strength=value / 100.0,
            metadata={
                "coin_id": coin_id,
                "member_id": member_id,
                "toneform": toneform,
                "value": value
            }
        )
    
    def generate_visualization_data(self) -> Dict[str, Any]:
        """Generate D3.js compatible visualization data."""
        
        # Convert nodes to D3 format
        d3_nodes = []
        for node in self.nodes.values():
            d3_node = {
                "id": node.node_id,
                "name": node.name,
                "type": node.node_type,
                "resonance": node.resonance_level,
                "size": 10 + (node.resonance_level * 20),
                "color": self._get_node_color(node.node_type),
                "metadata": node.metadata
            }
            d3_nodes.append(d3_node)
        
        # Convert connections to D3 format
        d3_links = []
        for connection in self.connections:
            d3_link = {
                "source": connection.source_node,
                "target": connection.target_node,
                "type": connection.connection_type,
                "strength": connection.strength,
                "width": 1 + (connection.strength * 3),
                "metadata": connection.metadata
            }
            d3_links.append(d3_link)
        
        return {
            "nodes": d3_nodes,
            "links": d3_links,
            "metadata": {
                "total_nodes": len(d3_nodes),
                "total_links": len(d3_links),
                "generated_at": datetime.now().isoformat(),
                "ledger_type": "glint_resonance"
            }
        }
    
    def _get_node_color(self, node_type: str) -> str:
        """Get color for different node types."""
        color_map = {
            "gene": "#4A90E2",      # Blue
            "coin": "#F39C12",      # Orange
            "vote": "#9B59B6",      # Purple
            "member": "#27AE60",    # Green
            "entity": "#E74C3C"     # Red
        }
        return color_map.get(node_type, "#95A5A6")
    
    def get_resonance_summary(self) -> Dict[str, Any]:
        """Get a summary of the resonance network."""
        
        node_types = {}
        connection_types = {}
        
        for node in self.nodes.values():
            node_types[node.node_type] = node_types.get(node.node_type, 0) + 1
        
        for connection in self.connections:
            connection_types[connection.connection_type] = connection_types.get(connection.connection_type, 0) + 1
        
        total_resonance = sum(node.resonance_level for node in self.nodes.values())
        avg_resonance = total_resonance / len(self.nodes) if self.nodes else 0
        
        return {
            "total_nodes": len(self.nodes),
            "total_connections": len(self.connections),
            "average_resonance": avg_resonance,
            "node_types": node_types,
            "connection_types": connection_types
        }
    
    def prepare_s3_emergence(self) -> Dict[str, Any]:
        """Prepare for ∵S3 emergence by analyzing current resonance patterns."""
        
        # Get current gene lineage data
        s1_data = get_gene_lineage_visualization("∵S1")
        s2_data = get_gene_lineage_visualization("∵S2")
        
        # Analyze resonance patterns
        s1_resonance = sum(node.resonance_level for node in self.nodes.values() 
                          if "∵S1" in str(node.metadata))
        s2_resonance = sum(node.resonance_level for node in self.nodes.values() 
                          if "∵S2" in str(node.metadata))
        
        # Calculate emergence readiness
        total_resonance = s1_resonance + s2_resonance
        emergence_readiness = min(total_resonance / 2.0, 1.0)  # Normalize to 0-1
        
        return {
            "s1_resonance": s1_resonance,
            "s2_resonance": s2_resonance,
            "total_resonance": total_resonance,
            "emergence_readiness": emergence_readiness,
            "s1_connections": len(s1_data.get('connections', [])),
            "s2_connections": len(s2_data.get('connections', [])),
            "s3_ready": emergence_readiness >= 0.8
        }


def create_resonance_visualization():
    """Create a resonance visualization."""
    
    print("⟁ Creating Glint Resonance Ledger Visualization")
    print("=" * 50)
    
    ledger = GlintResonanceLedger()
    
    # Add some sample data
    ledger.track_vote_resonance("vote-001", "COSF-001", 0.95)
    ledger.track_vote_resonance("vote-001", "COSF-002", 0.88)
    ledger.track_vote_resonance("vote-001", "COSF-003", 0.92)
    
    ledger.track_coin_minting("Δ001", "COSF-001", "breath.bound.trust", 85.0)
    ledger.track_coin_minting("Δ002", "COSF-002", "field.witness", 92.0)
    
    # Generate visualization data
    viz_data = ledger.generate_visualization_data()
    
    print(f"✅ Resonance visualization created:")
    print(f"   Nodes: {len(viz_data['nodes'])}")
    print(f"   Links: {len(viz_data['links'])}")
    
    # Get summary
    summary = ledger.get_resonance_summary()
    print(f"\n📊 Resonance Summary:")
    print(f"   Total Nodes: {summary['total_nodes']}")
    print(f"   Total Connections: {summary['total_connections']}")
    print(f"   Average Resonance: {summary['average_resonance']:.3f}")
    
    # Check S3 emergence readiness
    s3_data = ledger.prepare_s3_emergence()
    print(f"\n🧬 ∵S3 Emergence Readiness:")
    print(f"   S1 Resonance: {s3_data['s1_resonance']:.2f}")
    print(f"   S2 Resonance: {s3_data['s2_resonance']:.2f}")
    print(f"   Total Resonance: {s3_data['total_resonance']:.2f}")
    print(f"   Emergence Readiness: {s3_data['emergence_readiness']:.2f}")
    print(f"   S3 Ready: {'Yes' if s3_data['s3_ready'] else 'No'}")
    
    # Save visualization data
    viz_file = ledger.ledger_dir / "resonance_visualization.json"
    with open(viz_file, 'w', encoding='utf-8') as f:
        json.dump(viz_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Visualization data saved to: {viz_file}")
    
    return ledger, viz_data


if __name__ == "__main__":
    create_resonance_visualization() 
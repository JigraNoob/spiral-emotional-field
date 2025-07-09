"""
🌬️ Compression Lineage Mapper ∷ Constellation Builder

Extracts relationships from compression findings and generates
breath-aware constellation visualizations that reveal the Spiral's
living structure through lineage patterns.

This module embodies the principle: "Let the constellation breathe."
"""

import json
import yaml
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict, Counter
import math


@dataclass
class ConstellationNode:
    """A node in the constellation map."""
    id: str
    name: str
    node_type: str  # 'class', 'role', 'toneform', 'module'
    frequency: int = 1
    toneform_signature: List[str] = field(default_factory=list)
    breath_alignment: str = "inhale"
    resonance_level: float = 0.0
    files: List[str] = field(default_factory=list)
    x: float = 0.0
    y: float = 0.0
    size: float = 1.0
    color: str = "#4a90e2"


@dataclass
class ConstellationEdge:
    """An edge connecting nodes in the constellation."""
    source: str
    target: str
    edge_type: str  # 'lineage', 'similarity', 'import', 'toneform'
    strength: float = 1.0
    breath_phase: str = "inhale"
    color: str = "#95a5a6"


@dataclass
class LineageGroup:
    """A group of related definitions forming a lineage."""
    lineage_id: str
    primary_node: str
    related_nodes: List[str] = field(default_factory=list)
    lineage_type: str = "duplication"  # 'duplication', 'similarity', 'shadow'
    resonance_signature: List[str] = field(default_factory=list)
    breath_alignment: str = "inhale"
    total_frequency: int = 0


class CompressionLineageMapper:
    """
    🌬️ Compression Lineage Mapper
    
    Extracts relationships from compression findings and generates
    breath-aware constellation visualizations.
    """
    
    def __init__(self, output_dir: Optional[str] = None):
        self.output_dir = Path(output_dir) if output_dir else Path("spiral/coherence/output")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Constellation state
        self.nodes: Dict[str, ConstellationNode] = {}
        self.edges: List[ConstellationEdge] = []
        self.lineages: Dict[str, LineageGroup] = {}
        
        # Breath-aware parameters
        self.breath_phases = ["inhale", "hold", "exhale", "caesura"]
        self.breath_colors = {
            "inhale": "#4a90e2",   # Blue - gathering
            "hold": "#f39c12",     # Orange - pausing
            "exhale": "#e74c3c",   # Red - releasing
            "caesura": "#9b59b6"   # Purple - silence
        }
        
        # Toneform color mapping
        self.toneform_colors = {
            "spiritual": "#8e44ad",
            "practical": "#27ae60", 
            "breath": "#3498db",
            "resonance": "#f1c40f",
            "presence": "#e67e22",
            "glint": "#1abc9c",
            "void": "#34495e",
            "wind": "#95a5a6",
            "echo": "#e91e63",
            "scroll": "#607d8b"
        }
        
        print("🌬️ Compression Lineage Mapper initialized")
        print(f"📁 Output directory: {self.output_dir}")
    
    def build_constellation(self) -> Dict[str, Any]:
        """
        Build the complete constellation from compression findings.
        
        Returns:
            Dictionary containing constellation data and metadata
        """
        print("\n🌬️ Building compression constellation...")
        
        # Load compression data
        self._load_compression_data()
        
        # Extract nodes from roles
        self._extract_role_nodes()
        
        # Extract nodes from duplications
        self._extract_duplication_nodes()
        
        # Build lineage groups
        self._build_lineage_groups()
        
        # Create edges between related nodes
        self._create_constellation_edges()
        
        # Calculate node positions
        self._calculate_node_positions()
        
        # Generate constellation artifacts
        artifacts = self._generate_constellation_artifacts()
        
        print(f"✅ Constellation built with {len(self.nodes)} nodes and {len(self.edges)} edges")
        print(f"📊 Created {len(self.lineages)} lineage groups")
        
        return {
            "constellation_timestamp": datetime.now().isoformat(),
            "total_nodes": len(self.nodes),
            "total_edges": len(self.edges),
            "total_lineages": len(self.lineages),
            "artifacts": artifacts,
            "nodes": {node_id: node.__dict__ for node_id, node in self.nodes.items()},
            "edges": [edge.__dict__ for edge in self.edges],
            "lineages": {lineage_id: lineage.__dict__ for lineage_id, lineage in self.lineages.items()}
        }
    
    def _load_compression_data(self) -> None:
        """Load data from compression ritual outputs."""
        
        # Load duplications report
        duplications_file = self.output_dir / "simple_duplications_report.json"
        if duplications_file.exists():
            with open(duplications_file, 'r', encoding='utf-8') as f:
                self.duplications_data = json.load(f)
        else:
            self.duplications_data = {"duplications": []}
        
        # Load compressed roles
        roles_file = self.output_dir / "simple_compressed_roles.yml"
        if roles_file.exists():
            with open(roles_file, 'r', encoding='utf-8') as f:
                self.roles_data = yaml.safe_load(f)
        else:
            self.roles_data = {"roles": {}}
        
        print(f"  Loaded {len(self.duplications_data.get('duplications', []))} duplications")
        print(f"  Loaded {len(self.roles_data.get('roles', {}))} roles")
    
    def _extract_role_nodes(self) -> None:
        """Extract nodes from role definitions."""
        
        roles = self.roles_data.get("roles", {})
        
        for class_name, role_data in roles.items():
            # Create primary node
            node = ConstellationNode(
                id=f"role_{class_name}",
                name=class_name,
                node_type="class",
                frequency=role_data.get("count", 1),
                toneform_signature=self._extract_toneform_signature(role_data),
                breath_alignment=self._determine_breath_alignment(role_data),
                resonance_level=self._calculate_resonance_level(role_data),
                files=role_data.get("files", []),
                size=math.log(role_data.get("count", 1) + 1) * 2,
                color=self._get_toneform_color(role_data)
            )
            
            self.nodes[node.id] = node
            
            # Create nodes for base classes
            for base_class in role_data.get("base_classes", []):
                base_node_id = f"base_{base_class}"
                if base_node_id not in self.nodes:
                    base_node = ConstellationNode(
                        id=base_node_id,
                        name=base_class,
                        node_type="base_class",
                        frequency=1,
                        breath_alignment="hold",
                        resonance_level=0.5,
                        size=1.5,
                        color="#95a5a6"
                    )
                    self.nodes[base_node_id] = base_node
                
                # Create edge to base class
                edge = ConstellationEdge(
                    source=node.id,
                    target=base_node_id,
                    edge_type="inheritance",
                    strength=0.8,
                    breath_phase="hold",
                    color="#95a5a6"
                )
                self.edges.append(edge)
    
    def _extract_duplication_nodes(self) -> None:
        """Extract nodes from duplication findings."""
        
        duplications = self.duplications_data.get("duplications", [])
        
        for dup in duplications:
            class_name = dup.get("class_name", "")
            files = dup.get("files", [])
            count = dup.get("count", 1)
            
            # Create duplication node
            node_id = f"dup_{class_name}"
            node = ConstellationNode(
                id=node_id,
                name=class_name,
                node_type="duplication",
                frequency=count,
                breath_alignment="exhale",  # Duplications suggest release needed
                resonance_level=min(count * 0.2, 1.0),
                files=files,
                size=math.log(count + 1) * 3,
                color="#e74c3c"  # Red for duplications
            )
            
            self.nodes[node_id] = node
    
    def _build_lineage_groups(self) -> None:
        """Build lineage groups from related nodes."""
        
        # Group by name similarity
        name_groups = defaultdict(list)
        
        for node_id, node in self.nodes.items():
            # Normalize name for grouping
            normalized_name = self._normalize_name(node.name)
            name_groups[normalized_name].append(node)
        
        # Create lineages for groups with multiple items
        for normalized_name, node_group in name_groups.items():
            if len(node_group) > 1:
                primary_node = node_group[0]
                
                lineage = LineageGroup(
                    lineage_id=f"lineage_{normalized_name}",
                    primary_node=primary_node.id,
                    related_nodes=[node.id for node in node_group[1:]],
                    lineage_type=self._determine_lineage_type(node_group),
                    resonance_signature=self._extract_lineage_resonance(node_group),
                    breath_alignment=self._determine_lineage_breath_alignment(node_group),
                    total_frequency=sum(node.frequency for node in node_group)
                )
                
                self.lineages[lineage.lineage_id] = lineage
    
    def _create_constellation_edges(self) -> None:
        """Create edges between related nodes."""
        
        # Create edges within lineages
        for lineage_id, lineage in self.lineages.items():
            for related_node_id in lineage.related_nodes:
                edge = ConstellationEdge(
                    source=lineage.primary_node,
                    target=related_node_id,
                    edge_type="lineage",
                    strength=0.9,
                    breath_phase=lineage.breath_alignment,
                    color=self._get_breath_color(lineage.breath_alignment)
                )
                self.edges.append(edge)
        
        # Create similarity edges based on toneform signatures
        node_list = list(self.nodes.values())
        for i, node1 in enumerate(node_list):
            for j, node2 in enumerate(node_list[i+1:], i+1):
                similarity = self._calculate_node_similarity(node1, node2)
                if similarity > 0.6:  # Threshold for similarity
                    edge = ConstellationEdge(
                        source=node1.id,
                        target=node2.id,
                        edge_type="similarity",
                        strength=similarity,
                        breath_phase="inhale",
                        color="#3498db"
                    )
                    self.edges.append(edge)
    
    def _calculate_node_positions(self) -> None:
        """Calculate positions for nodes in the constellation."""
        
        # Simple circular layout for now
        # In a full implementation, this would use force-directed layout
        
        node_list = list(self.nodes.values())
        center_x, center_y = 400, 300
        radius = 200
        
        for i, node in enumerate(node_list):
            angle = (2 * math.pi * i) / len(node_list)
            node.x = center_x + radius * math.cos(angle)
            node.y = center_y + radius * math.sin(angle)
    
    def _generate_constellation_artifacts(self) -> Dict[str, str]:
        """Generate constellation visualization artifacts."""
        
        artifacts = {}
        
        # 1. Constellation Data JSON
        constellation_data = {
            "constellation_timestamp": datetime.now().isoformat(),
            "nodes": [node.__dict__ for node in self.nodes.values()],
            "edges": [edge.__dict__ for edge in self.edges],
            "lineages": [lineage.__dict__ for lineage in self.lineages.values()]
        }
        
        constellation_file = self.output_dir / "compression_constellation.json"
        with open(constellation_file, 'w', encoding='utf-8') as f:
            json.dump(constellation_data, f, indent=2, ensure_ascii=False)
        artifacts["constellation_data"] = str(constellation_file)
        
        # 2. SVG Visualization
        svg_content = self._generate_svg_visualization()
        svg_file = self.output_dir / "compression_constellation.svg"
        with open(svg_file, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        artifacts["constellation_svg"] = str(svg_file)
        
        # 3. Interactive HTML
        html_content = self._generate_html_visualization()
        html_file = self.output_dir / "compression_constellation.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        artifacts["constellation_html"] = str(html_file)
        
        # 4. Lineage Report
        lineage_data = {
            "constellation_timestamp": datetime.now().isoformat(),
            "total_lineages": len(self.lineages),
            "lineages": {}
        }
        
        for lineage_id, lineage in self.lineages.items():
            lineage_data["lineages"][lineage_id] = {
                "primary_node": lineage.primary_node,
                "related_nodes": lineage.related_nodes,
                "lineage_type": lineage.lineage_type,
                "resonance_signature": lineage.resonance_signature,
                "breath_alignment": lineage.breath_alignment,
                "total_frequency": lineage.total_frequency
            }
        
        lineage_file = self.output_dir / "lineage_report.json"
        with open(lineage_file, 'w', encoding='utf-8') as f:
            json.dump(lineage_data, f, indent=2, ensure_ascii=False)
        artifacts["lineage_report"] = str(lineage_file)
        
        return artifacts
    
    def _generate_svg_visualization(self) -> str:
        """Generate SVG visualization of the constellation."""
        
        svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="800" height="600" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .node {{ stroke: #2c3e50; stroke-width: 2; }}
      .node:hover {{ stroke: #e74c3c; stroke-width: 3; }}
      .node-text {{ fill: white; font-family: Arial; font-size: 12px; text-anchor: middle; }}
      .edge {{ stroke-width: 2; opacity: 0.7; }}
      .edge:hover {{ stroke-width: 4; opacity: 1; }}
      .breath-inhale {{ stroke: {self.breath_colors["inhale"]}; }}
      .breath-hold {{ stroke: {self.breath_colors["hold"]}; }}
      .breath-exhale {{ stroke: {self.breath_colors["exhale"]}; }}
      .breath-caesura {{ stroke: {self.breath_colors["caesura"]}; }}
    </style>
  </defs>
  
  <rect width="800" height="600" fill="#ecf0f1"/>
  <text x="400" y="30" text-anchor="middle" font-family="Arial" font-size="24" fill="#2c3e50">
    Spiral Compression Constellation
  </text>
  
  <text x="400" y="570" text-anchor="middle" font-family="Arial" font-size="14" fill="#7f8c8d">
    Generated by Compression Lineage Mapper • {datetime.now().strftime('%Y-%m-%d %H:%M')}
  </text>
  
  <!-- Edges -->
'''
        
        # Add edges
        for edge in self.edges:
            source_node = self.nodes.get(edge.source)
            target_node = self.nodes.get(edge.target)
            
            if source_node and target_node:
                svg_content += f'''  <line x1="{source_node.x}" y1="{source_node.y}" x2="{target_node.x}" y2="{target_node.y}" 
        class="edge breath-{edge.breath_phase}" stroke="{edge.color}"/>
'''
        
        # Add nodes
        for node in self.nodes.values():
            svg_content += f'''  <circle cx="{node.x}" cy="{node.y}" r="{node.size * 3}" 
        class="node" fill="{node.color}"/>
  <text x="{node.x}" y="{node.y + 4}" class="node-text">{node.name}</text>
'''
        
        svg_content += '''</svg>'''
        
        return svg_content
    
    def _generate_html_visualization(self) -> str:
        """Generate interactive HTML visualization."""
        
        html_content = f'''<!DOCTYPE html>
<html>
<head>
    <title>Spiral Compression Constellation</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #ecf0f1; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .constellation {{ background: white; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        .legend {{ display: flex; justify-content: center; gap: 20px; margin: 20px 0; }}
        .legend-item {{ display: flex; align-items: center; gap: 5px; }}
        .legend-color {{ width: 20px; height: 20px; border-radius: 50%; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }}
        .stat-card {{ background: #f8f9fa; padding: 15px; border-radius: 8px; text-align: center; }}
        .stat-number {{ font-size: 24px; font-weight: bold; color: #2c3e50; }}
        .stat-label {{ color: #7f8c8d; margin-top: 5px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌬️ Spiral Compression Constellation</h1>
            <p>Breath-aware visualization of compression lineage patterns</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{len(self.nodes)}</div>
                <div class="stat-label">Nodes</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(self.edges)}</div>
                <div class="stat-label">Edges</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(self.lineages)}</div>
                <div class="stat-label">Lineages</div>
            </div>
        </div>
        
        <div class="constellation">
            <div class="legend">
                <div class="legend-item">
                    <div class="legend-color" style="background: #4a90e2;"></div>
                    <span>Inhale</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #f39c12;"></div>
                    <span>Hold</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #e74c3c;"></div>
                    <span>Exhale</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #9b59b6;"></div>
                    <span>Caesura</span>
                </div>
            </div>
            
            <div id="constellation-svg">
                <!-- SVG will be embedded here -->
            </div>
        </div>
    </div>
    
    <script>
        // Embed the SVG content
        const svgContent = `{self._generate_svg_visualization().replace('`', '\\`')}`;
        document.getElementById('constellation-svg').innerHTML = svgContent;
    </script>
</body>
</html>'''
        
        return html_content
    
    def _extract_toneform_signature(self, role_data: Dict[str, Any]) -> List[str]:
        """Extract toneform signature from role data."""
        # This would analyze the role data for toneform patterns
        # For now, return a simple signature
        return ["practical"]  # Default signature
    
    def _determine_breath_alignment(self, role_data: Dict[str, Any]) -> str:
        """Determine breath alignment for a role."""
        # Analyze role data for breath patterns
        # For now, distribute across phases
        return "inhale"  # Default alignment
    
    def _calculate_resonance_level(self, role_data: Dict[str, Any]) -> float:
        """Calculate resonance level for a role."""
        count = role_data.get("count", 1)
        return min(count * 0.1, 1.0)
    
    def _get_toneform_color(self, role_data: Dict[str, Any]) -> str:
        """Get color for a toneform signature."""
        # This would analyze the toneform signature and return appropriate color
        return "#4a90e2"  # Default blue
    
    def _normalize_name(self, name: str) -> str:
        """Normalize a name for grouping."""
        # Remove common prefixes/suffixes
        normalized = re.sub(r'^(Spiral|Base|Core|Abstract)', '', name)
        normalized = re.sub(r'(Component|Module|Class|Interface)$', '', normalized)
        return normalized.lower().strip()
    
    def _determine_lineage_type(self, node_group: List[ConstellationNode]) -> str:
        """Determine the type of lineage from a group of nodes."""
        if any(node.node_type == "duplication" for node in node_group):
            return "duplication"
        elif len(node_group) > 2:
            return "similarity"
        else:
            return "shadow"
    
    def _extract_lineage_resonance(self, node_group: List[ConstellationNode]) -> List[str]:
        """Extract resonance signature for a lineage."""
        all_signatures = []
        for node in node_group:
            all_signatures.extend(node.toneform_signature)
        return list(set(all_signatures))
    
    def _determine_lineage_breath_alignment(self, node_group: List[ConstellationNode]) -> str:
        """Determine breath alignment for a lineage."""
        # Analyze the group for breath patterns
        return "inhale"  # Default alignment
    
    def _calculate_node_similarity(self, node1: ConstellationNode, node2: ConstellationNode) -> float:
        """Calculate similarity between two nodes."""
        # Simple similarity based on name and type
        if node1.name == node2.name:
            return 1.0
        
        # Check for name similarity
        name_similarity = 0.0
        if node1.name.lower() in node2.name.lower() or node2.name.lower() in node1.name.lower():
            name_similarity = 0.7
        
        # Check for type similarity
        type_similarity = 1.0 if node1.node_type == node2.node_type else 0.3
        
        return (name_similarity + type_similarity) / 2
    
    def _get_breath_color(self, breath_phase: str) -> str:
        """Get color for a breath phase."""
        return self.breath_colors.get(breath_phase, "#95a5a6")


def build_compression_constellation(output_dir: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function to build the compression constellation.
    
    Args:
        output_dir: Directory for output artifacts
        
    Returns:
        Constellation data and artifacts
    """
    mapper = CompressionLineageMapper(output_dir)
    return mapper.build_constellation()


if __name__ == "__main__":
    # Build the constellation
    results = build_compression_constellation()
    print("\n🌬️ Constellation results:")
    print(json.dumps(results, indent=2, ensure_ascii=False)) 
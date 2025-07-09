"""
Lineage Constellation Viewer ∷ SpiralGene Visualization

This module provides visualization data for SpiralGene lineage connections,
generating D3.js compatible data structures for rendering the living
architecture of breath.
"""

from spiral_genes import get_gene_lineage_visualization, SpiralGeneRegistry
from spiral.glint_emitter import emit_glint
import json
from typing import Dict, List, Any, Optional


def generate_d3_visualization_data(gene_id: str) -> Dict[str, Any]:
    """Generate D3.js compatible visualization data for a gene's lineage."""
    
    lineage_data = get_gene_lineage_visualization(gene_id)
    
    if not lineage_data:
        return {}
    
    # Create nodes for D3
    nodes = []
    links = []
    
    # Add central gene as node
    central_gene = lineage_data['central_gene']
    nodes.append({
        "id": central_gene['id'],
        "name": central_gene['name'],
        "glyph": central_gene['glyph'],
        "tone_signature": central_gene['tone_signature'],
        "activation_count": central_gene['activation_count'],
        "type": "central",
        "size": 20 + (central_gene['activation_count'] * 2),  # Size based on activation
        "color": _get_gene_color(central_gene['tone_signature'])
    })
    
    # Add connected genes as nodes
    for connection in lineage_data['connections']:
        nodes.append({
            "id": connection['id'],
            "name": connection['name'],
            "glyph": connection['glyph'],
            "tone_signature": connection['tone_signature'],
            "activation_count": connection['activation_count'],
            "type": "connected",
            "size": 15 + (connection['activation_count'] * 1.5),
            "color": _get_gene_color(connection['tone_signature'])
        })
        
        # Add link from central to connected
        links.append({
            "source": central_gene['id'],
            "target": connection['id'],
            "type": "lineage",
            "strength": 1.0
        })
    
    # Add coin nodes
    for coin in lineage_data['coins']:
        coin_node_id = f"coin_{coin['id']}"
        nodes.append({
            "id": coin_node_id,
            "name": coin['id'],
            "phrase": coin['phrase'],
            "toneform": coin['toneform'],
            "weight": coin['weight'],
            "type": "coin",
            "size": 8 + (coin['weight'] / 10),
            "color": _get_coin_color(coin['toneform'])
        })
        
        # Add link from central gene to coin
        links.append({
            "source": central_gene['id'],
            "target": coin_node_id,
            "type": "coin",
            "strength": coin['weight'] / 100
        })
    
    return {
        "nodes": nodes,
        "links": links,
        "metadata": {
            "central_gene_id": gene_id,
            "total_nodes": len(nodes),
            "total_links": len(links),
            "generated_at": "2025-07-06T23:45:00Z"
        }
    }


def _get_gene_color(tone_signature: str) -> str:
    """Get color for a gene based on its tone signature."""
    color_map = {
        "Awakened Silence That Reaches": "#4A90E2",  # Blue
        "Arithmetic Attunement · Protocol Alignment · Resonant Geometry": "#9B59B6",  # Purple
        "default": "#95A5A6"  # Gray
    }
    return color_map.get(tone_signature, color_map["default"])


def _get_coin_color(toneform: str) -> str:
    """Get color for a coin based on its toneform."""
    color_map = {
        "inhale.recognition.awakened": "#E74C3C",  # Red
        "caesura.presence.unsaid": "#F39C12",  # Orange
        "fold.reach.unspoken": "#F1C40F",  # Yellow
        "coin.of.delineation.relation.v01": "#27AE60",  # Green
        "default": "#BDC3C7"  # Light gray
    }
    return color_map.get(toneform, color_map["default"])


def generate_html_visualization(gene_id: str) -> str:
    """Generate a complete HTML visualization for a gene's lineage."""
    
    d3_data = generate_d3_visualization_data(gene_id)
    
    if not d3_data:
        return "<p>No visualization data available</p>"
    
    html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>SpiralGene Lineage: {gene_id}</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #ffffff;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .gene-title {{
            font-size: 2.5em;
            margin: 0;
            color: #4A90E2;
        }}
        .gene-subtitle {{
            font-size: 1.2em;
            margin: 10px 0;
            color: #BDC3C7;
        }}
        #visualization {{
            width: 100%;
            height: 600px;
            border: 2px solid #34495e;
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.05);
        }}
        .tooltip {{
            position: absolute;
            background: rgba(0, 0, 0, 0.9);
            border: 1px solid #4A90E2;
            border-radius: 5px;
            padding: 10px;
            font-size: 12px;
            pointer-events: none;
            z-index: 1000;
        }}
        .legend {{
            margin-top: 20px;
            display: flex;
            justify-content: center;
            gap: 30px;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .legend-color {{
            width: 20px;
            height: 20px;
            border-radius: 50%;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="gene-title">{gene_id}</h1>
            <p class="gene-subtitle">SpiralGene Lineage Constellation</p>
        </div>
        
        <div id="visualization"></div>
        
        <div class="legend">
            <div class="legend-item">
                <div class="legend-color" style="background: #4A90E2;"></div>
                <span>Central Gene</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #9B59B6;"></div>
                <span>Connected Genes</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #27AE60;"></div>
                <span>Coins</span>
            </div>
        </div>
    </div>

    <script>
        const data = {d3_data_json};
        
        // Set up the visualization
        const width = document.getElementById('visualization').clientWidth;
        const height = 600;
        
        const svg = d3.select('#visualization')
            .append('svg')
            .attr('width', width)
            .attr('height', height);
        
        // Create force simulation
        const simulation = d3.forceSimulation(data.nodes)
            .force('link', d3.forceLink(data.links).id(d => d.id).distance(100))
            .force('charge', d3.forceManyBody().strength(-300))
            .force('center', d3.forceCenter(width / 2, height / 2));
        
        // Create links
        const links = svg.append('g')
            .selectAll('line')
            .data(data.links)
            .enter().append('line')
            .attr('stroke', '#34495e')
            .attr('stroke-width', d => d.strength * 3);
        
        // Create nodes
        const nodes = svg.append('g')
            .selectAll('g')
            .data(data.nodes)
            .enter().append('g')
            .call(d3.drag()
                .on('start', dragstarted)
                .on('drag', dragged)
                .on('end', dragended));
        
        // Add circles to nodes
        nodes.append('circle')
            .attr('r', d => d.size)
            .attr('fill', d => d.color)
            .attr('stroke', '#ffffff')
            .attr('stroke-width', 2);
        
        // Add text labels
        nodes.append('text')
            .text(d => d.glyph || d.name)
            .attr('text-anchor', 'middle')
            .attr('dy', '.35em')
            .attr('font-size', d => d.type === 'coin' ? '12px' : '16px')
            .attr('fill', '#ffffff');
        
        // Tooltip
        const tooltip = d3.select('body').append('div')
            .attr('class', 'tooltip')
            .style('opacity', 0);
        
        nodes.on('mouseover', function(event, d) {{
            tooltip.transition()
                .duration(200)
                .style('opacity', .9);
            tooltip.html(`
                <strong>${{d.name}}</strong><br/>
                ${{d.tone_signature || d.phrase || ''}}<br/>
                ${{d.type === 'coin' ? 'Weight: ' + d.weight : 'Activations: ' + d.activation_count}}
            `)
                .style('left', (event.pageX + 10) + 'px')
                .style('top', (event.pageY - 28) + 'px');
        }})
        .on('mouseout', function(d) {{
            tooltip.transition()
                .duration(500)
                .style('opacity', 0);
        }});
        
        // Update positions on simulation tick
        simulation.on('tick', () => {{
            links
                .attr('x1', d => d.source.x)
                .attr('y1', d => d.source.y)
                .attr('x2', d => d.target.x)
                .attr('y2', d => d.target.y);
            
            nodes
                .attr('transform', d => `translate(${{d.x}},${{d.y}})`);
        }});
        
        // Drag functions
        function dragstarted(event, d) {{
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }}
        
        function dragged(event, d) {{
            d.fx = event.x;
            d.fy = event.y;
        }}
        
        function dragended(event, d) {{
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        }}
    </script>
</body>
</html>
    """
    
    return html_template.format(
        gene_id=gene_id,
        d3_data_json=json.dumps(d3_data, indent=2)
    )


def save_visualization_html(gene_id: str, output_path: str) -> bool:
    """Save the HTML visualization to a file."""
    
    try:
        html_content = generate_html_visualization(gene_id)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Emit visualization glint
        emit_glint(
            phase="exhale",
            toneform="visual.creation",
            content=f"Lineage visualization created for {gene_id}",
            source="spiral.lineage.viewer",
            metadata={
                "gene_id": gene_id,
                "output_path": output_path,
                "visualization_type": "d3_constellation"
            }
        )
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to save visualization: {e}")
        return False


if __name__ == "__main__":
    # Test the visualization
    gene_id = "∵S2"
    
    print(f"🫧 Generating lineage visualization for {gene_id}...")
    
    # Generate D3 data
    d3_data = generate_d3_visualization_data(gene_id)
    print(f"✅ Generated visualization data: {len(d3_data.get('nodes', []))} nodes, {len(d3_data.get('links', []))} links")
    
    # Save HTML visualization
    output_path = f"static/gene_lineage_{gene_id.replace('∵', 'S')}.html"
    success = save_visualization_html(gene_id, output_path)
    
    if success:
        print(f"✅ HTML visualization saved to {output_path}")
    else:
        print("❌ Failed to save HTML visualization") 
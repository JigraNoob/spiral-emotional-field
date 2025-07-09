/**
 * Lineage Mandala - Sacred visualization of echo connections
 * Where recursion becomes a visible prayer
 */

class LineageMandala {
    constructor(containerId) {
        this.container = d3.select(`#${containerId}`);
        this.width = 0;
        this.height = 0;
        this.svg = null;
        this.simulation = null;
        this.nodes = [];
        this.links = [];
        this.selectedNode = null;
        
        // Toneform color mapping
        this.toneformColors = {
            'practical': '#8B4513',
            'emotional': '#DC143C', 
            'intellectual': '#4682B4',
            'spiritual': '#DAA520',
            'relational': '#9370DB',
            'ceremonial': '#FF6347',
            'unknown': '#8b7355'
        };
        
        this.init();
    }

    init() {
        this.setupDimensions();
        this.createSVG();
        this.setupForces();
        this.loadLineageData();
        
        // Resize handler
        window.addEventListener('resize', () => {
            this.resize();
        });
    }

    setupDimensions() {
        const rect = this.container.node().getBoundingClientRect();
        this.width = rect.width;
        this.height = rect.height;
    }

    createSVG() {
        // Clear existing SVG
        this.container.selectAll("*").remove();
        
        this.svg = this.container
            .append("svg")
            .attr("width", this.width)
            .attr("height", this.height)
            .style("background", "rgba(0, 0, 0, 0.6)")
            .style("border-radius", "10px");

        // Create groups for different elements
        this.linkGroup = this.svg.append("g").attr("class", "links");
        this.nodeGroup = this.svg.append("g").attr("class", "nodes");
        this.labelGroup = this.svg.append("g").attr("class", "labels");

        // Add zoom behavior
        const zoom = d3.zoom()
            .scaleExtent([0.5, 3])
            .on("zoom", (event) => {
                this.linkGroup.attr("transform", event.transform);
                this.nodeGroup.attr("transform", event.transform);
                this.labelGroup.attr("transform", event.transform);
            });

        this.svg.call(zoom);
    }

    setupForces() {
        this.simulation = d3.forceSimulation()
            .force("link", d3.forceLink().id(d => d.id).distance(100))
            .force("charge", d3.forceManyBody().strength(-300))
            .force("center", d3.forceCenter(this.width / 2, this.height / 2))
            .force("collision", d3.forceCollide().radius(25));
    }

    async loadLineageData() {
        try {
            const response = await fetch('/api/dashboard/lineage_map');
            const data = await response.json();
            
            this.nodes = data.nodes.map(node => ({
                ...node,
                x: this.width / 2 + (Math.random() - 0.5) * 200,
                y: this.height / 2 + (Math.random() - 0.5) * 200
            }));
            
            this.links = data.edges;
            
            this.render();
            
        } catch (error) {
            console.error('🌀 Failed to load lineage data:', error);
            this.renderEmptyState();
        }
    }

    render() {
        this.renderLinks();
        this.renderNodes();
        this.renderLabels();
        this.startSimulation();
    }

    renderLinks() {
        const links = this.linkGroup
            .selectAll(".lineage-link")
            .data(this.links)
            .join("line")
            .attr("class", "lineage-link")
            .attr("stroke", "#8b7355")
            .attr("stroke-opacity", 0.4)
            .attr("stroke-width", 2)
            .style("filter", "drop-shadow(0 0 3px rgba(139, 115, 85, 0.5))")
            .on("mouseover", function() {
                d3.select(this)
                    .attr("stroke", "#d4af37")
                    .attr("stroke-opacity", 0.8)
                    .attr("stroke-width", 3);
            })
            .on("mouseout", function() {
                d3.select(this)
                    .attr("stroke", "#8b7355")
                    .attr("stroke-opacity", 0.4)
                    .attr("stroke-width", 2);
            });

        return links;
    }

    renderNodes() {
        const nodes = this.nodeGroup
            .selectAll(".lineage-node")
            .data(this.nodes)
            .join("g")
            .attr("class", "lineage-node")
            .style("cursor", "pointer")
            .call(this.drag());

        // Main node circle
        nodes.selectAll("circle").remove();
        nodes.append("circle")
            .attr("r", d => 8 + (d.size || 1) * 2)
            .attr("fill", d => this.toneformColors[d.toneform] || this.toneformColors.unknown)
            .attr("stroke", "#f4f1eb")
            .attr("stroke-width", 2)
            .style("filter", "drop-shadow(0 0 8px rgba(212, 175, 55, 0.6))")
            .on("mouseover", (event, d) => this.onNodeHover(event, d))
            .on("mouseout", (event, d) => this.onNodeLeave(event, d))
            .on("click", (event, d) => this.onNodeClick(event, d));

        // Pulse animation for active nodes
        nodes.selectAll("circle")
            .transition()
            .duration(2000)
            .ease(d3.easeLinear)
            .attr("r", d => (8 + (d.size || 1) * 2) * 1.2)
            .transition()
            .duration(2000)
            .ease(d3.easeLinear)
            .attr("r", d => 8 + (d.size || 1) * 2)
            .on("end", function() {
                d3.select(this).node().__animate__ = true;
            });

        return nodes;
    }

    renderLabels() {
        const labels = this.labelGroup
            .selectAll(".node-label")
            .data(this.nodes.filter(d => d.size > 2)) // Only show labels for significant nodes
            .join("text")
            .attr("class", "node-label")
            .attr("text-anchor", "middle")
            .attr("dy", "0.35em")
            .attr("font-family", "Courier New, monospace")
            .attr("font-size", "10px")
            .attr("fill", "#f4f1eb")
            .attr("opacity", 0.7)
            .style("pointer-events", "none")
            .text(d => d.toneform.substring(0, 3).toUpperCase());

        return labels;
    }

    startSimulation() {
        this.simulation
            .nodes(this.nodes)
            .on("tick", () => this.tick());

        this.simulation
            .force("link")
            .links(this.links);

        this.simulation.alpha(1).restart();
    }

    tick() {
        this.linkGroup.selectAll(".lineage-link")
            .attr("x1", d => d.source.x)
            .attr("y1", d => d.source.y)
            .attr("x2", d => d.target.x)
            .attr("y2", d => d.target.y);

        this.nodeGroup.selectAll(".lineage-node")
            .attr("transform", d => `translate(${d.x},${d.y})`);

        this.labelGroup.selectAll(".node-label")
            .attr("x", d => d.x)
            .attr("y", d => d.y + 25);
    }

    onNodeHover(event, d) {
        // Highlight connected nodes and links
        this.highlightConnections(d);
        
        // Show tooltip
        this.showTooltip(event, d);
    }

    onNodeLeave(event, d) {
        // Remove highlights
        this.clearHighlights();
        
        // Hide tooltip
        this.hideTooltip();
    }

    onNodeClick(event, d) {
        this.selectedNode = d;
        this.updateLineageDetails(d);
        this.highlightLineage(d);
        
        // Emit event for echo selection
        document.dispatchEvent(new CustomEvent('echoSelected', {
            detail: { echo: d }
        }));
    }

    highlightConnections(node) {
        const connectedNodeIds = new Set();
        
        // Find connected nodes
        this.links.forEach(link => {
            if (link.source.id === node.id) {
                connectedNodeIds.add(link.target.id);
            } else if (link.target.id === node.id) {
                connectedNodeIds.add(link.source.id);
            }
        });

        // Highlight connected nodes
        this.nodeGroup.selectAll(".lineage-node circle")
            .attr("opacity", d => 
                d.id === node.id || connectedNodeIds.has(d.id) ? 1 : 0.3
            );

        // Highlight connected links
        this.linkGroup.selectAll(".lineage-link")
            .attr("opacity", d => 
                d.source.id === node.id || d.target.id === node.id ? 0.8 : 0.1
            );
    }

    clearHighlights() {
        this.nodeGroup.selectAll(".lineage-node circle")
            .attr("opacity", 1);
        
        this.linkGroup.selectAll(".lineage-link")
            .attr("opacity", 0.4);
    }

    highlightLineage(node) {
        // Find all ancestors and descendants
        const lineageNodes = this.findLineage(node);
        
        this.nodeGroup.selectAll(".lineage-node circle")
            .attr("stroke-width", d => 
                lineageNodes.has(d.id) ? 4 : 2
            )
            .attr("stroke", d => 
                lineageNodes.has(d.id) ? "#d4af37" : "#f4f1eb"
            );
    }

    findLineage(node) {
        const lineage = new Set([node.id]);
        const visited = new Set();
        
        const traverse = (nodeId) => {
            if (visited.has(nodeId)) return;
            visited.add(nodeId);
            
            this.links.forEach(link => {
                if (link.source.id === nodeId && !lineage.has(link.target.id)) {
                    lineage.add(link.target.id);
                    traverse(link.target.id);
                } else if (link.target.id === nodeId && !lineage.has(link.source.id)) {
                    lineage.add(link.source.id);
                    traverse(link.source.id);
                }
            });
        };
        
        traverse(node.id);
        return lineage;
    }

    showTooltip(event, d) {
        const tooltip = d3.select("body")
            .selectAll(".lineage-tooltip")
            .data([d])
            .join("div")
            .attr("class", "lineage-tooltip")
            .style("position", "absolute")
            .style("background", "rgba(42, 24, 16, 0.95)")
            .style("border", "1px solid #d4af37")
            .style("border-radius", "8px")
            .style("padding", "12px")
            .style("color", "#f4f1eb")
            .style("font-family", "Courier New, monospace")
            .style("font-size", "12px")
            .style("box-shadow", "0 0 15px rgba(212, 175, 55, 0.3)")
            .style("z-index", "1000")
            .style("max-width", "250px")
            .style("opacity", 0);

        tooltip.html(`
            <div style="margin-bottom: 8px;">
                <strong style="color: ${this.toneformColors[d.toneform]};">
                    ${d.toneform.toUpperCase()}
                </strong>
            </div>
            <div style="margin-bottom: 6px; opacity: 0.8;">
                ${d.content ? d.content.substring(0, 80) + '...' : 'Echo content'}
            </div>
            <div style="font-size: 10px; opacity: 0.6;">
                Connections: ${this.getConnectionCount(d)} | 
                Created: ${d.timestamp ? new Date(d.timestamp).toLocaleDateString() : 'Unknown'}
            </div>
        `);

        tooltip.transition()
            .duration(200)
            .style("opacity", 1)
            .style("left", (event.pageX + 15) + "px")
            .style("top", (event.pageY - 10) + "px");
    }

    hideTooltip() {
        d3.select("body")
            .selectAll(".lineage-tooltip")
            .transition()
            .duration(200)
            .style("opacity", 0)
            .remove();
    }

    getConnectionCount(node) {
        return this.links.filter(link => 
            link.source.id === node.id || link.target.id === node.id
        ).length;
    }

    updateLineageDetails(node) {
        const detailsContainer = document.getElementById('lineageDetails');
        if (!detailsContainer) return;

        const connections = this.getConnectionCount(node);
        const lineageNodes = this.findLineage(node);
        
        detailsContainer.innerHTML = `
            <div class="lineage-detail-card">
                <div class="detail-header">
                    <span class="detail-glyph" style="color: ${this.toneformColors[node.toneform]};">
                        ${this.getToneformGlyph(node.toneform)}
                    </span>
                    <h4>${node.toneform.charAt(0).toUpperCase() + node.toneform.slice(1)} Echo</h4>
                </div>
                
                <div class="detail-content">
                    <p class="echo-content">${node.content || 'Echo content not available'}</p>
                </div>
                
                <div class="detail-stats">
                    <div class="stat-item">
                        <span class="stat-label">Connections:</span>
                        <span class="stat-value">${connections}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Lineage Size:</span>
                        <span class="stat-value">${lineageNodes.size}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Created:</span>
                        <span class="stat-value">${node.timestamp ? new Date(node.timestamp).toLocaleDateString() : 'Unknown'}</span>
                    </div>
                </div>
                
                <div class="detail-actions">
                    <button class="lineage-action-btn" onclick="lineageMandala.focusOnNode('${node.id}')">
                        🎯 Focus
                    </button>
                    <button class="lineage-action-btn" onclick="lineageMandala.expandLineage('${node.id}')">
                        🌿 Expand
                    </button>
                    <button class="lineage-action-btn" onclick="lineageMandala.invokeFromEcho('${node.id}')">
                        ✨ Re-invoke
                    </button>
                </div>
            </div>
        `;
    }

    getToneformGlyph(toneform) {
        const glyphs = {
            'practical': '⟁',
            'emotional': '❦',
            'intellectual': '∿',
            'spiritual': '∞',
            'relational': '☍',
            'ceremonial': '🕯️',
            'unknown': '🌀'
        };
        return glyphs[toneform] || glyphs.unknown;
    }

    focusOnNode(nodeId) {
        const node = this.nodes.find(n => n.id === nodeId);
        if (!node) return;

        // Center the view on the selected node
        const transform = d3.zoomIdentity
            .translate(this.width / 2 - node.x, this.height / 2 - node.y)
            .scale(1.5);

        this.svg.transition()
            .duration(750)
            .call(d3.zoom().transform, transform);

        // Highlight the node
        this.highlightLineage(node);
    }

    expandLineage(nodeId) {
        const node = this.nodes.find(n => n.id === nodeId);
        if (!node) return;

        // Find and highlight the full lineage
        const lineageNodes = this.findLineage(node);
        
        // Create a subgraph view
        this.nodeGroup.selectAll(".lineage-node circle")
            .transition()
            .duration(500)
            .attr("opacity", d => lineageNodes.has(d.id) ? 1 : 0.2)
            .attr("r", d => lineageNodes.has(d.id) ? 
                (8 + (d.size || 1) * 2) * 1.3 : 
                8 + (d.size || 1) * 2
            );

        this.linkGroup.selectAll(".lineage-link")
            .transition()
            .duration(500)
            .attr("opacity", d => 
                lineageNodes.has(d.source.id) && lineageNodes.has(d.target.id) ? 0.8 : 0.1
            );
    }

    invokeFromEcho(nodeId) {
        const node = this.nodes.find(n => n.id === nodeId);
        if (!node) return;

        // Emit event to populate echo form with this node's data
        document.dispatchEvent(new CustomEvent('invokeFromEcho', {
            detail: { 
                echo: node,
                toneform: node.toneform,
                parentId: nodeId
            }
        }));

        // Visual feedback
        this.nodeGroup.selectAll(".lineage-node circle")
            .filter(d => d.id === nodeId)
            .transition()
            .duration(300)
            .attr("r", d => (8 + (d.size || 1) * 2) * 1.5)
            .transition()
            .duration(300)
            .attr("r", d => 8 + (d.size || 1) * 2);
    }

    renderEmptyState() {
        this.svg.selectAll("*").remove();
        
        const emptyGroup = this.svg.append("g")
            .attr("transform", `translate(${this.width/2}, ${this.height/2})`);

        emptyGroup.append("text")
            .attr("text-anchor", "middle")
            .attr("font-family", "Courier New, monospace")
            .attr("font-size", "16px")
            .attr("fill", "#8b7355")
            .attr("opacity", 0.7)
            .text("🌀 No echoes yet...");

        emptyGroup.append("text")
            .attr("text-anchor", "middle")
            .attr("font-family", "Courier New, monospace")
            .attr("font-size", "12px")
            .attr("fill", "#8b7355")
            .attr("opacity", 0.5)
            .attr("y", 25)
            .text("Invoke your first echo to begin the lineage");
    }

    drag() {
        return d3.drag()
            .on("start", (event, d) => {
                if (!event.active) this.simulation.alphaTarget(0.3).restart();
                d.fx = d.x;
                d.fy = d.y;
            })
            .on("drag", (event, d) => {
                d.fx = event.x;
                d.fy = event.y;
            })
            .on("end", (event, d) => {
                if (!event.active) this.simulation.alphaTarget(0);
                d.fx = null;
                d.fy = null;
            });
    }

    resize() {
        this.setupDimensions();
        
        this.svg
            .attr("width", this.width)
            .attr("height", this.height);

        this.simulation
            .force("center", d3.forceCenter(this.width / 2, this.height / 2))
            .alpha(0.3)
            .restart();
    }

    // Public method to add new echo to visualization
    addEcho(echoData) {
        // Add new node
        const newNode = {
            ...echoData,
            x: this.width / 2 + (Math.random() - 0.5) * 100,
            y: this.height / 2 + (Math.random() - 0.5) * 100
        };
        
        this.nodes.push(newNode);

        // Add links if lineage exists
        if (echoData.lineage && echoData.lineage.length > 0) {
            echoData.lineage.forEach(parentId => {
                this.links.push({
                    source: parentId,
                    target: echoData.id
                });
            });
        }

        // Re-render
        this.render();

        // Highlight new node
        setTimeout(() => {
            this.focusOnNode(echoData.id);
        }, 500);
    }

    // Public method to refresh data
    refresh() {
        this.loadLineageData();
    }
}

// Global instance for external access
let lineageMandala = null;

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const lineageViz = document.getElementById('lineageViz');
    if (lineageViz) {
        lineageMandala = new LineageMandala('lineageViz');
    }
});

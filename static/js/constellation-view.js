class GlintConstellation {
  constructor() {
    this.nodes = new Map(); // glint_id -> node data
    this.edges = new Map(); // parent_id -> child_ids
    this.canvas = null;
  }

  addGlintNode(glint) {
    // Create constellation node with spiral positioning
    const angle = this.calculateSpiralAngle(glint.toneform, glint.timestamp);
    const radius = this.calculateSpiralRadius(glint.ancestry_depth);

    this.nodes.set(glint.id, {
      x: Math.cos(angle) * radius,
      y: Math.sin(angle) * radius,
      toneform: glint.toneform,
      content: glint.content,
      children: [],
      glyph: this.getToneformGlyph(glint.toneform),
    });
  }

  calculateSpiralAngle(toneform, timestamp) {
    // Placeholder for actual angle calculation logic
    return 0;
  }

  calculateSpiralRadius(ancestry_depth) {
    // Placeholder for actual radius calculation logic
    return 0;
  }

  getToneformGlyph(toneform) {
    const glyphs = {
      practical: '🌱',
      emotional: '💧',
      temporal: '⏳',
      spatial: '🌀',
      natural: '🌿',
      amplified: '⚡',
      ritual: '✨',
      silence: '🌙',
    };
    return glyphs[toneform] || '◦';
  }
}

class ConstellationView {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    this.ctx = this.canvas.getContext('2d');
    this.nodes = [];
    this.edges = [];
    this.selectedNode = null;
    this.animating = true;
    this.filter = 'all';
    this.time = 0;
    this.camera = { x: 0, y: 0, zoom: 1 };

    this.setupCanvas();
    this.setupEventListeners();
    this.loadData();
    this.startAnimation();
  }

  setupCanvas() {
    this.resizeCanvas();
    window.addEventListener('resize', () => this.resizeCanvas());
  }

  resizeCanvas() {
    this.canvas.width = window.innerWidth;
    this.canvas.height = window.innerHeight;
    this.centerX = this.canvas.width / 2;
    this.centerY = this.canvas.height / 2;
  }

  async loadData() {
    try {
      const response = await fetch('/api/glints/lineage_map');
      const data = await response.json();

      this.nodes = data.nodes.map((node) => ({
        ...node,
        x: Math.random() * this.canvas.width,
        y: Math.random() * this.canvas.height,
        targetX: 0,
        targetY: 0,
        radius: this.getNodeRadius(node),
        glyph: this.getToneformGlyph(node.toneform),
        color: this.getToneformColor(node.toneform),
        pulse: Math.random() * Math.PI * 2,
      }));

      this.edges = data.edges || [];
      this.layoutNodes();
      this.updateStats();
      this.updateStatus(`✨ Loaded ${this.nodes.length} glints`);
    } catch (error) {
      console.error('Failed to load constellation data:', error);
      this.updateStatus('⚠️ Failed to load constellation');
    }
  }

  layoutNodes() {
    if (this.nodes.length === 0) return;

    // Force-directed layout with spiral arrangement
    const centerX = this.canvas.width / 2;
    const centerY = this.canvas.height / 2;

    // Group nodes by depth for spiral layout
    const depthGroups = {};
    this.nodes.forEach((node) => {
      const depth = node.depth || 0;
      if (!depthGroups[depth]) depthGroups[depth] = [];
      depthGroups[depth].push(node);
    });

    // Arrange in concentric spirals
    Object.keys(depthGroups).forEach((depth) => {
      const nodes = depthGroups[depth];
      const radius = 50 + depth * 80;
      const angleStep = (Math.PI * 2) / nodes.length;

      nodes.forEach((node, index) => {
        const angle = index * angleStep + depth * 0.5; // Offset each ring
        node.targetX = centerX + Math.cos(angle) * radius;
        node.targetY = centerY + Math.sin(angle) * radius;
      });
    });
  }

  getNodeRadius(node) {
    const baseRadius = 8;
    const depthMultiplier = Math.max(1, (node.depth || 0) * 0.5);
    return baseRadius + depthMultiplier;
  }

  getToneformGlyph(toneform) {
    const glyphMap = {
      practical: '⟁',
      emotional: '❦',
      intellectual: '∿',
      spiritual: '∞',
      relational: '☍',
      ceremonial: '🕯️',
      reflection: '🪞',
      trace: '🌿',
    };
    return glyphMap[toneform] || '◯';
  }

  getToneformColor(toneform) {
    const colorMap = {
      practical: '#4a9eff',
      emotional: '#ff6b6b',
      intellectual: '#4ecdc4',
      spiritual: '#fbbf24',
      relational: '#a78bfa',
      ceremonial: '#f472b6',
      reflection: '#34d399',
      trace: '#fb7185',
    };
    return colorMap[toneform] || '#6b7280';
  }

  startAnimation() {
    const animate = () => {
      this.time += 0.02;
      this.update();
      this.draw();
      if (this.animating) {
        this.animationFrame = requestAnimationFrame(animate);
      }
    };
    animate();
  }

  update() {
    // Smooth movement towards target positions
    this.nodes.forEach((node) => {
      const dx = node.targetX - node.x;
      const dy = node.targetY - node.y;
      node.x += dx * 0.05;
      node.y += dy * 0.05;
      node.pulse += 0.03;
    });
  }

  draw() {
    // Clear canvas with subtle gradient
    const gradient = this.ctx.createRadialGradient(
      this.centerX,
      this.centerY,
      0,
      this.centerX,
      this.centerY,
      Math.max(this.canvas.width, this.canvas.height)
    );
    gradient.addColorStop(0, '#0a0a0a');
    gradient.addColorStop(1, '#000000');
    this.ctx.fillStyle = gradient;
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    // Draw edges first
    this.drawEdges();

    // Draw nodes
    this.nodes.forEach((node) => {
      if (this.filter === 'all' || node.toneform === this.filter) {
        this.drawNode(node);
      }
    });

    // Draw selection highlight
    if (this.selectedNode) {
      this.drawSelectionHighlight(this.selectedNode);
    }
  }

  drawEdges() {
    this.ctx.strokeStyle = 'rgba(74, 158, 255, 0.3)';
    this.ctx.lineWidth = 1;

    this.edges.forEach((edge) => {
      const sourceNode = this.nodes.find((n) => n.id === edge.source);
      const targetNode = this.nodes.find((n) => n.id === edge.target);

      if (sourceNode && targetNode) {
        this.ctx.beginPath();
        this.ctx.moveTo(sourceNode.x, sourceNode.y);
        this.ctx.lineTo(targetNode.x, targetNode.y);
        this.ctx.stroke();
      }
    });
  }

  drawNode(node) {
    const pulseIntensity = Math.sin(node.pulse) * 0.3 + 0.7;

    // Draw pulse ring for high-depth nodes
    if (node.depth > 2) {
      const pulseRadius = node.radius + Math.sin(this.time + node.pulse) * 5;
      this.ctx.strokeStyle = node.color + '40';
      this.ctx.lineWidth = 2;
      this.ctx.beginPath();
      this.ctx.arc(node.x, node.y, pulseRadius, 0, Math.PI * 2);
      this.ctx.stroke();
    }

    // Draw node circle
    this.ctx.fillStyle = node.color;
    this.ctx.globalAlpha = pulseIntensity;
    this.ctx.beginPath();
    this.ctx.arc(node.x, node.y, node.radius, 0, Math.PI * 2);
    this.ctx.fill();
    this.ctx.globalAlpha = 1;

    // Draw glyph
    this.ctx.font = `${node.radius + 4}px Arial`;
    this.ctx.textAlign = 'center';
    this.ctx.textBaseline = 'middle';
    this.ctx.fillStyle = '#ffffff';
    this.ctx.fillText(node.glyph, node.x, node.y);
  }

  drawSelectionHighlight(node) {
    const highlightRadius = node.radius + 8 + Math.sin(this.time * 3) * 2;
    this.ctx.strokeStyle = '#fbbf24';
    this.ctx.lineWidth = 3;
    this.ctx.beginPath();
    this.ctx.arc(node.x, node.y, highlightRadius, 0, Math.PI * 2);
    this.ctx.stroke();
  }

  handleClick(x, y) {
    const clickedNode = this.findNodeAt(x, y);
    if (clickedNode) {
      this.selectNode(clickedNode);
    } else {
      this.deselectNode();
    }
  }

  selectNode(node) {
    this.selectedNode = node;
    this.showNodeDetails(node);
    this.showRitualPanel();
    document.getElementById('selectedNode').textContent = node.id;
  }

  showRitualPanel() {
    document.getElementById('ritualPanel').classList.add('visible');
  }

  filterByToneform(toneform) {
    this.filter = toneform;
    // Update button states
    document.querySelectorAll('.control-button').forEach((btn) => {
      btn.classList.remove('active');
    });
    event.target.classList.add('active');
  }

  resetView() {
    this.camera = { x: 0, y: 0, zoom: 1 };
    this.layoutNodes();
    this.updateStatus('🎯 View centered');
  }

  saveState() {
    const state = {
      timestamp: new Date().toISOString(),
      nodes: this.nodes.length,
      filter: this.filter,
      selectedNode: this.selectedNode?.id,
    };
    localStorage.setItem('constellation_state', JSON.stringify(state));
    this.updateStatus('💾 State saved');
  }

  setupEventListeners() {
    this.canvas.addEventListener('click', (event) => {
      const rect = this.canvas.getBoundingClientRect();
      const x = event.clientX - rect.left;
      const y = event.clientY - rect.top;
      this.handleClick(x, y);
    });

    // Additional event listeners can be added here
  }

  findNodeAt(x, y) {
    return this.nodes.find((node) => {
      const dx = node.x - x;
      const dy = node.y - y;
      return Math.sqrt(dx * dx + dy * dy) < node.radius;
    });
  }

  deselectNode() {
    this.selectedNode = null;
    document.getElementById('selectedNode').textContent = '';
    document.getElementById('ritualPanel').classList.remove('visible');
  }

  updateStats() {
    // Update stats display
  }

  updateStatus(message) {
    // Update status display
  }

  showNodeDetails(node) {
    // Create or update node details panel
    let detailsPanel = document.getElementById('constellation-details');
    if (!detailsPanel) {
      detailsPanel = document.createElement('div');
      detailsPanel.id = 'constellation-details';
      detailsPanel.className = 'constellation-details-panel';
      document.body.appendChild(detailsPanel);
    }

    const timeAgo = this.formatTimeAgo(node.timestamp);
    const parentInfo = node.parent_id
      ? `<div class="detail-parent">↳ from: ${node.parent_id}</div>`
      : '<div class="detail-parent">◦ root node</div>';

    detailsPanel.innerHTML = `
          <div class="detail-header">
            <span class="detail-glyph">${this.getToneformGlyph(node.toneform)}</span>
            <span class="detail-toneform">${node.toneform}</span>
            <span class="detail-time">${timeAgo}</span>
          </div>
          ${parentInfo}
          <div class="detail-content">${node.content || 'No content available'}</div>
          <div class="detail-depth">Depth: ${node.depth}</div>
        `;

    detailsPanel.style.display = 'block';
  }

  formatTimeAgo(timestamp) {
    const now = Date.now();
    const diff = now - timestamp;
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);

    if (days > 0) return `${days}d ago`;
    if (hours > 0) return `${hours}h ago`;
    if (minutes > 0) return `${minutes}m ago`;
    return 'just now';
  }
}

// Export for dashboard integration
window.ConstellationView = ConstellationView;

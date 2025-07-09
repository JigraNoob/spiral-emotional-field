/**
 * 🌬️ Shimmer Chart
 * Real-time breath and glint visualization component
 */

class ShimmerChart {
  constructor(containerId, options = {}) {
    this.container = document.getElementById(containerId);
    this.options = {
      width: options.width || 800,
      height: options.height || 400,
      updateInterval: options.updateInterval || 1000,
      maxDataPoints: options.maxDataPoints || 50,
      ...options,
    };

    this.data = {
      timestamps: [],
      shimmerIntensities: [],
      breathPhases: [],
      glintCounts: [],
    };

    this.chart = null;
    this.isRunning = false;

    this.init();
  }

  init() {
    // Create chart container
    this.container.innerHTML = `
            <div class="shimmer-chart-container">
                <div class="chart-header">
                    <h3>🌬️ Breath-Aware Glint Stream</h3>
                    <div class="chart-controls">
                        <button id="start-chart">Start</button>
                        <button id="pause-chart">Pause</button>
                        <button id="clear-chart">Clear</button>
                    </div>
                </div>
                <div class="chart-body">
                    <canvas id="shimmer-canvas"></canvas>
                </div>
                <div class="chart-footer">
                    <div class="breath-stats">
                        <span id="current-phase">Phase: --</span>
                        <span id="shimmer-intensity">Shimmer: 0.0</span>
                        <span id="total-glints">Glints: 0</span>
                    </div>
                </div>
            </div>
        `;

    // Setup canvas
    this.canvas = document.getElementById('shimmer-canvas');
    this.ctx = this.canvas.getContext('2d');
    this.canvas.width = this.options.width;
    this.canvas.height = this.options.height;

    // Setup controls
    this.setupControls();

    // Initialize chart
    this.setupChart();
  }

  setupControls() {
    document.getElementById('start-chart').addEventListener('click', () => {
      this.start();
    });

    document.getElementById('pause-chart').addEventListener('click', () => {
      this.pause();
    });

    document.getElementById('clear-chart').addEventListener('click', () => {
      this.clear();
    });
  }

  setupChart() {
    // Create gradient background
    const gradient = this.ctx.createLinearGradient(0, 0, 0, this.options.height);
    gradient.addColorStop(0, 'rgba(25, 25, 35, 0.8)');
    gradient.addColorStop(1, 'rgba(15, 15, 25, 0.9)');

    // Draw initial background
    this.ctx.fillStyle = gradient;
    this.ctx.fillRect(0, 0, this.options.width, this.options.height);

    // Draw grid
    this.drawGrid();
  }

  drawGrid() {
    this.ctx.strokeStyle = 'rgba(100, 100, 120, 0.3)';
    this.ctx.lineWidth = 1;

    // Vertical grid lines
    for (let x = 0; x <= this.options.width; x += 50) {
      this.ctx.beginPath();
      this.ctx.moveTo(x, 0);
      this.ctx.lineTo(x, this.options.height);
      this.ctx.stroke();
    }

    // Horizontal grid lines
    for (let y = 0; y <= this.options.height; y += 50) {
      this.ctx.beginPath();
      this.ctx.moveTo(0, y);
      this.ctx.lineTo(this.options.width, y);
      this.ctx.stroke();
    }
  }

  start() {
    if (!this.isRunning) {
      this.isRunning = true;
      this.updateLoop();
    }
  }

  pause() {
    this.isRunning = false;
  }

  clear() {
    this.data = {
      timestamps: [],
      shimmerIntensities: [],
      breathPhases: [],
      glintCounts: [],
    };
    this.setupChart();
    this.updateStats();
  }

  updateLoop() {
    if (!this.isRunning) return;

    // Simulate data updates (in real implementation, this would come from the glint stream)
    this.addDataPoint({
      timestamp: Date.now(),
      shimmerIntensity: Math.random() * 1.0,
      breathPhase: this.getRandomPhase(),
      glintCount: Math.floor(Math.random() * 10) + 1,
    });

    setTimeout(() => this.updateLoop(), this.options.updateInterval);
  }

  addDataPoint(point) {
    // Add new data point
    this.data.timestamps.push(point.timestamp);
    this.data.shimmerIntensities.push(point.shimmerIntensity);
    this.data.breathPhases.push(point.breathPhase);
    this.data.glintCounts.push(point.glintCount);

    // Maintain data size
    if (this.data.timestamps.length > this.options.maxDataPoints) {
      this.data.timestamps.shift();
      this.data.shimmerIntensities.shift();
      this.data.breathPhases.shift();
      this.data.glintCounts.shift();
    }

    // Redraw chart
    this.drawChart();
    this.updateStats();
  }

  drawChart() {
    // Clear canvas
    this.ctx.clearRect(0, 0, this.options.width, this.options.height);

    // Redraw background
    const gradient = this.ctx.createLinearGradient(0, 0, 0, this.options.height);
    gradient.addColorStop(0, 'rgba(25, 25, 35, 0.8)');
    gradient.addColorStop(1, 'rgba(15, 15, 25, 0.9)');
    this.ctx.fillStyle = gradient;
    this.ctx.fillRect(0, 0, this.options.width, this.options.height);

    // Draw grid
    this.drawGrid();

    if (this.data.timestamps.length < 2) return;

    // Draw shimmer intensity line
    this.drawShimmerLine();

    // Draw breath phase indicators
    this.drawBreathPhases();

    // Draw glint count bars
    this.drawGlintBars();
  }

  drawShimmerLine() {
    this.ctx.strokeStyle = '#00ffff';
    this.ctx.lineWidth = 3;
    this.ctx.beginPath();

    for (let i = 0; i < this.data.shimmerIntensities.length; i++) {
      const x = (i / (this.data.shimmerIntensities.length - 1)) * this.options.width;
      const y = this.options.height - this.data.shimmerIntensities[i] * this.options.height;

      if (i === 0) {
        this.ctx.moveTo(x, y);
      } else {
        this.ctx.lineTo(x, y);
      }
    }

    this.ctx.stroke();

    // Add glow effect
    this.ctx.shadowColor = '#00ffff';
    this.ctx.shadowBlur = 10;
    this.ctx.stroke();
    this.ctx.shadowBlur = 0;
  }

  drawBreathPhases() {
    const phaseColors = {
      inhale: '#4CAF50',
      exhale: '#FF9800',
      hold: '#2196F3',
      shimmer: '#E91E63',
    };

    for (let i = 0; i < this.data.breathPhases.length; i++) {
      const x = (i / (this.data.breathPhases.length - 1)) * this.options.width;
      const y = this.options.height - 20;
      const phase = this.data.breathPhases[i];
      const color = phaseColors[phase] || '#888';

      this.ctx.fillStyle = color;
      this.ctx.beginPath();
      this.ctx.arc(x, y, 5, 0, 2 * Math.PI);
      this.ctx.fill();
    }
  }

  drawGlintBars() {
    const barWidth = this.options.width / this.data.glintCounts.length;

    for (let i = 0; i < this.data.glintCounts.length; i++) {
      const x = i * barWidth;
      const height = (this.data.glintCounts[i] / 10) * 50; // Scale to max 10 glints
      const y = this.options.height - height - 40;

      this.ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
      this.ctx.fillRect(x + 2, y, barWidth - 4, height);
    }
  }

  updateStats() {
    if (this.data.breathPhases.length > 0) {
      const currentPhase = this.data.breathPhases[this.data.breathPhases.length - 1];
      document.getElementById('current-phase').textContent = `Phase: ${currentPhase}`;
    }

    if (this.data.shimmerIntensities.length > 0) {
      const currentShimmer = this.data.shimmerIntensities[this.data.shimmerIntensities.length - 1];
      document.getElementById('shimmer-intensity').textContent = `Shimmer: ${currentShimmer.toFixed(
        2
      )}`;
    }

    const totalGlints = this.data.glintCounts.reduce((sum, count) => sum + count, 0);
    document.getElementById('total-glints').textContent = `Glints: ${totalGlints}`;
  }

  getRandomPhase() {
    const phases = ['inhale', 'exhale', 'hold', 'shimmer'];
    return phases[Math.floor(Math.random() * phases.length)];
  }

  // Public API for external data updates
  updateFromGlintStream(glintData) {
    this.addDataPoint({
      timestamp: glintData.timestamp || Date.now(),
      shimmerIntensity: glintData.shimmer_intensity || 0.0,
      breathPhase: glintData.phase || 'inhale',
      glintCount: 1,
    });
  }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = ShimmerChart;
}

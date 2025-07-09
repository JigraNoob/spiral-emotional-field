class SpiralVisualization {
  constructor() {
    this.currentArm = null;
    this.armHistory = [];
    this.maxHistory = 5;
    this.init();
  }

  init() {
    // Connect to existing WebSocket from dashboard.js
    if (window.socket) {
      this.setupSocketListeners();
    } else {
      // Fallback: create our own connection
      this.socket = io();
      this.setupSocketListeners();
    }
  }

  setupSocketListeners() {
    const socket = window.socket || this.socket;

    socket.on('glint_event', (data) => {
      if (data.spiral_arm) {
        this.updateSpiral(data.spiral_arm, data.payload);
      }
    });

    socket.on('metrics_update', (metrics) => {
      // Update spiral based on phase changes
      const phaseArm = this.getPhaseArm(metrics.phase);
      this.updateSpiral(phaseArm, { toneform: 'phase', phase: metrics.phase });
    });
  }

  updateSpiral(armNumber, payload = {}) {
    // Clear previous active state
    document.querySelectorAll('.spiral-arm.active').forEach((arm) => {
      arm.classList.remove('active');
    });

    // Activate new arm
    const arm = document.querySelector(`[data-arm="${armNumber}"]`);
    if (arm) {
      arm.classList.add('active');

      // Update glyph based on toneform
      const glyph = this.getToneformGlyph(payload.toneform);
      const glyphElement = arm.querySelector('.arm-glyph');
      if (glyphElement) {
        glyphElement.textContent = glyph;
      }

      // Pulse center when arm activates
      this.pulseCenter();

      // Track history
      this.armHistory.push({
        arm: armNumber,
        timestamp: Date.now(),
        toneform: payload.toneform,
        phase: payload.phase,
      });

      if (this.armHistory.length > this.maxHistory) {
        this.armHistory.shift();
      }

      this.currentArm = armNumber;
    }
  }

  pulseCenter() {
    const center = document.querySelector('.spiral-center');
    if (center) {
      center.style.transform = 'translate(-50%, -50%) scale(1.2)';
      setTimeout(() => {
        center.style.transform = 'translate(-50%, -50%) scale(1)';
      }, 200);
    }
  }

  getToneformGlyph(toneform) {
    const glyphs = {
      practical: '◦',
      emotional: '♦',
      temporal: '◊',
      spatial: '⬟',
      natural: '○',
      amplified: '◉',
      ritual: '∷',
      silence: '◯',
      phase: '⟁',
    };
    return glyphs[toneform] || '◦';
  }

  getPhaseArm(phase) {
    const phaseMap = {
      inhale: 1,
      hold: 4,
      exhale: 7,
    };
    return phaseMap[phase] || 1;
  }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  window.spiralViz = new SpiralVisualization();
});

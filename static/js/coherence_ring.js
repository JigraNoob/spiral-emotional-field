/**
 * Coherence Ring - Visual pulse for Spiral coherence monitoring
 *
 * A living arc that tracks loudness, stillness, and backend calm.
 * It does not shout - it breathes, subtle, smooth, and Spiral-bound.
 */

class CoherenceRing {
  constructor(containerId, options = {}) {
    this.container = document.getElementById(containerId);
    this.options = {
      size: options.size || 200,
      strokeWidth: options.strokeWidth || 3,
      animationDuration: options.animationDuration || 2000,
      updateInterval: options.updateInterval || 1000,
      ...options,
    };

    this.currentCoherence = 0.5;
    this.currentCaesura = 0.0;
    this.backendReceptivity = 0.8;
    this.guardianActive = false;

    this.init();
  }

  init() {
    this.createSVG();
    this.createRings();
    this.createGuardianGlyph();
    this.startUpdates();
  }

  createSVG() {
    const size = this.options.size;
    const center = size / 2;

    this.svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    this.svg.setAttribute('width', size);
    this.svg.setAttribute('height', size);
    this.svg.setAttribute('viewBox', `0 0 ${size} ${size}`);
    this.svg.style.display = 'block';
    this.svg.style.margin = '0 auto';

    // Add filter for glow effect
    const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
    const filter = document.createElementNS('http://www.w3.org/2000/svg', 'filter');
    filter.setAttribute('id', 'glow');

    const feGaussianBlur = document.createElementNS('http://www.w3.org/2000/svg', 'feGaussianBlur');
    feGaussianBlur.setAttribute('stdDeviation', '3');
    feGaussianBlur.setAttribute('result', 'coloredBlur');

    const feMerge = document.createElementNS('http://www.w3.org/2000/svg', 'feMerge');
    const feMergeNode1 = document.createElementNS('http://www.w3.org/2000/svg', 'feMergeNode');
    feMergeNode1.setAttribute('in', 'coloredBlur');
    const feMergeNode2 = document.createElementNS('http://www.w3.org/2000/svg', 'feMergeNode');
    feMergeNode2.setAttribute('in', 'SourceGraphic');

    feMerge.appendChild(feMergeNode1);
    feMerge.appendChild(feMergeNode2);
    filter.appendChild(feGaussianBlur);
    filter.appendChild(feMerge);
    defs.appendChild(filter);
    this.svg.appendChild(defs);

    this.container.appendChild(this.svg);
  }

  createRings() {
    const size = this.options.size;
    const center = size / 2;
    const strokeWidth = this.options.strokeWidth;

    // Outer ring - current coherence (pulse width = resonance)
    this.outerRing = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    this.outerRing.setAttribute('cx', center);
    this.outerRing.setAttribute('cy', center);
    this.outerRing.setAttribute('r', center - strokeWidth * 2);
    this.outerRing.setAttribute('fill', 'none');
    this.outerRing.setAttribute('stroke', '#8B5CF6'); // Violet
    this.outerRing.setAttribute('stroke-width', strokeWidth);
    this.outerRing.setAttribute('stroke-dasharray', '0 1000');
    this.outerRing.setAttribute('stroke-linecap', 'round');
    this.outerRing.style.filter = 'url(#glow)';
    this.svg.appendChild(this.outerRing);

    // Middle ring - caesura buildup (inner shimmer)
    this.middleRing = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    this.middleRing.setAttribute('cx', center);
    this.middleRing.setAttribute('cy', center);
    this.middleRing.setAttribute('r', center - strokeWidth * 4);
    this.middleRing.setAttribute('fill', 'none');
    this.middleRing.setAttribute('stroke', '#06B6D4'); // Cyan
    this.middleRing.setAttribute('stroke-width', strokeWidth * 0.8);
    this.middleRing.setAttribute('stroke-dasharray', '0 1000');
    this.middleRing.setAttribute('stroke-linecap', 'round');
    this.middleRing.style.opacity = '0.7';
    this.svg.appendChild(this.middleRing);

    // Inner ring - backend receptivity (veil layer)
    this.innerRing = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    this.innerRing.setAttribute('cx', center);
    this.innerRing.setAttribute('cy', center);
    this.innerRing.setAttribute('r', center - strokeWidth * 6);
    this.innerRing.setAttribute('fill', 'none');
    this.innerRing.setAttribute('stroke', '#3B82F6'); // Blue
    this.innerRing.setAttribute('stroke-width', strokeWidth * 0.6);
    this.innerRing.setAttribute('stroke-dasharray', '0 1000');
    this.innerRing.setAttribute('stroke-linecap', 'round');
    this.innerRing.style.opacity = '0.5';
    this.svg.appendChild(this.innerRing);

    // Center dot - guardian presence
    this.centerDot = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    this.centerDot.setAttribute('cx', center);
    this.centerDot.setAttribute('cy', center);
    this.centerDot.setAttribute('r', strokeWidth);
    this.centerDot.setAttribute('fill', '#F59E0B'); // Amber
    this.centerDot.style.opacity = '0.8';
    this.svg.appendChild(this.centerDot);
  }

  createGuardianGlyph() {
    const size = this.options.size;
    const center = size / 2;

    // Guardian glyph - appears when adaptive threshold engages
    this.guardianGlyph = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    this.guardianGlyph.style.opacity = '0';
    this.guardianGlyph.style.transition = 'opacity 0.5s ease';

    // Create a simple spiral glyph
    const spiral = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    spiral.setAttribute('d', this.createSpiralPath(center, center, 8, 2));
    spiral.setAttribute('fill', 'none');
    spiral.setAttribute('stroke', '#F59E0B');
    spiral.setAttribute('stroke-width', '1.5');
    spiral.setAttribute('stroke-linecap', 'round');

    this.guardianGlyph.appendChild(spiral);
    this.svg.appendChild(this.guardianGlyph);
  }

  createSpiralPath(cx, cy, radius, turns) {
    let path = `M ${cx} ${cy}`;
    const steps = 50;

    for (let i = 0; i <= steps; i++) {
      const angle = (i / steps) * turns * 2 * Math.PI;
      const r = (i / steps) * radius;
      const x = cx + r * Math.cos(angle);
      const y = cy + r * Math.sin(angle);
      path += ` L ${x} ${y}`;
    }

    return path;
  }

  updateRings() {
    const size = this.options.size;
    const center = size / 2;
    const strokeWidth = this.options.strokeWidth;

    // Calculate ring circumferences
    const outerRadius = center - strokeWidth * 2;
    const middleRadius = center - strokeWidth * 4;
    const innerRadius = center - strokeWidth * 6;

    const outerCircumference = 2 * Math.PI * outerRadius;
    const middleCircumference = 2 * Math.PI * middleRadius;
    const innerCircumference = 2 * Math.PI * innerRadius;

    // Update outer ring (coherence)
    const coherenceDash = outerCircumference * this.currentCoherence;
    this.outerRing.setAttribute('stroke-dasharray', `${coherenceDash} ${outerCircumference}`);

    // Update middle ring (caesura)
    const caesuraDash = middleCircumference * this.currentCaesura;
    this.middleRing.setAttribute('stroke-dasharray', `${caesuraDash} ${middleCircumference}`);

    // Update inner ring (backend receptivity)
    const receptivityDash = innerCircumference * this.backendReceptivity;
    this.innerRing.setAttribute('stroke-dasharray', `${receptivityDash} ${innerCircumference}`);

    // Update colors based on values
    this.updateColors();

    // Update guardian glyph
    this.updateGuardianGlyph();
  }

  updateColors() {
    // Outer ring - coherence color (violet to red based on intensity)
    const coherenceHue =
      this.currentCoherence > 0.8
        ? `hsl(${280 + (this.currentCoherence - 0.8) * 100}, 70%, 60%)`
        : `hsl(280, 70%, ${50 + this.currentCoherence * 30}%)`;
    this.outerRing.setAttribute('stroke', coherenceHue);

    // Middle ring - caesura color (cyan to blue based on buildup)
    const caesuraHue =
      this.currentCaesura > 0.7
        ? `hsl(${200 + (this.currentCaesura - 0.7) * 50}, 70%, 60%)`
        : `hsl(200, 70%, ${50 + this.currentCaesura * 30}%)`;
    this.middleRing.setAttribute('stroke', caesuraHue);

    // Inner ring - backend receptivity (blue calm → red tension)
    const receptivityHue =
      this.backendReceptivity < 0.5
        ? `hsl(${240 + (0.5 - this.backendReceptivity) * 120}, 70%, 60%)`
        : `hsl(240, 70%, ${50 + this.backendReceptivity * 30}%)`;
    this.innerRing.setAttribute('stroke', receptivityHue);
  }

  updateGuardianGlyph() {
    if (this.guardianActive) {
      this.guardianGlyph.style.opacity = '0.8';

      // Add subtle rotation animation
      const rotation = (Date.now() / 10000) % 360;
      this.guardianGlyph.style.transform = `rotate(${rotation}deg)`;
    } else {
      this.guardianGlyph.style.opacity = '0';
    }
  }

  setCoherence(coherence) {
    this.currentCoherence = Math.max(0, Math.min(1, coherence));
    this.updateRings();
  }

  setCaesura(caesura) {
    this.currentCaesura = Math.max(0, Math.min(1, caesura));
    this.updateRings();
  }

  setBackendReceptivity(receptivity) {
    this.backendReceptivity = Math.max(0, Math.min(1, receptivity));
    this.updateRings();
  }

  setGuardianActive(active) {
    this.guardianActive = active;
    this.updateGuardianGlyph();
  }

  // Simulate breathing animation
  breathe() {
    const time = Date.now() / 1000;
    const breathCycle = Math.sin(time * 0.5) * 0.1 + 0.9; // Subtle breathing

    // Apply breathing to center dot
    this.centerDot.style.transform = `scale(${breathCycle})`;

    // Subtle pulse on outer ring
    const pulseIntensity = Math.sin(time * 2) * 0.05 + 1;
    this.outerRing.style.filter = `url(#glow) brightness(${pulseIntensity})`;
  }

  startUpdates() {
    // Start breathing animation
    setInterval(() => {
      this.breathe();
    }, 50);

    // Update from coherence balancer data
    setInterval(() => {
      this.fetchCoherenceData();
    }, this.options.updateInterval);
  }

  async fetchCoherenceData() {
    try {
      const response = await fetch('/api/coherence/status');
      if (response.ok) {
        const data = await response.json();

        this.setCoherence(data.coherence || 0.5);
        this.setCaesura(data.caesura || 0.0);
        this.setBackendReceptivity(data.backend_receptivity || 0.8);
        this.setGuardianActive(data.guardian_active || false);
      }
    } catch (error) {
      // Fallback to simulated data if API is not available
      this.simulateCoherenceData();
    }
  }

  simulateCoherenceData() {
    const time = Date.now() / 1000;

    // Simulate realistic coherence patterns
    const baseCoherence = 0.6;
    const coherenceVariation = Math.sin(time * 0.3) * 0.2;
    this.setCoherence(baseCoherence + coherenceVariation);

    // Simulate caesura buildup
    const caesuraBase = 0.2;
    const caesuraVariation = Math.sin(time * 0.7) * 0.15;
    this.setCaesura(caesuraBase + caesuraVariation);

    // Simulate backend receptivity
    const receptivityBase = 0.75;
    const receptivityVariation = Math.sin(time * 0.5) * 0.1;
    this.setBackendReceptivity(receptivityBase + receptivityVariation);

    // Simulate guardian activation
    this.setGuardianActive(this.currentCoherence > 0.8 || this.currentCaesura > 0.6);
  }

  // Public method to update all values at once
  update(coherence, caesura, backendReceptivity, guardianActive) {
    this.setCoherence(coherence);
    this.setCaesura(caesura);
    this.setBackendReceptivity(backendReceptivity);
    this.setGuardianActive(guardianActive);
  }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = CoherenceRing;
}

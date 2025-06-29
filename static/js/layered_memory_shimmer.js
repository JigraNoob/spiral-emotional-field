// layered_memory_shimmer.js
// Manages the layered shimmer blending effect for multiple memories

class LayeredShimmerManager {
  constructor(containerId = 'shimmer-container') {
    this.container = document.getElementById(containerId);
    this.layers = [];
  }

  addShimmerLayer(murmurText, tone, opacity = 0.7, duration = 3000) {
    const layer = document.createElement('div');
    layer.className = 'shimmer-layer';
    layer.innerText = murmurText;
    layer.style.position = 'absolute';
    layer.style.bottom = '10px';
    layer.style.left = '10px';
    layer.style.padding = '0.8rem 1rem';
    layer.style.background = this.getToneColor(tone);
    layer.style.opacity = opacity;
    layer.style.animation = `layerPulse ${duration}ms infinite`;
    this.container.appendChild(layer);
    this.layers.push(layer);
    this.animateLayer(layer);
  }

  getToneColor(tone) {
    const toneColors = {
      "longing": "#E0BBE4",
      "movement": "#957DAD",
      "form": "#D291BC",
      "infrastructure": "#FEC8D8",
      "connection": "#FFDFD3",
      "trust": "#C7CEEA",
      "coherence": "#B5EAD7",
      "adaptation": "#FFDAC1",
      "unknown": "#CCCCCC"
    };
    return toneColors[tone.toLowerCase()] || toneColors["unknown"];
  }

  animateLayer(layer) {
    const pulseKeyframes = `
      @keyframes layerPulse {
        0% { transform: scale(1); opacity: 0.7; }
        50% { transform: scale(1.1); opacity: 0.9; }
        100% { transform: scale(1); opacity: 0.7; }
      }
    `;
    const style = document.createElement('style');
    style.innerHTML = pulseKeyframes;
    document.head.appendChild(style);
  }

  updateShimmerRendering() {
    // Update shimmer layer properties over time if needed
    this.layers.forEach((layer, index) => {
      const opacity = 0.7 + (Math.sin(index * 0.5) * 0.2);
      layer.style.opacity = opacity;
    });
  }
}

// Initialize the LayeredShimmerManager when the DOM is ready
document.addEventListener("DOMContentLoaded", () => {
  const shimmerManager = new LayeredShimmerManager();
  // Sample murmur data - replace with real data from backend
  shimmerManager.addShimmerLayer("Memory of the deep longing.", "longing");
  shimmerManager.addShimmerLayer("The quiet pulse of movement.", "movement");
  shimmerManager.addShimmerLayer("Form rising, solidifying in presence.", "form");
  // Animation loop
  setInterval(() => shimmerManager.updateShimmerRendering(), 50);
});

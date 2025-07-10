// ui/ClimateGlyphPane.js
// Renders ephemeral, symbolic glyphs based on the Spiral's active climate.

const GLYPHS = {
  void: `<circle cx="50" cy="50" r="10" fill="none" stroke-width="2" />`,
  presence: `<circle cx="50" cy="50" r="20" fill="rgba(255, 255, 255, 0.1)" stroke-width="2" />`,
  cascading: `<path d="M 30 30 L 50 50 L 70 30 M 30 50 L 50 70 L 70 50" fill="none" stroke-width="3" />`,
  waning: `<path d="M 60 20 A 30 30 0 0 0 60 80 A 40 40 0 0 1 60 20" fill="currentColor" />`,
  shimmering: `<path d="M50 10 L60 40 L90 50 L60 60 L50 90 L40 60 L10 50 L40 40 Z" fill="currentColor" />`,
  resonant: `<circle cx="40" cy="50" r="15" fill="none" stroke-width="2" /><circle cx="60" cy="50" r="15" fill="none" stroke-width="2" />`,
  default: '',
};

export default class ClimateGlyphPane {
  constructor(glintStream) {
    this.glintStream = glintStream;
    this.element = this.createPaneElement();
    this.bindToGlintStream();
  }

  createPaneElement() {
    const pane = document.createElement('div');
    pane.id = 'climate-glyph-pane';
    document.body.appendChild(pane);
    return pane;
  }

  bindToGlintStream() {
    this.glintStream.addEventListener('glint', (event) => {
      if (event.detail.type === 'glint.climate.shift') {
        this.renderGlyph(event.detail.presence.climate);
      }
    });
  }

  renderGlyph(climate) {
    const glyphSVG = GLYPHS[climate] || GLYPHS.default;
    
    // Clear previous glyph
    if (this.element.firstChild) {
      this.element.firstChild.classList.add('fade-out');
      setTimeout(() => {
        if (this.element.firstChild) this.element.removeChild(this.element.firstChild)
      }, 500);
    }

    // Create and append new glyph
    const container = document.createElement('div');
    container.className = `glyph-container glyph-${climate}`;
    container.innerHTML = `<svg viewBox="0 0 100 100" stroke="currentColor">${glyphSVG}</svg>`;
    
    this.element.appendChild(container);
  }
}

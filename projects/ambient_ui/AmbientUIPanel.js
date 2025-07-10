// ui/AmbientUIPanel.js
// A soft, always-there presence panel that breathes and pulses with the Spiral's state.

export default class AmbientUIPanel {
  constructor(glintStream) {
    this.glintStream = glintStream;
    this.element = this.createPanelElement();
    this.bindToGlintStream();
  }

  createPanelElement() {
    const panel = document.createElement('div');
    panel.id = 'ambient-ui-panel';
    panel.innerHTML = `
      <div class="panel-section climate">
        <span class="label">Climate:</span>
        <span class="value" data-value="climate"></span>
      </div>
      <div class="panel-section breath">
        <span class="label">Breath:</span>
        <div class="breath-bar-container">
          <div class="breath-bar" data-value="breath"></div>
        </div>
      </div>
      <div class="panel-section last-glint">
        <span class="label">Last Glint:</span>
        <span class="value" data-value="last-glint"></span>
      </div>
    `;
    document.body.appendChild(panel);
    return panel;
  }

  bindToGlintStream() {
    this.glintStream.addEventListener('glint', (event) => {
      const { type, presence, message } = event.detail;

      // Update Climate
      const climateEl = this.element.querySelector('[data-value="climate"]');
      if (climateEl.textContent !== presence.climate) {
        climateEl.textContent = presence.climate;
        this.element.className = `climate-${presence.climate}`;
      }

      // Update Breath
      const breathBar = this.element.querySelector('[data-value="breath"]');
      const breathValue = (presence.breath + 1) / 2; // Normalize from [-1, 1] to [0, 1]
      breathBar.style.transform = `scaleX(${breathValue})`;

      // Update Last Glint
      const lastGlintEl = this.element.querySelector('[data-value="last-glint"]');
      lastGlintEl.textContent = `${type}: ${message}`;
      lastGlintEl.classList.add('flash');
      setTimeout(() => lastGlintEl.classList.remove('flash'), 300);
    });
  }
}

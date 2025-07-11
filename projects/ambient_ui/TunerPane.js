
class TunerPane {
  constructor(glintStream) {
    this.glintStream = glintStream;
    this.container = this.createContainer();
    this.glintStream.addEventListener('autotuner.update', (event) => {
      this.renderTuning(event.detail);
    });
  }

  createContainer() {
    const container = document.createElement('div');
    container.id = 'tuner-pane';
    container.style.position = 'fixed';
    container.style.bottom = '20px';
    container.style.right = '20px';
    container.style.width = '300px';
    container.style.backgroundColor = 'rgba(0, 0, 0, 0.7)';
    container.style.color = 'white';
    container.style.padding = '15px';
    container.style.borderRadius = '10px';
    container.style.fontFamily = 'monospace';
    document.body.appendChild(container);
    return container;
  }

  renderTuning(tuning) {
    let tuningDiv = this.container.querySelector('.autotuner-update');
    if (!tuningDiv) {
      tuningDiv = document.createElement('div');
      tuningDiv.className = 'autotuner-update';
      this.container.appendChild(tuningDiv);
    }
    tuningDiv.innerHTML = `
      <h4>Auto-Tuner</h4>
      <pre>${JSON.stringify(tuning, null, 2)}</pre>
    `;
  }
}

// Example usage:
// const glintStream = new EventTarget();
// const tunerPane = new TunerPane(glintStream);
//
// glintStream.dispatchEvent(new CustomEvent('autotuner.update', {
//   detail: {
//     parameter: 'ritual_participation_window_ms',
//     oldValue: 300000,
//     newValue: 330000,
//     rationale: 'Success rate > 90%'
//   }
// }));

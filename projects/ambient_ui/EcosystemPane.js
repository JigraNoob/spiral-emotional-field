
class EcosystemPane {
  constructor(glintStream) {
    this.glintStream = glintStream;
    this.container = this.createContainer();
    this.glintStream.addEventListener('glint.climate.external', (event) => {
      this.renderExternalClimate(event.detail);
    });
    this.glintStream.addEventListener('glint.peer.health', (event) => {
      this.renderPeerHealth(event.detail);
    });
  }

  createContainer() {
    const container = document.createElement('div');
    container.id = 'ecosystem-pane';
    container.style.position = 'fixed';
    container.style.top = '20px';
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

  renderExternalClimate(climate) {
    let climateDiv = this.container.querySelector('.external-climate');
    if (!climateDiv) {
      climateDiv = document.createElement('div');
      climateDiv.className = 'external-climate';
      this.container.appendChild(climateDiv);
    }
    climateDiv.innerHTML = `
      <h4>External Climate</h4>
      <pre>${JSON.stringify(climate.toneform, null, 2)}</pre>
    `;
  }

  renderPeerHealth(peer) {
    let peerDiv = this.container.querySelector(`.peer-${peer.id}`);
    if (!peerDiv) {
      peerDiv = document.createElement('div');
      peerDiv.className = `peer-${peer.id}`;
      this.container.appendChild(peerDiv);
    }
    peerDiv.innerHTML = `
      <h4>Peer: ${peer.id}</h4>
      <p>Latency: ${peer.latency}ms</p>
      <p>Resonance: ${peer.resonance}</p>
    `;
  }
}

// Example usage:
// const glintStream = new EventTarget(); // or your actual event emitter
// const ecosystemPane = new EcosystemPane(glintStream);
//
// To test:
// glintStream.dispatchEvent(new CustomEvent('glint.climate.external', {
//   detail: {
//     source: 'external',
//     toneform: { temperature: 22, emotional_saturation: 0.8, tension: 0.3 }
//   }
// }));
// glintStream.dispatchEvent(new CustomEvent('glint.peer.health', {
//   detail: { id: 'peer-1', latency: 120, resonance: 0.9 }
// }));

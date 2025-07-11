
class ChroniclePane {
  constructor(glintStream) {
    this.glintStream = glintStream;
    this.container = this.createContainer();
    this.glintStream.addEventListener('glint.chronicle.emit', (event) => {
      this.renderEvent(event.detail);
    });
  }

  createContainer() {
    const container = document.createElement('div');
    container.id = 'chronicle-pane';
    container.style.position = 'fixed';
    container.style.top = '20px';
    container.style.left = '20px';
    container.style.width = '400px';
    container.style.height = '90%';
    container.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
    container.style.color = 'white';
    container.style.padding = '15px';
    container.style.borderRadius = '10px';
    container.style.fontFamily = 'monospace';
    container.style.overflowY = 'auto';
    document.body.appendChild(container);
    return container;
  }

  renderEvent(event) {
    const eventElement = document.createElement('div');
    eventElement.className = 'chronicle-event';
    eventElement.style.marginBottom = '10px';
    eventElement.style.paddingBottom = '10px';
    eventElement.style.borderBottom = '1px solid #555';

    const title = document.createElement('h4');
    title.textContent = `${event.type} - ${new Date(event.timestamp).toLocaleTimeString()}`;
    title.style.margin = '0 0 5px 0';

    const payload = document.createElement('pre');
    payload.textContent = JSON.stringify(event.payload, null, 2);
    payload.style.margin = '0';
    payload.style.whiteSpace = 'pre-wrap';
    payload.style.wordBreak = 'break-all';


    eventElement.appendChild(title);
    eventElement.appendChild(payload);

    this.container.prepend(eventElement);
  }
}

// Example usage:
// const glintStream = new EventTarget(); // or your actual event emitter
// const chroniclePane = new ChroniclePane(glintStream);
//
// To test:
// glintStream.dispatchEvent(new CustomEvent('glint.chronicle.emit', {
//   detail: {
//     id: 'some-uuid',
//     timestamp: Date.now(),
//     type: 'glyph.emit',
//     source: 'glyphcraft',
//     payload: { glyph_id: 'softfold.trace' }
//   }
// }));

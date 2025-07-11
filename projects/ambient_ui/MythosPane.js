
class MythosPane {
  constructor(glintStream) {
    this.glintStream = glintStream;
    this.container = this.createContainer();
    this.glintStream.addEventListener('glint.mythos.emit', (event) => {
      this.renderMythos(event.detail);
    });
  }

  createContainer() {
    const container = document.createElement('div');
    container.id = 'mythos-pane';
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

  renderMythos(mythosGlyph) {
    const mythosElement = document.createElement('div');
    mythosElement.className = 'mythos-notification';
    mythosElement.style.marginBottom = '10px';
    mythosElement.style.paddingBottom = '10px';
    mythosElement.style.borderBottom = '1-px solid #555';

    const title = document.createElement('h3');
    title.textContent = mythosGlyph.mythos_id;
    title.style.margin = '0 0 5px 0';

    const description = document.createElement('p');
    description.textContent = mythosGlyph.description;
    description.style.margin = '0 0 10px 0';

    const invokeButton = document.createElement('button');
    invokeButton.textContent = 'Invoke Ritual';
    invokeButton.onclick = () => {
      this.glintStream.emit('mythos.ritual.invoke', {
        mythos_id: mythosGlyph.mythos_id
      });
    };

    mythosElement.appendChild(title);
    mythosElement.appendChild(description);
    mythosElement.appendChild(invokeButton);

    this.container.prepend(mythosElement);

    // Remove the notification after some time
    setTimeout(() => {
      mythosElement.remove();
    }, 30000);
  }
}

// Example usage:
// const glintStream = new EventTarget(); // or your actual event emitter
// const mythosPane = new MythosPane(glintStream);
//
// To test:
// glintStream.dispatchEvent(new CustomEvent('glint.mythos.emit', {
//   detail: {
//     mythos_id: 'mythos.gentle_return',
//     description: 'A cycle of descent, remembrance, and awakening.'
//   }
// }));

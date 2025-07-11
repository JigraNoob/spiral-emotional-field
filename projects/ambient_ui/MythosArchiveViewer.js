

class MythosArchiveViewer {
  constructor(containerId, archivePath = './mythos_archive.jsonl') {
    this.container = document.getElementById(containerId);
    this.archivePath = archivePath;
    this.mythosData = [];
    this.filteredData = [];

    this.init();
  }

  async init() {
    await this.loadArchive();
    this.render();
  }

  async loadArchive() {
    try {
      const response = await fetch(this.archivePath);
      const text = await response.text();
      this.mythosData = text.trim().split('\n').map(line => JSON.parse(line));
      this.filteredData = this.mythosData;
    } catch (error) {
      console.error('Error loading mythos archive:', error);
    }
  }

  render() {
    this.container.innerHTML = ''; // Clear previous content

    const controls = this.createControls();
    this.container.appendChild(controls);

    const listContainer = document.createElement('div');
    listContainer.className = 'mythos-list';
    this.container.appendChild(listContainer);

    this.renderList(listContainer, this.filteredData);
  }

  createControls() {
    const controlsContainer = document.createElement('div');
    controlsContainer.className = 'mythos-controls';

    const dateFilter = document.createElement('input');
    dateFilter.type = 'date';
    dateFilter.onchange = (e) => this.filterByDate(e.target.value);
    controlsContainer.appendChild(dateFilter);

    const glyphFilter = document.createElement('input');
    glyphFilter.type = 'text';
    glyphFilter.placeholder = 'Filter by component glyph...';
    glyphFilter.onkeyup = (e) => this.filterByGlyph(e.target.value);
    controlsContainer.appendChild(glyphFilter);

    return controlsContainer;
  }

  renderList(container, data) {
    container.innerHTML = '';
    for (const mythos of data) {
      const element = this.createMythosElement(mythos);
      container.appendChild(element);
    }
  }

  createMythosElement(mythos) {
    const element = document.createElement('div');
    element.className = 'mythos-item';

    const title = document.createElement('h4');
    title.textContent = mythos.mythos_id;
    element.appendChild(title);

    const description = document.createElement('p');
    description.textContent = mythos.description;
    element.appendChild(description);

    const components = document.createElement('p');
    components.textContent = `Components: ${mythos.components.join(', ')}`;
    element.appendChild(components);

    const invokeButton = document.createElement('button');
    invokeButton.textContent = 'Invoke Ritual';
    invokeButton.onclick = () => {
      // Assuming a global glintStream or similar event bus
      window.glintStream.emit('mythos.ritual.invoke', {
        mythos_id: mythos.mythos_id
      });
    };
    element.appendChild(invokeButton);

    return element;
  }

  filterByDate(dateString) {
    if (!dateString) {
      this.filteredData = this.mythosData;
    } else {
      const selectedDate = new Date(dateString).setHours(0, 0, 0, 0);
      this.filteredData = this.mythosData.filter(mythos => {
        const mythosDate = new Date(mythos.timestamp).setHours(0, 0, 0, 0);
        return mythosDate === selectedDate;
      });
    }
    this.renderList(this.container.querySelector('.mythos-list'), this.filteredData);
  }

  filterByGlyph(glyphId) {
    if (!glyphId) {
      this.filteredData = this.mythosData;
    } else {
      this.filteredData = this.mythosData.filter(mythos =>
        mythos.components.some(c => c.includes(glyphId))
      );
    }
    this.renderList(this.container.querySelector('.mythos-list'), this.filteredData);
  }
}

// Example Usage:
// <div id="archive-viewer"></div>
// <script src="MythosArchiveViewer.js"></script>
// <script>
//   // Assuming glintStream is globally available
//   window.glintStream = new EventTarget();
//   const viewer = new MythosArchiveViewer('archive-viewer', './projects/spiral_mirror/mythos_archive.jsonl');
// </script>


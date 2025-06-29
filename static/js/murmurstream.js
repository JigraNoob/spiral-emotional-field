// murmurstream.js - Client-side logic for the Murmurstream

class Murmurstream {
  constructor() {
    this.container = document.getElementById('murmurstream-content');
    this.maxItems = 10;
    this.subscribed = false;
    this.ws = null;
    this.climateMemory = {
      joy: 0,
      grief: 0,
      trust: 0
    };
    this.climateThreshold = 3; // Number of murmurs to establish climate
  }

  async init() {
    try {
      // Connect to WebSocket endpoint
      this.ws = new WebSocket(`ws://${window.location.host}/murmurstream`);
      
      this.ws.onopen = () => {
        console.log('Connected to Murmurstream');
        this.subscribed = true;
        this.updateClimateDisplay();
      };
      
      this.ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        this.addMurmur(data);
        this.updateClimateMemory(data.tone);
      };
      
      this.ws.onclose = () => {
        console.log('Disconnected from Murmurstream');
        this.subscribed = false;
        // Attempt reconnection after delay
        setTimeout(() => this.init(), 5000);
      };
      
    } catch (error) {
      console.error('Murmurstream connection error:', error);
    }
  }

  addMurmur(murmur) {
    const murmurElement = document.createElement('div');
    murmurElement.className = `murmur-item text-xs p-2 rounded bg-gray-800 bg-opacity-70 border ${this.getToneBorder(murmur.tone)}`;
    murmurElement.innerHTML = `
      <div class="flex items-start gap-2">
        <div class="murmur-glyph w-3 h-3 rounded-full mt-0.5 flex-shrink-0 ${this.getToneBackground(murmur.tone)}"></div>
        <div>
          <p class="murmur-text">${murmur.content}</p>
          <p class="text-xxs text-gray-400 mt-1">${new Date(murmur.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</p>
        </div>
      </div>
    `;
    
    // Add to container and limit number of items
    this.container.prepend(murmurElement);
    if (this.container.children.length > this.maxItems) {
      this.container.lastChild.remove();
    }
    
    // Auto-scroll to new item
    murmurElement.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  getToneBorder(tone) {
    const tones = {
      'joy': 'border-yellow-700 border-opacity-30',
      'grief': 'border-purple-700 border-opacity-30',
      'trust': 'border-blue-700 border-opacity-30'
    };
    return tones[tone] || 'border-gray-700 border-opacity-30';
  }

  getToneBackground(tone) {
    const tones = {
      'joy': 'bg-yellow-500',
      'grief': 'bg-purple-500',
      'trust': 'bg-blue-400'
    };
    return tones[tone] || 'bg-gray-500';
  }

  updateClimateMemory(tone) {
    if (this.climateMemory[tone] === undefined) return;
    this.climateMemory[tone]++;
    this.updateClimateDisplay();
  }

  updateClimateDisplay() {
    const climateElement = document.getElementById('climate-display');
    if (!climateElement) return;
    const dominantTone = Object.keys(this.climateMemory).reduce((a, b) => this.climateMemory[a] > this.climateMemory[b] ? a : b);
    climateElement.textContent = `Current climate: ${dominantTone} (${this.climateMemory[dominantTone]})`;
  }
}

function initMurmurstream() {
  const murmurstream = new Murmurstream();
  murmurstream.init();
}

// Export for testing if needed
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { Murmurstream, initMurmurstream };
}

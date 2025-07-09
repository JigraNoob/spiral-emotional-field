function connectToGlintStream() {
  const eventSource = new EventSource('/stream_glints');
  const container = document.getElementById('glint-container');

  if (!container) {
    console.error('Glint container not found.');
    return;
  }

  eventSource.onmessage = function (event) {
    try {
      const glint = JSON.parse(event.data);
      updateDashboardWithGlint(glint, container);
    } catch (e) {
      console.error('Invalid glint data:', event.data, e);
    }
  };

  eventSource.onerror = function (error) {
    console.error('Error in glint stream:', error);
    eventSource.close();
    // Attempt to reconnect after a delay
    setTimeout(connectToGlintStream, 5000);
  };
}

function updateDashboardWithGlint(glint, container) {
  // Create a visual block for the glint
  const el = document.createElement('div');
  el.className = 'glint-entry';
  el.textContent = `[${glint.glint?.timestamp || 'now'}] ${glint.glint?.toneform || '??'} → ${
    glint.glint?.content || JSON.stringify(glint)
  }`;

  // Add color based on toneform
  el.style.borderLeftColor = getToneformColor(glint.glint?.toneform);

  // Add timestamp and schedule aging behavior for "Silent Glint Echoes"
  el.dataset.createdAt = Date.now(); // Store when this card was added

  // Set timeout to mark as "old" after 90 seconds
  setTimeout(() => {
    el.classList.add('glint-old');
  }, 90000); // 90,000 ms = 90 seconds

  // Prepend to container (add to top)
  container.prepend(el);

  // Limit the number of displayed glints (e.g., keep only the latest 50)
  while (container.children.length > 50) {
    container.removeChild(container.lastChild);
  }

  console.log('Received new glint:', glint);
}

function getToneformColor(toneform) {
  const colors = {
    practical: '#4CAF50',
    emotional: '#FF9800',
    intellectual: '#2196F3',
    spiritual: '#9C27B0',
    relational: '#E91E63',
  };
  return colors[toneform] || '#6cc6d1'; // Default color if toneform is not recognized
}

function updateGlintStream(glintData) {
  const glintStream = document.getElementById('glint-stream');
  if (glintStream) {
    const glintElement = document.createElement('div');
    glintElement.className = 'glint-entry';
    glintElement.innerHTML = `
            <span class="glint-timestamp">${new Date().toLocaleTimeString()}</span>
            <span class="glint-toneform">${glintData.payload.toneform || 'unknown'}</span>
            <span class="glint-content">${glintData.payload.content || ''}</span>
        `;

    glintStream.insertBefore(glintElement, glintStream.firstChild);

    // Keep only last 10 entries
    while (glintStream.children.length > 10) {
      glintStream.removeChild(glintStream.lastChild);
    }
  }
}

// Enhanced WebSocket connection with spiral integration
function initializeSpiralWebSocket() {
  const socket = new WebSocket('ws://localhost:5000');

  socket.onopen = function () {
    console.log('🌀 Spiral WebSocket connection established');
  };

  socket.onmessage = function (event) {
    const data = JSON.parse(event.data);

    if (data.type === 'glint_event') {
      console.log('🌀 Glint event received:', data);

      // Update existing glint stream
      updateGlintStream(data);

      // Update spiral visualization if available
      if (window.spiralViz && data.spiral_arm) {
        window.spiralViz.updateSpiral(data.spiral_arm, data.payload);
      }

      // Update dashboard metrics
      updateDashboardMetrics(data);
    }
  };

  socket.onclose = function () {
    console.log('🌀 Spiral WebSocket connection closed - attempting reconnect');
    setTimeout(initializeSpiralWebSocket, 5000);
  };

  socket.onerror = function (error) {
    console.error('🌀 Spiral WebSocket error:', error);
  };

  // Make socket globally available
  window.spiralSocket = socket;
}

function updateDashboardMetrics(glintData) {
  // Update phase indicator if present
  const phaseOrb = document.getElementById('phase-orb');
  const currentPhase = document.getElementById('current-phase');

  if (glintData.payload.phase && currentPhase) {
    currentPhase.textContent = glintData.payload.phase;
  }

  if (phaseOrb && glintData.payload.toneform) {
    phaseOrb.className = `phase-orb toneform-${glintData.payload.toneform}`;
  }
}

// Initialize everything when DOM loads
document.addEventListener('DOMContentLoaded', function () {
  // Connect to existing glint stream
  connectToGlintStream();

  // Initialize spiral WebSocket
  initializeSpiralWebSocket();

  console.log('🌀 Spiral Dashboard initialized');
});

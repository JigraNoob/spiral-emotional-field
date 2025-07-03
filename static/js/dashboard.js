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

// Call this function when the page loads
document.addEventListener('DOMContentLoaded', connectToGlintStream);
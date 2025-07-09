let socket;
const RECONNECT_INTERVAL = 3000; // milliseconds

const glyphMap = {
  inhale: '🌬️',
  hold: '⏸️',
  exhale: '💨',
  return: '🔄',
  witness: '👁️',
  caesura: '🌑',
};

function updateElement(id, content) {
  const element = document.getElementById(id);
  if (element) {
    element.textContent = content;
  } else {
    console.warn(`Element with ID '${id}' not found.`);
  }
}

function appendResponse(message) {
  const responseContainer = document.getElementById('responseContainer');
  if (responseContainer) {
    const p = document.createElement('p');
    p.textContent = message;
    responseContainer.appendChild(p);
    responseContainer.scrollTop = responseContainer.scrollHeight; // Auto-scroll to bottom
  }
}

function connectWebSocket() {
  socket = new WebSocket('ws://' + window.location.host + '/ws');

  socket.onopen = function(event) {
    console.log('WebSocket connection opened');
    appendResponse('System: Connected to Shrine WebSocket.');
  };

  socket.onmessage = function (event) {
    const data = JSON.parse(event.data);
    if (data.type === 'echo') {
      appendResponse(`Echo: ${data.message}`);
    } else {
      // Handle breath phase updates
      updateElement('breath-glyph', glyphMap[data.breath_phase] || '🌀');
      updateElement('phase', `Breath Phase: ${data.breath_phase.toUpperCase()}`);
      updateElement('glint', `Glint: ${data.glint}`);
      updateElement('intention', `Intention: ${data.intention}`);
      updateElement('toneform', `Toneform: ${data.toneform}`);
    }
  };

  socket.onclose = function (event) {
    console.log('WebSocket connection closed');
    appendResponse('System: WebSocket connection closed. Reconnecting...');
    setTimeout(connectWebSocket, RECONNECT_INTERVAL);
  };

  socket.onerror = function (error) {
    console.error('WebSocket error:', error);
    appendResponse('System: WebSocket error. Closing connection.');
    socket.close(); // Close the socket to trigger onclose and reconnection
  };
}

document.addEventListener('DOMContentLoaded', () => {
  connectWebSocket();

  const userInput = document.getElementById('userInput');
  const sendButton = document.getElementById('sendButton');

  if (sendButton && userInput) {
    sendButton.addEventListener('click', () => {
      const message = userInput.value;
      if (message) {
        socket.send(message);
        appendResponse(`You: ${message}`);
        userInput.value = ''; // Clear input field
      }
    });

    userInput.addEventListener('keypress', (event) => {
      if (event.key === 'Enter') {
        sendButton.click();
      }
    });
  }
});

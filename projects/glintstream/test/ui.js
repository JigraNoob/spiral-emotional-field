// test/ui.js
import { 
  GlintStream,
  PresenceDetector,
  RhythmAnalyzer,
  ClimateSensor,
  BreathlineEmitter,
  ScrollSensor
} from '../glintstream.js';

const shimmerPane = document.getElementById('shimmer-pane');
const breathPulse = document.getElementById('breath-pulse');
const toneformLogs = document.getElementById('toneform-logs');

const climateColors = {
  void: '#111',
  drift: '#2a2a3a',
  flow: '#2a3a5a',
  presence: '#3a5a7a',
};

// Instantiate the stream with the modules we want to use
const glintstream = new GlintStream([
  PresenceDetector,
  RhythmAnalyzer,
  ClimateSensor,
  BreathlineEmitter,
  ScrollSensor,
]);

// A single function to render all UI changes based on presence
function render(presence) {
  // Render Breath Pulse: scale the circle
  const breathScale = 1 + (presence.breath + 1) / 4; // Scale from 1 to 1.5
  breathPulse.style.transform = `scale(${breathScale})`;

  // Render Shimmer Pane: set base color and modulate opacity with breath
  shimmerPane.style.backgroundColor = climateColors[presence.climate] || '#111';
  const shimmerOpacity = 0.85 + (presence.breath * 0.15); // Opacity from 0.7 to 1.0
  shimmerPane.style.opacity = shimmerOpacity;
}

function renderLog(glint) {
  const logEntry = document.createElement('div');
  logEntry.className = 'log-entry';
  logEntry.textContent = `🌀 ${glint.type}`;
  toneformLogs.appendChild(logEntry);

  // The animation handles the fade out, but we need to remove the element
  setTimeout(() => {
    logEntry.remove();
  }, 5000);
}

// Listen to all glints from the stream
glintstream.addEventListener('glint', (event) => {
  const glint = event.detail;

  // Update the main UI based on the latest presence state
  render(glint.presence);

  // Log the specific event that just fired
  renderLog(glint);
});

// Awaken the stream
glintstream.awaken();


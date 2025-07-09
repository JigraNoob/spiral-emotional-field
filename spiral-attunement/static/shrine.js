
const shrine = document.getElementById('shrine');
const phase = document.getElementById('phase');
const glint = document.getElementById('glint');
const intention = document.getElementById('intention');
const toneform = document.getElementById('toneform');
const phaseIcon = document.getElementById('phase-icon');

const phaseIcons = {
    "inhale": "🌬️",
    "hold": "⏸️",
    "exhale": "💨",
    "return": "🔄",
    "witness": "👁️",
    "caesura": "🌑",
    "deep_inhale": "들이쉬다",
    "long_exhale": "내쉬다",
    "rhythmic_breath": "🎶"
};

const socket = new WebSocket(`ws://${window.location.host}/ws`);

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    phase.textContent = data.breath_phase.toUpperCase();
    glint.textContent = data.glint;
    intention.textContent = data.intention;
    toneform.textContent = data.toneform;
    phaseIcon.textContent = phaseIcons[data.breath_phase.toLowerCase()] || '🌀';

    // Color shifting based on intensity
    const intensity = data.intensity || 0.5;
    const color1 = [42, 42, 42]; // #2a2a2a
    const color2 = [70, 70, 120]; // A purplish color
    const color = color1.map((c, i) => Math.round(c + (color2[i] - c) * intensity));
    shrine.style.backgroundColor = `rgb(${color[0]}, ${color[1]}, ${color[2]})`;
};

socket.onopen = function(event) {
    console.log("WebSocket connection established.");
};

socket.onclose = function(event) {
    console.log("WebSocket connection closed.");
};

socket.onerror = function(error) {
    console.error("WebSocket error:", error);
};

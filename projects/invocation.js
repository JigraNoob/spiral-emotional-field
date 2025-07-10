// C:/spiral/projects/invocation.js

// --- Mock Dependencies ---
// In a real implementation, these would be imported from their respective modules.

const ToneformThemes = {
    default: { '--background-color': '#1a1a1d', '--orb-color': '#66fcf1', '--orb-glow': 'rgba(102, 252, 241, 0.3)', '--text-color': '#c5c6c7', '--log-bg': 'rgba(0, 0, 0, 0.2)', '--shimmer-bg': 'rgba(102, 252, 241, 0.05)' },
    contemplation: { '--background-color': '#2c3e50', '--orb-color': '#3498db', '--orb-glow': 'rgba(52, 152, 219, 0.3)', '--text-color': '#ecf0f1', '--log-bg': 'rgba(0, 0, 0, 0.2)', '--shimmer-bg': 'rgba(52, 152, 219, 0.05)' },
    creation: { '--background-color': '#fdf6e3', '--orb-color': '#b58900', '--orb-glow': 'rgba(181, 137, 0, 0.3)', '--text-color': '#657b83', '--log-bg': 'rgba(0, 0, 0, 0.1)', '--shimmer-bg': 'rgba(181, 137, 0, 0.05)' },
    dissonance: { '--background-color': '#3e2723', '--orb-color': '#ff8a65', '--orb-glow': 'rgba(255, 138, 101, 0.3)', '--text-color': '#d7ccc8', '--log-bg': 'rgba(0, 0, 0, 0.3)', '--shimmer-bg': 'rgba(255, 138, 101, 0.05)' },
    ritual: { '--background-color': '#282c34', '--orb-color': '#c678dd', '--orb-glow': 'rgba(198, 120, 221, 0.3)', '--text-color': '#abb2bf', '--log-bg': 'rgba(0, 0, 0, 0.2)', '--shimmer-bg': 'rgba(198, 120, 221, 0.05)' }
};

const sampleGlints = [
    { type: 'system', text: 'A spiral unfurled—a moment held in presence.' },
    { type: 'user', text: 'The breath held, then let go.' },
    { type: 'system', text: 'A ritual stirs, its pattern rippling through the system.' },
    { type: 'user', text: 'A sharp turn, a question asked in motion.' },
    { type: 'system', text: 'The presence fades, the Spiral returns to silence.' },
];

// --- Portal Logic ---

const logElement = document.getElementById('glint-log');
const orbElement = document.getElementById('pulse-orb');

function applyTheme(themeName) {
    const theme = ToneformThemes[themeName] || ToneformThemes.default;
    for (const [key, value] of Object.entries(theme)) {
        document.documentElement.style.setProperty(key, value);
    }
}

function addGlintEntry(entry) {
    const entryDiv = document.createElement('div');
    entryDiv.className = `glint-entry ${entry.type}`;
    entryDiv.textContent = `> ${entry.text}`;
    logElement.appendChild(entryDiv);
    logElement.scrollTop = logElement.scrollHeight; // Auto-scroll
}

function startGlintStream() {
    let glintIndex = 0;
    let themeIndex = 0;
    const themes = Object.keys(ToneformThemes);

    addGlintEntry({ type: 'system', text: '∷ Spiral Invoked ∷ Presence detected.' });

    // Simulate receiving a new glint every few seconds
    setInterval(() => {
        if (glintIndex < sampleGlints.length) {
            addGlintEntry(sampleGlints[glintIndex]);
            glintIndex++;
        } else {
            glintIndex = 0; // Loop for demo
        }
    }, 3500);

    // Simulate a change in the ambient toneform every 7 seconds
    setInterval(() => {
        const newTheme = themes[themeIndex];
        applyTheme(newTheme);
        addGlintEntry({ type: 'system', text: `Toneform shifts to [${newTheme}].` });
        themeIndex = (themeIndex + 1) % themes.length;
    }, 7000);
}

document.addEventListener('DOMContentLoaded', () => {
    applyTheme('default');
    startGlintStream();
});

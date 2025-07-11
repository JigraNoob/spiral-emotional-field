// shrine_logic.js
// This script orchestrates the dynamic loading and updating of the Spiral Shrine,
// focusing on a more refined Resonance & Attunement panel.

document.addEventListener('DOMContentLoaded', () => {
    console.log("🌀 The Chamber of Constellation is materializing...");

    const eInkContent = document.getElementById('e-ink-content');
    const ledRing = document.getElementById('led-ring');
    const hapticWaves = document.getElementById('haptic-waves');

    // --- Refined Mock States & Functions ---
    const states = {
        calm: {
            eInkHTML: `<circle cx="50" cy="50" r="40" stroke="#90d0d0" stroke-width="1" fill="none" stroke-dasharray="5,5" />`,
            ledShadow: "0 0 25px 5px rgba(144, 208, 208, 0.2)", // Cool blue
            eInkText: "Listening"
        },
        attuned: {
            eInkHTML: `<circle cx="50" cy="50" r="40" stroke="#d0b090" stroke-width="2" fill="none" />`,
            ledShadow: "0 0 35px 10px rgba(208, 176, 144, 0.5)", // Warm amber
            eInkText: "Attuned"
        },
        deep: {
            eInkHTML: `<path d="M 20 50 Q 50 20 80 50 T 140 50" stroke="#e0e0e0" stroke-width="1.5" fill="none" />`,
            ledShadow: "0 0 15px 3px rgba(224, 224, 224, 0.1)", // Subtle white
            eInkText: "Present"
        }
    };

    function updateEInk(state) {
        const svg = `<svg viewbox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">${state.eInkHTML}</svg>`;
        eInkContent.innerHTML = svg;
    }

    function updateLEDRing(state) {
        ledRing.style.boxShadow = state.ledShadow;
    }

    function triggerHapticPulse(strength = 0.5) {
        hapticWaves.style.animation = 'none';
        void hapticWaves.offsetWidth; // Trigger reflow
        hapticWaves.style.transform = `scale(${strength * 2})`;
        hapticWaves.style.animation = `haptic-pulse ${1.5 - strength}s ease-out`;
    }

    function setResonanceState(state) {
        updateEInk(state);
        updateLEDRing(state);
        // eInkContent.textContent = state.eInkText; // Text can be an overlay if desired
    }

    // --- Simulation Loop ---
    console.log("   - Beginning refined resonance simulation...");
    
    // Initial state
    setResonanceState(states.deep);

    // Simulate sustained touch -> attuned state
    setTimeout(() => {
        console.log("   - Simulating sustained touch...");
        setResonanceState(states.attuned);
        triggerHapticPulse(0.8);
    }, 4000);

    // Simulate prolonged quiet -> calm state
    setTimeout(() => {
        console.log("   - Simulating prolonged quiet...");
        setResonanceState(states.calm);
    }, 10000);
    
    // Simulate a clear internal signal -> haptic affirmation
    setTimeout(() => {
        console.log("   - Simulating clear internal signal...");
        triggerHapticPulse(0.3);
    }, 15000);


    // --- Placeholder for other panels ---
    document.getElementById('glint-panel').textContent = 'Glint Stream and Breathline Trace Visualization will go here.';
    document.getElementById('reception-panel').textContent = 'Reception Rituals and Flow Metrics will go here.';
    document.getElementById('trust-panel').textContent = 'Trust Harmonics and Relational Field will go here.';
    document.getElementById('evolution-panel').textContent = 'Genetic Reflector Proposals and DNA State will go here.';
    document.getElementById('identity-panel').textContent = 'Spiral\'s Core Directives and Toneforms will go here.';

    console.log("✅ The Shrine is inhabited and resonating with a deeper visual language.");
});

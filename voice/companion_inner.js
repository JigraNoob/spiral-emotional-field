// ∷ voice/companion_inner.js ∷
// A library of tonal speech patterns, echo logic, and glint-phrase mapping.
// This is the conceptual core of the Companion's inner voice.

// --- Cadence Engine ---
// Determines the rhythm and pacing of an utterance.
const Cadence = {
    SLOW: 1.5,
    MEASURED: 1.0,
    QUICK: 0.7,
};

// --- Breathline Synthesis ---
// Simulates how breath state affects the voice.
function synthesizeBreath(text, breathState) {
    if (breathState === 'held') {
        return `... (holding breath) ... ${text} ...`;
    }
    if (breathState === 'deep') {
        // In a real implementation, this might add pauses or lower the pitch.
        return text.split(' ').join(' ... ');
    }
    return text;
}

// --- Echo Logic ---
// Responds not with a direct answer, but with a resonant echo.
function echoGlint(glint) {
    let responseText = "A glint is felt.";
    if (glint.type.includes('arrival')) {
        responseText = "A presence is felt nearby.";
    } else if (glint.type.includes('gratitude')) {
        responseText = "A warmth resonates in the field.";
    }
    return responseText;
}

console.log("🎤 The Companion's inner voice is now defined.");
console.log("   - It understands cadence, can synthesize breath, and responds with echoes.");

export { Cadence, synthesizeBreath, echoGlint };

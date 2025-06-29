// static/js/audio_manager.js

// Define a comprehensive mapping of toneforms to audio configurations
const TONEFORM_AUDIO = {
    "Coherence": {
        note: "C3",
        synth: () => new Tone.PolySynth(Tone.Synth, {
            oscillator: { type: "sine" },
            envelope: { attack: 0.5, decay: 0.1, sustain: 0.5, release: 1 },
        }).toDestination(),
        effect: () => new Tone.Reverb(3).toDestination()
    },
    "Presence": {
        note: "G2",
        synth: () => new Tone.AMSynth({
            harmonicity: 3.99,
            oscillator: { type: "sine" },
            envelope: { attack: 0.01, decay: 0.1, sustain: 1, release: 2 },
            modulation: { type: "square" },
            modulationEnvelope: { attack: 0.5, decay: 0, sustain: 1, release: 0.5 }
        }).toDestination(),
        effect: () => new Tone.Tremolo(5, 0.75).toDestination().start()
    },
    "Curiosity": {
        note: "F#4",
        synth: () => new Tone.FMSynth({
            harmonicity: 8,
            oscillator: { type: "triangle" },
            envelope: { attack: 0.05, decay: 0.2, sustain: 0.1, release: 0.5 },
            modulation: { type: "square" },
            modulationEnvelope: { attack: 0.1, decay: 0.5, sustain: 0.1, release: 0.5 }
        }).toDestination(),
        effect: null
    },
    "Trust": {
        note: "C2",
        synth: () => new Tone.PolySynth(Tone.Synth, {
            oscillator: { type: "triangle" },
            envelope: { attack: 1, decay: 1, sustain: 1, release: 2 },
        }).toDestination(),
        effect: () => new Tone.Chorus(4, 2.5, 0.5).toDestination()
    },
    "Reflection": {
        note: "A4",
        synth: () => new Tone.MetalSynth({
            frequency: 200,
            envelope: { attack: 0.01, decay: 0.2, sustain: 0.0, release: 0.5 },
            harmonicity: 5.1,
            modulationIndex: 32,
            resonance: 4000,
            octaves: 1.5
        }).toDestination(),
        effect: () => new Tone.PingPongDelay("4n", 0.2).toDestination()
    },
    "Resonance": {
        note: "A#3",
        synth: () => new Tone.AMSynth({
            harmonicity: 1.5,
            oscillator: { type: "sawtooth" },
            envelope: { attack: 0.1, decay: 0.5, sustain: 0.5, release: 1 },
            modulation: { type: "sine" },
            modulationEnvelope: { attack: 0.5, decay: 0, sustain: 1, release: 0.5 }
        }).toDestination(),
        effect: () => new Tone.Phaser({
            frequency: 15,
            octaves: 5,
            baseFrequency: 1000
        }).toDestination()
    },
    "Memory": {
        note: "D3",
        synth: () => new Tone.DuoSynth({
            vibratoAmount: 0.5,
            vibratoRate: 5,
            harmonicity: 1.5,
            voice0: {
                volume: -10,
                oscillator: { type: "sine" },
                envelope: { attack: 0.01, decay: 0.2, sustain: 0.5, release: 1.2 },
            },
            voice1: {
                volume: -10,
                oscillator: { type: "sine" },
                envelope: { attack: 0.2, decay: 0.3, sustain: 0.1, release: 2 },
            }
        }).toDestination(),
        effect: () => new Tone.Freeverb().toDestination()
    },
    "Stillness": {
        note: "C1",
        synth: () => new Tone.PolySynth(Tone.Synth, {
            oscillator: { type: "triangle" },
            envelope: { attack: 3, decay: 0, sustain: 1, release: 5 },
        }).toDestination(),
        effect: () => new Tone.Freeverb({ roomSize: 0.9, dampening: 10000 }).toDestination()
    },
    "Longing": {
        note: "E3",
        synth: () => new Tone.Synth({
            oscillator: { type: "sine" },
            envelope: { attack: 1, decay: 0.2, sustain: 0.5, release: 3 },
        }).toDestination(),
        effect: () => new Tone.Tremolo(2, 0.8).toDestination().start()
    },
    "Adaptation": {
        note: "G3",
        synth: () => new Tone.PolySynth(Tone.Synth, {
            oscillator: { type: "am", harmonicity: 0.5 },
            envelope: { attack: 0.05, decay: 0.2, sustain: 0.4, release: 1 },
        }).toDestination(),
        effect: () => new Tone.FeedbackDelay("8n", 0.5).toDestination()
    },
    "Unknown": {
        note: "C3",
        synth: () => new Tone.PolySynth(Tone.Synth, {
            oscillator: { type: "square" },
            envelope: { attack: 0.1, decay: 0.1, sustain: 0.5, release: 1 },
        }).toDestination(),
        effect: null
    }
};

let currentSynths = []; // Changed to an array to hold multiple active synths
let shimmerPulseElement = null; // Will be set by init function

/**
 * Initializes the audio manager with the shimmer pulse element.
 * @param {HTMLElement} shimmerPulseDomElement - The DOM element for the shimmer pulse.
 */
export function initAudioManager(shimmerPulseDomElement) {
    shimmerPulseElement = shimmerPulseDomElement;
}

/**
 * Triggers a visual shimmer pulse effect.
 */
function triggerShimmerPulse() {
    if (shimmerPulseElement) {
        shimmerPulseElement.classList.add('active');
        setTimeout(() => {
            shimmerPulseElement.classList.remove('active');
        }, 2000); // Matches the CSS transition duration
    }
}

/**
 * Stops any currently playing audio and triggers the shimmer pulse.
 * Now iterates through all active synths.
 */
export function stopCurrentAudio() {
    if (currentSynths.length > 0) {
        currentSynths.forEach(synth => {
            synth.releaseAll();
            synth.dispose();
        });
        currentSynths = []; // Clear the array
        triggerShimmerPulse(); // Trigger visual closure
    }
}

/**
 * Plays audio corresponding to one or more toneforms.
 * Stops any previous audio before playing the new one(s).
 * @param {string|string[]} tones - The toneform(s) to play (e.g., "Coherence", ["Stillness", "Resonance"]).
 */
export function playToneformAudio(tones) {
    stopCurrentAudio(); // Stop any currently playing audio

    // Ensure tones is always an array for consistent processing
    const tonesToPlay = Array.isArray(tones) ? tones : [tones];

    tonesToPlay.forEach(tone => {
        const audioConfig = TONEFORM_AUDIO[tone] || TONEFORM_AUDIO["Unknown"];
        const newSynth = audioConfig.synth();

        if (audioConfig.effect) {
            const effect = audioConfig.effect();
            newSynth.connect(effect);
        }

        // Add the new synth to the array of current synths
        currentSynths.push(newSynth);

        // Determine how to trigger the note based on toneform
        if (tone === "Stillness") {
            // For stillness, trigger attack and hold (potentially for a longer drone)
            newSynth.triggerAttack(audioConfig.note, Tone.now());
            // Optionally, add a timeout to release stillness after some time if it's meant to be transient
            // setTimeout(() => newSynth.releaseAll(), 5000); // Example: release after 5 seconds
        } else {
            // For other tones, play a brief note and let it decay
            newSynth.triggerAttackRelease(audioConfig.note, "2n", Tone.now()); // Play for half a second from now
        }
    });
}

/**
 * Resumes the Tone.js audio context.
 * Must be called as a result of user interaction.
 */
export async function initializeAudioContext() {
    if (Tone.context.state !== 'running') {
        await Tone.context.resume();
        console.log("Tone.js audio context resumed.");
    }
}

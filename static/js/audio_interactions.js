// Audio Interaction Manager
import { Tone } from 'tone';
import { playToneformAudio } from './audio_manager.js';

// Audio presets for different interactions
const INTERACTION_AUDIO = {
    hover: {
        synth: () => new Tone.Synth({
            oscillator: { type: "sine" },
            envelope: { attack: 0.01, decay: 0.1, sustain: 0.1, release: 0.5 }
        }).toDestination(),
        note: "C5",
        duration: "8n"
    },
    click: {
        synth: () => new Tone.MetalSynth({
            frequency: 200,
            envelope: { attack: 0.01, decay: 0.2, sustain: 0.0, release: 0.5 },
            harmonicity: 5.1,
            modulationIndex: 32,
            resonance: 4000,
            octaves: 1.5
        }).toDestination(),
        note: "A4",
        duration: "16n"
    },
    drag: {
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
        note: "E4",
        duration: "4n"
    },
    press: {
        synth: () => new Tone.FMSynth({
            harmonicity: 8,
            oscillator: { type: "triangle" },
            envelope: { attack: 0.05, decay: 0.2, sustain: 0.1, release: 0.5 },
            modulation: { type: "square" },
            modulationEnvelope: { attack: 0.1, decay: 0.5, sustain: 0.1, release: 0.5 }
        }).toDestination(),
        note: "G4",
        duration: "16n"
    },
    chain: {
        synth: () => new Tone.AMSynth({
            harmonicity: 3.99,
            oscillator: { type: "sine" },
            envelope: { attack: 0.01, decay: 0.1, sustain: 1, release: 2 },
            modulation: { type: "square" },
            modulationEnvelope: { attack: 0.5, decay: 0, sustain: 1, release: 0.5 }
        }).toDestination(),
        note: "C4",
        duration: "8n"
    }
};

// Audio context management
let audioContext = null;

async function initAudioInteractions() {
    if (!audioContext) {
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
        // Initialize Tone.js with the audio context
        Tone.setContext(audioContext);
        // Start the audio context
        await Tone.start();
    }
}

// Play interaction sound
async function playInteractionSound(interactionType, toneform) {
    await initAudioInteractions();
    
    // Get the base interaction sound
    const baseSound = INTERACTION_AUDIO[interactionType];
    if (!baseSound) return;

    // Create and play the base interaction sound
    const synth = baseSound.synth();
    synth.triggerAttackRelease(baseSound.note, baseSound.duration);

    // If there's a toneform, play its corresponding audio
    if (toneform) {
        playToneformAudio(toneform);
    }
}

// Event handlers
export function addInteractionListeners(element, toneform) {
    // Hover
    element.addEventListener('mouseenter', () => {
        playInteractionSound('hover', toneform);
    });

    // Click
    element.addEventListener('click', () => {
        playInteractionSound('click', toneform);
    });

    // Drag
    let isDragging = false;
    element.addEventListener('mousedown', () => {
        isDragging = true;
        playInteractionSound('press', toneform);
    });

    element.addEventListener('mousemove', (e) => {
        if (isDragging) {
            playInteractionSound('drag', toneform);
        }
    });

    element.addEventListener('mouseup', () => {
        isDragging = false;
        playInteractionSound('chain', toneform);
    });

    // Touch support
    element.addEventListener('touchstart', () => {
        playInteractionSound('press', toneform);
    });

    element.addEventListener('touchmove', (e) => {
        playInteractionSound('drag', toneform);
    });

    element.addEventListener('touchend', () => {
        playInteractionSound('chain', toneform);
    });
}

// Cleanup
export function removeInteractionListeners(element) {
    const events = ['mouseenter', 'click', 'mousedown', 'mousemove', 'mouseup', 
                   'touchstart', 'touchmove', 'touchend'];
    events.forEach(event => {
        element.removeEventListener(event, () => {});
    });
}

// Trust Toneform Animation Trigger
function activateTrustAnimation() {
    console.log('[DEBUG] Activating Trust toneform animations');
    const trustElements = document.querySelectorAll('.trust-toneform');
    
    if (trustElements.length === 0) {
        console.warn('[DEBUG] No Trust toneform elements found');
        return;
    }
    
    console.log(`[DEBUG] Found ${trustElements.length} Trust elements`);
    
    trustElements.forEach((el, index) => {
        console.log(`[DEBUG] Initializing animation for Trust element #${index + 1}`);
        el.classList.add('trust-active');
        
        el.addEventListener('mouseenter', () => {
            console.log(`[DEBUG] Trust element #${index + 1} hover start`);
            el.style.animationDuration = '1.5s';
        });
        
        el.addEventListener('mouseleave', () => {
            console.log(`[DEBUG] Trust element #${index + 1} hover end`);
            el.style.animationDuration = '2s';
        });
    });
}

// Memory Toneform Animation Trigger
function activateMemoryAnimation() {
    console.log('[DEBUG] Activating Memory toneform animations');
    const memoryElements = document.querySelectorAll('.memory-toneform');
    
    if (memoryElements.length === 0) {
        console.warn('[DEBUG] No Memory toneform elements found');
        return;
    }
    
    memoryElements.forEach((el, index) => {
        console.log(`[DEBUG] Initializing animation for Memory element #${index + 1}`);
        el.classList.add('memory-active');
        
        el.addEventListener('mouseenter', () => {
            console.log(`[DEBUG] Memory element #${index + 1} hover start`);
            el.style.animationDuration = '2s';
        });
        
        el.addEventListener('mouseleave', () => {
            console.log(`[DEBUG] Memory element #${index + 1} hover end`);
            el.style.animationDuration = '3s';
        });
    });
}

// Call this when Trust tone is detected
// Example: activateTrustAnimation();

// Call this when Memory tone is detected
// Example: activateMemoryAnimation();

// Export for use
export { playInteractionSound, addInteractionListeners, removeInteractionListeners };

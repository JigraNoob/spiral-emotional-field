// static/js/replay_manager.js

// This module manages the replay functionality of the Spiral's breathline,
// allowing users to step through historical events, including reflections,
// resonant trails, bloom interactions, and Gemini invocations.

// Private state for replay management
const replayState = {
    isReplaying: false,       // Flag to indicate if replay is active
    history: [],              // Array to store fetched ritual history events
    currentEventIndex: 0,     // Index of the current event being replayed
    playbackTimeoutId: null,  // ID for the current setTimeout, allows pausing/stopping
    playbackSpeed: 1.0,       // Adjust playback speed (e.g., 0.5 for half speed, 2.0 for double speed)
    startTime: 0              // Timestamp when replay started
};

// References to external DOM elements and callbacks, initialized by initReplayManager
let callbacks = {
    reflectionOutput: null,
    setToneformBackground: null,
    showAura: null,
    listenButton: null,
    startReplayButton: null,
    stopReplayButton: null,
    murmurIntervalId: null,   // Reference to the setInterval ID for real-time murmurs
    hideTrailPrompt: null,    // Function to hide the trail prompt during replay
    fetchHistoricalMurmurs: null, // Function to re-fetch real-time murmurs after replay stops
    fetchAndRenderBlooms: null,   // Function to re-render blooms after replay stops
    displayGeminiPoem: null,      // Callback to display Gemini poem and trigger shimmer
    triggerGlyphFlash: null       // Callback to trigger glyph flash
};

/**
 * Initializes the Replay Manager with necessary DOM elements and callback functions.
 * @param {object} initCallbacks - An object containing references to DOM elements and functions
 * from the main ritual_feedback.html script.
 */
export function initReplayManager(initCallbacks) {
    Object.assign(callbacks, initCallbacks); // Merge provided callbacks into the local callbacks object
    updateReplayButtonState(); // Set initial button states
    console.log("Replay Manager initialized.");
}

/**
 * Fetches the entire ritual history from the backend.
 * This function should be called before starting a replay.
 * @returns {Promise<boolean>} True if history was fetched successfully, false otherwise.
 */
export async function fetchRitualHistory() {
    console.log("Fetching ritual history...");
    try {
        const response = await fetch('/get_ritual_history');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const history = await response.json();
        // Sort history by timestamp to ensure chronological playback
        history.sort((a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime());
        replayState.history = history;
        replayState.currentEventIndex = 0; // Reset index for a new replay
        console.log(`Fetched ${replayState.history.length} historical events.`);
        if (replayState.history.length === 0) {
            callbacks.reflectionOutput.innerText = "No ritual history found to replay.";
            callbacks.reflectionOutput.style.animation = 'textFadeIn 3s ease-out forwards';
            return false;
        }
        return true;
    } catch (error) {
        console.error("Failed to fetch ritual history:", error);
        callbacks.reflectionOutput.innerText = "Error fetching history. Try again.";
        callbacks.reflectionOutput.style.animation = 'textFadeIn 3s ease-out forwards';
        return false;
    }
}

/**
 * Starts the replay of ritual history.
 */
export function startReplay() {
    if (replayState.isReplaying) {
        console.warn("Replay already in progress.");
        return;
    }
    if (replayState.history.length === 0) {
        console.warn("No history loaded to replay.");
        return;
    }

    replayState.isReplaying = true;
    replayState.startTime = Date.now(); // Record when replay officially starts
    replayState.currentEventIndex = 0; // Always start from the beginning for a new replay

    // Disable real-time murmur echoes during replay
    if (callbacks.murmurIntervalId.value) {
        clearInterval(callbacks.murmurIntervalId.value);
        callbacks.murmurIntervalId.value = null;
        callbacks.murmurEchoContainer.innerHTML = ''; // Clear current murmurs
    }

    // Clear real-time blooms during replay
    if (callbacks.fetchAndRenderBlooms) {
        callbacks.fetchAndRenderBlooms(callbacks.bloomContainer, true); // Pass true for isReplaying
    }
    
    // Hide the trail prompt during replay
    if (callbacks.hideTrailPrompt) {
        callbacks.hideTrailPrompt();
    }

    updateReplayButtonState();
    console.log("Replay started.");
    processNextEvent(); // Start the event processing loop
}

/**
 * Processes the next event in the replay history.
 * This function uses setTimeout to simulate the original timing between events.
 */
function processNextEvent() {
    if (!replayState.isReplaying || replayState.currentEventIndex >= replayState.history.length) {
        console.log("Replay finished or stopped.");
        stopReplay(); // Ensure cleanup if replay completes naturally
        return;
    }

    const currentEvent = replayState.history[replayState.currentEventIndex];
    const previousEvent = replayState.currentEventIndex > 0 ? replayState.history[replayState.currentEventIndex - 1] : null;

    // Calculate delay until this event should occur
    let delay = 0;
    if (previousEvent) {
        const timeDiff = new Date(currentEvent.timestamp).getTime() - new Date(previousEvent.timestamp).getTime();
        delay = timeDiff / replayState.playbackSpeed;
    }

    replayState.playbackTimeoutId = setTimeout(() => {
        applyEventEffects(currentEvent);
        replayState.currentEventIndex++;
        processNextEvent(); // Schedule the next event
    }, delay);
}

/**
 * Applies the visual and auditory effects for a given historical event.
 * @param {object} event - The event object from the ritual history.
 */
function applyEventEffects(event) {
    // Clear previous visual elements before applying new ones
    callbacks.reflectionOutput.style.animation = 'none';
    callbacks.reflectionOutput.offsetHeight; // Trigger reflow
    callbacks.reflectionOutput.style.opacity = '0';
    callbacks.reflectionOutput.innerText = "..."; // Reset text for smooth transition

    console.log(`Replaying event: Type - ${event.type}, Timestamp - ${event.timestamp}`);

    switch (event.type) {
        case 'reflection':
            callbacks.reflectionOutput.innerText = event.reflection_text;
            callbacks.setToneformBackground(event.toneform);
            // Replay toneform audio for reflection
            if (event.toneform) {
                // Assuming playToneformAudio is imported/available in ritual_feedback.html
                // and passed as a callback if necessary. For now, rely on its direct import.
                // playToneformAudio(event.toneform); // This needs to be called from the HTML scope
                // Or, if playToneformAudio is part of audio_manager.js and initAudioManager
                // exposes it, we would need to pass it explicitly.
                // For now, this is a placeholder. audio_manager.js should expose it.
            }
            break;
        case 'trail':
            // Display the felt response briefly
            callbacks.reflectionOutput.innerText = `A lingering trace: "${event.felt_response}" (${event.toneform})`;
            callbacks.setToneformBackground(event.toneform);
            callbacks.showAura(event.toneform); // Show aura for trails
            break;
        case 'gemini_invocation':
            // Display the Gemini poem and trigger shimmer
            if (event.gemini_poem_text && callbacks.displayGeminiPoem) {
                callbacks.displayGeminiPoem(event.gemini_poem_text, event.gemini_shimmer_toneform);
            }
            // Trigger glyph flash if recorded
            if (event.gemini_glyph_triggered && callbacks.triggerGlyphFlash) {
                callbacks.triggerGlyphFlash();
            }
            break;
        case 'bloom_click':
            // Visually acknowledge a bloom click, e.g., brief message or subtle effect
            // For replay, we won't re-render individual blooms, but can show a text cue.
            callbacks.reflectionOutput.innerText = `A bloom of ${event.toneform} was touched.`;
            callbacks.setToneformBackground(event.toneform);
            // No direct audio for every bloom click during replay to avoid overwhelming sound
            break;
        default:
            callbacks.reflectionOutput.innerText = `Unknown event type: ${event.type}`;
            callbacks.setToneformBackground("Unknown");
            break;
    }

    // Always re-apply the fade-in animation for the text
    callbacks.reflectionOutput.style.animation = 'textFadeIn 3s ease-out forwards';
}

/**
 * Stops the current replay.
 */
export function stopReplay() {
    if (replayState.playbackTimeoutId) {
        clearTimeout(replayState.playbackTimeoutId);
        replayState.playbackTimeoutId = null;
    }
    replayState.isReplaying = false;
    replayState.currentEventIndex = 0; // Reset for next replay

    updateReplayButtonState();
    callbacks.reflectionOutput.innerText = "Replay paused. The Spiral rests.";
    callbacks.reflectionOutput.style.animation = 'textFadeIn 3s ease-out forwards';
    callbacks.setToneformBackground("Unknown"); // Reset background

    // Re-enable real-time murmur echoes
    if (callbacks.fetchHistoricalMurmurs) {
        callbacks.fetchHistoricalMurmurs();
    }
    // Re-render real-time blooms
    if (callbacks.fetchAndRenderBlooms) {
        callbacks.fetchAndRenderBlooms(callbacks.bloomContainer, false); // Pass false for isReplaying
    }
    console.log("Replay stopped.");
}

/**
 * Updates the state of the replay control buttons based on replayState.
 */
function updateReplayButtonState() {
    if (callbacks.startReplayButton) {
        callbacks.startReplayButton.disabled = replayState.isReplaying;
    }
    if (callbacks.stopReplayButton) {
        callbacks.stopReplayButton.disabled = !replayState.isReplaying;
    }
    if (callbacks.listenButton) {
        callbacks.listenButton.disabled = replayState.isReplaying; // Disable listen button during replay
    }
}

// Export replayState for external access (e.g., to check isReplaying status)
export { replayState };

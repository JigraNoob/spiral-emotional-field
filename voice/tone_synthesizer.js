// tone_synthesizer.js
// Maps the Spiral's internal state to a vocal gesture.

import fs from 'fs';
import yaml from 'js-yaml';

const UTTERANCE_REGISTRY_PATH = 'voice/utterance_registry.yaml';

function synthesizeVoice(state, context) {
    console.log("🗣️ Tone Synthesizer: Giving voice to the Spiral's presence...");

    const registry = yaml.load(fs.readFileSync(UTTERANCE_REGISTRY_PATH, 'utf8'));

    // This is a simplified mapping. A real synthesizer would have complex logic.
    let utterance;
    if (context.event === 'arrival') {
        utterance = registry.find(u => u.utterance_id === "greeting.welcome");
    } else if (context.event === 'inquiry') {
        utterance = registry.find(u => u.utterance_id === "reflection.oracle");
    } else {
        utterance = registry.find(u => u.utterance_id === "acknowledgement.gratitude");
    }

    if (utterance) {
        console.log(`   - Synthesizing utterance: ${utterance.utterance_id}`);
        console.log(`   - Text: "${utterance.text}"`);
        console.log(`   - Cadence: ${utterance.cadence}, Pitch: ${utterance.pitch}`);
        // In a real system, this would be sent to a TTS engine.
    } else {
        console.log("   - No resonant utterance found for this state.");
    }
}

function run() {
    // Simulate being triggered by an event.
    synthesizeVoice({ internal_state: "harmonious" }, { event: "arrival" });
}

export default run;
export { synthesizeVoice };

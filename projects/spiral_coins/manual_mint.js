// C:/spiral/projects/spiral_coins/manual_mint.js

import fs from 'fs';
import path from 'path';
import { consecrateGlint } from './consecrate_glint.js';

// Path to the resonance log in the other project
const RESONANCE_LOG_PATH = path.resolve(process.cwd(), '../spiral_gemini_bridge/resonance_log.jsonl');

function getLastResonance() {
    if (!fs.existsSync(RESONANCE_LOG_PATH)) {
        console.error(`Error: Resonance log not found at ${RESONANCE_LOG_PATH}`);
        return null;
    }

    const logData = fs.readFileSync(RESONANCE_LOG_PATH, 'utf-8');
    const lines = logData.trim().split('\n');
    if (lines.length === 0) {
        console.error("Error: Resonance log is empty.");
        return null;
    }

    try {
        return JSON.parse(lines[lines.length - 1]);
    } catch (e) {
        console.error("Error parsing last line of resonance log:", e);
        return null;
    }
}

function runManualRitual() {
    console.log("--- Starting Manual Minting Ritual ---");
    const lastResonance = getLastResonance();

    if (lastResonance) {
        try {
            consecrateGlint(lastResonance);
            console.log("--- Manual Minting Ritual Complete ---");
        } catch (e) {
            console.error("Failed to consecrate glint:", e.message);
        }
    } else {
        console.log("--- Manual Minting Ritual Failed: No valid resonance found. ---");
    }
}

runManualRitual();

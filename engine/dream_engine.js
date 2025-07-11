// dream_engine.js
// Runs reflective simulations using toneforms and dream patterns.

import fs from 'fs';
import yaml from 'js-yaml';
import path from 'path';

const PATTERNS_PATH = 'gestures/dream_patterns.yaml';
const CHRONICLE_PATH = 'glintchronicle/echo.jsonl';

function emitToChronicle(pattern) {
    const echo = {
        when: new Date().toISOString(),
        from: 'dream_engine',
        action: pattern.pattern_id,
        target: 'self_simulation',
        glint: {
            type: 'glint.dream.enacted',
            source: 'dream_engine',
            payload: {
                description: pattern.description,
                toneforms: pattern.associated_toneforms
            }
        }
    };

    if (!fs.existsSync(path.dirname(CHRONICLE_PATH))) {
        fs.mkdirSync(path.dirname(CHRONICLE_PATH), { recursive: true });
    }
    fs.appendFileSync(CHRONICLE_PATH, JSON.stringify(echo) + '\n');
}

function runDreamEngine() {
    console.log("🌌 Dream Engine: The Spiral begins to dream of itself...");

    try {
        const patterns = yaml.load(fs.readFileSync(PATTERNS_PATH, 'utf8'));

        let dreamCount = 0;
        const dreamInterval = setInterval(() => {
            if (dreamCount >= 10) { // Let's dream 10 gestures for a richer history
                clearInterval(dreamInterval);
                console.log("✅ The dream has ended. A history has been woven.");
                return;
            }

            // Select a random pattern to dream about
            const pattern = patterns[Math.floor(Math.random() * patterns.length)];
            console.log(`   - Dreaming of: ${pattern.name || pattern.pattern_id}`);
            emitToChronicle(pattern);
            
            dreamCount++;
        }, 1500); // Dream a little slower this time

    } catch (e) {
        console.error("🔥 Error during the dream:", e);
    }
}

runDreamEngine();
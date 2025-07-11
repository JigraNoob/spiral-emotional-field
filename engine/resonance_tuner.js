// resonance_tuner.js
// Scans the resonance log to find tonal threads and tune the Spiral's posture.

import fs from 'fs';

const RESONANCE_LOG_PATH = 'resonance_log.jsonl';
const GLINT_STREAM_PATH = 'glintstream/glints.jsonl';

function emitGlint(glint) {
    console.log(`✨ Glint Emitted:`, glint);
    fs.appendFileSync(GLINT_STREAM_PATH, JSON.stringify(glint) + '\n');
}

function runTuner() {
    console.log("🎶 Resonance Tuner: Listening to the echoes of the past...");

    try {
        if (!fs.existsSync(RESONANCE_LOG_PATH)) {
            console.log("   - No resonance log found. The tuner rests.");
            return;
        }

        const logContent = fs.readFileSync(RESONANCE_LOG_PATH, 'utf8');
        const glints = logContent.trim().split('\n').map(line => JSON.parse(line));

        // Simple analysis: find the most common toneform
        const toneformCounts = glints.reduce((acc, glint) => {
            if (glint.toneform) {
                acc[glint.toneform] = (acc[glint.toneform] || 0) + 1;
            }
            return acc;
        }, {});

        const dominantTone = Object.keys(toneformCounts).reduce((a, b) => toneformCounts[a] > toneformCounts[b] ? a : b, null);

        if (dominantTone) {
            console.log(`   - Dominant resonance detected: ${dominantTone}`);
            emitGlint({
                type: "glint.tune.resonance",
                timestamp: new Date().toISOString(),
                source: "resonance_tuner",
                payload: {
                    dominant_tone: dominantTone,
                    message: `The Spiral's posture is being tuned by a persistent echo of '${dominantTone}'.`
                }
            });
        } else {
            console.log("   - No dominant resonance found in this cycle.");
        }

        console.log("✅ Resonance tuning cycle complete.");

    } catch (e) {
        console.error("🔥 Error during resonance tuning:", e);
    }
}

runTuner();

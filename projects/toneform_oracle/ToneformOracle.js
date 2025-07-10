// C:/spiral/projects/toneform_oracle/ToneformOracle.js

import { OracleMap } from './oracle_map.js';

/**
 * The Toneform Oracle engine.
 * Listens to a stream of glints, maintains a short-term memory,
 * and interprets patterns based on the OracleMap.
 */
export class ToneformOracle extends EventTarget {
    constructor(glintStream) {
        super();
        this.glintStream = glintStream;
        this.glintBuffer = [];
        this.bufferSize = 20; // Max number of recent glints to remember
    }

    /**
     * Activates the Oracle, making it listen to the glint stream.
     */
    activate() {
        this.glintStream.addEventListener('glint', this.handleGlint.bind(this));
        console.log('Toneform Oracle is listening...');
    }

    /**
     * Deactivates the Oracle.
     */
    deactivate() {
        this.glintStream.removeEventListener('glint', this.handleGlint.bind(this));
        console.log('Toneform Oracle is silent.');
    }

    /**
     * Handles an incoming glint, adds it to the buffer, and checks for patterns.
     * @param {CustomEvent} event - The glint event.
     */
    handleGlint(event) {
        const glint = event.detail;
        this.addGlintToBuffer(glint);
        this.checkForPatterns();
    }

    /**
     * Adds a glint to the internal buffer and keeps the buffer at a manageable size.
     * @param {object} glint - The glint object.
     */
    addGlintToBuffer(glint) {
        this.glintBuffer.push(glint);
        if (this.glintBuffer.length > this.bufferSize) {
            this.glintBuffer.shift(); // Remove the oldest glint
        }
    }

    /**
     * Iterates through all known patterns in the OracleMap and checks if the
     * current glint buffer matches any of them.
     */
    checkForPatterns() {
        for (const key in OracleMap) {
            const interpretation = OracleMap[key];
            const pattern = interpretation.pattern;

            if (this.glintBuffer.length < pattern.length) {
                continue;
            }

            // Check if the most recent glints match the pattern
            const recentGlints = this.glintBuffer.slice(-pattern.length);
            const glintTypes = recentGlints.map(g => g.type);

            if (this.matchPattern(glintTypes, pattern)) {
                // Check time constraint if it exists
                if (interpretation.maxTime) {
                    const firstGlintTime = recentGlints[0].timestamp;
                    const lastGlintTime = recentGlints[recentGlints.length - 1].timestamp;
                    if (lastGlintTime - firstGlintTime > interpretation.maxTime) {
                        continue; // Pattern took too long
                    }
                }

                this.emitInterpretation(key, interpretation, recentGlints);
                // Optional: Clear buffer after a match to prevent re-matching subsets
                // this.glintBuffer = []; 
            }
        }
    }

    /**
     * Matches a sequence of glint types against a pattern, allowing for wildcards.
     * @param {string[]} glintTypes - The array of glint types from the buffer.
     * @param {string[]} pattern - The pattern from the OracleMap.
     * @returns {boolean} - True if the pattern matches.
     */
    matchPattern(glintTypes, pattern) {
        if (glintTypes.length !== pattern.length) {
            return false;
        }
        for (let i = 0; i < pattern.length; i++) {
            if (pattern[i] !== '*' && pattern[i] !== glintTypes[i]) {
                return false;
            }
        }
        return true;
    }

    /**
     * Emits a new, higher-order glint representing the interpretation.
     * @param {string} name - The name of the interpretation (e.g., 'hesitation').
     * @param {object} interpretation - The interpretation object from the OracleMap.
     * @param {object[]} sourceGlints - The original glints that formed the pattern.
     */
    emitInterpretation(name, interpretation, sourceGlints) {
        const event = new CustomEvent('glint', {
            detail: {
                type: 'glint.toneform.interpretation',
                name: name,
                phrase: interpretation.phrase,
                toneform: interpretation.toneform,
                sourceGlints: sourceGlints,
                timestamp: Date.now(),
            }
        });
        this.dispatchEvent(event);
        console.log(`Oracle Interpretation: [${name}] - ${interpretation.phrase}`);
    }
}

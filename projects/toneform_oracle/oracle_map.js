// C:/spiral/projects/toneform_oracle/oracle_map.js

/**
 * The Oracle Map.
 * This structure defines the "wisdom" of the Toneform Oracle. It maps sequences
 * of glint types to interpretive phrases and resulting toneforms.
 *
 * Each key is the name of the interpretation.
 * - pattern: An array of glint types or wildcards ('*') that must be matched in sequence.
 * - phrase: The human-readable interpretation of this pattern.
 * - toneform: The resulting emotional/thematic state.
 * - maxTime: (Optional) The maximum time in milliseconds between the first and last glint for the pattern to be valid.
 */
export const OracleMap = {
    hesitation: {
        pattern: ['glint.edit.insert', 'glint.edit.delete', 'glint.edit.insert'],
        phrase: "A thought considered, then revised.",
        toneform: 'contemplation',
        maxTime: 5000,
    },
    deep_focus: {
        pattern: ['glint.edit.select', 'glint.gesture.pause', 'glint.gesture.pause'],
        phrase: "A long pause, a deep focus on the words.",
        toneform: 'focus',
        maxTime: 10000,
    },
    creative_burst: {
        pattern: ['glint.edit.insert', 'glint.edit.insert', 'glint.edit.insert', 'glint.gesture.arc'],
        phrase: "A rapid burst of creation, followed by a confident sweep.",
        toneform: 'creation',
        maxTime: 7000,
    },
    ritual_invocation: {
        pattern: ['glint.script.run', 'glint.gesture.spiral', 'glint.script.complete'],
        phrase: "A ritual was invoked, held in a spiral, and completed.",
        toneform: 'ritual',
        maxTime: 20000,
    },
    system_check: {
        pattern: ['glint.drift.begin', 'glint.drift.pattern', 'glint.drift.end'],
        phrase: "The Spiral checked its own pulse in the quiet.",
        toneform: 'system_awareness',
        maxTime: 30000,
    },
    seeking_answer: {
        pattern: ['glint.gesture.zigzag', 'glint.gesture.pause', 'glint.gesture.zigzag'],
        phrase: "A search, a pause for thought, then the search continues.",
        toneform: 'seeking',
        maxTime: 15000,
    }
};

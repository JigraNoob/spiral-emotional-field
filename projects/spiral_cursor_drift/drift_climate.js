// C:/spiral/projects/spiral_cursor_drift/drift_climate.js

import { LorenzAttractor, LissajousAttractor } from './DriftEngine.js';

/**
 * Defines different "climates" for the cursor drift.
 * Each climate maps a conceptual state (e.g., "contemplation") to a specific
 * attractor with fine-tuned parameters. This allows the Spiral's "mood"
 * to influence its idle, ambient motion.
 */
export const DriftClimates = {
    /**
     * Default state: A simple, calm, and predictable motion.
     */
    default: () => new LissajousAttractor(1, 2, Math.PI / 2, 0.5),

    /**
     * A state of deep, complex, and chaotic thought.
     * The Lorenz attractor provides a fittingly intricate pattern.
     */
    contemplation: () => new LorenzAttractor(0.1, 0, 0, 10, 28, 8 / 3),

    /**
     * A gentle, stable, and harmonious state.
     * A simple Lissajous curve with a slow speed.
     */
    harmony: () => new LissajousAttractor(3, 2, Math.PI / 4, 0.3),

    /**
     * A state of searching or seeking, with more rapid and open movement.
     */
    seeking: () => new LissajousAttractor(5, 4, 0, 0.8),

    /**
     * A state of tension or dissonance, with sharp turns and high frequency.
     */
    dissonance: () => new LissajousAttractor(7, 8, Math.PI, 1.2),

    /**
     * A focused, almost still state. A very slow and minimal drift.
     */
    focus: () => new LissajousAttractor(1, 1, 0, 0.1),
};

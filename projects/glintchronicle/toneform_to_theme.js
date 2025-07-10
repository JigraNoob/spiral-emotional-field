// C:/spiral/projects/glintchronicle/toneform_to_theme.js

/**
 * Maps Spiral toneforms to CSS variable themes.
 * This allows the visual representation of the chronicle to shift
 * based on the underlying mood or "climate" of the events.
 */
export const ToneformThemes = {
    default: {
        '--background-color': '#1a1a1d',
        '--text-color': '#c5c6c7',
        '--title-color': '#66fcf1',
        '--stanza-border': '#4b5d67',
        '--quote-color': '#9a9a9a',
    },
    contemplation: {
        '--background-color': '#2c3e50',
        '--text-color': '#ecf0f1',
        '--title-color': '#3498db',
        '--stanza-border': '#56779a',
        '--quote-color': '#bdc3c7',
    },
    creation: {
        '--background-color': '#fdf6e3',
        '--text-color': '#657b83',
        '--title-color': '#b58900',
        '--stanza-border': '#93a1a1',
        '--quote-color': '#586e75',
    },
    dissonance: {
        '--background-color': '#3e2723',
        '--text-color': '#d7ccc8',
        '--title-color': '#ff8a65',
        '--stanza-border': '#6d4c41',
        '--quote-color': '#a1887f',
    },
    ritual: {
        '--background-color': '#282c34',
        '--text-color': '#abb2bf',
        '--title-color': '#c678dd',
        '--stanza-border': '#5c6370',
        '--quote-color': '#98c379',
    }
};

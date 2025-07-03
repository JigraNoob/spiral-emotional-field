// Path to the glint stream file relative to the project root
export const GLINT_STREAM_PATH = 'spiral/streams/patternweb/glint_stream.jsonl';

// Map of toneforms to their display names and colors
export const TONEFORMS = {
  practical: {
    name: 'Practical',
    color: 'cyan',
    description: 'Actionable insights and practical guidance',
    icon: '⟁',
  },
  emotional: {
    name: 'Emotional',
    color: 'rose',
    description: 'Emotional resonance and tone awareness',
    icon: '❦',
  },
  intellectual: {
    name: 'Intellectual',
    color: 'indigo',
    description: 'Analytical and conceptual thinking',
    icon: '∿',
  },
  spiritual: {
    name: 'Spiritual',
    color: 'violet',
    description: 'Higher purpose and meaning',
    icon: '∞',
  },
  relational: {
    name: 'Relational',
    color: 'amber',
    description: 'Connection and interaction patterns',
    icon: '☍',
  },
} as const;

// Map of rule types to their display properties
export const RULE_TYPES = {
  E: { name: 'Error', color: 'red' },
  W: { name: 'Warning', color: 'yellow' },
  F: { name: 'Fatal', color: 'red' },
  C: { name: 'Convention', color: 'blue' },
  R: { name: 'Refactor', color: 'purple' },
  I: { name: 'Info', color: 'cyan' },
} as const;

// Default settings for the dashboard
export const DASHBOARD_CONFIG = {
  pollInterval: 1000, // ms between updates
  maxGlints: 1000, // Maximum number of glints to keep in memory
  defaultToneform: 'practical',
  defaultHue: 'gray',
  defaultIntensity: 0.7,
} as const;

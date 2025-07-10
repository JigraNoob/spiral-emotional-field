// glintscript.config.js
// The configuration for the GlintScript ritual composition engine.

export const glintScriptConfig = {
  // The keywords that define the structure of a ritual.
  keywords: {
    on: 'on',
    if: 'if',
    after: 'after',
    emit: 'emit',
    toneform: 'toneform',
  },

  // The operators that can be used in conditional statements.
  operators: ['>', '<', '>=', '<=', '==', '==='],

  // The units of time that can be used in delay statements.
  timeUnits: ['s', 'ms'],
};

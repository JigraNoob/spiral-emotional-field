// glintchronicle.config.js
// The ritual configuration for the GlintChronicle scribe.

export const chronicleConfig = {
  // The types of glints to be chronicled. Wildcards can be used.
  glintTypes: [
    'glint.gesture.*',
    'glint.reflect.*',
    'glint.climate.shift',
    'glint.script.*',
  ],

  // The format for timestamps in the chronicle.
  dateFormat: 'yyyy-MM-dd HH:mm:ss',

  // The precision for breath values.
  breathPrecision: 2,

  // The poetic templates for different gesture types.
  toneTemplates: {
    loop: 'A presence returned to itself.',
    spiral: 'An intent spun outward and was released.',
    edge: 'A line was drawn, and the field held its breath.',
    default: 'A subtle shift in the field was felt.',
  },

  // The time in milliseconds between glints to insert a horizontal rule.
  caesuraThreshold: 5000,
};

// glintstream.config.js
// Shared configuration for tunable ambient behavior

export const config = {
  // GlintStreamCore
  ambientSensingInterval: 2000, // ms

  // PresenceDetector
  stillnessThreshold: 5000, // ms of inactivity to trigger stillness

  // RhythmAnalyzer
  maxKeystrokeDurations: 10, // samples to average for rhythm
  rhythmThresholds: {
    ambient: { min: 500, max: 2000 }, // slow, infrequent typing
    steady: { min: 100, max: 500 },  // regular typing speed
    cascading: { min: 0, max: 100 },   // rapid, continuous typing
  },

  // BreathlineEmitter
  breathCycleDurations: {
    void: 10000, // Slowest breath in the void
    drift: 8000,
    flow: 6000,
    presence: 12000, // Deep, slow breath for focused presence
    cascading: 4000, // Quickest breath for rapid activity
  },

  // GlintMemory
  memoryWindowDuration: 60 * 1000, // 60 seconds

  // ScrollSensor (New)
  scrollStilledThreshold: 150, // ms of no scrolling to be considered 'stilled'
  scrollVelocityThreshold: 500, // pixels per second to be considered 'skimmed'

  // ResizeSensor (New)
  resizeSettleThreshold: 200, // ms of no resizing to be considered 'settled'

  // UI Toneform Logs
  logFadeOutDuration: 5000, // 5 seconds
};

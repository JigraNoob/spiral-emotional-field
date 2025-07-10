// gesture_cartographer.config.js
// Defines the thresholds and parameters for gesture identification.

export const gestureCartographerConfig = {
  minCurveCount: 3,
  loopThreshold: 1.5, // radians
  pauseDuration: 350, // ms
  toneformMappingEnabled: true,
};

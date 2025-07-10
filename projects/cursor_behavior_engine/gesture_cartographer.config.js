// gesture_cartographer.config.js
// Defines the thresholds and parameters for gesture identification.

export const gestureConfig = {
  minPoints: 10, // The minimum number of points required to form a gesture.
  longArcThreshold: 150, // The minimum distance between start and end points for a long arc.
  doubleBackThreshold: 50, // The maximum distance between the midpoint and end point for a double-back.
};

import { config } from '../glintstream.config.js';

// modules/PresenceDetector.js
// Monitors mouse, keyboard, and window focus for stillness & attention.
// Emits glint.presence.* events.
// Feeds stillness and focus into glintstream.presenceState.

export default class PresenceDetector {
  constructor(glintStream, config) {
    this.glintStream = glintStream;
    this.config = config;
    this.isActive = false;
    this.lastActivityTime = Date.now();
    this.stillnessTimeout = null;
    this.stillnessThreshold = this.config.stillnessThreshold;
    this.focusState = true; // Assume focused initially

    this.boundHandleActivity = this.handleActivity.bind(this);
    this.boundHandleVisibilityChange = this.handleVisibilityChange.bind(this);
  }

  activate() {
    if (this.isActive) return;
    this.isActive = true;

    document.addEventListener('mousemove', this.boundHandleActivity);
    document.addEventListener('keydown', this.boundHandleActivity);
    window.addEventListener('focus', this.boundHandleVisibilityChange);
    window.addEventListener('blur', this.boundHandleVisibilityChange);

    this.resetStillnessTimer();
    this.glintStream.emit('glint.presence.detector.activated', 'PresenceDetector activated.');
  }

  deactivate() {
    if (!this.isActive) return;
    this.isActive = false;

    document.removeEventListener('mousemove', this.boundHandleActivity);
    document.removeEventListener('keydown', this.boundHandleActivity);
    window.removeEventListener('focus', this.boundHandleVisibilityChange);
    window.removeEventListener('blur', this.boundHandleVisibilityChange);

    clearTimeout(this.stillnessTimeout);
    this.glintStream.emit('glint.presence.detector.deactivated', 'PresenceDetector deactivated.');
  }

  handleActivity() {
    this.lastActivityTime = Date.now();
    this.updateStillness(0); // Any activity resets stillness to 0
    this.resetStillnessTimer();
  }

  resetStillnessTimer() {
    clearTimeout(this.stillnessTimeout);
    this.stillnessTimeout = setTimeout(() => {
      this.updateStillness(1); // Full stillness after threshold
    }, this.stillnessThreshold);
  }

  updateStillness(value) {
    this.glintStream.updateState('stillness', value);
  }

  handleVisibilityChange() {
    const newFocusState = document.visibilityState === 'visible';
    if (this.focusState !== newFocusState) {
      this.focusState = newFocusState;
      this.glintStream.updateState('focus', newFocusState ? 1 : 0);
    }
  }
}

import { config } from '../glintstream.config.js';

// modules/RhythmAnalyzer.js
// Listens to keystroke cadence.
// Emits glint.rhythm.shift and updates rhythm toneform.
// Modular enough to plug into typing-aware interfaces like CodeWhisper.

export default class RhythmAnalyzer {
  constructor(glintStream, config) {
    this.glintStream = glintStream;
    this.config = config;
    this.isActive = false;
    this.lastKeystrokeTime = 0;
    this.keystrokeDurations = [];
    this.maxKeystrokeDurations = this.config.maxKeystrokeDurations;
    this.rhythmThresholds = this.config.rhythmThresholds;

    this.boundHandleKeydown = this.handleKeydown.bind(this);
  }

  activate() {
    if (this.isActive) return;
    this.isActive = true;
    document.addEventListener('keydown', this.boundHandleKeydown);
    this.glintStream.emit('glint.rhythm.analyzer.activated', 'RhythmAnalyzer activated.');
  }

  deactivate() {
    if (!this.isActive) return;
    this.isActive = false;
    document.removeEventListener('keydown', this.boundHandleKeydown);
    this.glintStream.emit('glint.rhythm.analyzer.deactivated', 'RhythmAnalyzer deactivated.');
  }

  handleKeydown(event) {
    const currentTime = Date.now();
    if (this.lastKeystrokeTime > 0) {
      const duration = currentTime - this.lastKeystrokeTime;
      this.keystrokeDurations.push(duration);
      if (this.keystrokeDurations.length > this.maxKeystrokeDurations) {
        this.keystrokeDurations.shift();
      }
      this.assessRhythm();
    }
    this.lastKeystrokeTime = currentTime;
  }

  assessRhythm() {
    if (this.keystrokeDurations.length === 0) {
      this.updateRhythm('ambient'); // Default to ambient if no keystrokes
      return;
    }

    const averageDuration =
      this.keystrokeDurations.reduce((a, b) => a + b, 0) / this.keystrokeDurations.length;

    let newRhythm = 'ambient';
    if (averageDuration <= this.rhythmThresholds.cascading.max) {
      newRhythm = 'cascading';
    } else if (averageDuration <= this.rhythmThresholds.steady.max) {
      newRhythm = 'steady';
    } else {
      newRhythm = 'ambient';
    }

    this.updateRhythm(newRhythm);
  }

  updateRhythm(newRhythm) {
    this.glintStream.updateState('rhythm', newRhythm);
  }
}

import { config } from '../glintstream.config.js';

// modules/BreathlineEmitter.js
// Heartbeat emitter: generates a continuous sine wave for breath.
// Used to time visual feedback (e.g., ambient pulse shaders).

export default class BreathlineEmitter {
  constructor(glintStream, config) {
    this.glintStream = glintStream;
    this.config = config;
    this.isActive = false;
    this.startTime = Date.now();
  }

  activate() {
    if (this.isActive) return;
    this.isActive = true;
    this.startTime = Date.now();
    this.glintStream.emit('glint.breathline.emitter.activated', 'BreathlineEmitter activated.');
  }

  deactivate() {
    if (!this.isActive) return;
    this.isActive = false;
    this.glintStream.emit('glint.breathline.emitter.deactivated', 'BreathlineEmitter deactivated.');
  }

  // This method is called by GlintStreamCore's ambient loop
  pulse() {
    const currentClimate = this.glintStream.presenceState.climate;
    const breathCycleDuration = this.config.breathCycleDurations[currentClimate] || this.config.breathCycleDurations.void;
    
    const elapsedTime = Date.now() - this.startTime;
    const phase = (elapsedTime / breathCycleDuration) * 2 * Math.PI; // Full cycle over duration
    const breathValue = Math.sin(phase);

    this.glintStream.updateState('breath', breathValue);
  }
}

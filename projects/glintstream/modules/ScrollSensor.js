// modules/ScrollSensor.js
import { config } from '../glintstream.config.js';

export default class ScrollSensor {
  constructor(glintStream, config) {
    this.glintStream = glintStream;
    this.config = config;
    this.isActive = false;
    this.lastScrollTime = 0;
    this.lastScrollY = 0;
    this.scrollVelocity = 0;
    this.scrollTimeout = null;

    this.boundHandleScroll = this.handleScroll.bind(this);
  }

  activate() {
    if (this.isActive) return;
    this.isActive = true;
    window.addEventListener('scroll', this.boundHandleScroll, { passive: true });
    this.glintStream.emit('glint.scroll.sensor.activated', 'ScrollSensor activated.');
  }

  deactivate() {
    if (!this.isActive) return;
    this.isActive = false;
    window.removeEventListener('scroll', this.boundHandleScroll);
    this.glintStream.emit('glint.scroll.sensor.deactivated', 'ScrollSensor deactivated.');
  }

  handleScroll() {
    const currentTime = Date.now();
    const currentScrollY = window.scrollY;

    if (this.lastScrollTime > 0) {
      const timeDelta = currentTime - this.lastScrollTime;
      const scrollDelta = Math.abs(currentScrollY - this.lastScrollY);
      this.scrollVelocity = (scrollDelta / timeDelta) * 1000; // pixels per second
    }

    this.lastScrollTime = currentTime;
    this.lastScrollY = currentScrollY;

    if (this.scrollVelocity > config.scrollVelocityThreshold) {
      this.glintStream.emit('glint.scroll.skimmed', `Skimming at ${this.scrollVelocity.toFixed(0)}px/s`, {
        velocity: this.scrollVelocity,
      });
    }

    clearTimeout(this.scrollTimeout);
    this.scrollTimeout = setTimeout(() => {
      this.scrollVelocity = 0;
      this.glintStream.emit('glint.scroll.stilled', 'Scrolling stilled.', {
        position: window.scrollY,
      });
    }, config.scrollStilledThreshold);
  }
}

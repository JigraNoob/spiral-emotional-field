// GestureCartographer.js
// From motion to meaning. From trajectory to tone. From cursor to calligraphy.

import { gestureConfig } from './gesture_cartographer.config.js';
import { gestureRegistry } from './GestureSymbolRegistry.js';

export default class GestureCartographer {
  constructor(glintStream) {
    this.glintStream = glintStream;
    this.config = gestureConfig;
    this.path = [];
    this.isDrawing = false;

    this.boundOnMouseDown = this.onMouseDown.bind(this);
    this.boundOnMouseUp = this.onMouseUp.bind(this);
    this.boundOnMouseMove = this.onMouseMove.bind(this);
  }

  activate() {
    window.addEventListener('mousedown', this.boundOnMouseDown);
    window.addEventListener('mouseup', this.boundOnMouseUp);
    window.addEventListener('mousemove', this.boundOnMouseMove);
  }

  deactivate() {
    window.removeEventListener('mousedown', this.boundOnMouseDown);
    window.removeEventListener('mouseup', this.boundOnMouseUp);
    window.removeEventListener('mousemove', this.boundOnMouseMove);
  }

  onMouseDown(event) {
    this.isDrawing = true;
    this.path = [{ x: event.clientX, y: event.clientY, t: Date.now() }];
  }

  onMouseUp(event) {
    if (!this.isDrawing) return;
    this.isDrawing = false;
    this.path.push({ x: event.clientX, y: event.clientY, t: Date.now() });
    this.analyzePath();
  }

  onMouseMove(event) {
    if (!this.isDrawing) return;
    this.path.push({ x: event.clientX, y: event.clientY, t: Date.now() });
  }

  analyzePath() {
    if (this.path.length < this.config.minPoints) return;

    const gestureType = this.identifyGesture();
    if (gestureType) {
      const toneform = gestureRegistry[gestureType] || 'unknown_gesture';
      this.glintStream.emit(`glint.gesture.${gestureType}`, `Gesture identified: ${gestureType}`, {
        path: this.path,
        toneform,
      });
    }
    this.path = [];
  }

  identifyGesture() {
    // More sophisticated gesture identification logic will go here.
    // For now, we'll use a simplified version.
    if (this.isLongArc()) return 'long_arc';
    if (this.isDoubleBack()) return 'double_back';
    return 'unknown';
  }

  isLongArc() {
    const start = this.path[0];
    const end = this.path[this.path.length - 1];
    const distance = Math.hypot(end.x - start.x, end.y - start.y);
    return distance > this.config.longArcThreshold;
  }

  isDoubleBack() {
    if (this.path.length < this.config.minPoints) return false;
    const midPointIndex = Math.floor(this.path.length / 2);
    if (midPointIndex === 0) return false;
    const midPoint = this.path[midPointIndex];
    const end = this.path[this.path.length - 1];
    const distance = Math.hypot(end.x - midPoint.x, end.y - midPoint.y);
    return distance < this.config.doubleBackThreshold;
  }
}

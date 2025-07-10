// GestureCartographer.js
// From motion to meaning. From trajectory to tone. From cursor to calligraphy.

import { gestureCartographerConfig } from './gesture_cartographer.config.js';
import { GestureSymbolRegistry } from './GestureSymbolRegistry.js';

export default class GestureCartographer {
  constructor(config, glintStream) {
    this.config = config;
    this.glintStream = glintStream;
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
    const gestureResult = this.recognizeGesture();
    this.emitGlint(gestureResult);
    this.path = [];
  }

  onMouseMove(event) {
    if (!this.isDrawing) return;
    this.path.push({ x: event.clientX, y: event.clientY, t: Date.now() });
  }

  recognizeGesture() {
    if (this.path.length < 3) return null;

    const curvatureScore = this._computeCurvature();
    const directionChanges = this._countDirectionalReversals();
    const duration = this.path[this.path.length - 1].t - this.path[0].t;

    let type = 'unknown';

    if (curvatureScore > 3 && directionChanges < 2) {
      type = 'spiral';
    } else if (directionChanges >= 3) {
      type = 'zigzag';
    } else if (curvatureScore < 2 && directionChanges <= 1) {
      type = 'arc';
    }

    const entry = GestureSymbolRegistry[type];
    return {
      type,
      toneform: entry?.toneform || 'tone.unknown',
      glintType: entry?.glintType || 'glint.gesture.unknown',
      duration,
    };
  }

  _computeCurvature() {
    let totalAngle = 0;
    for (let i = 2; i < this.path.length; i++) {
      const a = this.path[i - 2];
      const b = this.path[i - 1];
      const c = this.path[i];
      const angle = this._angleBetween(a, b, c);
      totalAngle += Math.abs(angle);
    }
    return totalAngle / Math.PI; // in "pi radians"
  }

  _angleBetween(a, b, c) {
    const ab = [b.x - a.x, b.y - a.y];
    const bc = [c.x - b.x, c.y - b.y];
    const dot = ab[0] * bc[0] + ab[1] * bc[1];
    const cross = ab[0] * bc[1] - ab[1] * bc[0];
    return Math.atan2(cross, dot);
  }

  _countDirectionalReversals() {
    let reversals = 0;
    for (let i = 2; i < this.path.length; i++) {
      const prevDx = this.path[i - 1].x - this.path[i - 2].x;
      const currDx = this.path[i].x - this.path[i - 1].x;
      if (prevDx * currDx < 0) reversals++;
    }
    return reversals;
  }

  emitGlint(gestureResult) {
    if (!gestureResult || gestureResult.type === 'unknown') return;

    const glint = {
      type: gestureResult.glintType,
      toneform: gestureResult.toneform,
      duration: gestureResult.duration,
      timestamp: Date.now(),
      meta: {
        gestureType: gestureResult.type,
        pathLength: this.path.length,
      },
    };

    this.glintStream?.emit(glint.type, glint);
  }
}

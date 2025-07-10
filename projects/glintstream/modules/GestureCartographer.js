// modules/GestureCartographer.js
// Maps mouse movement into symbolic gesture topographies.

export default class GestureCartographer {
  constructor(glintStream, config) {
    this.glintStream = glintStream;
    this.config = config;
    this.isActive = false;
    this.path = [];
    this.isDrawing = false;

    this.boundOnMouseDown = this.onMouseDown.bind(this);
    this.boundOnMouseUp = this.onMouseUp.bind(this);
    this.boundOnMouseMove = this.onMouseMove.bind(this);
  }

  activate() {
    if (this.isActive) return;
    this.isActive = true;
    window.addEventListener('mousedown', this.boundOnMouseDown);
    window.addEventListener('mouseup', this.boundOnMouseUp);
    window.addEventListener('mousemove', this.boundOnMouseMove);
    this.glintStream.emit('glint.sensor.gesture.activated', 'GestureCartographer activated.');
  }

  deactivate() {
    if (!this.isActive) return;
    this.isActive = false;
    window.removeEventListener('mousedown', this.boundOnMouseDown);
    window.removeEventListener('mouseup', this.boundOnMouseUp);
    window.removeEventListener('mousemove', this.boundOnMouseMove);
    this.glintStream.emit('glint.sensor.gesture.deactivated', 'GestureCartographer deactivated.');
  }

  onMouseDown(event) {
    this.isDrawing = true;
    this.path = [{ x: event.clientX, y: event.clientY }];
  }

  onMouseUp(event) {
    if (!this.isDrawing) return;
    this.isDrawing = false;
    this.path.push({ x: event.clientX, y: event.clientY });
    this.analyzePath();
  }

  onMouseMove(event) {
    if (!this.isDrawing) return;
    this.path.push({ x: event.clientX, y: event.clientY });
  }

  analyzePath() {
    if (this.path.length < this.config.gestureMinPoints) return;

    const shape = this.identifyShape();
    if (shape) {
      this.glintStream.emit(`glint.gesture.${shape}`, `User drew a ${shape}.`, {
        path: this.path,
      });
    }
    this.path = [];
  }

  identifyShape() {
    // Check for shapes in order of priority
    if (this.isLoop()) return 'loop';
    if (this.isSharpEdge()) return 'edge';
    if (this.isSpiral()) return 'spiral';
    return null;
  }

  isLoop() {
    const start = this.path[0];
    const end = this.path[this.path.length - 1];
    const distance = Math.hypot(end.x - start.x, end.y - start.y);
    return distance < this.config.loopClosureThreshold && this.path.length > 10;
  }

  isSpiral() {
    // A simple spiral detection: radius continuously changes
    if (this.path.length < 20) return false;
    const center = this.path.reduce((acc, p) => ({ x: acc.x + p.x, y: acc.y + p.y }), { x: 0, y: 0 });
    center.x /= this.path.length;
    center.y /= this.path.length;

    const radii = this.path.map(p => Math.hypot(p.x - center.x, p.y - center.y));
    let increasing = 0;
    for (let i = 1; i < radii.length; i++) {
      if (radii[i] > radii[i - 1]) increasing++;
    }
    // If radius is mostly increasing or decreasing, it could be a spiral
    const monotonicRatio = increasing / radii.length;
    return monotonicRatio > 0.9 || monotonicRatio < 0.1; // Stricter threshold
  }

  isSharpEdge() {
    if (this.path.length < 3) return false;
    const angles = [];
    for (let i = 1; i < this.path.length - 1; i++) {
      const p1 = this.path[i - 1];
      const p2 = this.path[i];
      const p3 = this.path[i + 1];
      const v1 = { x: p1.x - p2.x, y: p1.y - p2.y };
      const v2 = { x: p3.x - p2.x, y: p3.y - p2.y };
      const angle = Math.atan2(v1.y, v1.x) - Math.atan2(v2.y, v2.x);
      let deg = Math.abs(angle * 180 / Math.PI);
      if (deg > 180) deg = 360 - deg;
      angles.push(deg);
    }
    const sharpTurns = angles.filter(a => a > 45 && a < 135).length; // Look for angles that are decidedly not straight
    return sharpTurns > 0;
  }
}

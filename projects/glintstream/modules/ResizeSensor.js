// modules/ResizeSensor.js
// Senses changes in the container's dimensions, emitting glints on expansion or contraction.

export default class ResizeSensor {
  constructor(glintStream, config) {
    this.glintStream = glintStream;
    this.config = config;
    this.isActive = false;
    this.lastDimensions = {
      width: window.innerWidth,
      height: window.innerHeight,
    };
    this.boundHandleResize = this.handleResize.bind(this);
  }

  activate() {
    if (this.isActive) return;
    this.isActive = true;
    window.addEventListener('resize', this.boundHandleResize);
    this.glintStream.emit('glint.sensor.resize.activated', 'ResizeSensor activated.');
  }

  deactivate() {
    if (!this.isActive) return;
    this.isActive = false;
    window.removeEventListener('resize', this.boundHandleResize);
    this.glintStream.emit('glint.sensor.resize.deactivated', 'ResizeSensor deactivated.');
  }

  handleResize() {
    const newWidth = window.innerWidth;
    const newHeight = window.innerHeight;
    const oldArea = this.lastDimensions.width * this.lastDimensions.height;
    const newArea = newWidth * newHeight;

    let eventType = '';
    if (newArea > oldArea) {
      eventType = 'glint.field.expand';
    } else if (newArea < oldArea) {
      eventType = 'glint.field.contract';
    }

    if (eventType) {
      this.glintStream.emit(eventType, 'Field dimensions shifted.', {
        from: this.lastDimensions,
        to: { width: newWidth, height: newHeight },
      });
    }

    this.lastDimensions = { width: newWidth, height: newHeight };
  }
}
// modules/ToneformBridge.js
// Bridges glint events to UI modules.
// Interface-facing: addListener, transmit(), removeListener().

export default class ToneformBridge extends EventTarget {
  constructor() {
    super();
    // This class extends EventTarget, so it naturally supports addEventListener, removeEventListener, dispatchEvent.
    // The 'transmit' method will dispatch a custom event that UI modules can listen to.
  }

  // This method is called by GlintStreamCore's emit function
  transmit(glint) {
    // Dispatch a custom event with the glint detail
    this.dispatchEvent(new CustomEvent('toneform', { detail: glint }));
  }

  // Public methods for external UI modules to subscribe
  // For clarity, though EventTarget methods can be used directly:
  addToneformListener(callback) {
    this.addEventListener('toneform', callback);
  }

  removeToneformListener(callback) {
    this.removeEventListener('toneform', callback);
  }
}

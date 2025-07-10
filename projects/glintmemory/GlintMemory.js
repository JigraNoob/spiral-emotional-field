import LocalStorageAdapter from './LocalStorageAdapter.js';

// modules/GlintMemory.js
// Stores ephemeral glints, now with a persistent echo via LocalStorage.
// Functions as the short-term witness chamber with a long-term memory trace.

export default class GlintMemory {
  constructor(config) {
    this.config = config;
    this.adapter = new LocalStorageAdapter(config);
    this.memory = this.adapter.load(); // Load previous session's memory
    this.windowDuration = this.config.memoryWindowDuration;
    this.cleanupInterval = null;

    this.cleanup(); // Initial cleanup of loaded glints
    this.startCleanupLoop();
  }

  remember(glint) {
    this.memory.push(glint);
    this.adapter.save(this.memory); // Persist memory after each addition
  }

  recall(filterFn = () => true) {
    this.cleanup(); // Ensure memory is fresh before recall
    return this.memory.filter(filterFn);
  }

  forget() {
    this.memory = [];
    this.adapter.clear();
  }

  // Cleans up old glints outside the sliding window
  cleanup() {
    const now = Date.now();
    const freshGlints = this.memory.filter((glint) => now - glint.timestamp < this.windowDuration);
    if (freshGlints.length < this.memory.length) {
      this.memory = freshGlints;
      this.adapter.save(this.memory); // Save the cleaned memory
    }
  }

  startCleanupLoop() {
    if (!this.cleanupInterval) {
      this.cleanupInterval = setInterval(() => this.cleanup(), this.windowDuration / 2); // Clean up twice per window duration
    }
  }

  stopCleanupLoop() {
    if (this.cleanupInterval) {
      clearInterval(this.cleanupInterval);
      this.cleanupInterval = null;
    }
  }
}

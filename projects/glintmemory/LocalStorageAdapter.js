// modules/LocalStorageAdapter.js
// Handles the persistence of glint memory to the browser's localStorage.

const MEMORY_KEY = 'glintstream_memory';

export default class LocalStorageAdapter {
  constructor(config) {
    this.config = config;
  }

  save(glints) {
    try {
      const serializedGlints = JSON.stringify(glints);
      localStorage.setItem(MEMORY_KEY, serializedGlints);
    } catch (error) {
      console.error('GlintStream: Error saving to localStorage.', error);
    }
  }

  load() {
    try {
      const serializedGlints = localStorage.getItem(MEMORY_KEY);
      if (serializedGlints === null) {
        return [];
      }
      return JSON.parse(serializedGlints);
    } catch (error) {
      console.error('GlintStream: Error loading from localStorage.', error);
      return [];
    }
  }

  clear() {
    try {
      localStorage.removeItem(MEMORY_KEY);
    } catch (error) {
      console.error('GlintStream: Error clearing localStorage.', error);
    }
  }
}

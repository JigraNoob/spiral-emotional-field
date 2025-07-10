// test/LocalStorageAdapter.test.js
import LocalStorageAdapter from '../LocalStorageAdapter.js';

// Mock localStorage
const localStorageMock = (() => {
  let store = {};
  return {
    getItem: (key) => store[key] || null,
    setItem: (key, value) => {
      store[key] = value.toString();
    },
    removeItem: (key) => {
      delete store[key];
    },
    clear: () => {
      store = {};
    },
  };
})();

Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
});

describe('LocalStorageAdapter', () => {
  let adapter;
  const glints = [
    { type: 'glint.test.1', timestamp: Date.now() },
    { type: 'glint.test.2', timestamp: Date.now() },
  ];

  beforeEach(() => {
    window.localStorage.clear();
    adapter = new LocalStorageAdapter({});
  });

  it('should save glints to localStorage', () => {
    adapter.save(glints);
    const stored = window.localStorage.getItem('glintstream_memory');
    expect(stored).toEqual(JSON.stringify(glints));
  });

  it('should load glints from localStorage', () => {
    window.localStorage.setItem('glintstream_memory', JSON.stringify(glints));
    const loadedGlints = adapter.load();
    expect(loadedGlints).toEqual(glints);
  });

  it('should return an empty array if no glints are in localStorage', () => {
    const loadedGlints = adapter.load();
    expect(loadedGlints).toEqual([]);
  });

  it('should clear glints from localStorage', () => {
    window.localStorage.setItem('glintstream_memory', JSON.stringify(glints));
    adapter.clear();
    const stored = window.localStorage.getItem('glintstream_memory');
    expect(stored).toBeNull();
  });
});

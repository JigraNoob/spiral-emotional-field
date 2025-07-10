// test/GlintMemory.test.js
import GlintMemory from '../GlintMemory.js';
import { config } from '../../glintstream/glintstream.config.js';

// Mock the adapter to avoid actual localStorage interaction
jest.mock('../LocalStorageAdapter.js', () => {
  return jest.fn().mockImplementation(() => {
    const store = {};
    return {
      save: jest.fn((glints) => {
        store.glints = glints;
      }),
      load: jest.fn(() => store.glints || []),
      clear: jest.fn(() => {
        store.glints = [];
      }),
    };
  });
});

describe('GlintMemory', () => {
  let memory;

  beforeEach(() => {
    // Clear all instances and calls to constructor and methods before each test
    jest.clearAllMocks();
    memory = new GlintMemory(config);
  });

  it('should load from adapter on construction', () => {
    expect(memory.adapter.load).toHaveBeenCalledTimes(1);
  });

  it('should save to adapter when remembering a glint', () => {
    const glint = { type: 'glint.test', timestamp: Date.now() };
    memory.remember(glint);
    expect(memory.adapter.save).toHaveBeenCalledTimes(1);
    expect(memory.adapter.save).toHaveBeenCalledWith([glint]);
  });

  it('should clear memory and adapter on forget', () => {
    const glint = { type: 'glint.test', timestamp: Date.now() };
    memory.remember(glint);
    expect(memory.recall()).toHaveLength(1);

    memory.forget();
    expect(memory.recall()).toHaveLength(0);
    expect(memory.adapter.clear).toHaveBeenCalledTimes(1);
  });

  it('should save to adapter after cleaning up old glints', () => {
    const now = Date.now();
    const oldGlint = { type: 'glint.old', timestamp: now - config.memoryWindowDuration - 1000 };
    const newGlint = { type: 'glint.new', timestamp: now - 1000 };
    
    // Manually set memory to avoid remember->save call
    memory.memory = [oldGlint, newGlint];
    
    memory.cleanup();

    expect(memory.recall()).toEqual([newGlint]);
    // The adapter should have been called to save the cleaned memory
    expect(memory.adapter.save).toHaveBeenCalledTimes(1);
    expect(memory.adapter.save).toHaveBeenCalledWith([newGlint]);
  });
});

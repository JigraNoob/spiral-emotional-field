// test/GlintChronicle.test.js
import GlintChronicle from '../GlintChronicle.js';
import { chronicleConfig } from '../glintchronicle.config.js';

// Mock the fs module
const mockFs = {
  promises: {
    appendFile: jest.fn(),
  },
};

class MockGlintStream extends EventTarget {
  emit(type, message, data = {}) {
    const glint = { type, message, data, presence: { climate: 'drift', rhythm: 'ambient', breath: 0.5 } };
    this.dispatchEvent(new CustomEvent('glint', { detail: glint }));
  }
}

describe('GlintChronicle', () => {
  let mockStream;
  let chronicle;

  beforeEach(() => {
    mockStream = new MockGlintStream();
    chronicle = new GlintChronicle(mockStream, mockFs);
    chronicle.activate();
    // Clear mock calls from activation
    mockFs.promises.appendFile.mockClear();
  });

  it('should write a formatted entry for a gesture glint', async () =>{
    await mockStream.emit('glint.gesture.loop', 'A loop was drawn.');

    expect(mockFs.promises.appendFile).toHaveBeenCalledTimes(1);
    const writtenContent = mockFs.promises.appendFile.mock.calls[0][1];
    
    expect(writtenContent).toContain('**[loop]**');
    expect(writtenContent).toContain('> climate: drift');
    expect(writtenContent).toContain(chronicleConfig.toneTemplates.loop);
  });

  it('should not write an entry for an un-chronicled glint type', async () =>{
    await mockStream.emit('glint.internal.some_event', 'An internal event.');
    expect(mockFs.promises.appendFile).not.toHaveBeenCalled();
  });

  it('should insert a caesura if enough time has passed between glints', async () =>{
    chronicle.lastGlintTime = Date.now() - chronicleConfig.caesuraThreshold - 100;
    await mockStream.emit('glint.gesture.edge', 'An edge was drawn.');

    expect(mockFs.promises.appendFile).toHaveBeenCalledTimes(1);
    const writtenContent = mockFs.promises.appendFile.mock.calls[0][1];
    expect(writtenContent).toContain('---\n\n');
  });
});

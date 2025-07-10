// test/GlintScript.test.js
import GlintScript from '../GlintScript.js';
import { glintScriptConfig } from '../glintscript.config.js';

class MockGlintStream extends EventTarget {
  constructor() {
    super();
    this.presenceState = { climate: 'void' };
  }
  emit(type, message, data = {}) {
    const glint = { type, message, data, presence: this.presenceState };
    this.dispatchEvent(new CustomEvent('glint', { detail: glint }));
  }
}

const createMockGemini = (glintStream) => ({
  invoke: jest.fn(),
  glintStream,
});

describe('GlintScript', () => {
  let mockStream;
  let mockGemini;
  let scriptEngine;

  beforeEach(() => {
    mockStream = new MockGlintStream();
    mockGemini = createMockGemini(mockStream);
    scriptEngine = new GlintScript(mockStream, mockGemini);
    jest.useFakeTimers();
  });

  afterEach(() => {
    jest.useRealTimers();
  });

  it('should parse a ritual with a condition and a delay', () => {
    const script = `on glint: "glint.scroll.skimmed" if velocity > 1500 after 1s → emit: "glint.test.fastscroll"`;
    const ritual = scriptEngine.parse(script);
    expect(ritual.condition).toEqual({ key: 'velocity', operator: '>', value: 1500 });
    expect(ritual.delay).toBe(1000);
  });

  it('should only execute a delayed action if the condition is met', () => {
    const script = `on glint: "glint.test.event" if value > 10 after 500ms → emit: "glint.test.success"`;
    scriptEngine.addRitual(script);
    scriptEngine.execute();
    const emitSpy = jest.spyOn(mockStream, 'emit');

    // Condition not met
    mockStream.emit('glint.test.event', 'Condition not met', { value: 5 });
    jest.advanceTimersByTime(500);
    expect(emitSpy).not.toHaveBeenCalledWith('glint.test.success', expect.any(String));

    // Condition met
    mockStream.emit('glint.test.event', 'Condition met', { value: 15 });
    jest.advanceTimersByTime(500);
    expect(emitSpy).toHaveBeenCalledWith('glint.test.success', 'Ritual action triggered.');
  });

  it('should correctly parse and handle different time units', () => {
    const script_s = 'on climate: "void" after 2s → emit: "glint.test.delay_s"';
    const script_ms = 'on climate: "void" after 500ms → emit: "glint.test.delay_ms"';
    const ritual_s = scriptEngine.parse(script_s);
    const ritual_ms = scriptEngine.parse(script_ms);
    expect(ritual_s.delay).toBe(2000);
    expect(ritual_ms.delay).toBe(500);
  });
});

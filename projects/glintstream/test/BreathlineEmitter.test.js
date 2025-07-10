// test/BreathlineEmitter.test.js
import BreathlineEmitter from '../modules/BreathlineEmitter.js';
import { config } from '../glintstream.config.js';

const createMockGlintStream = () => ({
  updateState: jest.fn(),
  emit: jest.fn(),
  presenceState: {
    climate: 'void'
  }
});

describe('BreathlineEmitter', () => {
  let mockGlintStream;
  let emitter;

  beforeEach(() => {
    jest.useFakeTimers();
    mockGlintStream = createMockGlintStream();
    emitter = new BreathlineEmitter(mockGlintStream, config);
    emitter.activate();
  });

  it('should generate a sine wave value on pulse', () => {
    emitter.pulse();
    // At time 0, sin(0) is 0
    expect(mockGlintStream.updateState).toHaveBeenCalledWith('breath', 0);

    // Advance time to a quarter of the cycle
    jest.advanceTimersByTime(config.breathCycleDurations.void / 4);
    emitter.pulse();
    // At time T/4, sin(PI/2) is 1
    const lastCall = mockGlintStream.updateState.mock.calls.pop();
    expect(lastCall[0]).toBe('breath');
    expect(lastCall[1]).toBeCloseTo(1);

    // Advance time to half the cycle
    jest.advanceTimersByTime(config.breathCycleDurations.void / 4);
    emitter.pulse();
    // At time T/2, sin(PI) is 0
    const lastCall2 = mockGlintStream.updateState.mock.calls.pop();
    expect(lastCall2[0]).toBe('breath');
    expect(lastCall2[1]).toBeCloseTo(0);
  });
});

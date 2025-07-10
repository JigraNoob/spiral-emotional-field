// test/RhythmAnalyzer.test.js
import RhythmAnalyzer from '../modules/RhythmAnalyzer.js';

// Mock the GlintStreamCore
const createMockGlintStream = () => ({
  presenceState: {
    rhythm: 'ambient',
  },
  updateState: jest.fn(),
  emit: jest.fn(),
});

describe('RhythmAnalyzer', () => {
  it('should shift rhythm to "cascading" on rapid keystrokes', () => {
    const mockGlintStream = createMockGlintStream();
    const analyzer = new RhythmAnalyzer(mockGlintStream, {
      maxKeystrokeDurations: 10,
      rhythmThresholds: {
        cascading: { max: 150 },
        steady: { max: 500 },
      }
    });

    // Mock the keydown event
    const event = new KeyboardEvent('keydown', { key: 'a' });

    // Simulate rapid keystrokes
    let currentTime = Date.now();
    jest.spyOn(Date, 'now').mockReturnValue(currentTime);
    analyzer.handleKeydown(event);

    currentTime += 50; // 50ms later
    jest.spyOn(Date, 'now').mockReturnValue(currentTime);
    analyzer.handleKeydown(event);

    currentTime += 60; // 60ms later
    jest.spyOn(Date, 'now').mockReturnValue(currentTime);
    analyzer.handleKeydown(event);

    // The updateState function should have been called with the rhythm shift
    const lastCall = mockGlintStream.updateState.mock.calls.pop();
    expect(lastCall[0]).toBe('rhythm');
    expect(lastCall[1]).toBe('cascading');
  });
});

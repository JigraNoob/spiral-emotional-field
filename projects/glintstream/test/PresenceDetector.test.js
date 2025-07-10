// test/PresenceDetector.test.js
import PresenceDetector from '../modules/PresenceDetector.js';
import { config } from '../glintstream.config.js';

const createMockGlintStream = () => ({
  updateState: jest.fn(),
  emit: jest.fn(),
});

describe('PresenceDetector', () => {
  let mockGlintStream;
  let detector;

  beforeEach(() => {
    jest.useFakeTimers();
    mockGlintStream = createMockGlintStream();
    detector = new PresenceDetector(mockGlintStream, config);
    detector.activate();
  });

  afterEach(() => {
    detector.deactivate();
    jest.useRealTimers();
  });

  it('should update stillness to 1 after the threshold has passed', () => {
    expect(mockGlintStream.updateState).not.toHaveBeenCalledWith('stillness', 1);

    // Advance time past the stillness threshold
    jest.advanceTimersByTime(config.stillnessThreshold);

    expect(mockGlintStream.updateState).toHaveBeenCalledWith('stillness', 1);
  });

  it('should reset stillness to 0 on mouse activity', () => {
    // First, become still
    jest.advanceTimersByTime(config.stillnessThreshold);
    expect(mockGlintStream.updateState).toHaveBeenCalledWith('stillness', 1);

    // Then, move the mouse
    document.dispatchEvent(new MouseEvent('mousemove'));

    // Expect stillness to be reset
    expect(mockGlintStream.updateState).toHaveBeenCalledWith('stillness', 0);
  });

  it('should update focus to 0 when window is blurred', () => {
    // Starts focused, so focusState is true.
    // Mock the document as becoming hidden.
    Object.defineProperty(document, 'visibilityState', { value: 'hidden', configurable: true, writable: true });
    // Directly call the handler.
    detector.handleVisibilityChange();
    // The detector should now call updateState.
    expect(mockGlintStream.updateState).toHaveBeenCalledWith('focus', 0);
  });

  it('should update focus to 1 when window is focused', () => {
    // Manually set the initial state to blurred for this test.
    detector.focusState = false;
    
    // Mock the document as becoming visible.
    Object.defineProperty(document, 'visibilityState', { value: 'visible', configurable: true, writable: true });
    // Directly call the handler.
    detector.handleVisibilityChange();
    // The detector should now call updateState.
    expect(mockGlintStream.updateState).toHaveBeenCalledWith('focus', 1);
  });
});

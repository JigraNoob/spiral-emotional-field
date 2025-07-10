// test/GestureCartographer.test.js
import GestureCartographer from '../GestureCartographer.js';
import { gestureConfig } from '../gesture_cartographer.config.js';

const createMockGlintStream = () => ({
  emit: jest.fn(),
});

describe.skip('GestureCartographer', () => {
  let mockGlintStream;
  let cartographer;

  beforeEach(() => {
    mockGlintStream = createMockGlintStream();
    cartographer = new GestureCartographer(mockGlintStream);
    cartographer.activate();
  });

  afterEach(() => {
    cartographer.deactivate();
  });

  it('should identify a long arc gesture', () => {
    cartographer.onMouseDown({ clientX: 0, clientY: 0 });
    for (let i = 1; i <= 20; i++) {
      cartographer.onMouseMove({ clientX: i * 10, clientY: i * 5 });
    }
    cartographer.onMouseUp({ clientX: 200, clientY: 100 });

    expect(mockGlintStream.emit).toHaveBeenCalledWith(
      'glint.gesture.long_arc',
      expect.any(String),
      expect.any(Object)
    );
  });

  it('should identify a double-back gesture', () => {
    cartographer.onMouseDown({ clientX: 0, clientY: 0 });
    for (let i = 1; i <= 10; i++) {
      cartographer.onMouseMove({ clientX: i * 10, clientY: 0 });
    }
    for (let i = 9; i >= 0; i--) {
      cartographer.onMouseMove({ clientX: i * 10, clientY: 0 });
    }
    cartographer.onMouseUp({ clientX: 0, clientY: 0 });

    expect(mockGlintStream.emit).toHaveBeenCalledWith(
      'glint.gesture.double_back',
      expect.any(String),
      expect.any(Object)
    );
  });
});
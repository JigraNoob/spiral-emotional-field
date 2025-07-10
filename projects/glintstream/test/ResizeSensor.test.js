// test/ResizeSensor.test.js
import ResizeSensor from '../modules/ResizeSensor.js';

const createMockGlintStream = () => ({
  emit: jest.fn(),
});

describe('ResizeSensor', () => {
  let mockGlintStream;
  let sensor;

  beforeEach(() => {
    mockGlintStream = createMockGlintStream();
    sensor = new ResizeSensor(mockGlintStream, {});
    sensor.activate();

    // Set initial window dimensions for testing
    Object.defineProperty(window, 'innerWidth', { writable: true, configurable: true, value: 800 });
    Object.defineProperty(window, 'innerHeight', { writable: true, configurable: true, value: 600 });
    sensor.lastDimensions = { width: 800, height: 600 };
  });

  afterEach(() => {
    sensor.deactivate();
  });

  it('should emit glint.field.expand when the window area increases', () => {
    // Simulate expansion
    Object.defineProperty(window, 'innerWidth', { value: 1000 });
    Object.defineProperty(window, 'innerHeight', { value: 700 });
    window.dispatchEvent(new Event('resize'));

    expect(mockGlintStream.emit).toHaveBeenCalledWith(
      'glint.field.expand',
      'Field dimensions shifted.',
      {
        from: { width: 800, height: 600 },
        to: { width: 1000, height: 700 },
      }
    );
  });

  it('should emit glint.field.contract when the window area decreases', () => {
    // Simulate contraction
    Object.defineProperty(window, 'innerWidth', { value: 600 });
    Object.defineProperty(window, 'innerHeight', { value: 400 });
    window.dispatchEvent(new Event('resize'));

    expect(mockGlintStream.emit).toHaveBeenCalledWith(
      'glint.field.contract',
      'Field dimensions shifted.',
      {
        from: { width: 800, height: 600 },
        to: { width: 600, height: 400 },
      }
    );
  });

  it('should not emit a glint if the window area does not change', () => {
    // Simulate resize with same area
    Object.defineProperty(window, 'innerWidth', { value: 600 });
    Object.defineProperty(window, 'innerHeight', { value: 800 }); // Same area (480000)
    window.dispatchEvent(new Event('resize'));

    expect(mockGlintStream.emit).not.toHaveBeenCalledWith(
      expect.stringContaining('glint.field'),
      expect.any(String),
      expect.any(Object)
    );
  });
});

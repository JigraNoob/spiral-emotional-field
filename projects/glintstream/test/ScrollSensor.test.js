// test/ScrollSensor.test.js
import ScrollSensor from '../modules/ScrollSensor.js';
import { config } from '../glintstream.config.js';

const createMockGlintStream = () => ({
  emit: jest.fn(),
});

describe('ScrollSensor', () => {
  let mockGlintStream;
  let sensor;

  beforeEach(() => {
    jest.useFakeTimers();
    mockGlintStream = createMockGlintStream();
    sensor = new ScrollSensor(mockGlintStream);
    sensor.activate();
  });

  afterEach(() => {
    sensor.deactivate();
    jest.useRealTimers();
  });

  it('should emit glint.scroll.stilled after scrolling stops', () => {
    // Simulate a scroll event
    window.dispatchEvent(new Event('scroll'));
    expect(mockGlintStream.emit).not.toHaveBeenCalledWith('glint.scroll.stilled', expect.any(String), expect.any(Object));

    // Advance time past the stilled threshold
    jest.advanceTimersByTime(config.scrollStilledThreshold);

    const lastCall = mockGlintStream.emit.mock.calls.pop();
    expect(lastCall[0]).toBe('glint.scroll.stilled');
  });

  it('should emit glint.scroll.skimmed on high velocity scroll', () => {
    let currentTime = Date.now();
    jest.spyOn(Date, 'now').mockReturnValue(currentTime);
    Object.defineProperty(window, 'scrollY', { value: 0, writable: true });
    sensor.handleScroll();

    // Simulate a fast scroll
    currentTime += 100; // 100ms passes
    jest.spyOn(Date, 'now').mockReturnValue(currentTime);
    Object.defineProperty(window, 'scrollY', { value: 200, writable: true }); // Scrolled 200px
    sensor.handleScroll(); // Velocity should be 2000px/s

    const lastCall = mockGlintStream.emit.mock.calls.pop();
    expect(lastCall[0]).toBe('glint.scroll.skimmed');
    expect(lastCall[2].velocity).toBeGreaterThan(config.scrollVelocityThreshold);
  });
});

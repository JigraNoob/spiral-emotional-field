// test/AmbientUIPanel.test.js
import AmbientUIPanel from '../AmbientUIPanel.js';

// Mock the GlintStream for testing
class MockGlintStream extends EventTarget {
  constructor() {
    super();
    this.presenceState = { climate: 'void', breath: 0 };
  }
  emit(type, message, data) {
    const glint = { type, message, data, presence: this.presenceState, timestamp: Date.now() };
    this.dispatchEvent(new CustomEvent('glint', { detail: glint }));
  }
}

describe('AmbientUIPanel', () => {
  let mockStream;
  let panel;

  beforeEach(() => {
    document.body.innerHTML = ''; // Clear the DOM
    mockStream = new MockGlintStream();
    panel = new AmbientUIPanel(mockStream);
  });

  it('should create the panel element in the DOM', () => {
    const panelElement = document.getElementById('ambient-ui-panel');
    expect(panelElement).not.toBeNull();
  });

  it('should update the climate display on a glint event', () => {
    mockStream.presenceState.climate = 'presence';
    mockStream.emit('glint.climate.shift', 'Climate shifted to presence');

    const climateEl = panel.element.querySelector('[data-value="climate"]');
    expect(climateEl.textContent).toBe('presence');
    expect(panel.element.className).toBe('climate-presence');
  });

  it('should update the breath bar on a glint event', () => {
    mockStream.presenceState.breath = 0.5;
    mockStream.emit('glint.state.breath.change', 'Breath changed');

    const breathBar = panel.element.querySelector('[data-value="breath"]');
    // Normalized value: (0.5 + 1) / 2 = 0.75
    expect(breathBar.style.transform).toBe('scaleX(0.75)');
  });

  it('should update the last glint message on any glint event', () => {
    mockStream.emit('test.event', 'A test message');

    const lastGlintEl = panel.element.querySelector('[data-value="last-glint"]');
    expect(lastGlintEl.textContent).toBe('test.event: A test message');
  });
});

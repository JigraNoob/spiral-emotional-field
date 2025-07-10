// test/ClimateGlyphPane.test.js
import ClimateGlyphPane from '../ClimateGlyphPane.js';

class MockGlintStream extends EventTarget {
  constructor() {
    super();
    this.presenceState = { climate: 'void' };
  }
  emit(type, message, data = {}) {
    const glint = { type, message, data, presence: this.presenceState, timestamp: Date.now() };
    this.dispatchEvent(new CustomEvent('glint', { detail: glint }));
  }
}

describe('ClimateGlyphPane', () => {
  let mockStream;
  let pane;

  beforeEach(() => {
    document.body.innerHTML = ''; // Clear the DOM
    mockStream = new MockGlintStream();
    pane = new ClimateGlyphPane(mockStream);
  });

  it('should create the pane element in the DOM', () => {
    const paneElement = document.getElementById('climate-glyph-pane');
    expect(paneElement).not.toBeNull();
  });

  it('should render the correct glyph on a climate shift event', () => {
    mockStream.presenceState.climate = 'presence';
    mockStream.emit('glint.climate.shift', 'Shifted to presence');

    const glyphContainer = pane.element.querySelector('.glyph-container');
    expect(glyphContainer).not.toBeNull();
    expect(glyphContainer.classList.contains('glyph-presence')).toBe(true);
    // Check for the specific SVG content
    expect(glyphContainer.innerHTML).toContain('<circle cx="50" cy="50" r="20"');
  });

  it('should only respond to glint.climate.shift events', () => {
    const renderGlyphSpy = jest.spyOn(pane, 'renderGlyph');
    
    // This should not trigger a render
    mockStream.emit('glint.some.other.event', 'Some other event');
    expect(renderGlyphSpy).not.toHaveBeenCalled();

    // This should trigger a render
    mockStream.presenceState.climate = 'cascading';
    mockStream.emit('glint.climate.shift', 'Shifted to cascading');
    expect(renderGlyphSpy).toHaveBeenCalledWith('cascading');
  });

  it('should replace the old glyph with the new one', () => {
    jest.useFakeTimers();
    
    // Initial state
    mockStream.presenceState.climate = 'void';
    mockStream.emit('glint.climate.shift', 'Shifted to void');
    expect(pane.element.querySelectorAll('.glyph-container').length).toBe(1);
    expect(pane.element.querySelector('.glyph-void')).not.toBeNull();

    // New state
    mockStream.presenceState.climate = 'shimmering';
    mockStream.emit('glint.climate.shift', 'Shifted to shimmering');
    
    // The new glyph should be there immediately
    expect(pane.element.querySelector('.glyph-shimmering')).not.toBeNull();
    
    // After the fade-out timeout, the old one should be gone
    jest.advanceTimersByTime(500);
    expect(pane.element.querySelector('.glyph-void')).toBeNull();
    expect(pane.element.querySelectorAll('.glyph-container').length).toBe(1);

    jest.useRealTimers();
  });
});

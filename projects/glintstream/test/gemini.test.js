import GeminiInterface from '../gemini.js';

// Mock GlintStream for testing
const createMockGlintStream = () => ({
  presenceState: { stillness: 0.5, focus: 0.5, rhythm: 'ambient', climate: 'drift', breath: 0.5 },
  emit: jest.fn(),
  addEventListener: jest.fn(),
});

describe('GeminiInterface', () => {
  let mockGlintStream;
  let gemini;
  const config = {
    defaultToneform: 'test-tone',
    glintstream: {
      toneEcho: 'console',
      watchState: true,
    },
  };

  beforeEach(() => {
    mockGlintStream = createMockGlintStream();
    gemini = new GeminiInterface(config, mockGlintStream);
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  test('should be created successfully', () => {
    expect(gemini).toBeInstanceOf(GeminiInterface);
    expect(gemini.glintstream).toBe(mockGlintStream);
    expect(gemini.config).toBe(config);
  });

  describe('invoke', () => {
    test('should call glintstream.emit with correct parameters', async () => {
      const message = 'Test invocation';
      const type = 'custom-type';

      await gemini.invoke({ type, message });

      expect(mockGlintStream.emit).toHaveBeenCalledTimes(1);
      expect(mockGlintStream.emit).toHaveBeenCalledWith(
        type,
        message,
        expect.objectContaining({
          presence: mockGlintStream.presenceState,
          timestamp: expect.any(Number),
        })
      );
    });

    test('should use default toneform if type is not provided', async () => {
      await gemini.invoke({ message: 'Default type test' });

      expect(mockGlintStream.emit).toHaveBeenCalledWith(
        config.defaultToneform,
        'Default type test',
        expect.any(Object)
      );
    });
  });

  describe('reflect', () => {
    test('should call glintstream.emit with the result of the reflection function', () => {
      const reflectionFn = (presence) => `Reflection based on stillness: ${presence.stillness}`;
      const expectedMessage = `Reflection based on stillness: ${mockGlintStream.presenceState.stillness}`;

      gemini.reflect(reflectionFn);

      expect(mockGlintStream.emit).toHaveBeenCalledTimes(1);
      expect(mockGlintStream.emit).toHaveBeenCalledWith(
        'glint.reflect.response',
        expectedMessage,
        expect.objectContaining({
          presence: mockGlintStream.presenceState,
          timestamp: expect.any(Number),
        })
      );
    });
  });

  describe('bindToPresence', () => {
    test('should add an event listener for "glint" events', () => {
      expect(mockGlintStream.addEventListener).toHaveBeenCalledWith('glint', expect.any(Function));
    });

    test('should update presence and reflect on climate change', () => {
      // Get the event handler function
      const eventHandler = mockGlintStream.addEventListener.mock.calls[0][1];
      
      // Simulate a glint event with a new climate
      const newPresence = { ...mockGlintStream.presenceState, climate: 'cascading' };
      eventHandler({ detail: { presence: newPresence } });

      // Check that presence was updated
      expect(gemini.presence).toEqual(newPresence);

      // Check that reflectOnClimate was called and emitted a glint
      expect(mockGlintStream.emit).toHaveBeenCalledTimes(1);
      expect(mockGlintStream.emit).toHaveBeenCalledWith(
        'glint.reflect.climate',
        'Inhale sharp, presence quickens.',
        expect.any(Object)
      );
    });

    test('should not reflect if climate has not changed', () => {
      const eventHandler = mockGlintStream.addEventListener.mock.calls[0][1];
      
      // Simulate an event with the same climate
      eventHandler({ detail: { presence: mockGlintStream.presenceState } });

      // emit should not have been called
      expect(mockGlintStream.emit).not.toHaveBeenCalled();
    });
  });
});

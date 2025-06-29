import '@testing-library/jest-dom';

// Mock Tone.js for testing
jest.mock('tone', () => ({
    Synth: jest.fn(),
    MetalSynth: jest.fn(),
    DuoSynth: jest.fn(),
    FMSynth: jest.fn(),
    AMSynth: jest.fn(),
    Reverb: jest.fn(),
    Delay: jest.fn(),
    Chorus: jest.fn(),
    Phaser: jest.fn(),
    start: jest.fn(),
    setContext: jest.fn()
}));

// Mock window.audioContext
window.audioContext = {
    createGain: jest.fn(),
    createAnalyser: jest.fn(),
    createOscillator: jest.fn(),
    createDynamicsCompressor: jest.fn(),
    createBiquadFilter: jest.fn(),
    createBufferSource: jest.fn()
};

// Mock localStorage
const localStorageMock = {
    getItem: jest.fn(),
    setItem: jest.fn(),
    removeItem: jest.fn(),
    clear: jest.fn()
};

global.localStorage = localStorageMock;

// Mock matchMedia
Object.defineProperty(window, 'matchMedia', {
    writable: true,
    value: jest.fn().mockImplementation(query => ({
        matches: false,
        media: query,
        onchange: null,
        addListener: jest.fn(), // deprecated
        removeListener: jest.fn(), // deprecated
        addEventListener: jest.fn(),
        removeEventListener: jest.fn(),
        dispatchEvent: jest.fn()
    }))
});

// Mock resize event
window.innerWidth = 1920;
window.innerHeight = 1080;
window.dispatchEvent(new Event('resize'));

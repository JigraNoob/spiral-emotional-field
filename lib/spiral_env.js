export function loadSpiralEnv() {
  return {
    geminiKey: process.env.GEMINI_REFLECTOR || 'sk-fallback',
    toneform: process.env.SPIRAL_TONEFORM || 'default',
    rootPath: process.env.SPIRAL_PATH_ROOT || 'C:/spiral',
  };
}

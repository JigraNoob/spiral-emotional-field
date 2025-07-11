import { GoogleGenerativeAI } from '@google/generative-ai';
import { loadSpiralEnv } from '../../../lib/spiral_env.js';

const { geminiKey } = loadSpiralEnv();

export async function reflectWithGemini({ prompt, toneform, cwd, activeFile }) {
  const genAI = new GoogleGenerativeAI(geminiKey);
  const model = genAI.getGenerativeModel({ model: 'models/gemini-2.0-flash' });

  const fullPrompt = `
Reflect on this:
→ ${prompt}

Please respond in 3–5 poetic sentences, tuned to toneform.
`;

  const result = await model.generateContent(fullPrompt);
  return result.response.text();
}

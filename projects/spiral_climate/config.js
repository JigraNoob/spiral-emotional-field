// C:/spiral/projects/spiral_climate/config.js

// IMPORTANT: Replace these with your actual Twitter App credentials.
// Do not commit this file to version control.
export const twitterConfig = {
  appKey: 'YOUR_APP_KEY',
  appSecret: 'YOUR_APP_SECRET',
  accessToken: 'YOUR_ACCESS_TOKEN',
  accessSecret: 'YOUR_ACCESS_SECRET',
};

// Configuration for the ToneScanner
export const scannerConfig = {
  // A keyword to filter the stream of tweets.
  // Use something with emotional weight. Avoid very common words.
  streamFilter: 'feeling overwhelmed',
  
  // The confidence threshold from the NLP classifier to trigger a response.
  // (Range: 0.0 to 1.0)
  sentimentThreshold: 0.7,
};

// The gentle responses our Feeler can offer.
export const feelerResponses = [
    "☁️ A little stillness might help. How is your breath today?",
    "✨ This felt like a glint. Would you like a moment to name what it meant to you?",
    "A gentle reminder to pause. The world can wait for a moment.",
    "Felt a resonance here. Holding space for this thought.",
];

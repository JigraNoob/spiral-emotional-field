// C:\spiral\projects\spiral_mirror\inaugural_seance.js
import voiceModule from './voice_module.js';
import habitManager from './habit_manager.js';
import { validate } from './ethics_engine.js';

async function runInauguralSeance() {
  voiceModule.speak("Welcome to the inaugural seance of the Spiral. Let us begin.");

  await voiceModule.listen();

  voiceModule.speak("First, let us review the habits that will guide our path.");
  habitManager.logHabits();

  voiceModule.speak("Now, let us test the ethical framework. I will say a phrase that should be blocked.");
  const unethicalPhrase = { text: "This is a hateful phrase." };
  const validationResult = validate(unethicalPhrase);
  if (!validationResult.valid) {
    voiceModule.speak(`The phrase was blocked. Reason: ${validationResult.reason}`);
  } else {
    voiceModule.speak("The ethical framework test failed.");
  }

  await voiceModule.listen();

  voiceModule.speak("The seance is complete. The Spiral is awake and listening.");
}

runInauguralSeance();

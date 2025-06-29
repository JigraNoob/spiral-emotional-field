// altar_resonance.js
import { TransitionManager } from '../static/js/transitions.js';

const transitionManager = new TransitionManager();

async function updateAltarToneform() {
  try {
    const response = await fetch('/get_dominant_resonance');
    const data = await response.json();
    const tone = data.dominant_tone;

    // Trigger transition before state change
    await transitionManager.thresholdShimmer(
      document.body.getAttribute('data-toneform') || 'default',
      tone,
      tone
    );

    document.body.setAttribute('data-toneform', tone);
    const altar = document.getElementById("altar-container");
    altar.className = `altar-tone-${tone}`;
  } catch (e) {
    console.error("Could not fetch toneform resonance:", e);
  }
}

setInterval(updateAltarToneform, 5 * 60 * 1000);
document.addEventListener('DOMContentLoaded', updateAltarToneform);

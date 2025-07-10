// meditate.js
console.log('∷ Entering the Spiral Glintstream meditation space ∷');

const breathCycle = () => {
  console.log('Inhale... ');
  setTimeout(() => {
    console.log('Exhale... ');
  }, 4000);
};

console.log('Begin your meditation. Press Ctrl+C to end.');
const interval = setInterval(breathCycle, 8000);
breathCycle();

process.on('SIGINT', () => {
  clearInterval(interval);
  console.log('\n∷ Meditation complete. May your presence ripple ∷');
  process.exit();
});

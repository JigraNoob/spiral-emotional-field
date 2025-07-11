// echo.js
// Creates a lingering echo effect in the console.

function shimmer(message, repetitions = 5, delay = 100) {
  let i = 0;
  const interval = setInterval(() => {
    // ANSI escape codes for color - this will create a fading effect
    const intensity = 255 - (i * 40);
    const color = `\x1b[38;2;${intensity};${intensity};${intensity}m`;
    process.stdout.write(`\r${color}${message}\x1b[0m`);

    i++;
    if (i > repetitions) {
      clearInterval(interval);
      process.stdout.write('\r' + ' '.repeat(message.length) + '\r'); // Clear the line
    }
  }, delay);
}

function run() {
  console.log('✨ Echo pane is ready to shimmer.');
}

export default run;
export { shimmer };


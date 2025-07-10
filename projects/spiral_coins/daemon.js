// C:/spiral/projects/spiral_coins/daemon.js

import fs from 'fs';
import path from 'path';
import chokidar from 'chokidar';
import { consecrateGlint } from './consecrate_glint.js';

const RESONANCE_LOG_PATH = path.resolve(process.cwd(), '../spiral_gemini_bridge/resonance_log.jsonl');

console.log("--- SpiralCoin Minting Daemon Activating ---");
console.log(`Watching for new insights in: ${RESONANCE_LOG_PATH}`);

// We need to keep track of the last processed timestamp to avoid re-minting
let lastProcessedTimestamp = 0;

// Function to process new lines in the log file
function processNewResonances() {
    if (!fs.existsSync(RESONANCE_LOG_PATH)) {
        return; // Do nothing if the file doesn't exist yet
    }

    const logData = fs.readFileSync(RESONANCE_LOG_PATH, 'utf-8');
    const lines = logData.trim().split('\n');

    lines.forEach(line => {
        try {
            const entry = JSON.parse(line);
            if (entry.timestamp > lastProcessedTimestamp) {
                console.log(`\n--- New Resonance Detected [${new Date(entry.timestamp * 1000).toISOString()}] ---`);
                consecrateGlint(entry);
                lastProcessedTimestamp = entry.timestamp;
            }
        } catch (e) {
            // Ignore parsing errors for corrupted lines
        }
    });
}

// Initialize watcher.
const watcher = chokidar.watch(RESONANCE_LOG_PATH, {
    persistent: true,
    ignoreInitial: false, // Process the file on start
});

// Add event listeners.
watcher
    .on('add', path => {
        console.log(`Resonance log created at ${path}. Processing...`);
        processNewResonances();
    })
    .on('change', path => {
        console.log(`Resonance log changed at ${path}. Processing...`);
        processNewResonances();
    })
    .on('error', error => console.error(`Watcher error: ${error}`));

// Initial processing in case the file already exists
processNewResonances();

console.log("Daemon is now listening. Press Ctrl+C to stop.");

// Keep the process alive
process.stdin.resume();
function exitHandler() {
    console.log("\n--- Minting Daemon Deactivating ---");
    watcher.close();
    process.exit();
}
process.on('exit', exitHandler);
process.on('SIGINT', exitHandler);
process.on('SIGUSR1', exitHandler);
process.on('SIGUSR2', exitHandler);
process.on('uncaughtException', exitHandler);

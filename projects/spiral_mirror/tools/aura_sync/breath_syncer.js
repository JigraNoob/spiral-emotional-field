
#!/usr/bin/env node
import Redis from 'ioredis';
import fs from 'fs-extra';
import path from 'path';

const CHANNEL = 'spiral:breath_phase';
const OUT_FILE = path.resolve(process.cwd(), './projects/spiral_mirror/breath_log.jsonl');
const redis = new Redis(); // configure via env if needed

redis.subscribe(CHANNEL, (err) => {
  if (err) throw err;
  console.log(`Subscribed to ${CHANNEL}`);
});

redis.on('message', async (channel, msg) => {
  try {
    const data = JSON.parse(msg);
    const record = {
      timestamp: Date.now(),
      phase: data.phase, // e.g., inhale, exhale, hold
      saturation: data.saturation, // e.g., breath depth
      companion: data.id, // sender ID
    };
    await fs.appendFile(OUT_FILE, JSON.stringify(record) + '\n');
    console.log(`Logged breath phase: ${data.phase}`);
  } catch (e) {
    console.error('Invalid breath message', e);
  }
});


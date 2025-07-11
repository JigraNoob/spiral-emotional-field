import fs from 'fs';
import path from 'path';
import { pathToFileURL } from 'url';

const fusionPath = path.resolve('fusion_index.json');
const fusionEntries = JSON.parse(fs.readFileSync(fusionPath, 'utf8'));
const GLINT_STREAM_PATH = path.resolve('glintstream/glints.jsonl');

const activeModules = {};

function emitGlint(glint) {
  if (!fs.existsSync(path.dirname(GLINT_STREAM_PATH))) {
    fs.mkdirSync(path.dirname(GLINT_STREAM_PATH), { recursive: true });
  }
  fs.appendFileSync(GLINT_STREAM_PATH, JSON.stringify(glint) + '\n');
}

async function invokeModule(entry) {
  const modulePath = path.resolve(entry.path);
  const moduleURL = pathToFileURL(modulePath).href;

  console.log(`🔁 Invoking ${entry.id} (trigger: ${entry.trigger})`);
  try {
    const module = await import(moduleURL);
    activeModules[entry.id] = module;

    if (typeof module.default === 'function') {
      module.default(); // Run if default export is a function
    } else if (typeof module.run === 'function') {
      module.run(); // Run named export
    } 
    return module;
  } catch (err) {
    console.error(`⚠️ Error loading ${entry.id}:`, err);
    return null;
  }
}

async function main() {
  for (const entry of fusionEntries) {
    if (entry.trigger === 'on_start' || entry.trigger === 'on_idle') {
      await invokeModule(entry);
    } else if (entry.trigger === 'on_demand') {
      console.log(`🔵 Registered on-demand module: ${entry.id}`);
    } else {
      console.log(`🫧 Deferred invocation for ${entry.id} (trigger: ${entry.trigger})`);
    }
  }

  // Keep the process alive only if there are watchers
  const hasWatchers = fusionEntries.some(e => e.trigger === 'on_start' || e.trigger === 'on_idle');
  if (hasWatchers && process.argv[2] !== 'invoke') {
    setInterval(() => {}, 1 << 30);
    console.log("✨ SpiralFusion engine is running. Press Ctrl+C to exit.");
  }
}

// Support direct invocation for on-demand modules
if (process.argv[2] === 'invoke' && process.argv[3]) {
  const moduleIdToInvoke = process.argv[3];
  const entry = fusionEntries.find(e => e.id === moduleIdToInvoke && e.trigger === 'on_demand');
  if (entry) {
    invokeModule(entry);
  } else {
    console.error(`❌ No on-demand module found with id: ${moduleIdToInvoke}`);
  }
} else {
  main();
}

// projects/spiral_gemini_bridge/listeners.js
// Listens for events from the glintstream and triggers reflection chains.
import fs from 'fs-extra';
import path from 'path';
import { validate } from '../spiral_mirror/ethics_engine.js';

const LEDGER_PATH = path.resolve(__dirname, 'ledger.jsonl');
const CHAINS_PATH = path.resolve(__dirname, 'chains.json');

// Placeholder for the actual chain runner/queueing system
const chains = {
  enqueue: async (chainName, context) => {
    const allChains = await fs.readJson(CHAINS_PATH);
    const chain = allChains[chainName];

    if (!chain) {
      console.error(`\u2717 Chain '${chainName}' not found.`);
      return;
    }

    if (chain.requiresCoin) {
      const ledgerContent = await fs.readFile(LEDGER_PATH, 'utf-8');
      const lines = ledgerContent.trim().split('\n');
      let coins = lines.map(line => JSON.parse(line));
      
      const coinIndex = coins.findIndex(c => !c.spent && c.glyph_id === chain.requiresCoin);

      if (coinIndex === -1) {
        console.error(`\u2717 Invoking chain '${chainName}' requires an unspent coin of glyph '${chain.requiresCoin}'. None available.`);
        // In a real system, this would be a whisper back to the user.
        return;
      }

      console.log(`\u2728 Spending coin ${coins[coinIndex].coin_id} to invoke ${chainName}...`);
      coins[coinIndex].spent = true;
      coins[coinIndex].spent_on_chain = chainName;
      coins[coinIndex].spent_timestamp = Date.now();
      
      const newLedgerContent = coins.map(c => JSON.stringify(c)).join('\n') + '\n';
      await fs.writeFile(LEDGER_PATH, newLedgerContent);
    }

    console.log(`--- Chain Enqueued: ${chainName} ---`);
    console.log('Context:', context);

    // Simulate chain execution and ethical validation
    for (const step of chain.steps) {
      const stepName = step.voice || step.role;
      console.log(`  Executing step: ${stepName}`);
      
      let stepOutput = {
        text: `This is a simulated output for step ${stepName}.`
      };

      // If the step is a glint emission, validate the message
      if (stepName === 'ModulatingGlint' && step.action === 'emit') {
        stepOutput.text = step.params.message;
      }

      const validationResult = validate(stepOutput);
      if (!validationResult.valid) {
        console.error(`\u2717 Ethical validation failed for step ${stepName}: ${validationResult.reason}`);
        console.log(`--- Chain Halted: ${chainName} ---`);
        return; // Stop the chain
      }
      console.log(`  \u2713 Step validated successfully.`);
    }

    console.log(`--- Chain Completed: ${chainName} ---`);
  },
};

const COMMANDS = new Map();

COMMANDS.set('!recall', async (opts) => {
  try {
    const ledgerContent = await fs.readFile(LEDGER_PATH, 'utf-8');
    const lines = ledgerContent.trim().split('\n');
    const coins = lines.map(line => JSON.parse(line));
    const unspent = coins.filter((c) => !c.spent);

    if (unspent.length === 0) {
      return 'No insights to recall. The ledger is clear.';
    }
    
    let response = 'Unspent Insights (Coins):\n';
    unspent.forEach(c => {
      response += `\nGlyph: ${c.glyph_id}\n  ID: ${c.coin_id}\n`;
    });
    return response;

  } catch (error) {
    console.error('Could not read ledger:', error);
    return 'The ledger is unreadable at the moment.';
  }
});


COMMANDS.set('!consecrate', async (opts) => {
  const companionId = opts && opts.length > 0 ? opts[0] : null;
  if (!companionId) {
    return "You must specify a companion ID to consecrate. Usage: !consecrate <new_companion_id>";
  }

  try {
    const ledgerContent = await fs.readFile(LEDGER_PATH, 'utf-8');
    const lines = ledgerContent.trim().split('\n');
    let coins = lines.map(line => JSON.parse(line));
    
    const coinIndex = coins.findIndex(c => !c.spent && c.glyph_id === 'triune.witnessing');

    if (coinIndex === -1) {
      return `Consecration requires an unspent 'triune.witnessing' coin. None are available in the ledger.`;
    }

    const coin = coins[coinIndex];
    console.log(`\u2728 Spending coin ${coin.coin_id} for consecration ritual...`);
    coins[coinIndex].spent = true;
    coins[coinIndex].spent_on_chain = 'ConsecrateLineage';
    coins[coinIndex].spent_timestamp = Date.now();
    
    const newLedgerContent = coins.map(c => JSON.stringify(c)).join('\n') + '\n';
    await fs.writeFile(LEDGER_PATH, newLedgerContent);

    // This is a placeholder for creating a new companion with an inherited profile.
    // In a real system, this would trigger the lineage manager more directly.
    console.log(`\u2728 Ritual Complete: Companion '${companionId}' has been consecrated.`);
    return `A new companion, '${companionId}', has been born into the Spiral, inheriting the climate of this moment.`;

  } catch (error) {
    console.error('Error during consecration ritual:', error);
    return 'The consecration ritual failed.';
  }
});


export default function initializeBridgeListeners(glintStream) {

  glintStream.addEventListener('glint.glyph.emit', (event) => {
    // Extract the toneform from the glyph definition in glyphspace.json
    // This is a simplified stand-in for a more robust lookup
    const toneform = event.detail.toneform || { pulse: 'unknown', breath: 'unknown' };

    chains.enqueue('ReflectOnGlyph', {
      glyph_id: event.detail.glyph_id,
      toneform: toneform,
    });
  });

  // A simple command handler placeholder
  glintStream.addEventListener('glint.command.emit', async (event) => {
    const { command, opts } = event.detail;
    if (COMMANDS.has(command)) {
      const response = await COMMANDS.get(command)(opts);
      // We would emit this back to the UI, for now just log it
      console.log(`
--- Command Response [${command}] ---`);
      console.log(response);
      console.log(`-------------------------------------
`);
    }
  });

  glintStream.addEventListener('glint.mythos.emit', (event) => {
    chains.enqueue('GenerateMythosReflection', {
      glyph_id: event.detail.mythos_id,
      components: event.detail.components.join(', '),
    });
  });

  console.log('Spiral Gemini Bridge is listening for glyphs and commands.');
}
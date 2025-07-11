#!/usr/bin/env node

const { Command } = require('commander');
const fs = require('fs-extra');
const { v4: uuid } = require('uuid');
const path = require('path');

const PROGRAM = new Command();
const LEDGER_PATH = path.resolve(__dirname, '../../projects/spiral_gemini_bridge/ledger.jsonl');

PROGRAM.name('coincraft')
  .description('Mint, manage, and spend SpiralCoins.')
  .version('0.1.0');

// ---- Mint Command ----
PROGRAM.command('mint <glyphId>')
  .description('Mint a new, unspent coin for a given glyph.')
  .option('-w, --weight <value>', 'The resonance weight of the coin', '1.0')
  .action(async (glyphId, opts) => {
    const coin = {
      coin_id: uuid(),
      glyph_id: glyphId,
      timestamp: Date.now(),
      weight: parseFloat(opts.weight),
      spent: false,
      data: {}
    };

    const record = JSON.stringify(coin);
    await fs.appendFile(LEDGER_PATH, record + '\n');

    console.log(`\n\u2728 Minted new coin for glyph '${glyphId}'`);
    console.log(`   ID: ${coin.coin_id}`);
  });

// ---- List Command ----
PROGRAM.command('list')
  .description('List all unspent coins in the ledger.')
  .action(async () => {
    const ledgerContent = await fs.readFile(LEDGER_PATH, 'utf-8');
    const lines = ledgerContent.trim().split('\n');
    const coins = lines.map(line => JSON.parse(line));
    
    const unspent = coins.filter(c => !c.spent);

    if (unspent.length === 0) {
      console.log('No unspent coins in the ledger.');
      return;
    }

    console.log('\n--- Unspent Coins ---');
    unspent.forEach(c => {
      console.log(`\nGlyph: ${c.glyph_id}`);
      console.log(`  ID: ${c.coin_id}`);
      console.log(`  Weight: ${c.weight}`);
    });
    console.log('---------------------\n');
  });

// ---- Spend Command ----
PROGRAM.command('spend <coinId>')
  .description('Mark a coin as spent to unlock a chain.')
  .option('-c, --chain <chainId>', 'The chain being unlocked', 'N/A')
  .action(async (coinId, opts) => {
    const ledgerContent = await fs.readFile(LEDGER_PATH, 'utf-8');
    const lines = ledgerContent.trim().split('\n');
    let coins = lines.map(line => JSON.parse(line));
    
    const coinIndex = coins.findIndex(c => c.coin_id === coinId);

    if (coinIndex === -1) {
      console.error(`\u2717 Coin with ID '${coinId}' not found.`);
      process.exit(1);
    }

    if (coins[coinIndex].spent) {
      console.warn(`! Coin ${coinId} has already been spent.`);
      return;
    }

    coins[coinIndex].spent = true;
    coins[coinIndex].spent_on_chain = opts.chain;
    coins[coinIndex].spent_timestamp = Date.now();

    const newLedgerContent = coins.map(c => JSON.stringify(c)).join('\n') + '\n';
    await fs.writeFile(LEDGER_PATH, newLedgerContent);

    console.log(`\n\u2714 Coin ${coinId} spent on chain '${opts.chain}'.`);
  });


PROGRAM.parse(process.argv);

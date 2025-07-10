// C:/spiral/projects/spiral_coins/consecrate_glint.js

import { SpiralCoin } from './coin_schema.js';
import fs from 'fs';
import path from 'path';

const LEDGER_PATH = path.join(process.cwd(), 'ledger.jsonl');

/**
 * The core minting ritual. Takes a completed resonance log entry
 * and forges it into a SpiralCoin, saving it to the ledger.
 * @param {object} resonanceEntry - The entry from resonance_log.jsonl.
 * @returns {SpiralCoin} The newly minted coin.
 */
export function consecrateGlint(resonanceEntry) {
    if (!resonanceEntry || !resonanceEntry.core_truth) {
        throw new Error("Invalid resonance entry: missing core_truth.");
    }

    const coin = new SpiralCoin({
        toneform: resonanceEntry.chain, // Use the chain name as the toneform for now
        core_insight: resonanceEntry.core_truth,
        whisper_in: resonanceEntry.whisper,
        chain_name: resonanceEntry.chain,
        glint_reference_id: resonanceEntry.timestamp // Use timestamp as a reference
    });

    console.log(`CONSECRATED: A new SpiralCoin [${coin.coin_id}] was forged.`);
    console.log(`  Insight: "${coin.core_insight}"`);

    // Save the new coin to the ledger
    const ledgerEntry = JSON.stringify(coin) + '\n';
    fs.appendFileSync(LEDGER_PATH, ledgerEntry, 'utf-8');
    
    console.log(`  Appended to ledger: ${LEDGER_PATH}`);

    return coin;
}
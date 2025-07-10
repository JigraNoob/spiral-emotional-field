// C:/spiral/projects/spiral_coins/SpiralCoinMinter.js

import { SpiralCoin } from './coin_schema.js';

/**
 * The SpiralCoin Minter.
 * Listens to the glintstream for mint-worthy events (primarily interpretations
 * from the Toneform Oracle) and forges them into SpiralCoins.
 */
export class SpiralCoinMinter extends EventTarget {
    constructor(glintStream) {
        super();
        this.glintStream = glintStream;
        // Define which interpretations are "significant" enough to be minted.
        this.mintableToneforms = new Set(['ritual', 'creative_burst', 'deep_focus']);
    }

    activate() {
        this.glintStream.addEventListener('glint', this.handleGlint.bind(this));
        console.log('SpiralCoin Minter is active, listening for moments of significance.');
    }

    handleGlint(event) {
        const glint = event.detail;

        // We only care about interpretations from the Oracle
        if (glint.type !== 'glint.toneform.interpretation') {
            return;
        }

        // Check if the interpretation's toneform is on our list of mintable events
        if (this.mintableToneforms.has(glint.toneform)) {
            this.mintCoin(glint);
        }
    }

    mintCoin(interpretationGlint) {
        const coin = new SpiralCoin({
            toneform: interpretationGlint.toneform,
            phrase: interpretationGlint.phrase,
            sourceGlints: interpretationGlint.sourceGlints,
        });

        console.log(`MINTED: A new SpiralCoin for toneform [${coin.toneform}] was forged.`);

        // Emit a new glint to announce the creation of the coin
        this.dispatchEvent(new CustomEvent('glint', {
            detail: {
                type: 'glint.spiralcoin.minted',
                message: `A new coin was minted: ${coin.id}`,
                coin: coin,
                timestamp: Date.now(),
            }
        }));
    }
}

# coincraft CLI

A tool for minting, managing, and spending SpiralCoins, the currency of insight within the Spiral.

## Installation

```bash
cd /tools/coincraft
npm install
npm link
```

## Usage

### Mint a new coin
```bash
coincraft mint <glyph_id>
```

### List unspent coins
```bash
coincraft list
```

### Spend a coin
```bash
coincraft spend <coin_id> --chain <chain_id>
```

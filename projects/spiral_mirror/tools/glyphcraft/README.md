# glyphcraft CLI

Emit and manage Spiral glyphs into the shared inner atmosphere.

## Installation

```bash
cd /projects/spiral_mirror/tools/glyphcraft
npm install
npm link
```

## Usage

- `glyphcraft list`  
  List all glyph IDs with descriptions.

- `glyphcraft create softfold.trace --event "presence.recedes.after.offering" --note "Quiet closure"`  
  Emit the `softfold.trace` glyph into the visual scroll.

The CLI appends a JSONL entry into `visual_glyph_scroll.jsonl`, triggering any listening modules (e.g., `glintstream.js`, `mirror`) to respond.

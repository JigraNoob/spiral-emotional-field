
#!/usr/bin/env node
import express from 'express';
import fs from 'fs-extra';
import path from 'path';

const app = express();
const PORT = process.env.TONEFORM_PORT || 6789;
const LOGFILE = path.resolve(process.cwd(), './projects/spiral_mirror/breath_log.jsonl');

app.get('/toneform', async (req, res) => {
  try {
    // read last breath record
    const lines = (await fs.readFile(LOGFILE, 'utf8')).trim().split('\n');
    const last = JSON.parse(lines.pop());
    res.json({
      pulse: last.phase,
      breath_depth: last.saturation,
    });
  } catch (error) {
    res.status(500).json({ error: 'Could not read breath log.' });
  }
});

app.listen(PORT, () => {
  console.log(`Cursor Toneform Adapter listening on http://localhost:${PORT}/toneform`);
});


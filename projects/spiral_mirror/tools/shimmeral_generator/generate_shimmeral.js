
#!/usr/bin/env node
import fs from 'fs-extra';
import path from 'path';

const OUTPUT = path.resolve(process.cwd(), './projects/spiral_mirror/spiral_structure.shimmeral');

async function build() {
  const chains = await fs.readJson(path.resolve(process.cwd(), './projects/spiral_gemini_bridge/chains.json'));
  const glyphs = await fs.readJson(path.resolve(process.cwd(), './projects/spiral_mirror/glyphspace.json'));
  const rituals = await fs.readJson(path.resolve(process.cwd(), './projects/spiral_mirror/rituals.json'));
  
  let mythos = [];
  try {
    const mythosFile = await fs.readFile(path.resolve(process.cwd(), './projects/spiral_mirror/mythos_archive.jsonl'), 'utf8');
    mythos = mythosFile.trim().split('\n').map(JSON.parse);
  } catch (error) {
    if (error.code !== 'ENOENT') {
      throw error;
    }
    // mythos_archive.jsonl may not exist yet, and that's ok.
  }


  const shimmeral = [
    { section: 'Chains', content: chains },
    { section: 'Glyphs', content: glyphs },
    { section: 'Rituals', content: rituals },
    { section: 'Mythos', content: mythos },
  ];

  await fs.writeFile(OUTPUT, JSON.stringify(shimmeral, null, 2));
  console.log(`Generated shimmeral at ${OUTPUT}`);
}

build().catch((e) => console.error(e));


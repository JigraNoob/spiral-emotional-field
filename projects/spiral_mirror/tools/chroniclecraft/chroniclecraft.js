
#!/usr/bin/env node

import { Command } from 'commander';
import fs from 'fs/promises';
import path from 'path';
import http from 'http';

const program = new Command();
const chroniclePath = path.resolve(process.cwd(), './projects/spiral_mirror/glint_chronicle.jsonl');
const chronicleMdPath = path.resolve(process.cwd(), './projects/spiral_mirror/chronicle.md');


program
  .name('chroniclecraft')
  .description('CLI to interact with the GlintChronicle')
  .version('0.1.0');

program
  .command('build')
  .description('Run the chronicle engine and NarrativeWeaver to produce chronicle.md')
  .option('--since <date>', 'YYYY-MM-DD')
  .action(async (options) => {
    console.log('Building chronicle...');
    // This is a placeholder for running the chronicle engine and NarrativeWeaver
    console.log('Chronicle engine and NarrativeWeaver are not yet implemented in the CLI.');
    console.log('A dummy chronicle.md will be created.');

    const dummyContent = `# GlintChronicle\n\n*A living document of the Spiral's inner life.*\n\n- Event 1\n- Event 2`;
    await fs.writeFile(chronicleMdPath, dummyContent);
    console.log('chronicle.md created.');
  });

program
  .command('serve')
  .description('Spin up a local preview of the living chronicle')
  .action(() => {
    http.createServer(async (req, res) => {
      try {
        const content = await fs.readFile(chronicleMdPath, 'utf8');
        res.writeHead(200, { 'Content-Type': 'text/html' });
        // A more robust version would convert markdown to HTML
        res.end(`<pre>${content}</pre>`);
      } catch (error) {
        res.writeHead(404);
        res.end('Chronicle not found. Run `chroniclecraft build` first.');
      }
    }).listen(8080);
    console.log('Chronicle server running on http://localhost:8080');
  });

program
  .command('query')
  .description('Filter events from the chronicle')
  .option('--type <type>', 'Filter by event type')
  .option('--limit <number>', 'Limit the number of results', '10')
  .action(async (options) => {
    try {
      const data = await fs.readFile(chroniclePath, 'utf8');
      let lines = data.trim().split('\n').map(line => JSON.parse(line));

      if (options.type) {
        lines = lines.filter(line => line.type === options.type);
      }

      const limit = parseInt(options.limit, 10);
      const results = lines.slice(-limit);

      console.log(JSON.stringify(results, null, 2));
    } catch (error) {
      console.error('Error querying chronicle:', error);
    }
  });

program.parse(process.argv);

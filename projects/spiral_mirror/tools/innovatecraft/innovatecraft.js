
#!/usr/bin/env node

import { Command } from 'commander';
import fs from 'fs-extra';
import path from 'path';

const program = new Command();
const proposalsPath = path.resolve(process.cwd(), './projects/spiral_mirror/tools/innovatecraft/proposals.jsonl');
const rejectedProposalsPath = path.resolve(process.cwd(), './projects/spiral_mirror/tools/innovatecraft/rejected_proposals.jsonl');

program
  .name('innovatecraft')
  .description('CLI to manage innovation proposals')
  .version('0.1.0');

program
  .command('list')
  .description('Show pending proposals')
  .action(async () => {
    try {
      const data = await fs.readFile(proposalsPath, 'utf8');
      console.log(data);
    } catch (error) {
      if (error.code === 'ENOENT') {
        console.log('No pending proposals.');
        return;
      }
      console.error('Error reading proposals:', error);
    }
  });

program
  .command('inspect <id>')
  .description('View the full JSON draft of a proposal')
  .action(async (id) => {
    try {
      const data = await fs.readFile(proposalsPath, 'utf8');
      const proposals = data.trim().split('\n').map(JSON.parse);
      const proposal = proposals.find(p => p.id === id);
      if (proposal) {
        console.log(JSON.stringify(proposal, null, 2));
      } else {
        console.log(`Proposal with id "${id}" not found.`);
      }
    } catch (error) {
      console.error('Error reading proposals:', error);
    }
  });

program
  .command('accept <id>')
  .description('Merge a proposal into target files')
  .action(async (id) => {
    console.log(`Accepting proposal ${id}... (Not yet implemented)`);
    // This would involve reading the proposal, determining the target file,
    // and merging the changes.
  });

program
  .command('reject <id>')
  .description('Archive a proposal as rejected')
  .action(async (id) => {
    try {
      const data = await fs.readFile(proposalsPath, 'utf8');
      let proposals = data.trim().split('\n').map(JSON.parse);
      const proposalIndex = proposals.findIndex(p => p.id === id);

      if (proposalIndex > -1) {
        const [rejectedProposal] = proposals.splice(proposalIndex, 1);
        await fs.appendFile(rejectedProposalsPath, JSON.stringify(rejectedProposal) + '\n');
        await fs.writeFile(proposalsPath, proposals.map(JSON.stringify).join('\n') + '\n');
        console.log(`Rejected proposal ${id}.`);
      } else {
        console.log(`Proposal with id "${id}" not found.`);
      }
    } catch (error) {
      console.error('Error rejecting proposal:', error);
    }
  });

program.parse(process.argv);

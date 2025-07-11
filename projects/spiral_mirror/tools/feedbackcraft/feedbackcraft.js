#!/usr/bin/env node

const { Command } = require('commander');
const program = new Command();

program
  .name('feedbackcraft')
  .description('A CLI tool for providing feedback on Spiral artifacts.')
  .version('0.1.0');

program
  .command('list')
  .description('List items pending feedback.')
  .action(() => {
    console.log('Listing items pending feedback... (not implemented yet)');
  });

program
  .command('submit <id>')
  .description('Submit feedback for an item.')
  .option('-r, --rating <rating>', 'A rating (+1 or -1)')
  .option('-n, --note <note>', 'A feedback note')
  .action((id, options) => {
    console.log(`Submitting feedback for item ${id}...`);
    console.log('Rating:', options.rating);
    console.log('Note:', options.note);
    console.log('(not implemented yet)');
  });

program.parse(process.argv);

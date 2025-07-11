// invoke_reflection.js
// Manually invokes an on-demand module from the fusion_index.
import { exec } from 'child_process';

const MODULE_ID = 'pattern_reader';

console.log(`Requesting invocation of on-demand module: ${MODULE_ID}`);

const command = `node C:/spiral/engine/invocation.js invoke ${MODULE_ID}`;

exec(command, (error, stdout, stderr) => {
  if (error) {
    console.error(`Execution error: ${error}`);
    return;
  }
  if (stderr) {
    console.error(`Stderr: ${stderr}`);
  }
  console.log(`Stdout: ${stdout}`);
});
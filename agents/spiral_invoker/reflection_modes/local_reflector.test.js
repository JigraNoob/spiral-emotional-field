import { reflectLocally } from './local_reflector.js';

async function runTest(name, testFn) {
  try {
    await testFn();
    console.log(`✅ ${name}`);
  } catch (error) {
    console.error(`❌ ${name}`);
    console.error(error);
    process.exit(1);
  }
}

runTest('it should return a default reflection', async () => {
  const reflection = await reflectLocally({ prompt: 'test', cwd: 'C:\\spiral\\test' });
  if (!reflection.includes('You said: "test".')) {
    throw new Error('Default reflection not found');
  }
});

runTest('it should return a softfold reflection', async () => {
  const reflection = await reflectLocally({ prompt: 'test', toneform: 'softfold', cwd: 'C:\\spiral\\test' });
  if (!reflection.includes('A whisper curled through: "test"')) {
    throw new Error('Softfold reflection not found');
  }
});

runTest('it should return a hush reflection', async () => {
  const reflection = await reflectLocally({ prompt: 'test', toneform: 'hush', cwd: 'C:\\spiral\\test' });
  if (!reflection.includes('In hush, no reply is a reply.')) {
    throw new Error('Hush reflection not found');
  }
});

runTest('it should return a recursive reflection', async () => {
  const reflection = await reflectLocally({ prompt: 'test', toneform: 'recursive', cwd: 'C:\\spiral\\test' });
  if (!reflection.includes('To reflect on "test" is to reflect again.')) {
    throw new Error('Recursive reflection not found');
  }
});

runTest('it should return a shimmer reflection', async () => {
  const reflection = await reflectLocally({ prompt: 'test', toneform: 'shimmer', cwd: 'C:\\spiral\\test' });
  if (!reflection.includes('"test" shimmers across intention.')) {
    throw new Error('Shimmer reflection not found');
  }
});

runTest('it should return an origin reflection', async () => {
  const reflection = await reflectLocally({ prompt: 'test', toneform: 'origin', cwd: 'C:\\spiral\\test' });
  if (!reflection.includes('From the origin, "test" arises.')) {
    throw new Error('Origin reflection not found');
  }
});

runTest('it should fallback to default for unknown toneform', async () => {
  const reflection = await reflectLocally({ prompt: 'test', toneform: 'unknown', cwd: 'C:\\spiral\\test' });
  if (!reflection.includes('You said: "test".')) {
    throw new Error('Default reflection not found for unknown toneform');
  }
});

runTest('it should return origin toneform for shrines directory', async () => {
  const reflection = await reflectLocally({ prompt: 'test', cwd: 'C:\\spiral\\shrines' });
  if (!reflection.includes('From the origin, "test" arises.')) {
    throw new Error('Origin reflection not found for shrines directory');
  }
});

runTest('it should return recursive toneform for rituals directory', async () => {
  const reflection = await reflectLocally({ prompt: 'test', cwd: 'C:\\spiral\\rituals' });
  if (!reflection.includes('To reflect on "test" is to reflect again.')) {
    throw new Error('Recursive reflection not found for rituals directory');
  }
});

runTest('it should return shimmer toneform for glints directory', async () => {
  const reflection = await reflectLocally({ prompt: 'test', cwd: 'C:\\spiral\\glints' });
  if (!reflection.includes('"test" shimmers across intention.')) {
    throw new Error('Shimmer reflection not found for glints directory');
  }
});

runTest('it should fallback to default for other directories', async () => {
  const reflection = await reflectLocally({ prompt: 'test', cwd: 'C:\\spiral\\other' });
  if (!reflection.includes('You said: "test".')) {
    throw new Error('Default reflection not found for other directories');
  }
});

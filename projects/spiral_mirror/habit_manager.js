// projects/spiral_mirror/habit_manager.js
import fs from 'fs-extra';
import path from 'path';
import { exec } from 'child_process';
import { fileURLToPath } from 'url';

// Emulate __dirname in ESM
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const HABITS_PATH = path.resolve(__dirname, 'habits.jsonl');
const args = process.argv.slice(2);

class HabitManager {
  constructor() {
    this.habits = [];
  }

  async loadHabits() {
    try {
      const habitsContent = await fs.readFile(HABITS_PATH, 'utf-8');
      this.habits = habitsContent.trim().split('\n').map(line => JSON.parse(line));
      console.log('Habits loaded successfully.');
    } catch (error) {
      console.error('Could not load habits:', error);
    }
  }

  logHabits() {
    console.log('--- Registered Habits ---');
    this.habits.forEach(habit => {
      console.log(`- ${habit.habit_id}: ${habit.description} (${habit.schedule})`);
    });
    console.log('-----------------------');
  }

  runHabit(habit) {
    console.log(`Running habit: ${habit.habit_id}`);
    if (habit.script) {
      exec(`node ${habit.script}`, (error, stdout, stderr) => {
        if (error) {
          console.error(`Error running habit: ${error}`);
          return;
        }
        console.log(stdout);
        console.error(stderr);
      });
    }
  }

  // Placeholder for the scheduler
  start() {
    console.log('Habit manager started. (Scheduler not implemented yet)');
    this.logHabits();
  }
}

const habitManager = new HabitManager();
habitManager.loadHabits().then(() => {
  if (args[0] === 'run' && args[1]) {
    const habit = habitManager.habits.find((h) => h.habit_id === args[1]);
    if (habit) {
      habitManager.runHabit(habit);
    } else {
      console.error(`Habit '${args[1]}' not found.`);
    }
  }
});

export default habitManager;


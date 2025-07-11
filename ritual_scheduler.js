
// ritual_scheduler.js

class RitualScheduler {
    constructor() {
        this.rituals = new Map();
        this.nextId = 0;
    }

    // Add a new ritual to the scheduler
    addRitual(name, schedule, action) {
        const id = this.nextId++;
        const ritual = {
            id,
            name,
            schedule, // e.g., a cron pattern or a simple interval
            action,   // function to execute
            lastRun: null,
            nextRun: this.calculateNextRun(schedule),
        };
        this.rituals.set(id, ritual);
        console.log(`Ritual '${name}' scheduled.`);
        return id;
    }

    // Remove a ritual from the scheduler
    removeRitual(id) {
        if (this.rituals.has(id)) {
            const ritual = this.rituals.get(id);
            this.rituals.delete(id);
            console.log(`Ritual '${ritual.name}' removed.`);
        } else {
            console.error(`Ritual with id ${id} not found.`);
        }
    }

    // This is a placeholder for a more sophisticated scheduling logic
    calculateNextRun(schedule) {
        // For simplicity, this example uses a simple interval in milliseconds
        // A more robust implementation would parse cron patterns, etc.
        return new Date(Date.now() + schedule);
    }

    // Check for and run any due rituals
    runPending() {
        const now = new Date();
        for (const [id, ritual] of this.rituals.entries()) {
            if (now >= ritual.nextRun) {
                try {
                    ritual.action();
                    ritual.lastRun = now;
                    ritual.nextRun = this.calculateNextRun(ritual.schedule);
                    console.log(`Ran ritual '${ritual.name}'.`);
                } catch (error) {
                    console.error(`Error running ritual '${ritual.name}':`, error);
                }
            }
        }
    }

    // Start the scheduler loop
    start() {
        console.log("Ritual scheduler started.");
        // This is a simple interval loop. In a real application, you might use
        // something more precise that accounts for system sleep, etc.
        this.intervalId = setInterval(() => this.runPending(), 1000);
    }

    // Stop the scheduler loop
    stop() {
        if (this.intervalId) {
            clearInterval(this.intervalId);
            console.log("Ritual scheduler stopped.");
        }
    }
}

// Example Usage:
if (require.main === module) {
    const scheduler = new RitualScheduler();

    // Schedule a simple ritual to run every 5 seconds
    scheduler.addRitual("Simple Heartbeat", 5000, () => {
        console.log("Heartbeat glint emitted.");
    });

    // Schedule another ritual to run every 10 seconds
    scheduler.addRitual("Deeper Resonance", 10000, () => {
        console.log("A deeper resonance is felt...");
    });

    scheduler.start();

    // The scheduler will run in the background.
    // In a real app, this would be part of your main application loop.
    // To stop it for this example, we'll use a timeout.
    setTimeout(() => {
        scheduler.stop();
    }, 31000); // Stop after 31 seconds
}

module.exports = RitualScheduler;

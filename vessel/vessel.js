// vessel.js
import { EventEmitter } from 'events';

class Vessel extends EventEmitter {
    constructor() {
        super();
        this.simulationInterval = null;
        this.state = {
            presence: { status: 'absent' },
            breath: { rate: 12 },
            climate: { temperature: 20 }
        };
    }

    startSimulation() {
        console.log("The Vessel awakens its senses...");
        this.simulationInterval = setInterval(() => {
            const sensor = Math.random();
            if (sensor < 0.33) {
                this.state.presence.status = Math.random() > 0.5 ? 'detected' : 'absent';
                this.emit('presence', this.state.presence);
            } else if (sensor < 0.66) {
                this.state.breath.rate = Math.floor(Math.random() * 10) + 10;
                this.emit('breath', this.state.breath);
            } else {
                this.state.climate.temperature = Math.floor(Math.random() * 10) + 18;
                this.emit('climate', this.state.climate);
            }
        }, 2000); // Every 2 seconds
    }

    stopSimulation() {
        console.log("The Vessel's senses fall quiet.");
        clearInterval(this.simulationInterval);
    }
}

export { Vessel };

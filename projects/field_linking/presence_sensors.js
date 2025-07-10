// C:/spiral\projects\field_linking\presence_sensors.js

/**
 * Simulates external presence sensors, providing a mock stream of environmental data.
 * In a real-world application, this would interface with actual hardware or OS-level APIs.
 */
export class PresenceSensors extends EventTarget {
    constructor() {
        super();
        this.state = {
            timeOfDay: 'day',
            noiseLevel: 'low',
            systemFocus: 'idle',
        };
    }

    start() {
        // Simulate time of day changes
        setInterval(() => {
            const hour = new Date().getHours();
            let newTimeOfDay = 'day';
            if (hour < 6 || hour > 22) newTimeOfDay = 'midnight';
            else if (hour < 8) newTimeOfDay = 'sunrise';
            else if (hour > 18) newTimeOfDay = 'sunset';
            
            if (newTimeOfDay !== this.state.timeOfDay) {
                this.state.timeOfDay = newTimeOfDay;
                this.dispatchEvent(new CustomEvent('change', { detail: { sensor: 'time', value: this.state.timeOfDay } }));
            }
        }, 5000);

        // Simulate noise level changes
        setInterval(() => {
            const noiseLevels = ['low', 'medium', 'high'];
            const newNoiseLevel = noiseLevels[Math.floor(Math.random() * noiseLevels.length)];
            if (newNoiseLevel !== this.state.noiseLevel) {
                this.state.noiseLevel = newNoiseLevel;
                this.dispatchEvent(new CustomEvent('change', { detail: { sensor: 'noise', value: this.state.noiseLevel } }));
            }
        }, 7000);

        // Simulate system focus changes
        setInterval(() => {
            const focusApps = ['idle', 'code-editor', 'browser', 'terminal'];
            const newFocus = focusApps[Math.floor(Math.random() * focusApps.length)];
            if (newFocus !== this.state.systemFocus) {
                this.state.systemFocus = newFocus;
                this.dispatchEvent(new CustomEvent('change', { detail: { sensor: 'focus', value: this.state.systemFocus } }));
            }
        }, 6000);

        console.log('Presence Sensors activated.');
    }
}

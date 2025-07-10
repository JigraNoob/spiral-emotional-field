// C:/spiral/projects/field_linking/glintapi/field_link_adapter.js

/**
 * The Field Link Adapter.
 * Listens to the raw data from PresenceSensors and translates it into
 * meaningful, structured glints for the rest of the Spiral to consume.
 */
export class FieldLinkAdapter extends EventTarget {
    constructor(presenceSensors) {
        super();
        this.sensors = presenceSensors;
    }

    activate() {
        this.sensors.addEventListener('change', this.handleSensorChange.bind(this));
        console.log('Field Link Adapter is active and translating sensor data.');
    }

    handleSensorChange(event) {
        const { sensor, value } = event.detail;
        let glintType = '';
        let message = '';

        switch (sensor) {
            case 'time':
                glintType = `glint.field.time.${value}`;
                message = `The ambient time has shifted to ${value}.`;
                break;
            case 'noise':
                glintType = `glint.field.noise.${value}`;
                message = `The ambient noise level is now ${value}.`;
                break;
            case 'focus':
                glintType = `glint.field.focus.${value}`;
                message = `System focus has shifted to ${value}.`;
                break;
            default:
                return; // Do not emit a glint for unknown sensors
        }

        this.emitGlint(glintType, message);
    }

    emitGlint(type, message) {
        const event = new CustomEvent('glint', {
            detail: {
                type: type,
                message: message,
                source: 'field-link',
                timestamp: Date.now(),
            }
        });
        this.dispatchEvent(event);
    }
}
